#!/usr/bin/env python3
"""
Scrape recipes from The Plant Based School website.
"""

import re
import json
import subprocess
from html.parser import HTMLParser
from urllib.parse import urljoin

class RecipeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recipes = []
        self.in_recipe_card = False
        self.in_recipe_title = False
        self.current_recipe = {}
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Look for recipe card containers
        if tag == 'article' and any('post' in attrs_dict.get('class', '').lower() for _ in [1]):
            self.in_recipe_card = True
            self.current_recipe = {}
        
        # Look for recipe images
        if self.in_recipe_card and tag == 'img':
            # Get image URL from various possible attributes
            for attr in ['data-src', 'src', 'data-lazy-src']:
                if attr in attrs_dict:
                    img_url = attrs_dict[attr]
                    # Skip placeholder images
                    if 'placeholder' not in img_url.lower() and img_url.startswith('http'):
                        self.current_recipe['image'] = img_url
                        break
        
        # Look for recipe links/titles
        if self.in_recipe_card and tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']
            if '/recipes/' in href or 'theplantbasedschool.com' in href:
                self.current_recipe['url'] = href
        
        # Look for title tags
        if self.in_recipe_card and tag in ['h2', 'h3']:
            class_val = attrs_dict.get('class', '')
            if 'title' in class_val.lower() or 'entry-title' in class_val.lower():
                self.in_recipe_title = True
    
    def handle_data(self, data):
        if self.in_recipe_title and data.strip():
            self.current_recipe['name'] = data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'article' and self.in_recipe_card:
            self.in_recipe_card = False
            # Save recipe if it has required fields
            if 'name' in self.current_recipe and 'image' in self.current_recipe:
                self.recipes.append(self.current_recipe)
            self.current_recipe = {}
        
        if tag in ['h2', 'h3']:
            self.in_recipe_title = False

def extract_ingredients_from_recipe_page(url):
    """Extract ingredients from individual recipe page."""
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return []
        
        html = result.stdout
        
        # Look for ingredients list - usually in ul or ol with specific class
        ingredients = []
        
        # Try to find ingredient list items
        # Common patterns: <li class="wprm-recipe-ingredient">
        ingredient_pattern = r'<li[^>]*class="[^"]*wprm-recipe-ingredient[^"]*"[^>]*>(.*?)</li>'
        matches = re.findall(ingredient_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            # Remove HTML tags and clean up
            ingredient = re.sub(r'<[^>]+>', ' ', match)
            ingredient = re.sub(r'\s+', ' ', ingredient).strip()
            # Clean up HTML entities
            ingredient = ingredient.replace('&#x25a2;', '').replace('&#32;', ' ')
            ingredient = re.sub(r'\s+', ' ', ingredient).strip()
            if ingredient:
                ingredients.append(ingredient)
        
        # Fallback: try other common ingredient patterns
        if not ingredients:
            ingredient_pattern = r'<li[^>]*class="[^"]*ingredient[^"]*"[^>]*>(.*?)</li>'
            matches = re.findall(ingredient_pattern, html, re.DOTALL | re.IGNORECASE)
            for match in matches:
                ingredient = re.sub(r'<[^>]+>', ' ', match)
                ingredient = re.sub(r'\s+', ' ', ingredient).strip()
                # Clean up HTML entities
                ingredient = ingredient.replace('&#x25a2;', '').replace('&#32;', ' ')
                ingredient = re.sub(r'\s+', ' ', ingredient).strip()
                if ingredient:
                    ingredients.append(ingredient)
        
        return ingredients[:15]  # Limit to 15 ingredients to keep card readable
        
    except Exception as e:
        print(f"Error fetching ingredients from {url}: {e}")
        return []

def extract_recipes_from_html(html_content):
    """Extract recipes from HTML using regex for a more robust approach."""
    recipes = []
    
    # Find all article elements that contain recipes
    article_pattern = r'<article[^>]*class="[^"]*post-summary[^"]*"[^>]*>(.*?)</article>'
    articles = re.findall(article_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    for article in articles:
        recipe = {}
        
        # Extract category from entry-category paragraph
        category_match = re.search(r'<p[^>]*class="[^"]*entry-category[^"]*"[^>]*>(.*?)</p>', article, re.DOTALL)
        if category_match:
            category = re.sub(r'<[^>]+>', '', category_match.group(1)).strip()
            # Clean up HTML entities
            category = category.replace('&amp;', '&')
            recipe['category'] = category
        else:
            recipe['category'] = 'Recipe'
        
        # Extract title from h3 with post-summary__title class
        title_match = re.search(r'<h3[^>]*class="[^"]*post-summary__title[^"]*"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', article, re.DOTALL)
        
        if title_match:
            url = title_match.group(1)
            title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
            # Clean up HTML entities
            title = title.replace('&amp;', '&').replace('&#8217;', "'")
            recipe['name'] = title
            recipe['url'] = url
        
        # Extract image URL - look for data-lazy-srcset first (better quality)
        img_match = re.search(r'data-lazy-srcset="([^"]+)"', article)
        if img_match:
            # Get the 600x600 image from srcset
            srcset = img_match.group(1)
            img_600_match = re.search(r'(https://[^\s]+600x600\.jpg)', srcset)
            if img_600_match:
                recipe['image'] = img_600_match.group(1)
        
        # Fallback to data-lazy-src
        if 'image' not in recipe:
            img_match = re.search(r'data-lazy-src="([^"]+)"', article)
            if img_match:
                img_url = img_match.group(1)
                if img_url.startswith('http'):
                    recipe['image'] = img_url
        
        # Only add if we have both name and image
        if 'name' in recipe and 'image' in recipe:
            recipes.append(recipe)
    
    return recipes

def main():
    print("Downloading recipes page...")
    
    # Fetch the HTML
    result = subprocess.run(
        ['curl', '-s', '-L', 'https://theplantbasedschool.com/recipes/'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error downloading page: {result.stderr}")
        return
    
    html_content = result.stdout
    
    print("Parsing recipes...")
    recipes = extract_recipes_from_html(html_content)
    
    if not recipes:
        print("No recipes found. Trying alternative parser...")
        parser = RecipeParser()
        parser.feed(html_content)
        recipes = parser.recipes
    
    print(f"\nFound {len(recipes)} recipes. Fetching ingredients...")
    
    # Fetch ingredients for each recipe
    for i, recipe in enumerate(recipes, 1):
        print(f"[{i}/{len(recipes)}] Fetching ingredients for: {recipe['name'][:50]}...")
        if 'url' in recipe:
            ingredients = extract_ingredients_from_recipe_page(recipe['url'])
            recipe['ingredients'] = ingredients
            if ingredients:
                print(f"   ✓ Found {len(ingredients)} ingredients")
            else:
                print(f"   ✗ No ingredients found")
        else:
            recipe['ingredients'] = []
    
    print(f"\n{'='*70}")
    print(f"Summary: {len(recipes)} recipes processed")
    for i, recipe in enumerate(recipes[:5], 1):
        print(f"\n{i}. {recipe['name']}")
        print(f"   Category: {recipe.get('category', 'N/A')}")
        print(f"   Ingredients: {len(recipe.get('ingredients', []))} items")
        if recipe.get('ingredients'):
            print(f"   First 3: {', '.join(recipe['ingredients'][:3])}")
    
    if len(recipes) > 5:
        print(f"\n... and {len(recipes) - 5} more")
    
    # Save to JSON for easy integration
    with open('recipes.json', 'w') as f:
        json.dump(recipes, f, indent=2)
    
    print(f"\n✓ Recipes saved to recipes.json")
    
    # Generate JavaScript array
    js_recipes = "const recipes = " + json.dumps(recipes, indent=12) + ";"
    
    print("\nJavaScript array snippet saved to recipes.js")
    with open('recipes.js', 'w') as f:
        f.write(js_recipes)

if __name__ == '__main__':
    main()

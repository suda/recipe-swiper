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
        title_match = re.search(r'<h3[^>]*class="[^"]*post-summary__title[^"]*"[^>]*>.*?<a[^>]*>(.*?)</a>', article, re.DOTALL)
        
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            # Clean up HTML entities
            title = title.replace('&amp;', '&').replace('&#8217;', "'")
            recipe['name'] = title
        
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
    
    print(f"\nFound {len(recipes)} recipes:")
    for i, recipe in enumerate(recipes[:10], 1):
        print(f"{i}. {recipe['name']}")
        print(f"   Category: {recipe.get('category', 'N/A')}")
        print(f"   Image: {recipe['image'][:80]}...")
    
    if len(recipes) > 10:
        print(f"... and {len(recipes) - 10} more")
    
    # Save to JSON for easy integration
    with open('recipes.json', 'w') as f:
        json.dump(recipes, f, indent=2)
    
    print(f"\nRecipes saved to recipes.json")
    
    # Generate JavaScript array
    js_recipes = "const recipes = " + json.dumps(recipes, indent=12) + ";"
    
    print("\nJavaScript array snippet saved to recipes.js")
    with open('recipes.js', 'w') as f:
        f.write(js_recipes)

if __name__ == '__main__':
    main()

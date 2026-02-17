# Recipe Swiper 🍽️

A Tinder-style recipe swiper that lets you quickly choose which recipes you want to cook by swiping right (like) or left (nope).

## Features

- 📱 **Touch-friendly** - Swipe with your finger on mobile or drag with mouse on desktop
- ❤️ **Tinder-style interface** - Familiar swipe-to-like mechanics
- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- 📋 **Results page** - See all your liked recipes at the end
- 🔄 **Start over** - Easily restart and try again

## How to Use

1. **Open the file:**

   **Option A: Quick preview server**
   ```bash
   cd ~/Projects/recipe-swiper
   ./serve.sh
   # Then visit http://localhost:8080
   ```

   **Option B: Direct file open**
   ```bash
   # Navigate to the project
   cd ~/Projects/recipe-swiper
   
   # Open in your default browser
   open index.html          # macOS
   xdg-open index.html      # Linux
   start index.html         # Windows
   ```

   Or simply double-click `index.html` in your file manager.

2. **Swipe through recipes:**
   - **Swipe right** (or click ♥) to like a recipe
   - **Swipe left** (or click ✕) to pass
   - **Drag** with mouse or touch to see the swipe indicators

3. **View your selections:**
   - After all recipes, you'll see your selected favorites
   - Click "Start Over" to go again

## Customization

### Adding More Recipes

Edit the `recipes` array in `index.html` (around line 262):

```javascript
const recipes = [
    {
        name: "Your Recipe Name",
        category: "Main/Dessert/Soup/etc",
        image: "https://example.com/image.jpg"
    },
    // Add more...
];
```

### Using Real Recipe Data

To fetch recipes from The Plant-Based School (or any website):

1. **Option A: Manual scraping**
   - Visit the recipe pages
   - Copy image URLs and names
   - Add to the `recipes` array

2. **Option B: API/Backend (advanced)**
   - Create a simple backend (Node.js/Python) to scrape the website
   - Fetch recipes dynamically on page load
   - Example:
     ```javascript
     fetch('/api/recipes')
         .then(res => res.json())
         .then(data => {
             recipes = data;
             init();
         });
     ```

3. **Option C: Browser extension**
   - Create a bookmarklet that extracts recipes from the source page
   - Copy the JSON output into the recipes array

### Changing Colors

The main gradient is defined in the `body` style (around line 20):

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Change `#667eea` and `#764ba2` to your preferred colors.

## Technical Details

- **Pure HTML/CSS/JavaScript** - No dependencies, frameworks, or build tools
- **Self-contained** - Everything in one file for easy sharing
- **Responsive** - Works on mobile, tablet, and desktop
- **Touch events** - Full touch screen support
- **Drag and drop** - Mouse dragging with smooth animations

## Browser Support

- ✅ Chrome/Edge (v90+)
- ✅ Firefox (v88+)
- ✅ Safari (v14+)
- ✅ Mobile browsers (iOS Safari, Chrome Android)

## Project Structure

```
recipe-swiper/
├── index.html        # Complete app (HTML + CSS + JS)
└── README.md         # This file
```

## Ideas for Enhancement

- [ ] Add recipe URLs that open when you click a selected recipe
- [ ] Category filters (show only soups, mains, etc.)
- [ ] Save selections to localStorage
- [ ] Share selected recipes list
- [ ] Undo last swipe
- [ ] Recipe details popup
- [ ] Integration with meal planning apps
- [ ] Export to shopping list

## Credits

- Sample recipe images from [Unsplash](https://unsplash.com)
- Inspired by [The Plant-Based School](https://theplantbasedschool.com/recipes/)

## License

MIT - Feel free to use and modify as you like!

---

**Quick Start:**
```bash
cd ~/Projects/recipe-swiper
open index.html
```

Enjoy finding your next favorite recipe! 🌱

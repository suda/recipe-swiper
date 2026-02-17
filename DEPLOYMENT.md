# GitHub Pages Deployment

This repository is configured to automatically deploy to GitHub Pages on every push to the `master` branch.

## Setup Instructions

1. **Push to GitHub:**
   ```bash
   git remote add origin git@github.com:USERNAME/recipe-swiper.git
   git push -u origin master
   ```

2. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - The workflow will automatically deploy on the next push

3. **Access Your Site:**
   - Your app will be available at: `https://USERNAME.github.io/recipe-swiper/`
   - First deployment may take 1-2 minutes

## Workflow

The `.github/workflows/deploy.yml` workflow:
- Triggers on every push to `master`
- Can also be manually triggered from the Actions tab
- Uploads the entire repository as a static site
- Deploys to GitHub Pages automatically

## Files Deployed

All files in the repository root are deployed, including:
- `index.html` - Main app
- `README.md` - Documentation
- `recipes.json` / `recipes.js` - Recipe data
- `scrape_recipes.py` - Scraper script (optional, won't affect the live site)

## Manual Deployment

You can also manually trigger deployment:
1. Go to **Actions** tab on GitHub
2. Select **Deploy to GitHub Pages** workflow
3. Click **Run workflow**

## Custom Domain (Optional)

To use a custom domain:
1. Add a `CNAME` file to the repository root with your domain
2. Configure DNS records with your domain provider
3. Enable HTTPS in GitHub Pages settings

## Troubleshooting

If deployment fails:
- Check the **Actions** tab for error logs
- Ensure GitHub Pages is enabled in repository settings
- Verify the source is set to **GitHub Actions** (not legacy branch-based deployment)
- Check that Pages permissions are enabled (Settings → Actions → General → Workflow permissions)

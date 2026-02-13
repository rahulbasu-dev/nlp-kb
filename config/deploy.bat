@echo off
echo ============================================
echo Deploying NLP Educational Tool to GitHub
echo ============================================
echo.

echo [1/4] Adding files to git...
git add .
echo.

echo [2/4] Committing changes...
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update educational content and visualizations
git commit -m "%commit_msg%"
echo.

echo [3/4] Pushing to GitHub...
git push origin main
echo.

echo [4/4] Deployment complete!
echo.
echo ============================================
echo Your site will be live at:
echo https://rahulbasu-dev.github.io/nlp-kb/nlp_guide_index.html
echo ============================================
echo.
echo Wait 2-3 minutes for GitHub Pages to update.
echo.
echo To enable GitHub Pages (if not already):
echo 1. Go to: https://github.com/rahulbasu-dev/nlp-kb/settings/pages
echo 2. Set Source to: Deploy from branch
echo 3. Select Branch: main, Folder: / (root)
echo 4. Click Save
echo.
pause

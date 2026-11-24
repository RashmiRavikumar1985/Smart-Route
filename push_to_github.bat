@echo off
echo ========================================
echo Smart Route - GitHub Push Script
echo ========================================
echo.

echo Step 1: Adding all files to Git...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

echo.
echo Step 2: Creating commit...
git commit -m "Initial commit: Smart Route - AI-Powered Traffic Signal Optimization System"
if errorlevel 1 (
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)

echo.
echo Step 3: Configure Git user (if needed)...
git config user.name "RashmiRavikumar1985"
git config user.email "your-email@example.com"

echo.
echo Step 4: Adding remote repository...
git remote add origin https://github.com/RashmiRavikumar1985/Smart-Route.git 2>nul
if errorlevel 1 (
    echo Remote already exists, updating...
    git remote set-url origin https://github.com/RashmiRavikumar1985/Smart-Route.git
)

echo.
echo Step 5: Renaming branch to main...
git branch -M main

echo.
echo Step 6: Pushing to GitHub...
echo NOTE: You may need to enter your GitHub credentials
echo Use Personal Access Token as password if prompted
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo PUSH FAILED - Possible Solutions:
    echo ========================================
    echo 1. Create the repository on GitHub first:
    echo    https://github.com/RashmiRavikumar1985
    echo.
    echo 2. Use Personal Access Token for authentication:
    echo    GitHub Settings ^> Developer settings ^> Personal access tokens
    echo.
    echo 3. Or use GitHub CLI:
    echo    gh auth login
    echo    gh repo create Smart-Route --public --source=. --push
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Repository pushed to GitHub
echo ========================================
echo.
echo Your repository is now live at:
echo https://github.com/RashmiRavikumar1985/Smart-Route
echo.
pause

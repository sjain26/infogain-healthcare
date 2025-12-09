#!/bin/bash

# GitHub Setup Script for Healthcare GenAI Analytics

echo "=========================================="
echo "GitHub Setup for Healthcare GenAI Analytics"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files (respecting .gitignore)
echo "Adding files to git..."
git add .

# Show status
echo ""
echo "Files to be committed:"
git status --short

echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: Healthcare GenAI Analytics System"
fi

# Commit
echo ""
echo "Committing changes..."
git commit -m "$commit_msg"

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Then run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Or provide your GitHub repository URL to continue:"
read -p "GitHub repository URL (or press Enter to skip): " repo_url

if [ ! -z "$repo_url" ]; then
    git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
    git branch -M main
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
    echo ""
    echo "✅ Successfully pushed to GitHub!"
else
    echo ""
    echo "✅ Local git repository ready!"
    echo "   Run the commands above when ready to push."
fi


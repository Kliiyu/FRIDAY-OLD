#!/bin/bash

# Prompt the user for the branch name
read -p "Enter the branch name: " BRANCH

# Check if a branch name is provided
if [ -z "$BRANCH" ]; then
    echo "Branch name cannot be empty."
    exit 1
fi

git add .

git commit -m "auto update $(date +'%Y-%m-%d %H:%M:%S')"

git push origin $BRANCH

read -p "Press any key to continue..." -n 1 -r
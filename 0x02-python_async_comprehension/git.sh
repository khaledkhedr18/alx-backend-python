#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
  echo "Error: No commit message provided."
  echo "Usage: $0 <commit-message>"
  exit 1
fi

# Use the provided argument as the commit message
commit_message="$1"

git add *
git commit -m "$commit_message"
git push

echo "All files pushed successfully with commit message: '$commit_message'"

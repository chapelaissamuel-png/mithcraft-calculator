#!/bin/bash
set -e
cd "$(dirname "$0")/.."

# Build first
npm run build

# Save dist
mkdir -p /tmp/mc-dist
cp -r dist/* /tmp/mc-dist/

# Switch to gh-pages
git checkout gh-pages

# Remove all files (except .git)
git rm -r --cached . > /dev/null 2>&1 || true
find . -not -path './.git/*' -not -name '.git' -not -name '.nojekyll' -delete 2>/dev/null || true

# Copy new build
cp -r /tmp/mc-dist/* .

# Add .nojekyll for static site
touch .nojekyll

# Commit and push
git add -A
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M')"
git push origin gh-pages

# Back to master
git checkout master
echo "Deploy complete!"

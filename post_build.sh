#!/usr/bin/env bash
# post_build.sh

# Log the start of browser install
echo "Running post_build.sh to install Playwright browsers..."

# Install the Playwright browsers (Chromium, Firefox, WebKit)
npx playwright install --with-deps

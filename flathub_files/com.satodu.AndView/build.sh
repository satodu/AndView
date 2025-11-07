#!/bin/bash
# Build script for Flathub

set -e

# Build the application
flatpak-builder --install-deps-from=flathub --repo=repo build com.satodu.AndView.yml

# Create bundle
flatpak build-bundle repo com.satodu.AndView.flatpak com.satodu.AndView

echo "✅ Build completed! Bundle: com.satodu.AndView.flatpak"

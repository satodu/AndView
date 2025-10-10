#!/bin/bash

# AndView Release Creator
# This script helps create GitHub releases with proper tagging

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if version is provided
if [ $# -eq 0 ]; then
    print_error "Usage: $0 <version> [release_notes]"
    print_error "Example: $0 0.0.3 'Added new features'"
    exit 1
fi

VERSION="$1"
RELEASE_NOTES="${2:-Release v$VERSION}"

print_status "Creating release v$VERSION..."

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_warning "You're not on main branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if working directory is clean
if ! git diff-index --quiet HEAD --; then
    print_error "Working directory is not clean. Please commit or stash changes first."
    exit 1
fi

# Check if tag already exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    print_error "Tag v$VERSION already exists!"
    exit 1
fi

# Build the AppImage
print_status "Building AppImage..."
if [ -f "scripts/build_appimage.sh" ]; then
    rm -rf build/AppImage
    ./scripts/build_appimage.sh
    if [ $? -ne 0 ]; then
        print_error "Failed to build AppImage!"
        exit 1
    fi
else
    print_error "build_appimage.sh not found!"
    exit 1
fi

# Find the built AppImage
APPIMAGE_FILE=$(find build/AppImage -name "*.AppImage" -type f | head -n 1)
if [ -z "$APPIMAGE_FILE" ]; then
    print_error "AppImage not found in build/AppImage/"
    exit 1
fi

print_success "AppImage built: $APPIMAGE_FILE"

# Create and push tag
print_status "Creating tag v$VERSION..."
git tag -a "v$VERSION" -m "$RELEASE_NOTES"
git push origin "v$VERSION"

print_success "Tag v$VERSION created and pushed!"

# Display next steps
echo
print_success "Release preparation complete!"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. Go to https://github.com/satodu/AndView/releases"
echo "2. Click 'Create a new release'"
echo "3. Select tag 'v$VERSION'"
echo "4. Use this title: AndView v$VERSION"
echo "5. Upload the AppImage: $APPIMAGE_FILE"
echo
echo -e "${BLUE}Suggested release description:${NC}"
echo "## 🎉 What's New in v$VERSION"
echo ""
echo "$RELEASE_NOTES"
echo ""
echo "## 📥 Download"
echo ""
echo "Download \`AndView-$VERSION-x86_64.AppImage\` above and make it executable:"
echo ""
echo "\`\`\`bash"
echo "chmod +x AndView-$VERSION-x86_64.AppImage"
echo "./AndView-$VERSION-x86_64.AppImage"
echo "\`\`\`"
echo ""
echo "## 📱 Setup"
echo ""
echo "Don't forget to enable USB debugging on your Android device!"
echo "See [DEBUG_MODE.md](https://github.com/satodu/AndView/blob/main/docs/DEBUG_MODE.md) for instructions."
echo ""
echo "---"
echo ""
echo "**Download the AppImage above and start mirroring your Android device!** 📱✨"

print_success "Ready for release! 🚀"
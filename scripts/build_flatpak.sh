#!/bin/bash
# Script para criar Flatpak do AndView

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Criador de Flatpak - AndView"
echo "===================================="
echo ""

# Verifica se flatpak está instalado
if ! command -v flatpak >/dev/null 2>&1; then
    echo "⚠️  Flatpak não encontrado!"
    echo ""
    echo "Para instalar o Flatpak:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt install flatpak"
    echo ""
    echo "Fedora:"
    echo "  sudo dnf install flatpak"
    echo ""
    echo "Arch Linux:"
    echo "  sudo pacman -S flatpak"
    echo ""
    exit 1
fi

# Verifica se flatpak está instalado e tem SDK
if ! flatpak list | grep -q "org.kde.Sdk"; then
    echo "⚠️  SDK do KDE não encontrado!"
    echo ""
    echo "Para instalar o SDK:"
    echo "  flatpak install flathub org.kde.Sdk//5.15-22.08"
    echo ""
    exit 1
fi

# Usa flatpak-builder através do SDK
FLATPAK_BUILDER="flatpak run --command=flatpak-builder org.kde.Sdk//5.15-22.08"

APP_ID="com.satodu.AndView"
BUILD_DIR="build/flatpak"
REPO_DIR="$BUILD_DIR/repo"

echo "🗑️  Limpando build anterior..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📦 Configurando repositório Flatpak..."
$FLATPAK_BUILDER --repo="$REPO_DIR" --force-clean "$BUILD_DIR/build" com.satodu.AndView.yml

if [ $? -eq 0 ]; then
    echo ""
    echo "🔨 Construindo bundle Flatpak..."
    flatpak build-bundle "$REPO_DIR" "$BUILD_DIR/AndView.flatpak" "$APP_ID"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "===================================="
        echo "  ✅ Flatpak criado com sucesso!"
        echo "===================================="
        echo ""
        echo "📦 Arquivo: $BUILD_DIR/AndView.flatpak"
        echo ""
        echo "Para instalar:"
        echo "  flatpak install --bundle $BUILD_DIR/AndView.flatpak"
        echo ""
        echo "Para executar:"
        echo "  flatpak run $APP_ID"
        echo ""
        echo "Para desinstalar:"
        echo "  flatpak uninstall $APP_ID"
        echo ""
    else
        echo "❌ Erro ao criar bundle Flatpak"
        exit 1
    fi
else
    echo "❌ Erro ao construir Flatpak"
    exit 1
fi

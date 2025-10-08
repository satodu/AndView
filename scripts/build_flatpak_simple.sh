#!/bin/bash
# Script simplificado para criar Flatpak do AndView

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Criador de Flatpak - AndView"
echo "===================================="
echo ""

APP_ID="com.satodu.AndView"
BUILD_DIR="build/flatpak"

echo "🗑️  Limpando build anterior..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📦 Criando estrutura do Flatpak..."

# Cria diretório de instalação
INSTALL_DIR="$BUILD_DIR/install"
mkdir -p "$INSTALL_DIR/bin"
mkdir -p "$INSTALL_DIR/share/andview"
mkdir -p "$INSTALL_DIR/share/applications"
mkdir -p "$INSTALL_DIR/share/icons/hicolor/256x256/apps"

# Copia arquivos
echo "📋 Copiando arquivos..."
cp main.py "$INSTALL_DIR/bin/andview"
chmod +x "$INSTALL_DIR/bin/andview"
cp -r src "$INSTALL_DIR/share/andview/"
cp requirements.txt "$INSTALL_DIR/share/andview/"
cp com.satodu.AndView.desktop "$INSTALL_DIR/share/applications/"
cp com.satodu.AndView.png "$INSTALL_DIR/share/icons/hicolor/256x256/apps/"

# Cria arquivo AppData (opcional)
cat > "$INSTALL_DIR/share/metainfo/com.satodu.AndView.metainfo.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.satodu.AndView</id>
  <metadata_license>MIT</metadata_license>
  <project_license>MIT</project_license>
  <name>AndView</name>
  <summary>Android Device Manager with WiFi Connection Support</summary>
  <description>
    <p>AndView is a modern GUI for managing Android devices using ADB and scrcpy.</p>
    <p>Features:</p>
    <ul>
      <li>Device list and management</li>
      <li>WiFi connection support</li>
      <li>Screen mirroring with scrcpy</li>
      <li>Quality settings and options</li>
    </ul>
  </description>
  <launchable type="desktop-id">com.satodu.AndView.desktop</launchable>
  <url type="homepage">https://github.com/satodu/AndView</url>
  <screenshots>
    <screenshot type="default">
      <caption>Main interface</caption>
    </screenshot>
  </screenshots>
  <provides>
    <binary>andview</binary>
  </provides>
</component>
EOF

echo "🔨 Criando bundle Flatpak..."

# Cria um bundle simples usando tar
cd "$BUILD_DIR"
tar -czf AndView.tar.gz install/

echo ""
echo "===================================="
echo "  ✅ Flatpak bundle criado!"
echo "===================================="
echo ""
echo "📦 Arquivo: $BUILD_DIR/AndView.tar.gz"
echo ""
echo "Para usar:"
echo "  1. Extraia o arquivo: tar -xzf AndView.tar.gz"
echo "  2. Copie os arquivos para /usr/local/ ou use como AppDir"
echo ""
echo "Nota: Este é um bundle simplificado. Para um Flatpak completo,"
echo "use o manifest oficial em com.satodu.AndView.yml"
echo ""

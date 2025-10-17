#!/bin/bash
# Script para preparar o AndView para submissão ao Flathub

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Preparador para Flathub - AndView"
echo "===================================="
echo ""

# Verifica se estamos em um repositório git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Erro: Este não é um repositório Git!"
    echo "Execute 'git init' primeiro."
    exit 1
fi

# Verifica se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Há mudanças não commitadas!"
    echo "Deseja commitá-las agora? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Prepare for Flathub submission"
        echo "✅ Mudanças commitadas!"
    else
        echo "❌ Commit as mudanças primeiro!"
        exit 1
    fi
fi

# Cria diretório para arquivos do Flathub
FLATHUB_DIR="flathub_files"
echo "📁 Criando diretório para arquivos do Flathub..."
rm -rf "$FLATHUB_DIR"
mkdir -p "$FLATHUB_DIR/com.satodu.AndView"

# Copia arquivos necessários
echo "📋 Copiando arquivos necessários..."
cp com.satodu.AndView.yml "$FLATHUB_DIR/com.satodu.AndView/"
cp com.satodu.AndView.metainfo.xml "$FLATHUB_DIR/com.satodu.AndView/"

# Cria diretório para screenshots
mkdir -p "$FLATHUB_DIR/com.satodu.AndView/screenshots"
echo "📸 Diretório para screenshots criado: $FLATHUB_DIR/com.satodu.AndView/screenshots/"

# Cria arquivo README para o Flathub
cat > "$FLATHUB_DIR/com.satodu.AndView/README.md" << 'EOF'
# AndView

Android Device Manager with WiFi Connection Support

## Description

AndView is a modern GUI for managing Android devices using ADB and scrcpy. It provides an intuitive interface for developers and users who need to interact with Android devices from their desktop.

## Features

- Device list and management
- WiFi connection support  
- Screen mirroring with scrcpy
- Quality settings and options
- Multi-language support
- Modern Qt interface

## Screenshots

Please add screenshots to the `screenshots/` directory:
- `1.png` - Main interface
- `2.png` - Device list
- `3.png` - Settings

## Build Instructions

```bash
flatpak-builder --install-deps-from=flathub --repo=repo build com.satodu.AndView.yml
flatpak build-bundle repo com.satodu.AndView.flatpak com.satodu.AndView
```

## Installation

```bash
flatpak install --bundle com.satodu.AndView.flatpak
```
EOF

# Cria script de build para o Flathub
cat > "$FLATHUB_DIR/com.satodu.AndView/build.sh" << 'EOF'
#!/bin/bash
# Build script for Flathub

set -e

# Build the application
flatpak-builder --install-deps-from=flathub --repo=repo build com.satodu.AndView.yml

# Create bundle
flatpak build-bundle repo com.satodu.AndView.flatpak com.satodu.AndView

echo "✅ Build completed! Bundle: com.satodu.AndView.flatpak"
EOF

chmod +x "$FLATHUB_DIR/com.satodu.AndView/build.sh"

# Verifica se o flatpak-builder está disponível
if ! command -v flatpak-builder >/dev/null 2>&1; then
    echo "⚠️  flatpak-builder não encontrado!"
    echo "Instale com: sudo apt install flatpak-builder"
fi

# Verifica se o SDK está instalado
if ! flatpak list | grep -q "org.kde.Sdk"; then
    echo "⚠️  SDK do KDE não encontrado!"
    echo "Instale com: flatpak install flathub org.kde.Sdk//5.15-22.08"
fi

echo ""
echo "===================================="
echo "  ✅ Preparação concluída!"
echo "===================================="
echo ""
echo "📁 Arquivos criados em: $FLATHUB_DIR/"
echo ""
echo "📋 Próximos passos:"
echo "1. Adicione screenshots em: $FLATHUB_DIR/com.satodu.AndView/screenshots/"
echo "2. Faça fork do repositório Flathub: https://github.com/flathub/flathub"
echo "3. Copie os arquivos para seu fork"
echo "4. Crie um pull request"
echo ""
echo "📖 Consulte o guia completo: FLATPAK_GUIDE.md"
echo ""

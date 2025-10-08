#!/bin/bash
# Script para criar release no GitHub com AppImage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "====================================="
echo "  🚀 Criador de Release - AndView"
echo "====================================="
echo ""

APP_VERSION="0.0.1"
APP_NAME="AndView"

# Verifica se gh está instalado
if ! command -v gh >/dev/null 2>&1; then
    echo "⚠️  GitHub CLI (gh) não encontrado!"
    echo ""
    echo "Para instalar:"
    echo "  # Ubuntu/Debian:"
    echo "  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
    echo "  echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"
    echo "  sudo apt update && sudo apt install gh"
    echo ""
    echo "  # Ou baixe de: https://github.com/cli/cli/releases"
    echo ""
    exit 1
fi

# Verifica se está logado no GitHub
if ! gh auth status >/dev/null 2>&1; then
    echo "⚠️  Não está logado no GitHub!"
    echo ""
    echo "Para fazer login:"
    echo "  gh auth login"
    echo ""
    exit 1
fi

# Constrói ambos os AppImages
echo "🔨 Construindo AppImages..."
echo ""

echo "📦 Construindo AppImage normal..."
./scripts/build_appimage.sh

echo ""
echo "📦 Construindo AppImage standalone..."
./scripts/build_appimage_standalone.sh

echo ""
echo "📋 Verificando arquivos gerados..."
NORMAL_APPIMAGE="build/AppImage/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
STANDALONE_APPIMAGE="build/AppImage-Standalone/${APP_NAME}-${APP_VERSION}-standalone-x86_64.AppImage"

if [ ! -f "$NORMAL_APPIMAGE" ]; then
    echo "❌ AppImage normal não encontrado: $NORMAL_APPIMAGE"
    exit 1
fi

if [ ! -f "$STANDALONE_APPIMAGE" ]; then
    echo "❌ AppImage standalone não encontrado: $STANDALONE_APPIMAGE"
    exit 1
fi

echo "✅ AppImage normal: $(ls -lh "$NORMAL_APPIMAGE" | awk '{print $5}')"
echo "✅ AppImage standalone: $(ls -lh "$STANDALONE_APPIMAGE" | awk '{print $5}')"
echo ""

# Cria release notes
RELEASE_NOTES_FILE="/tmp/release_notes.md"
cat > "$RELEASE_NOTES_FILE" << EOF
# 🎉 AndView v${APP_VERSION} - Primeiro Release!

## 📱 Sobre o AndView

AndView é um gerenciador moderno de dispositivos Android com suporte a conexão WiFi, desenvolvido em Python com PyQt5.

## ✨ Funcionalidades

- 📱 **Lista de dispositivos** conectados via USB e WiFi
- 🔗 **Conexão WiFi** para espelhamento sem cabo
- 🖥️ **Espelhamento de tela** com scrcpy
- ⚙️ **Configurações de qualidade** (bitrate, resolução, etc.)
- 📸 **Screenshots** e comandos ADB
- 🎨 **Interface moderna** e intuitiva

## 📦 Downloads

### AppImage Normal (290KB)
- Requer ADB e scrcpy instalados no sistema
- Menor tamanho
- Para usuários que já têm as ferramentas Android

### AppImage Standalone (~50MB)
- Inclui ADB e scrcpy
- Funciona sem dependências externas
- Recomendado para novos usuários

## 🚀 Como usar

1. Baixe o AppImage apropriado
2. Torne executável: \`chmod +x AndView-*.AppImage\`
3. Execute: \`./AndView-*.AppImage\`

## 📋 Requisitos

### Para AppImage Normal:
- ADB (Android Debug Bridge)
- scrcpy
- Python 3.11+

### Para AppImage Standalone:
- Nenhum requisito adicional!

## 🔧 Instalação das dependências

### Ubuntu/Debian:
\`\`\`bash
# ADB
sudo apt install android-tools-adb

# scrcpy
sudo apt install scrcpy
\`\`\`

### Fedora:
\`\`\`bash
# ADB
sudo dnf install android-tools

# scrcpy
sudo dnf install scrcpy
\`\`\`

### Arch Linux:
\`\`\`bash
# ADB
sudo pacman -S android-tools

# scrcpy
sudo pacman -S scrcpy
\`\`\`

## 🐛 Problemas conhecidos

- Primeira execução pode ser lenta (cache de dependências)
- Algumas distribuições podem precisar de bibliotecas adicionais

## 🤝 Contribuições

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

Desenvolvido com ❤️ usando Python e PyQt5
EOF

echo "📝 Release notes criadas em: $RELEASE_NOTES_FILE"
echo ""

# Pergunta se quer continuar
read -p "🤔 Deseja criar o release no GitHub? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Release cancelado pelo usuário"
    exit 0
fi

echo "🚀 Criando release no GitHub..."

# Cria o release
gh release create "v${APP_VERSION}" \
    --title "🎉 AndView v${APP_VERSION} - Primeiro Release!" \
    --notes-file "$RELEASE_NOTES_FILE" \
    --latest \
    "$NORMAL_APPIMAGE#AppImage Normal (290KB)" \
    "$STANDALONE_APPIMAGE#AppImage Standalone (~50MB)"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Release criado com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "  1. Verifique o release em: https://github.com/satodu/AndView/releases"
    echo "  2. Teste os downloads"
    echo "  3. Compartilhe com a comunidade!"
    echo ""
    echo "🔗 Links úteis:"
    echo "  - Release: https://github.com/satodu/AndView/releases/tag/v${APP_VERSION}"
    echo "  - Issues: https://github.com/satodu/AndView/issues"
    echo "  - Discussions: https://github.com/satodu/AndView/discussions"
    echo ""
else
    echo "❌ Erro ao criar release"
    exit 1
fi

# Limpa arquivo temporário
rm -f "$RELEASE_NOTES_FILE"

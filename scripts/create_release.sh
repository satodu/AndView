#!/bin/bash
# Script para criar release no GitHub com AppImage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "====================================="
echo "  🚀 Criador de Release - AndView"
echo "====================================="
echo ""

APP_VERSION="1.0.0"
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

# Constrói o AppImage
echo "🔨 Construindo AppImage..."
echo ""

echo "📦 Construindo AppImage..."
./scripts/build_appimage.sh

echo ""
echo "📋 Verificando arquivo gerado..."
APPIMAGE_FILE="build/AppImage/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"

if [ ! -f "$APPIMAGE_FILE" ]; then
    echo "❌ AppImage não encontrado: $APPIMAGE_FILE"
    exit 1
fi

echo "✅ AppImage: $(ls -lh "$APPIMAGE_FILE" | awk '{print $5}')"
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

## 📦 Download

### AppImage (~107MB)
- ✅ **Inclui ADB e scrcpy**
- ✅ **Funciona sem dependências externas**
- ✅ **Recomendado para todos os usuários**
- ✅ **Funciona em qualquer distribuição Linux**

## 🚀 Como usar

1. Baixe o AppImage
2. Torne executável: \`chmod +x AndView-*-x86_64.AppImage\`
3. Execute: \`./AndView-*-x86_64.AppImage\`

## 📋 Requisitos

### Para AppImage:
- ✅ **Nenhum requisito adicional!**
- ✅ Funciona em qualquer Linux
- ✅ Inclui todas as dependências

## 🔧 Instalação manual (apenas para desenvolvedores)

> **💡 Recomendamos usar o AppImage** - não requer instalação de dependências!

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
    "$APPIMAGE_FILE#AppImage (~107MB) - Funciona sem dependências!"

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

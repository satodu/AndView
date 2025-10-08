#!/bin/bash
# Script para criar AppImage do AndView

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Criador de AppImage - AndView"
echo "===================================="
echo ""

APP_NAME="AndView"
APP_VERSION="0.0.1"
BUILD_DIR="$PROJECT_ROOT/build/AppImage"
APPDIR="$BUILD_DIR/$APP_NAME.AppDir"

# Verifica se appimagetool está instalado
if ! command -v appimagetool >/dev/null 2>&1; then
    echo "⚠️  appimagetool não encontrado!"
    echo ""
    echo "Para instalar o appimagetool:"
    echo ""
    echo "1. Baixe o appimagetool:"
    echo "   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    echo ""
    echo "2. Torne-o executável:"
    echo "   chmod +x appimagetool-x86_64.AppImage"
    echo ""
    echo "3. Mova para /usr/local/bin (ou adicione ao PATH):"
    echo "   sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    echo ""
    exit 1
fi

echo "🗑️  Limpando build anterior..."
rm -rf "$BUILD_DIR"
mkdir -p "$APPDIR"

echo "📦 Criando estrutura do AppDir..."

# Cria estrutura de diretórios
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copia o código do aplicativo
echo "📋 Copiando código fonte..."
cp -r src "$APPDIR/usr/bin/"
cp main.py "$APPDIR/usr/bin/"
cp requirements.txt "$APPDIR/usr/bin/"

# Instala dependências Python em um diretório local
echo "🐍 Instalando dependências Python..."
python3 -m pip install --target="$APPDIR/usr/lib/python-packages" -r requirements.txt

# Cria script de execução
echo "🔧 Criando script de execução..."
cat > "$APPDIR/usr/bin/andview" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib/python-packages:$PYTHONPATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"

# Verifica se ADB está disponível
if ! command -v adb >/dev/null 2>&1; then
    zenity --warning --text="ADB não encontrado!\n\nPor favor, instale android-tools para usar o AndView." --width=300 2>/dev/null || \
    echo "AVISO: ADB não encontrado! Por favor, instale android-tools."
fi

# Verifica se scrcpy está disponível
if ! command -v scrcpy >/dev/null 2>&1; then
    zenity --warning --text="scrcpy não encontrado!\n\nPor favor, instale scrcpy para espelhamento de tela." --width=300 2>/dev/null || \
    echo "AVISO: scrcpy não encontrado! Por favor, instale scrcpy."
fi

cd "$APPDIR/usr/bin"
exec python3 main.py "$@"
EOF

chmod +x "$APPDIR/usr/bin/andview"

# Cria arquivo .desktop
echo "📝 Criando arquivo desktop..."
cat > "$APPDIR/usr/share/applications/andview.desktop" << EOF
[Desktop Entry]
Type=Application
Name=AndView
Comment=Interface Gráfica para scrcpy e ADB
Exec=andview
Icon=andview
Categories=Utility;Development;
Terminal=false
EOF

# Cria um ícone simples (você pode substituir por um ícone melhor)
echo "🎨 Criando ícone..."
# Por enquanto, vamos usar um ícone do sistema ou criar um placeholder
# Você pode substituir este ícone depois por um personalizado
if command -v convert >/dev/null 2>&1; then
    # Cria um ícone simples com ImageMagick
    convert -size 256x256 xc:transparent \
            -fill '#2196F3' -draw 'roundrectangle 20,20 236,236 30,30' \
            -fill white -pointsize 120 -gravity center -annotate +0+0 '📱' \
            "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png"
else
    # Usa um ícone do sistema como fallback
    cp /usr/share/icons/hicolor/256x256/apps/phone.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png" 2>/dev/null || \
    touch "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png"
fi

# Cria links simbólicos necessários no AppDir
ln -sf usr/share/applications/andview.desktop "$APPDIR/andview.desktop"
ln -sf usr/share/icons/hicolor/256x256/apps/andview.png "$APPDIR/andview.png"
ln -sf usr/bin/andview "$APPDIR/AppRun"

# Cria o arquivo AppRun principal
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PATH="$APPDIR/usr/bin:$PATH"
export PYTHONPATH="$APPDIR/usr/bin/src:$PYTHONPATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"

cd "$APPDIR/usr/bin"
exec python3 main.py "$@"
EOF

chmod +x "$APPDIR/AppRun"

echo "🔨 Construindo AppImage..."
cd "$BUILD_DIR"
ARCH=x86_64 appimagetool "$APPDIR" "${APP_NAME}-${APP_VERSION}-x86_64.AppImage"

if [ $? -eq 0 ]; then
    echo ""
    echo "===================================="
    echo "  ✅ AppImage criado com sucesso!"
    echo "===================================="
    echo ""
    echo "📦 Arquivo: $BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
    echo ""
    echo "Para testar:"
    echo "  $BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
    echo ""
    echo "Para distribuir:"
    echo "  mv $BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage ~/"
    echo ""
else
    echo "❌ Erro ao criar AppImage"
    exit 1
fi


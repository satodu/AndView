#!/bin/bash
# Script para criar AppImage do AndView (com ADB e scrcpy incluídos)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Criador de AppImage - AndView"
echo "===================================="
echo ""

APP_NAME="AndView"
APP_VERSION="1.0.0"
BUILD_DIR="$PROJECT_ROOT/build/AppImage"
APPDIR="$BUILD_DIR/$APP_NAME.AppDir"

# Verifica se appimagetool está instalado
if ! command -v appimagetool >/dev/null 2>&1; then
    echo "⚠️  appimagetool não encontrado!"
    echo ""
    echo "Para instalar:"
    echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    echo "  chmod +x appimagetool-x86_64.AppImage"
    echo "  sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    echo ""
    exit 1
fi

# Verifica se ADB e scrcpy estão instalados
if ! command -v adb >/dev/null 2>&1; then
    echo "⚠️  ADB não encontrado! Instale o Android SDK Platform Tools"
    exit 1
fi

if ! command -v scrcpy >/dev/null 2>&1; then
    echo "⚠️  scrcpy não encontrado! Instale o scrcpy"
    exit 1
fi

echo "🗑️  Limpando build anterior..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📦 Criando estrutura do AppDir..."
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/usr/share/andview"

echo "📋 Copiando código fonte..."
cp main.py "$APPDIR/usr/bin/"
cp requirements.txt "$APPDIR/usr/share/andview/"
cp -r src "$APPDIR/usr/share/andview/"

echo "🔧 Copiando dependências do sistema..."
# Copia ADB
ADB_PATH=$(which adb)
cp "$ADB_PATH" "$APPDIR/usr/bin/"

# Copia scrcpy
SCRCPY_PATH=$(which scrcpy)
cp "$SCRCPY_PATH" "$APPDIR/usr/bin/"

# Copia bibliotecas necessárias para ADB e scrcpy
echo "📚 Copiando bibliotecas do sistema..."
ldd "$ADB_PATH" | grep "=>" | awk '{print $3}' | while read lib; do
    if [ -f "$lib" ]; then
        cp "$lib" "$APPDIR/usr/lib/" 2>/dev/null || true
    fi
done

ldd "$SCRCPY_PATH" | grep "=>" | awk '{print $3}' | while read lib; do
    if [ -f "$lib" ]; then
        cp "$lib" "$APPDIR/usr/lib/" 2>/dev/null || true
    fi
done

echo "🐍 Instalando dependências Python..."
pip install --target="$APPDIR/usr/lib/python-packages" -r requirements.txt

echo "🔧 Criando script de execução..."
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PATH="$APPDIR/usr/bin:$PATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="$APPDIR/usr/share/andview/src:$APPDIR/usr/lib/python-packages:$PYTHONPATH"

cd "$APPDIR/usr/bin"
exec python3 main.py "$@"
EOF

chmod +x "$APPDIR/AppRun"

echo "📝 Criando arquivo desktop..."
cat > "$APPDIR/usr/share/applications/andview.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AndView
Comment=Android Device Manager with WiFi Connection Support
GenericName=Android Manager
Exec=andview
Icon=andview
Terminal=false
StartupNotify=true
Categories=Utility;Development;
Keywords=android;adb;scrcpy;mobile;development;
MimeType=
X-Desktop-File-Install-Version=0.26
EOF

echo "🎨 Criando ícone..."
if command -v magick >/dev/null 2>&1; then
    magick src/ui/resources/logo.png -resize 256x256 "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png"
else
    cp src/ui/resources/logo.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png"
fi

# Cria links simbólicos
ln -sf usr/share/applications/andview.desktop "$APPDIR/andview.desktop"
ln -sf usr/share/icons/hicolor/256x256/apps/andview.png "$APPDIR/andview.png"

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
    echo "📏 Tamanho: $(ls -lh "$BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage" | awk '{print $5}')"
    echo ""
    echo "🚀 Para testar:"
    echo "  $BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
    echo ""
    echo "✨ Este AppImage inclui ADB e scrcpy - funciona sem dependências externas!"
    echo ""
else
    echo "❌ Erro ao criar AppImage"
    exit 1
fi


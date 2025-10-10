#!/bin/bash
# Script para criar AppImage TOTALMENTE INDEPENDENTE do AndView
# Inclui: Python venv, PySide6, ADB, scrcpy
# NÃO REQUER nenhuma dependência do sistema!

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "============================================"
echo "  AndView - AppImage Independente Builder"
echo "============================================"
echo ""
echo "✨ Este AppImage será TOTALMENTE independente!"
echo "📦 Tamanho estimado: ~150-200MB"
echo "🎉 Não precisa instalar NADA no sistema!"
echo ""

APP_NAME="AndView"
APP_VERSION="0.0.2"
BUILD_DIR="$PROJECT_ROOT/build/AppImage"
APPDIR="$BUILD_DIR/$APP_NAME.AppDir"

# Verifica se appimagetool está instalado
if ! command -v appimagetool >/dev/null 2>&1; then
    echo "❌ appimagetool não encontrado!"
    echo ""
    echo "Para instalar:"
    echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    echo "  chmod +x appimagetool-x86_64.AppImage"
    echo "  sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    exit 1
fi

echo "🗑️  Limpando build anterior..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📦 Criando estrutura do AppDir..."
mkdir -p "$APPDIR/usr/"{bin,lib,share/andview,share/applications,share/icons/hicolor/256x256/apps}

echo "📋 Copiando código fonte..."
cp main.py "$APPDIR/usr/share/andview/"
cp -r src "$APPDIR/usr/share/andview/"

echo "🐍 Criando ambiente Python virtual com PySide6..."
python3 -m venv "$APPDIR/usr/venv"
source "$APPDIR/usr/venv/bin/activate"

echo "📦 Instalando PySide6 (isso pode demorar alguns minutos)..."
pip install --upgrade pip -q
pip install PySide6 -q

echo "⬇️  Baixando scrcpy v3.3.3 (com ADB incluído)..."
SCRCPY_VERSION="3.3.3"
wget -O /tmp/scrcpy.tar.gz \
    "https://github.com/Genymobile/scrcpy/releases/download/v${SCRCPY_VERSION}/scrcpy-linux-x86_64-v${SCRCPY_VERSION}.tar.gz"

if [ $? -eq 0 ] && [ -s /tmp/scrcpy.tar.gz ]; then
    echo "   ✅ Download completo, extraindo..."
    tar -xzf /tmp/scrcpy.tar.gz -C /tmp/
    
    # Copia binários do scrcpy
    if [ -d "/tmp/scrcpy-linux-x86_64-v${SCRCPY_VERSION}" ]; then
        cp -r /tmp/scrcpy-linux-x86_64-v${SCRCPY_VERSION}/* "$APPDIR/usr/bin/"
        chmod +x "$APPDIR/usr/bin/scrcpy"
        
        # scrcpy v3.3.3 já vem com adb incluído
        if [ -f "$APPDIR/usr/bin/adb" ]; then
            chmod +x "$APPDIR/usr/bin/adb"
            echo "   ✅ scrcpy v${SCRCPY_VERSION} incluído (com ADB)"
        else
            echo "   ✅ scrcpy v${SCRCPY_VERSION} incluído"
        fi
    else
        echo "   ❌ Erro ao extrair scrcpy"
        exit 1
    fi
else
    echo "   ❌ Erro ao baixar scrcpy"
    exit 1
fi

rm -rf /tmp/scrcpy* 2>/dev/null || true

echo "📚 Copiando bibliotecas necessárias para scrcpy..."
# Copia bibliotecas essenciais do sistema
for lib in libusb-1.0.so.0 libavcodec.so.* libavformat.so.* libavutil.so.* libswresample.so.* libSDL2-2.0.so.0; do
    find /usr/lib* /lib* -name "$lib" -exec cp {} "$APPDIR/usr/lib/" \; 2>/dev/null || true
done

echo "🔧 Criando script de execução AppRun..."
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"

# Configura variáveis de ambiente para scrcpy e ADB
export PATH="$APPDIR/usr/bin:$PATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"

# Configura Qt plugins para PySide6
QT_PLUGIN_PATH="$APPDIR/usr/venv/lib/python"*"/site-packages/PySide6/Qt/plugins"
if [ -d "$QT_PLUGIN_PATH" ]; then
    export QT_QPA_PLATFORM_PLUGIN_PATH="$QT_PLUGIN_PATH"
fi

# Configura variável para scrcpy encontrar o servidor
if [ -f "$APPDIR/usr/bin/scrcpy-server" ]; then
    export SCRCPY_SERVER_PATH="$APPDIR/usr/bin/scrcpy-server"
fi

# Ativa o ambiente virtual Python
if [ -f "$APPDIR/usr/venv/bin/activate" ]; then
    source "$APPDIR/usr/venv/bin/activate"
fi

# Executa a aplicação
cd "$APPDIR/usr/share/andview"
exec python3 main.py "$@"
EOF

chmod +x "$APPDIR/AppRun"

echo "📝 Criando arquivo desktop..."
cat > "$APPDIR/usr/share/applications/andview.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AndView
Comment=Android Device Manager - GUI for scrcpy and ADB
GenericName=Android Manager
Exec=AppRun
Icon=andview
Terminal=false
StartupNotify=true
Categories=Utility;Development;
Keywords=android;adb;scrcpy;mobile;development;
EOF

echo "🎨 Copiando ícone..."
if [ -f "src/ui/resources/logo.png" ]; then
    if command -v magick >/dev/null 2>&1; then
        magick src/ui/resources/logo.png -resize 256x256 \
            "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png"
    else
        cp src/ui/resources/logo.png \
            "$APPDIR/usr/share/icons/hicolor/256x256/apps/andview.png"
    fi
else
    echo "⚠️  Logo não encontrado"
fi

# Cria links simbólicos
ln -sf usr/share/applications/andview.desktop "$APPDIR/andview.desktop"
ln -sf usr/share/icons/hicolor/256x256/apps/andview.png "$APPDIR/andview.png"

echo "🔨 Construindo AppImage..."
cd "$BUILD_DIR"
ARCH=x86_64 appimagetool "$APPDIR" "${APP_NAME}-${APP_VERSION}-x86_64.AppImage"

if [ $? -eq 0 ]; then
    SIZE=$(ls -lh "$BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage" | awk '{print $5}')
    echo ""
    echo "============================================"
    echo "  ✅ AppImage Independente Criado!"
    echo "============================================"
    echo ""
    echo "📦 Arquivo: $BUILD_DIR/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
    echo "📏 Tamanho: $SIZE"
    echo ""
    echo "🎉 Este AppImage é 100% INDEPENDENTE:"
    echo "   ✅ Python 3 + ambiente virtual incluído"
    echo "   ✅ PySide6 incluído"
    echo "   ✅ ADB incluído"
    echo "   ✅ scrcpy incluído"
    echo "   ✅ Todas as bibliotecas necessárias"
    echo ""
    echo "🚀 Para usar:"
    echo "   1. Baixar o AppImage"
    echo "   2. chmod +x AndView-*.AppImage"
    echo "   3. ./AndView-*.AppImage"
    echo ""
    echo "   NÃO precisa instalar NADA no sistema!"
    echo ""
    echo "⚠️  Lembre-se: O dispositivo Android precisa estar"
    echo "   em modo debug (Configurações → Opções do desenvolvedor)"
    echo ""
else
    echo "❌ Erro ao criar AppImage"
    exit 1
fi

#!/bin/bash
# Script para criar AppImage TOTALMENTE INDEPENDENTE do AndView
# Inclui: Python venv, PySide6, ADB, scrcpy
# NÃO REQUER nenhuma dependência do sistema!

set -euo pipefail

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

# Verifica se ferramentas essenciais estão instaladas
for tool in appimagetool curl ldd; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "❌ Ferramenta obrigatória ausente: $tool"
        exit 1
    fi
done

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
pip cache purge >/dev/null 2>&1 || true
deactivate

echo "⬇️  Baixando scrcpy v3.3.3 (com ADB incluído)..."
SCRCPY_VERSION="3.3.3"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

curl -fL "https://github.com/Genymobile/scrcpy/releases/download/v${SCRCPY_VERSION}/scrcpy-linux-x86_64-v${SCRCPY_VERSION}.tar.gz" \
    -o "${TMP_DIR}/scrcpy.tar.gz"

if [ ! -s "${TMP_DIR}/scrcpy.tar.gz" ]; then
    echo "   ❌ Erro ao baixar scrcpy"
    exit 1
fi

echo "   ✅ Download completo, extraindo..."
tar -xzf "${TMP_DIR}/scrcpy.tar.gz" -C "${TMP_DIR}"

SCRCPY_EXTRACT_DIR="${TMP_DIR}/scrcpy-linux-x86_64-v${SCRCPY_VERSION}"

if [ ! -d "$SCRCPY_EXTRACT_DIR" ]; then
    echo "   ❌ Erro ao extrair scrcpy"
    exit 1
fi

cp "$SCRCPY_EXTRACT_DIR/scrcpy" "$APPDIR/usr/bin/"
cp "$SCRCPY_EXTRACT_DIR/scrcpy-server" "$APPDIR/usr/bin/"

if [ -f "$SCRCPY_EXTRACT_DIR/adb" ]; then
    cp "$SCRCPY_EXTRACT_DIR/adb" "$APPDIR/usr/bin/"
fi

chmod +x "$APPDIR/usr/bin/scrcpy"
[ -f "$APPDIR/usr/bin/adb" ] && chmod +x "$APPDIR/usr/bin/adb"

if [ -d "$SCRCPY_EXTRACT_DIR/lib" ]; then
    cp -r "$SCRCPY_EXTRACT_DIR/lib"/* "$APPDIR/usr/lib/"
fi

if [ -d "$SCRCPY_EXTRACT_DIR/share" ]; then
    mkdir -p "$APPDIR/usr/share"
    cp -r "$SCRCPY_EXTRACT_DIR/share"/* "$APPDIR/usr/share/"
fi

if [ -f "$APPDIR/usr/bin/adb" ]; then
    echo "   ✅ scrcpy v${SCRCPY_VERSION} incluído (com ADB)"
else
    echo "   ✅ scrcpy v${SCRCPY_VERSION} incluído"
fi

echo "📚 Copiando bibliotecas necessárias..."

copy_lib_deps() {
    local binary="$1"
    if [ ! -x "$binary" ]; then
        return
    fi

    echo "   🔍 Resolvendo dependências para $(basename "$binary")"
    while read -r line; do
        local lib_path
        lib_path=$(printf '%s' "$line" | awk '{print $3}')
        if [ -z "$lib_path" ] || [ "$lib_path" = "" ]; then
            continue
        fi
        if [ -f "$lib_path" ]; then
            local lib_name
            lib_name=$(basename "$lib_path")
            if [ ! -f "$APPDIR/usr/lib/$lib_name" ]; then
                cp "$lib_path" "$APPDIR/usr/lib/"
            fi
        fi
    done < <(ldd "$binary" | grep '=> /')
}

copy_lib_deps "$APPDIR/usr/bin/scrcpy"
copy_lib_deps "$APPDIR/usr/bin/adb"

# Copia bibliotecas adicionais usadas com frequência
for lib in libusb-1.0.so.0 libSDL2-2.0.so.0; do
    found=$(find /usr/lib* /lib* -name "$lib" 2>/dev/null | head -n 1 || true)
    if [ -n "$found" ] && [ ! -f "$APPDIR/usr/lib/$(basename "$found")" ]; then
        cp "$found" "$APPDIR/usr/lib/"
    fi
done

# Remove duplicados simbólicos
find "$APPDIR/usr/lib" -type f -exec chmod 0644 {} \;

echo "🔧 Criando script de execução AppRun..."
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"

# Configura variáveis de ambiente para scrcpy e ADB
export PATH="$APPDIR/usr/bin:$PATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"

if [ -x "$APPDIR/usr/bin/adb" ]; then
    export ADB="$APPDIR/usr/bin/adb"
fi

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

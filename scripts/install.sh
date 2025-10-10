#!/bin/bash
# Script de instalação para AndView

# Obtém o diretório do script e vai para a raiz do projeto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Instalador do AndView"
echo "===================================="
echo ""

# Verifica se está no Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Este projeto é apenas para Linux!"
    exit 1
fi

# Detecta a distribuição
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "⚠️  Não foi possível detectar a distribuição Linux"
    OS="unknown"
fi

echo "📋 Sistema detectado: $OS"
echo ""

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verifica Python
echo "🔍 Verificando Python..."
if ! command_exists python3; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION encontrado"
echo ""

# Verifica ADB
echo "🔍 Verificando ADB..."
if ! command_exists adb; then
    echo "⚠️  ADB não encontrado!"
    echo "Deseja instalar? (s/n)"
    read -r response
    if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
        if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
            sudo apt update
            sudo apt install -y android-tools-adb android-tools-fastboot
        elif [[ "$OS" == "fedora" ]] || [[ "$OS" == "nobara" ]]; then
            sudo dnf install -y android-tools
        elif [[ "$OS" == "arch" ]] || [[ "$OS" == "manjaro" ]]; then
            sudo pacman -S android-tools
        else
            echo "❌ Distribuição não suportada para instalação automática"
            echo "Por favor, instale o ADB manualmente"
            exit 1
        fi
    else
        echo "⚠️  Continuando sem ADB..."
    fi
else
    ADB_VERSION=$(adb version | head -n1)
    echo "✅ ADB encontrado: $ADB_VERSION"
fi
echo ""

# Verifica scrcpy
echo "🔍 Verificando scrcpy..."
if ! command_exists scrcpy; then
    echo "⚠️  scrcpy não encontrado!"
    echo "Deseja instalar? (s/n)"
    read -r response
    if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
        if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
            sudo apt update
            sudo apt install -y scrcpy
        elif [[ "$OS" == "fedora" ]] || [[ "$OS" == "nobara" ]]; then
            sudo dnf install -y scrcpy
        elif [[ "$OS" == "arch" ]] || [[ "$OS" == "manjaro" ]]; then
            sudo pacman -S scrcpy
        else
            echo "❌ Distribuição não suportada para instalação automática"
            echo "Por favor, instale o scrcpy manualmente"
            exit 1
        fi
    else
        echo "⚠️  Continuando sem scrcpy..."
    fi
else
    SCRCPY_VERSION=$(scrcpy --version | head -n1)
    echo "✅ scrcpy encontrado: $SCRCPY_VERSION"
fi
echo ""

# Cria ambiente virtual
echo "🐍 Configurando ambiente virtual Python..."
if [ -d "venv" ]; then
    echo "⚠️  Ambiente virtual já existe. Removendo..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Erro ao criar ambiente virtual!"
    echo "Instale python3-venv:"
    if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
        echo "  sudo apt install python3-venv"
    elif [[ "$OS" == "fedora" ]] || [[ "$OS" == "nobara" ]]; then
        echo "  sudo dnf install python3"
    fi
    exit 1
fi
echo "✅ Ambiente virtual criado"
echo ""

# Ativa o ambiente virtual e instala dependências
echo "📦 Instalando PySide6..."
source venv/bin/activate
pip install --upgrade pip -q
pip install PySide6
if [ $? -eq 0 ]; then
    echo "✅ PySide6 instalado com sucesso"
else
    echo "❌ Erro ao instalar PySide6"
    exit 1
fi
deactivate
echo ""

# Cria scripts de execução na raiz
echo "🔧 Criando scripts de execução..."

cat > andview << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ativa o ambiente virtual
source venv/bin/activate

# Executa o aplicativo
exec python3 main.py "$@"
EOF

cat > dev << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/scripts/dev.sh" "$@"
EOF

chmod +x andview dev
echo "✅ Scripts criados: ./andview e ./dev"
echo ""

# Cria arquivo .desktop (opcional)
echo "Deseja criar um atalho no menu de aplicações? (s/n)"
read -r response
if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
    DESKTOP_FILE="$HOME/.local/share/applications/andview.desktop"
    CURRENT_DIR=$(pwd)
    
    mkdir -p "$HOME/.local/share/applications"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AndView
Comment=Interface Gráfica para scrcpy e ADB
Exec=$CURRENT_DIR/andview
Icon=phone
Terminal=false
Categories=Utility;Development;
EOF
    
    chmod +x "$DESKTOP_FILE"
    echo "✅ Atalho criado no menu de aplicações"
fi

echo ""
echo "===================================="
echo "  ✅ Instalação concluída!"
echo "===================================="
echo ""
echo "Para executar o AndView:"
echo "  ./andview"
echo ""
echo "Para modo desenvolvimento:"
echo "  ./dev"
echo "  ./dev --debug"
echo "  ./dev --help"
echo ""
echo "📝 Nota: O projeto agora usa PySide6 dentro de um"
echo "   ambiente virtual Python (venv/)"
echo ""
echo "Documentação em: docs/"
echo "Scripts em: scripts/"
echo ""

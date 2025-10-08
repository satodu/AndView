#!/bin/bash
# Script de desenvolvimento do AndView

# Obtém o diretório do script e vai para a raiz do projeto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  AndView - Modo Desenvolvimento"
echo "===================================="
echo ""

# Verifica se PyQt5 está instalado
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo "❌ PyQt5 não encontrado!"
    echo ""
    echo "📦 Instale o PyQt5 do sistema:"
    echo ""
    if [ -f /etc/fedora-release ] || [ -f /etc/nobara-release ]; then
        echo "  sudo dnf install python3-qt5"
    elif [ -f /etc/debian_version ]; then
        echo "  sudo apt install python3-pyqt5"
    elif [ -f /etc/arch-release ]; then
        echo "  sudo pacman -S python-pyqt5"
    else
        echo "  Instale python3-pyqt5 para seu sistema"
    fi
    echo ""
    echo "⚠️  O PyQt5 do pip não compila no Python 3.13"
    echo "   Use a versão do repositório do sistema!"
    echo ""
    exit 1
fi

echo "✅ PyQt5 encontrado (versão do sistema)"
echo ""

# Verifica argumentos
case "$1" in
    --debug)
        echo "🐛 Modo DEBUG ativado"
        export ANDVIEW_DEBUG=1
        python3 -u main.py
        ;;
    --verbose)
        echo "📝 Modo VERBOSE ativado"
        export ANDVIEW_VERBOSE=1
        python3 -u main.py
        ;;
    --lint)
        echo "🔍 Executando linter..."
        if ! command -v pylint >/dev/null 2>&1; then
            echo "Instalando pylint..."
            pip install pylint
        fi
        pylint src/
        ;;
    --format)
        echo "✨ Formatando código..."
        if ! command -v black >/dev/null 2>&1; then
            echo "Instalando black..."
            pip install black
        fi
        black src/ main.py
        ;;
    --clean)
        echo "🧹 Limpando arquivos temporários..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete
        find . -type f -name "*.pyo" -delete
        echo "✅ Limpeza concluída"
        ;;
    --install-dev)
        echo "📦 Instalando ferramentas de desenvolvimento..."
        pip install pylint black pytest pytest-qt
        echo "✅ Ferramentas instaladas"
        ;;
    --help)
        echo "Uso: ./dev.sh [opção]"
        echo ""
        echo "Opções:"
        echo "  (nenhuma)      Executa o aplicativo normalmente"
        echo "  --debug        Executa com modo debug ativado"
        echo "  --verbose      Executa com saída verbose"
        echo "  --lint         Executa análise de código com pylint"
        echo "  --format       Formata o código com black"
        echo "  --clean        Remove arquivos temporários"
        echo "  --install-dev  Instala ferramentas de desenvolvimento"
        echo "  --help         Mostra esta ajuda"
        echo ""
        ;;
    *)
        echo "▶️  Executando AndView..."
        echo ""
        python3 main.py
        ;;
esac

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ AndView encerrado com código de erro: $EXIT_CODE"
else
    echo ""
    echo "✅ AndView encerrado normalmente"
fi

exit $EXIT_CODE


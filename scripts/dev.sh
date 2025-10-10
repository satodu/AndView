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

# Verifica se o venv existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo ""
    echo "Execute primeiro:"
    echo "  ./scripts/install.sh"
    echo ""
    exit 1
fi

# Ativa o ambiente virtual
source venv/bin/activate

# Verifica se PySide6 está instalado
if ! python3 -c "import PySide6" 2>/dev/null; then
    echo "❌ PySide6 não encontrado no ambiente virtual!"
    echo ""
    echo "📦 Reinstale as dependências:"
    echo "  pip install PySide6"
    echo ""
    exit 1
fi

echo "✅ PySide6 encontrado"
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
        echo "🔍 Executando análise de código (pylint)..."
        if ! command -v pylint >/dev/null 2>&1; then
            echo "⚠️  pylint não encontrado, instalando..."
            pip install pylint
        fi
        pylint src/ main.py
        ;;
    --format)
        echo "✨ Formatando código (black)..."
        if ! command -v black >/dev/null 2>&1; then
            echo "⚠️  black não encontrado, instalando..."
            pip install black
        fi
        black src/ main.py
        ;;
    --clean)
        echo "🗑️  Limpando arquivos temporários..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete
        find . -type f -name "*.pyo" -delete
        echo "✅ Limpeza concluída!"
        ;;
    --install-dev)
        echo "📦 Instalando ferramentas de desenvolvimento..."
        pip install pylint black
        echo "✅ Ferramentas instaladas!"
        ;;
    --help)
        echo "Uso: ./dev [opção]"
        echo ""
        echo "Opções:"
        echo "  (sem opção)   Executa normalmente"
        echo "  --debug       Ativa modo debug"
        echo "  --verbose     Ativa modo verbose"
        echo "  --lint        Análise de código com pylint"
        echo "  --format      Formata código com black"
        echo "  --clean       Limpa arquivos temporários"
        echo "  --install-dev Instala ferramentas de dev"
        echo "  --help        Mostra esta ajuda"
        ;;
    *)
        echo "▶️  Executando AndView..."
        echo ""
        python3 main.py
        EXIT_CODE=$?
        if [ $EXIT_CODE -ne 0 ]; then
            echo ""
            echo "❌ AndView encerrado com código de erro: $EXIT_CODE"
        fi
        exit $EXIT_CODE
        ;;
esac

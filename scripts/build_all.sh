#!/bin/bash
# Script para criar AppImage e Flatpak do AndView

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "===================================="
echo "  Build Completo - AndView"
echo "===================================="
echo ""

# Função para executar script e verificar resultado
run_script() {
    local script_name="$1"
    local script_path="$SCRIPT_DIR/$script_name"
    
    echo "🚀 Executando: $script_name"
    echo "------------------------------------"
    
    if [ -f "$script_path" ]; then
        bash "$script_path"
        local result=$?
        echo ""
        if [ $result -eq 0 ]; then
            echo "✅ $script_name concluído com sucesso!"
        else
            echo "❌ $script_name falhou!"
            return $result
        fi
    else
        echo "⚠️  Script $script_name não encontrado!"
        return 1
    fi
    echo ""
}

# Executa build do AppImage
run_script "build_appimage.sh"
appimage_result=$?

# Executa build do Flatpak
run_script "build_flatpak.sh"
flatpak_result=$?

echo "===================================="
echo "  Resumo do Build"
echo "===================================="
echo ""

if [ $appimage_result -eq 0 ]; then
    echo "✅ AppImage: Criado com sucesso"
    echo "   📦 scripts/build/AppImage/AndView-1.0.0-x86_64.AppImage"
else
    echo "❌ AppImage: Falhou"
fi

if [ $flatpak_result -eq 0 ]; then
    echo "✅ Flatpak: Criado com sucesso"
    echo "   📦 build/flatpak/AndView.flatpak"
else
    echo "❌ Flatpak: Falhou"
fi

echo ""
echo "===================================="

if [ $appimage_result -eq 0 ] && [ $flatpak_result -eq 0 ]; then
    echo "🎉 Todos os builds foram concluídos com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Teste os arquivos gerados"
    echo "   2. Faça upload para o GitHub Releases"
    echo "   3. Submeta o Flatpak para o Flathub (opcional)"
    echo ""
    exit 0
else
    echo "⚠️  Alguns builds falharam. Verifique os erros acima."
    exit 1
fi

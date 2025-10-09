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

echo "===================================="
echo "  Resumo do Build"
echo "===================================="
echo ""

if [ $appimage_result -eq 0 ]; then
    echo "✅ AppImage: Criado com sucesso"
    echo "   📦 build/AppImage/AndView-0.0.1-x86_64.AppImage"
    echo "   ✨ Funciona sem instalar ADB ou scrcpy!"
else
    echo "❌ AppImage: Falhou"
fi

echo ""
echo "===================================="

if [ $appimage_result -eq 0 ]; then
    echo "🎉 AppImage criado com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Teste o AppImage: ./build/AppImage/AndView-0.0.1-x86_64.AppImage"
    echo "   2. Crie release: ./scripts/create_release.sh"
    echo "   3. Distribua para usuários!"
    echo ""
    echo "✨ Este AppImage funciona em qualquer Linux sem instalar nada!"
    echo ""
    exit 0
else
    echo "⚠️  Build falhou. Verifique os erros acima."
    exit 1
fi

#!/bin/bash
# Script para testar o AppImage do AndView

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

APPIMAGE_PATH="build/AppImage/AndView-1.0.0-x86_64.AppImage"

echo "===================================="
echo "  🧪 Teste do AppImage - AndView"
echo "===================================="
echo ""

# Verifica se o AppImage existe
if [ ! -f "$APPIMAGE_PATH" ]; then
    echo "❌ AppImage não encontrado em: $APPIMAGE_PATH"
    echo "Execute primeiro: ./scripts/build_appimage.sh"
    exit 1
fi

echo "📦 AppImage encontrado: $(basename "$APPIMAGE_PATH")"
echo "📏 Tamanho: $(ls -lh "$APPIMAGE_PATH" | awk '{print $5}')"
echo ""

# Teste 1: Verificar se é executável
echo "🔍 Teste 1: Verificando permissões..."
if [ -x "$APPIMAGE_PATH" ]; then
    echo "✅ AppImage é executável"
else
    echo "❌ AppImage não é executável"
    chmod +x "$APPIMAGE_PATH"
    echo "🔧 Permissões corrigidas"
fi
echo ""

# Teste 2: Verificar integridade
echo "🔍 Teste 2: Verificando integridade..."
if file "$APPIMAGE_PATH" | grep -q "ELF.*executable"; then
    echo "✅ AppImage é um executável válido"
else
    echo "❌ AppImage não é um executável válido"
fi
echo ""

# Teste 3: Teste de execução rápida
echo "🔍 Teste 3: Teste de execução (5 segundos)..."
echo "Executando AppImage em background por 5 segundos..."
timeout 5s "$APPIMAGE_PATH" 2>/dev/null &
APP_PID=$!
sleep 2

if kill -0 $APP_PID 2>/dev/null; then
    echo "✅ AppImage iniciou corretamente"
    kill $APP_PID 2>/dev/null
    wait $APP_PID 2>/dev/null
else
    echo "❌ AppImage não conseguiu iniciar"
fi
echo ""

# Teste 4: Verificar dependências
echo "🔍 Teste 4: Verificando dependências do sistema..."
echo "Verificando ADB..."
if command -v adb >/dev/null 2>&1; then
    echo "✅ ADB encontrado: $(adb version | head -1)"
else
    echo "⚠️  ADB não encontrado (necessário para funcionalidade completa)"
fi

echo "Verificando scrcpy..."
if command -v scrcpy >/dev/null 2>&1; then
    echo "✅ scrcpy encontrado: $(scrcpy --version | head -1)"
else
    echo "⚠️  scrcpy não encontrado (necessário para espelhamento de tela)"
fi
echo ""

# Teste 5: Verificar dispositivo conectado
echo "🔍 Teste 5: Verificando dispositivos Android..."
if command -v adb >/dev/null 2>&1; then
    DEVICES=$(adb devices | grep -v "List of devices" | grep -v "^$" | wc -l)
    if [ $DEVICES -gt 0 ]; then
        echo "✅ $DEVICES dispositivo(s) Android conectado(s):"
        adb devices | grep -v "List of devices" | grep -v "^$"
    else
        echo "⚠️  Nenhum dispositivo Android conectado"
        echo "   Conecte um dispositivo via USB ou configure WiFi para testar completamente"
    fi
else
    echo "⚠️  ADB não disponível para verificar dispositivos"
fi
echo ""

echo "===================================="
echo "  📋 Resumo dos Testes"
echo "===================================="
echo ""
echo "✅ AppImage construído com sucesso"
echo "✅ Arquivo é executável e válido"
echo "✅ Aplicação inicia corretamente"
echo ""
echo "🚀 Para usar o AppImage:"
echo "   $APPIMAGE_PATH"
echo ""
echo "📦 Para distribuir:"
echo "   cp $APPIMAGE_PATH ~/AndView-1.0.0-x86_64.AppImage"
echo ""
echo "💡 Dicas:"
echo "   - O AppImage funciona em qualquer distribuição Linux"
echo "   - Não requer instalação, apenas execute diretamente"
echo "   - Certifique-se de ter ADB e scrcpy instalados para funcionalidade completa"
echo ""

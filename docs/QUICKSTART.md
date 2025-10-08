# Guia Rápido - AndView

## Instalação Rápida

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd AndView
```

### 2. Execute o instalador
```bash
chmod +x install.sh
./install.sh
```

O instalador irá:
- ✅ Verificar dependências
- ✅ Oferecer instalar ADB e scrcpy (se necessário)
- ✅ Criar ambiente virtual Python
- ✅ Instalar dependências Python
- ✅ Criar script de execução
- ✅ Criar atalho no menu (opcional)

### 3. Execute o aplicativo
```bash
./andview
```

Ou manualmente:
```bash
source venv/bin/activate
python3 main.py
```

## Preparando seu Dispositivo Android

### 1. Ative as Opções do Desenvolvedor
1. Vá em **Configurações** > **Sobre o telefone**
2. Toque 7 vezes em **Número da versão**
3. Volte para Configurações
4. Entre em **Opções do desenvolvedor**

### 2. Ative a Depuração USB
1. Em **Opções do desenvolvedor**
2. Ative **Depuração USB**

### 3. Conecte via USB
1. Conecte o dispositivo ao computador via USB
2. No dispositivo, autorize o computador quando solicitado
3. Marque "Sempre permitir deste computador"

## Usando o AndView

### Espelhamento Básico
1. Conecte seu dispositivo
2. Selecione o dispositivo na lista à esquerda
3. Clique em "▶️ Iniciar Espelhamento"

### Instalando APKs
1. Vá na aba "🛠️ Ferramentas"
2. Clique em "📁 Procurar" e selecione o APK
3. Clique em "📦 Instalar APK"

### Capturando Screenshots
1. Vá na aba "🛠️ Ferramentas"
2. Clique em "📸 Capturar Screenshot"
3. Escolha onde salvar

### Executando Comandos
1. Vá na aba "⌨️ Comandos"
2. Digite o comando shell (ex: `ls /sdcard/`)
3. Pressione Enter ou clique em "▶️ Executar"

## Presets de Qualidade

- **Padrão**: Configuração balanceada
- **Alta Qualidade**: Melhor qualidade visual (mais recursos)
- **Performance**: Melhor desempenho (menos recursos)
- **Baixa Latência**: Menor atraso possível
- **Gravação**: Otimizado para gravar vídeo

## Atalhos de Teclado

- `F5` - Atualizar lista de dispositivos
- `Ctrl+S` - Capturar screenshot
- `Ctrl+Q` - Sair

## Problemas Comuns

### "ADB não encontrado"
```bash
# Ubuntu/Debian
sudo apt install android-tools-adb

# Fedora/Nobara
sudo dnf install android-tools

# Arch
sudo pacman -S android-tools
```

### "scrcpy não encontrado"
```bash
# Ubuntu/Debian
sudo apt install scrcpy

# Fedora/Nobara
sudo dnf install scrcpy

# Arch
sudo pacman -S scrcpy
```

### Dispositivo não aparece
1. Verifique se a depuração USB está ativada
2. Tente outro cabo USB
3. Execute `adb kill-server && adb start-server` no terminal
4. Clique em "🔄 Atualizar" no AndView

### Tela preta no scrcpy
1. Desbloqueie a tela do dispositivo
2. Desative o protetor de tela
3. Verifique se não há outros aplicativos usando a tela

## Mais Ajuda

Para documentação completa, veja o [README.md](README.md)


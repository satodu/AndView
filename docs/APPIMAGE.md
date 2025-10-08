# Criando AppImage do AndView

Este guia explica como criar um AppImage do AndView para distribuição.

## O que é AppImage?

AppImage é um formato de pacote universal para Linux que permite distribuir aplicativos como arquivos executáveis únicos, sem necessidade de instalação.

## Pré-requisitos

### 1. Instalar appimagetool

```bash
# Baixar appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage

# Tornar executável
chmod +x appimagetool-x86_64.AppImage

# Mover para /usr/local/bin
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### 2. Instalar ImageMagick (opcional, para criar ícone)

```bash
# Ubuntu/Debian
sudo apt install imagemagick

# Fedora/Nobara
sudo dnf install ImageMagick

# Arch
sudo pacman -S imagemagick
```

## Criando o AppImage

### Método Automatizado (Recomendado)

Execute o script de build:

```bash
./build_appimage.sh
```

O AppImage será criado em `build/AppImage/AndView-1.0.0-x86_64.AppImage`

### Testando o AppImage

```bash
./build/AppImage/AndView-1.0.0-x86_64.AppImage
```

## Estrutura do AppImage

```
AndView.AppDir/
├── AppRun                    # Script principal de execução
├── andview.desktop          # Arquivo desktop (link simbólico)
├── andview.png             # Ícone (link simbólico)
└── usr/
    ├── bin/
    │   ├── andview         # Script wrapper
    │   ├── main.py         # Código principal
    │   └── src/            # Código fonte
    ├── lib/
    │   └── python-packages/  # Dependências Python
    └── share/
        ├── applications/
        │   └── andview.desktop
        └── icons/
            └── hicolor/256x256/apps/
                └── andview.png
```

## Personalizando o Ícone

Para usar um ícone personalizado:

1. Crie ou obtenha um ícone PNG de 256x256 pixels
2. Substitua o arquivo em:
   ```bash
   cp seu-icone.png build/AppImage/AndView.AppDir/usr/share/icons/hicolor/256x256/apps/andview.png
   ```
3. Reconstrua o AppImage

## Distribuindo

### 1. Upload para GitHub Releases

```bash
# Após criar uma release no GitHub
gh release upload v1.0.0 build/AppImage/AndView-1.0.0-x86_64.AppImage
```

### 2. AppImageHub

Para listar no AppImageHub:
1. Fork do repositório: https://github.com/AppImage/appimage.github.io
2. Adicione seu AppImage em `database/`
3. Crie um pull request

### 3. Distribuição Direta

Simplesmente compartilhe o arquivo `.AppImage`. Os usuários podem:

```bash
# Baixar
wget https://seu-site.com/AndView-1.0.0-x86_64.AppImage

# Tornar executável
chmod +x AndView-1.0.0-x86_64.AppImage

# Executar
./AndView-1.0.0-x86_64.AppImage
```

## Integração com o Sistema

Para integrar o AppImage ao menu de aplicações:

### Opção 1: AppImageLauncher (Recomendado)

Instale o AppImageLauncher que faz a integração automaticamente:

```bash
# Ubuntu/Debian
sudo add-apt-repository ppa:appimagelauncher-team/stable
sudo apt update
sudo apt install appimagelauncher

# Outras distros: baixar do GitHub
# https://github.com/TheAssassin/AppImageLauncher/releases
```

### Opção 2: Manual

```bash
# Copiar para ~/Applications
mkdir -p ~/Applications
cp AndView-1.0.0-x86_64.AppImage ~/Applications/

# Criar arquivo desktop
cat > ~/.local/share/applications/andview.desktop << EOF
[Desktop Entry]
Type=Application
Name=AndView
Comment=Interface Gráfica para scrcpy e ADB
Exec=$HOME/Applications/AndView-1.0.0-x86_64.AppImage
Icon=phone
Categories=Utility;Development;
Terminal=false
EOF
```

## Atualizações

Para criar uma nova versão:

1. Atualize a versão em `build_appimage.sh`
2. Execute `./build_appimage.sh`
3. Distribua o novo AppImage

## Troubleshooting

### Erro: "cannot open shared object file"

O AppImage precisa que as bibliotecas do sistema estejam disponíveis. Para ADB e scrcpy, eles devem estar instalados no sistema:

```bash
sudo apt install android-tools-adb scrcpy  # Ubuntu/Debian
sudo dnf install android-tools scrcpy      # Fedora/Nobara
```

### Erro ao executar: "No such file or directory"

```bash
# Certifique-se de que o AppImage é executável
chmod +x AndView-1.0.0-x86_64.AppImage

# Verifique se FUSE está instalado
sudo apt install fuse libfuse2  # Ubuntu/Debian
```

### AppImage muito grande

Para reduzir o tamanho:

1. Use `--no-cache-dir` ao instalar pacotes Python
2. Remova arquivos desnecessários (.pyc, __pycache__)
3. Use compressão:
   ```bash
   appimagetool --comp gzip AndView.AppDir
   ```

## Recursos Adicionais

- [AppImage Documentation](https://docs.appimage.org/)
- [AppImageKit GitHub](https://github.com/AppImage/AppImageKit)
- [Best Practices](https://github.com/AppImage/AppImageSpec/blob/master/draft.md)


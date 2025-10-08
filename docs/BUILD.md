# Build Guide - AndView

Este guia explica como gerar os pacotes de distribuição do AndView (AppImage e Flatpak).

## Pré-requisitos

### Para AppImage:
- `appimagetool` - Ferramenta para criar AppImages
- Python 3.8+
- Dependências do projeto (PyQt5, psutil, etc.)

### Para Flatpak:
- `flatpak` e `flatpak-builder`
- Python 3.8+
- SDK do KDE Platform

## Instalação das Ferramentas

### Ubuntu/Debian:
```bash
# AppImage
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool

# Flatpak
sudo apt install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.kde.Platform//5.15-22.08
flatpak install flathub org.kde.Sdk//5.15-22.08
```

### Fedora:
```bash
# AppImage
sudo dnf install appimagetool

# Flatpak
sudo dnf install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.kde.Platform//5.15-22.08
flatpak install flathub org.kde.Sdk//5.15-22.08
```

### Arch Linux:
```bash
# AppImage
sudo pacman -S appimagetool

# Flatpak
sudo pacman -S flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.kde.Platform//5.15-22.08
flatpak install flathub org.kde.Sdk//5.15-22.08
```

## Gerando os Pacotes

### Build Completo (Recomendado):
```bash
./scripts/build_all.sh
```

### Build Individual:

#### Apenas AppImage:
```bash
./scripts/build_appimage.sh
```

#### Apenas Flatpak:
```bash
./scripts/build_flatpak.sh
```

## Arquivos Gerados

Após o build bem-sucedido, os seguintes arquivos serão criados:

- **AppImage**: `scripts/build/AppImage/AndView-1.0.0-x86_64.AppImage`
- **Flatpak**: `build/flatpak/AndView.flatpak`

## Testando os Pacotes

### AppImage:
```bash
./scripts/build/AppImage/AndView-1.0.0-x86_64.AppImage
```

### Flatpak:
```bash
# Instalar
flatpak install --bundle build/flatpak/AndView.flatpak

# Executar
flatpak run com.satodu.AndView

# Desinstalar
flatpak uninstall com.satodu.AndView
```

## Distribuição

### GitHub Releases:
1. Vá para a página de releases no GitHub
2. Crie uma nova release
3. Faça upload dos arquivos `.AppImage` e `.flatpak`

### Flathub (Flatpak):
Para submeter o Flatpak ao Flathub:
1. Fork do repositório [flathub](https://github.com/flathub/flathub)
2. Adicione o arquivo `com.satodu.AndView.yml` na pasta `flathub/`
3. Crie um pull request

## Solução de Problemas

### AppImage não executa:
- Verifique se tem permissão de execução: `chmod +x AndView-*.AppImage`
- Verifique dependências do sistema (ADB, scrcpy)

### Flatpak falha no build:
- Verifique se o SDK do KDE está instalado
- Limpe o cache: `flatpak-builder --repo=repo --force-clean build com.satodu.AndView.yml`

### Dependências faltando:
- Instale as dependências do sistema necessárias
- Para Ubuntu/Debian: `sudo apt install android-tools-adb scrcpy`
- Para Fedora: `sudo dnf install android-tools scrcpy`
- Para Arch: `sudo pacman -S android-tools scrcpy`

## Estrutura dos Arquivos

```
scripts/
├── build_all.sh          # Build completo
├── build_appimage.sh     # Build AppImage
└── build_flatpak.sh      # Build Flatpak

com.satodu.AndView.yml    # Manifest do Flatpak
com.satodu.AndView.desktop # Arquivo desktop
com.satodu.AndView.png    # Ícone
```

## Personalização

Para modificar as configurações de build:

- **AppImage**: Edite `scripts/build_appimage.sh`
- **Flatpak**: Edite `com.satodu.AndView.yml`

Para alterar metadados (nome, descrição, ícone):
- Edite `com.satodu.AndView.desktop`
- Substitua `com.satodu.AndView.png` pelo seu ícone

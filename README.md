<div align="center">
  <img src="src/ui/resources/logo.png" alt="AndView Logo" width="120">
  <h1>AndView - Interface Gráfica para scrcpy e ADB</h1>
  
  <img src="docs/images/demo.png" alt="AndView - Gerenciador de Dispositivos Android" width="80%">
</div>

Uma interface gráfica moderna em Python para gerenciar dispositivos Android usando scrcpy e ADB (Android Debug Bridge).

![Linux](https://img.shields.io/badge/Linux-Only-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Início Rápido

### Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd AndView

# 2. Instale PyQt5 (do sistema)
sudo dnf install python3-qt5          # Fedora/Nobara
# ou
sudo apt install python3-pyqt5        # Ubuntu/Debian

# 3. Execute o instalador (ADB, scrcpy, etc.)
./scripts/install.sh

# 4. Execute o aplicativo
./andview
```

## 📖 Documentação

Toda a documentação está na pasta **`docs/`**:

- 👉 **[START_HERE.md](docs/START_HERE.md)** - **Comece por aqui!**
- 📚 **[QUICKSTART.md](docs/QUICKSTART.md)** - Guia rápido de uso
- 💻 **[DEV_GUIDE.md](docs/DEV_GUIDE.md)** - Guia de desenvolvimento
- 📦 **[APPIMAGE.md](docs/APPIMAGE.md)** - Como criar AppImage
- 🔧 **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Solução de problemas
- 🤝 **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Como contribuir
- 📋 **[CHANGELOG.md](docs/CHANGELOG.md)** - Histórico de versões
- 📁 **[STRUCTURE.md](docs/STRUCTURE.md)** - Estrutura do projeto
- 🐍 **[INSTALL_PYTHON313.md](docs/INSTALL_PYTHON313.md)** - Instalação no Python 3.13

## ✨ Características

- 🔍 Detecção automática de dispositivos Android conectados
- 📱 Espelhamento de tela com scrcpy
- 🎮 Controle remoto do dispositivo
- 📊 Informações detalhadas do dispositivo
- 🔧 Operações ADB comuns (instalação de APKs, screenshots, etc.)
- 🎨 Interface moderna e intuitiva com PyQt5

## 🛠️ Scripts Disponíveis

### Atalhos Rápidos (na raiz):

```bash
./andview              # Executa o aplicativo
./dev                  # Modo desenvolvimento
./dev --debug          # Debug ativado
./dev --help           # Ver todas opções
```

### Scripts Completos (em `scripts/`):

- **`./scripts/install.sh`** - Instalação completa e automatizada
- **`./scripts/dev.sh`** - Modo desenvolvimento com múltiplas opções
- **`./scripts/build_appimage.sh`** - Criar AppImage para distribuição

## 📋 Pré-requisitos

### 📦 Para AppImage Standalone (Recomendado)
**🎉 Nenhum requisito!** O AppImage inclui tudo que você precisa:
- ✅ Python e PyQt5
- ✅ ADB (Android Debug Bridge)  
- ✅ scrcpy
- ✅ Todas as bibliotecas necessárias

### 🛠️ Para instalação manual (desenvolvedores)

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **PyQt5 (do sistema)**
   ```bash
   sudo dnf install python3-qt5          # Fedora/Nobara
   sudo apt install python3-pyqt5        # Ubuntu/Debian
   sudo pacman -S python-pyqt5           # Arch/Manjaro
   ```

3. **ADB (Android Debug Bridge)**
   ```bash
   sudo dnf install android-tools        # Fedora/Nobara
   sudo apt install android-tools-adb    # Ubuntu/Debian
   sudo pacman -S android-tools          # Arch/Manjaro
   ```

4. **scrcpy**
   ```bash
   sudo dnf install scrcpy               # Fedora/Nobara
   sudo apt install scrcpy               # Ubuntu/Debian
   sudo pacman -S scrcpy                 # Arch/Manjaro
   ```

> **⚠️ Nota sobre Python 3.13**: O PyQt5 do pip ainda não é compatível com Python 3.13.  
> Este projeto usa o PyQt5 do repositório do sistema, que já funciona perfeitamente!  
> Veja [INSTALL_PYTHON313.md](docs/INSTALL_PYTHON313.md) para detalhes.

## 🎯 Uso

### Modo Normal

```bash
./andview
```

### Modo Desenvolvimento

```bash
./dev                 # ou ./scripts/dev.sh
./dev --debug         # Com debug
./dev --verbose       # Verbose
./dev --lint          # Análise de código
./dev --format        # Formata código
./dev --clean         # Limpa arquivos temp
```

## 📦 Criar AppImage

```bash
./scripts/build_appimage.sh
```

Veja [docs/APPIMAGE.md](docs/APPIMAGE.md) para detalhes.

## 📱 Preparando o Dispositivo Android

1. Ative as **Opções do Desenvolvedor** (toque 7x no número da versão)
2. Ative a **Depuração USB**
3. Conecte via USB
4. Autorize o computador no dispositivo

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🆘 Ajuda

- Problemas? Veja [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Dúvidas? Abra uma issue
- Quer contribuir? Veja [CONTRIBUTING.md](CONTRIBUTING.md)

---

Desenvolvido com ❤️ usando Python e PyQt5

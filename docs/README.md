# AndView - Interface Gráfica para scrcpy e ADB

Uma interface gráfica moderna em Python para gerenciar dispositivos Android usando scrcpy e ADB (Android Debug Bridge).

## Créditos

Este projeto utiliza as seguintes ferramentas:

- **[scrcpy](https://github.com/Genymobile/scrcpy)** - Mirror Android devices
- **[ADB (Android Debug Bridge)](https://developer.android.com/studio/command-line/adb)** - Android Debug Bridge

Desenvolvido por **Eduardo Sato** ([@satodu](https://github.com/satodu))

## Características

- 🔍 Detecção automática de dispositivos Android conectados
- 📱 Espelhamento de tela com scrcpy
- 🎮 Controle remoto do dispositivo
- 📊 Informações detalhadas do dispositivo
- 🔧 Operações ADB comuns (instalação de APKs, screenshots, etc.)
- 🎨 Interface moderna e intuitiva com PyQt5

## Pré-requisitos

### Instalação no Linux

1. **ADB (Android Debug Bridge)**
   ```bash
   sudo apt install android-tools-adb android-tools-fastboot  # Ubuntu/Debian
   # ou
   sudo dnf install android-tools  # Fedora/Nobara
   ```

2. **scrcpy**
   ```bash
   sudo apt install scrcpy  # Ubuntu/Debian
   # ou
   sudo dnf install scrcpy  # Fedora/Nobara
   ```

3. **Python 3.8+**
   ```bash
   python3 --version
   ```

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd AndView
   ```

2. Crie um ambiente virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Modo Normal

1. Conecte seu dispositivo Android via USB
2. Ative a depuração USB nas opções de desenvolvedor
3. Execute o aplicativo:
   ```bash
   ./andview
   ```
   
   Ou manualmente:
   ```bash
   source venv/bin/activate
   python3 main.py
   ```

### Modo Desenvolvimento

Para testar durante o desenvolvimento:

```bash
./dev.sh              # Execução normal
./dev.sh --debug      # Modo debug
./dev.sh --verbose    # Saída verbose
./dev.sh --lint       # Análise de código
./dev.sh --format     # Formata código
./dev.sh --clean      # Limpa arquivos temp
./dev.sh --help       # Mostra ajuda
```

## Funcionalidades

- **Lista de Dispositivos**: Visualize todos os dispositivos Android conectados
- **Espelhamento de Tela**: Inicie scrcpy com diferentes opções de configuração
- **Informações do Dispositivo**: Modelo, versão do Android, bateria, etc.
- **Instalação de APKs**: Arraste e solte ou selecione APKs para instalar
- **Screenshots**: Capture screenshots do dispositivo
- **Transferência de Arquivos**: Envie e receba arquivos do dispositivo
- **Shell ADB**: Execute comandos ADB personalizados

## Estrutura do Projeto

```
AndView/
├── main.py              # Ponto de entrada da aplicação
├── requirements.txt     # Dependências Python
├── README.md           # Documentação
├── src/
│   ├── __init__.py
│   ├── adb_manager.py  # Gerenciamento de comandos ADB
│   ├── scrcpy_manager.py  # Gerenciamento do scrcpy
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py  # Janela principal
│       └── widgets/
│           ├── __init__.py
│           ├── device_list.py
│           └── control_panel.py
└── resources/
    └── icons/
```

## Licença

MIT License

## Criando AppImage

Para criar um AppImage para distribuição:

1. Instale o `appimagetool`:
   ```bash
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
   chmod +x appimagetool-x86_64.AppImage
   sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
   ```

2. Execute o script de build:
   ```bash
   ./build_appimage.sh
   ```

3. O AppImage será criado em `build/AppImage/AndView-1.0.0-x86_64.AppImage`

Veja [APPIMAGE.md](APPIMAGE.md) para mais detalhes.

## Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

Sinta-se à vontade para abrir issues ou pull requests.


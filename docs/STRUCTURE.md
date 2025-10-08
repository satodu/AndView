# Estrutura do Projeto AndView

Documentação sobre a organização dos arquivos e diretórios do projeto.

## 📁 Estrutura de Diretórios

```
AndView/
├── andview                    # Wrapper para executar o app
├── dev                        # Wrapper para modo desenvolvimento
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── LICENSE                    # Licença MIT
├── README.md                  # Documentação principal
├── .gitignore                # Arquivos ignorados pelo Git
│
├── src/                       # Código fonte principal
│   ├── __init__.py
│   ├── adb_manager.py         # Gerenciamento de comandos ADB
│   ├── scrcpy_manager.py      # Gerenciamento do scrcpy
│   └── ui/                    # Interface gráfica
│       ├── __init__.py
│       ├── main_window.py     # Janela principal
│       └── widgets/           # Widgets customizados
│           ├── __init__.py
│           ├── device_list.py    # Lista de dispositivos
│           └── control_panel.py  # Painel de controle
│
├── scripts/                   # Scripts de automação
│   ├── install.sh             # Instalação completa
│   ├── dev.sh                 # Modo desenvolvimento
│   └── build_appimage.sh      # Criar AppImage
│
├── docs/                      # Documentação completa
│   ├── START_HERE.md          # Guia de início
│   ├── README.md              # Overview detalhado
│   ├── QUICKSTART.md          # Guia rápido
│   ├── DEV_GUIDE.md           # Guia de desenvolvimento
│   ├── APPIMAGE.md            # Criar AppImage
│   ├── TROUBLESHOOTING.md     # Solução de problemas
│   ├── CONTRIBUTING.md        # Como contribuir
│   ├── CHANGELOG.md           # Histórico de versões
│   └── STRUCTURE.md           # Este arquivo
│
└── venv/                      # Ambiente virtual Python (criado na instalação)
    ├── bin/
    ├── include/
    └── lib/
```

## 📄 Descrição dos Arquivos

### Raiz do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `andview` | Script wrapper para executar o aplicativo |
| `dev` | Script wrapper para modo desenvolvimento |
| `main.py` | Ponto de entrada da aplicação Python |
| `requirements.txt` | Lista de dependências Python (PyQt5, etc.) |
| `LICENSE` | Licença MIT do projeto |
| `README.md` | Documentação principal e overview |
| `.gitignore` | Arquivos e diretórios ignorados pelo Git |

### Diretório `src/`

Contém todo o código fonte da aplicação.

| Arquivo | Responsabilidade |
|---------|------------------|
| `adb_manager.py` | Classe `ADBManager` - gerencia comandos ADB, lista dispositivos, instala APKs, etc. |
| `scrcpy_manager.py` | Classe `ScrcpyManager` - gerencia scrcpy, inicia/para espelhamento, opções de configuração |
| `ui/main_window.py` | Classe `MainWindow` - janela principal da aplicação, integra todos os componentes |
| `ui/widgets/device_list.py` | Widget de lista de dispositivos conectados |
| `ui/widgets/control_panel.py` | Widget do painel de controle com abas (espelhamento, ferramentas, comandos) |

### Diretório `scripts/`

Scripts de automação para instalação, desenvolvimento e build.

| Script | Função |
|--------|--------|
| `install.sh` | Instalação completa: verifica dependências, cria venv, instala pacotes, cria atalhos |
| `dev.sh` | Modo desenvolvimento com várias opções (debug, lint, format, clean, etc.) |
| `build_appimage.sh` | Cria AppImage para distribuição |

### Diretório `docs/`

Toda a documentação do projeto.

| Documento | Conteúdo |
|-----------|----------|
| `START_HERE.md` | **Comece por aqui!** Guia inicial rápido |
| `README.md` | Overview detalhado do projeto (versão completa) |
| `QUICKSTART.md` | Guia rápido de uso do aplicativo |
| `DEV_GUIDE.md` | Guia completo para desenvolvedores |
| `APPIMAGE.md` | Como criar e distribuir AppImage |
| `TROUBLESHOOTING.md` | Solução de problemas comuns |
| `CONTRIBUTING.md` | Guia para contribuidores |
| `CHANGELOG.md` | Histórico de versões e mudanças |
| `STRUCTURE.md` | Este arquivo - estrutura do projeto |

## 🔄 Fluxo de Execução

### Execução Normal

```
./andview
  ↓
Ativa venv
  ↓
Executa main.py
  ↓
Importa MainWindow de src/ui/
  ↓
MainWindow importa ADBManager e ScrcpyManager
  ↓
MainWindow cria widgets (DeviceList, ControlPanel)
  ↓
Aplicação inicia
```

### Modo Desenvolvimento

```
./dev [opções]
  ↓
Executa scripts/dev.sh
  ↓
Verifica/cria venv
  ↓
Instala dependências se necessário
  ↓
Processa opções (--debug, --lint, etc.)
  ↓
Executa main.py com configurações apropriadas
```

### Instalação

```
./scripts/install.sh
  ↓
Detecta sistema operacional
  ↓
Verifica ADB, scrcpy, Python
  ↓
Oferece instalar dependências faltantes
  ↓
Cria ambiente virtual (venv/)
  ↓
Instala pacotes Python
  ↓
Cria wrappers (andview, dev)
  ↓
Opcionalmente cria atalho no menu
```

## 🎯 Padrões de Organização

### Código Python

- **Modularidade**: Cada classe em seu próprio arquivo
- **Separação de Responsabilidades**: 
  - `adb_manager.py` - apenas ADB
  - `scrcpy_manager.py` - apenas scrcpy  
  - `ui/` - apenas interface gráfica
- **Type Hints**: Usados em todas as funções
- **Docstrings**: Todas as classes e funções documentadas

### Scripts Shell

- **Portabilidade**: Compatíveis com bash
- **Validação**: Verificam dependências antes de executar
- **Feedback**: Mensagens claras com emojis
- **Tratamento de Erros**: Exit codes apropriados

### Documentação

- **Hierarquia**: Do geral (README) ao específico (DEV_GUIDE)
- **Markdown**: Formatação consistente
- **Exemplos**: Código e comandos sempre com exemplos
- **Acessibilidade**: Linguagem clara em português

## 🚀 Adicionando Novos Componentes

### Novo Widget UI

1. Criar arquivo em `src/ui/widgets/novo_widget.py`
2. Importar em `src/ui/widgets/__init__.py`
3. Usar em `src/ui/main_window.py`

### Nova Funcionalidade ADB

1. Adicionar método em `src/adb_manager.py`
2. Adicionar botão/ação em `src/ui/widgets/control_panel.py`
3. Conectar sinal em `src/ui/main_window.py`

### Novo Script

1. Criar script em `scripts/novo_script.sh`
2. Tornar executável: `chmod +x scripts/novo_script.sh`
3. (Opcional) Criar wrapper na raiz

### Nova Documentação

1. Criar arquivo em `docs/NOVO_DOC.md`
2. Adicionar link no README.md
3. Adicionar link no START_HERE.md se for importante

## 📦 Build e Distribuição

### Estrutura do AppImage

Quando você cria um AppImage com `./scripts/build_appimage.sh`:

```
build/
└── AppImage/
    ├── AndView.AppDir/          # Diretório de construção
    │   ├── AppRun               # Script de execução
    │   ├── andview.desktop      # Arquivo desktop
    │   ├── andview.png          # Ícone
    │   └── usr/
    │       ├── bin/             # Código da aplicação
    │       ├── lib/             # Dependências Python
    │       └── share/           # Recursos
    │
    └── AndView-1.0.0-x86_64.AppImage  # AppImage final
```

## 🔐 Arquivos Ignorados (.gitignore)

Não são versionados:

- `venv/` - Ambiente virtual
- `__pycache__/` - Cache Python
- `build/` - Artefatos de build
- `*.pyc`, `*.pyo` - Bytecode Python
- `.vscode/`, `.idea/` - Configurações IDE
- `*.log` - Logs
- `andview` (gerado) - Script wrapper gerado
- `*.AppImage` - Binários gerados

## 📊 Métricas do Projeto

- **Linhas de Código Python**: ~2000
- **Arquivos Python**: 6
- **Scripts Shell**: 3
- **Documentos**: 9
- **Dependências Python**: 3 (PyQt5, PyQt5-Qt5, PyQt5-sip)
- **Dependências Sistema**: 2 (adb, scrcpy)

## 🔗 Dependências

### Internas (entre módulos)

```
main.py
  └── ui/main_window.py
      ├── ui/widgets/device_list.py
      ├── ui/widgets/control_panel.py
      ├── adb_manager.py
      └── scrcpy_manager.py
```

### Externas

- **PyQt5** - Interface gráfica
- **adb** - Comunicação com Android
- **scrcpy** - Espelhamento de tela
- **Python 3.8+** - Runtime

## 📝 Convenções

### Nomenclatura

- **Arquivos Python**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções/métodos**: `snake_case()`
- **Constantes**: `UPPER_CASE`
- **Scripts**: `kebab-case.sh`

### Git

- **Branches**: `feature/nome-da-feature`
- **Commits**: Mensagens descritivas em português
- **Tags**: `v1.0.0` (versionamento semântico)

### Documentação

- **Arquivos**: `UPPER_CASE.md`
- **Seções**: Headers com emojis
- **Código**: Sempre em blocos ```bash ou ```python
- **Links**: Relativos quando possível

---

**Estrutura mantida simples, clara e escalável! 🚀**


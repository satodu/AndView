# Guia de Desenvolvimento - AndView

Este guia é para desenvolvedores que querem contribuir ou modificar o AndView.

## Configuração Inicial

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd AndView
```

### 2. Configuração Rápida

```bash
# Instala tudo automaticamente
./scripts/install.sh

# Ou configuração manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Desenvolvimento

### Script de Desenvolvimento

O script `dev` (ou `scripts/dev.sh`) facilita o desenvolvimento com várias opções:

```bash
# Execução normal (modo dev)
./dev

# Com debug ativado
./dev --debug

# Com saída verbose
./dev --verbose

# Análise de código (pylint)
./dev --lint

# Formatação automática de código (black)
./dev --format

# Limpar arquivos temporários
./dev --clean

# Instalar ferramentas de desenvolvimento
./dev --install-dev

# Mostrar ajuda
./dev --help
```

### Estrutura do Projeto

```
AndView/
├── main.py                    # Ponto de entrada
├── src/
│   ├── __init__.py
│   ├── adb_manager.py         # Gerenciamento ADB
│   ├── scrcpy_manager.py      # Gerenciamento scrcpy
│   └── ui/
│       ├── main_window.py     # Janela principal
│       └── widgets/
│           ├── device_list.py    # Lista de dispositivos
│           └── control_panel.py  # Painel de controle
├── dev                        # Wrapper para modo dev
├── andview                    # Wrapper para executar app
├── scripts/
│   ├── dev.sh                 # Script de desenvolvimento
│   ├── build_appimage.sh      # Script para criar AppImage
│   └── install.sh             # Script de instalação
└── docs/                      # Toda a documentação
```

## Workflow de Desenvolvimento

### 1. Fazendo Mudanças

```bash
# 1. Crie uma branch
git checkout -b feature/minha-feature

# 2. Faça suas alterações
# Edite os arquivos necessários

# 3. Teste suas alterações
./dev

# 4. Verifique o código
./dev --lint
./dev --format

# 5. Commit
git add .
git commit -m "Adiciona minha feature"

# 6. Push
git push origin feature/minha-feature
```

### 2. Testando

```bash
# Teste básico
./dev

# Teste com debug para ver mais detalhes
./dev --debug

# Limpe arquivos temporários antes de testar
./dev --clean
./dev
```

### 3. Verificação de Qualidade

```bash
# Instale ferramentas de dev (primeira vez)
./dev --install-dev

# Execute linter
./dev --lint

# Formate o código
./dev --format
```

## Adicionando Novas Funcionalidades

### Exemplo: Nova Função ADB

1. **Edite `src/adb_manager.py`**:

```python
def nova_funcao(self, serial: str) -> Tuple[bool, str]:
    """Descrição da nova função"""
    try:
        result = subprocess.run(
            [self.adb_path, "-s", serial, "shell", "comando"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except FileNotFoundError:
        return False, "ADB não encontrado"
```

2. **Adicione à UI em `src/ui/widgets/control_panel.py`**:

```python
# No setup_ui ou na aba apropriada
novo_btn = QPushButton("🔧 Nova Função")
novo_btn.clicked.connect(self._on_nova_funcao)

# Adicione o handler
def _on_nova_funcao(self):
    if not self.current_device:
        QMessageBox.warning(self, "Aviso", "Nenhum dispositivo!")
        return
    
    # Emita um sinal ou chame diretamente
    self.nova_funcao.emit()
```

3. **Conecte na janela principal em `src/ui/main_window.py`**:

```python
# No __init__ ou _setup_ui
self.control_panel.nova_funcao.connect(self._on_nova_funcao)

# Adicione o handler
def _on_nova_funcao(self):
    success, message = self.adb_manager.nova_funcao(
        self.current_device.serial
    )
    
    if success:
        QMessageBox.information(self, "Sucesso", message)
    else:
        QMessageBox.critical(self, "Erro", message)
```

4. **Teste**:

```bash
./dev --debug
```

## Depuração

### Debug com prints

```python
# Use prints para debug rápido
print(f"DEBUG: device={device.serial}")

# Ou use o módulo logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Device: {device.serial}")
```

### Debug com PyQt5

```bash
# Execute com QT_DEBUG_PLUGINS para ver problemas do Qt
QT_DEBUG_PLUGINS=1 ./dev --debug
```

### Debug do scrcpy/ADB

```bash
# Teste comandos manualmente
adb devices -l
scrcpy --version

# Veja o que o AndView está executando
./dev --verbose
```

## Criando Releases

### 1. Atualize a Versão

Edite nos seguintes arquivos:
- `src/__init__.py` → `__version__`
- `build_appimage.sh` → `APP_VERSION`
- `CHANGELOG.md` → Nova seção

### 2. Crie o AppImage

```bash
./scripts/build_appimage.sh
```

### 3. Teste o AppImage

```bash
./build/AppImage/AndView-1.0.0-x86_64.AppImage
```

### 4. Crie a Release

```bash
# Crie uma tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# Upload do AppImage no GitHub Releases
# Ou use gh CLI
gh release create v1.0.0 \
    build/AppImage/AndView-1.0.0-x86_64.AppImage \
    --title "AndView v1.0.0" \
    --notes "Release notes aqui"
```

## Troubleshooting de Desenvolvimento

### PyQt5 não encontrado

```bash
source venv/bin/activate
pip install --upgrade PyQt5
```

### Imports não funcionam

```bash
# Certifique-se de estar no diretório correto
cd /home/panda/Projects/satodu/AndView

# E que o ambiente virtual está ativo
source venv/bin/activate
```

### Mudanças não aparecem

```bash
# Limpe arquivos compilados
./dev --clean

# Ou manualmente
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
```

## Boas Práticas

### Código

- ✅ Siga PEP 8
- ✅ Use type hints quando possível
- ✅ Docstrings em todas as funções/classes
- ✅ Nomes descritivos de variáveis
- ✅ Mantenha funções pequenas e focadas

### Git

- ✅ Commits pequenos e focados
- ✅ Mensagens descritivas
- ✅ Teste antes de fazer commit
- ✅ Use branches para features

### UI

- ✅ Mensagens claras ao usuário
- ✅ Tratamento de erros adequado
- ✅ Feedback visual das ações
- ✅ Acessibilidade (tamanhos de fonte, contraste)

## Recursos Úteis

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [scrcpy GitHub](https://github.com/Genymobile/scrcpy)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [AppImage Documentation](https://docs.appimage.org/)

## Ajuda

Se precisar de ajuda:
1. Veja a documentação nos arquivos `.md`
2. Abra uma issue no GitHub
3. Consulte os exemplos no código existente

Boa codificação! 🚀


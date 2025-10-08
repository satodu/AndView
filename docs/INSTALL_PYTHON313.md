# Instalação no Python 3.13

## Sobre PyQt5 e Python 3.13

O PyQt5 disponível no **PyPI (pip)** ainda não é totalmente compatível com **Python 3.13**, apresentando erros de compilação. 

Por isso, este projeto foi configurado para usar o **PyQt5 do repositório do sistema**, que já está compilado e funcionando perfeitamente com Python 3.13.

## ✅ Solução Implementada

Ao invés de usar um ambiente virtual (venv) com PyQt5 do pip, o AndView agora:

1. **Usa o Python do sistema** (Python 3.13)
2. **Usa o PyQt5 do repositório** (instalado via dnf/apt)
3. **Não requer ambiente virtual** (mais simples!)

## 📦 Instalação

### Fedora/Nobara (Python 3.13)

```bash
# 1. Instale PyQt5 do sistema
sudo dnf install python3-qt5

# 2. Instale ADB e scrcpy
sudo dnf install android-tools scrcpy

# 3. Execute o instalador do projeto
./scripts/install.sh

# 4. Execute o app
./andview
```

### Ubuntu/Debian

```bash
# 1. Instale PyQt5 do sistema
sudo apt install python3-pyqt5

# 2. Instale ADB e scrcpy
sudo apt install android-tools-adb scrcpy

# 3. Execute o instalador do projeto
./scripts/install.sh

# 4. Execute o app
./andview
```

### Arch/Manjaro

```bash
# 1. Instale PyQt5 do sistema
sudo pacman -S python-pyqt5

# 2. Instale ADB e scrcpy
sudo pacman -S android-tools scrcpy

# 3. Execute o instalador do projeto
./scripts/install.sh

# 4. Execute o app
./andview
```

## 🔍 Verificando a Instalação

Para verificar se o PyQt5 está instalado corretamente:

```bash
python3 -c "from PyQt5.QtCore import PYQT_VERSION_STR; print('PyQt5:', PYQT_VERSION_STR)"
```

Deve mostrar algo como: `PyQt5: 5.15.11`

## ❓ Por que não usar venv?

### Antes (com venv e PyQt5 do pip):
```bash
python3 -m venv venv
source venv/bin/activate
pip install PyQt5  # ❌ Falha ao compilar no Python 3.13
```

**Erro típico:**
```
error: assignment to 'sipSimpleWrapper *' from incompatible pointer type 'PyObject *'
error: command '/usr/bin/gcc' failed with exit code 1
```

### Agora (sem venv, PyQt5 do sistema):
```bash
sudo dnf install python3-qt5  # ✅ Já está compilado!
python3 main.py                # ✅ Funciona direto!
```

## 🎯 Vantagens da Nova Abordagem

✅ **Mais simples** - Sem venv para gerenciar  
✅ **Mais rápido** - PyQt5 já está compilado  
✅ **Mais confiável** - Pacote testado pela distribuição  
✅ **Compatível** - Funciona com Python 3.13  
✅ **Menos espaço** - Não duplica o PyQt5  

## 🔄 Migração de Versões Antigas

Se você já tinha o projeto instalado com venv:

```bash
# 1. Remova o ambiente virtual antigo
rm -rf venv

# 2. Instale PyQt5 do sistema
sudo dnf install python3-qt5

# 3. Pronto! Agora funciona direto
./andview
```

## 📝 Desenvolvimento

Para desenvolvimento, o script `./dev` foi atualizado para funcionar sem venv:

```bash
./dev              # Executa normalmente
./dev --debug      # Modo debug
./dev --lint       # Análise de código
```

## 🚀 AppImage

O AppImage também foi atualizado para incluir o PyQt5 do sistema.

```bash
./scripts/build_appimage.sh
```

O AppImage resultante incluirá o PyQt5 e funcionará em qualquer distribuição Linux.

## ⚠️ Notas Importantes

1. **Python 3.12 e anteriores**: Também funcionam com esta abordagem
2. **PyQt5 futuro**: Quando o PyQt5 do pip suportar Python 3.13, poderemos voltar a usar venv se desejado
3. **Outras dependências**: Se você adicionar outras libs Python, pode instalar via pip sem problemas:
   ```bash
   # Instalação global
   pip3 install --user nome-do-pacote
   
   # Ou crie venv apenas para outras dependências
   python3 -m venv venv --system-site-packages
   ```

## 🆘 Problemas?

Se encontrar algum erro:

1. Verifique se PyQt5 está instalado:
   ```bash
   python3 -c "import PyQt5"
   ```

2. Verifique a versão do Python:
   ```bash
   python3 --version
   ```

3. Reinstale PyQt5 do sistema:
   ```bash
   sudo dnf reinstall python3-qt5
   ```

4. Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para mais soluções

---

**Configuração otimizada para Python 3.13! 🎉**


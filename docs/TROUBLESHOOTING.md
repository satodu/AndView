# Troubleshooting - AndView

Guia de resolução de problemas comuns.

## Problemas de Instalação

### Erro: "Python.h: Arquivo ou diretório inexistente"

**Causa**: Faltam ferramentas de desenvolvimento Python.

**Solução**:

```bash
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# Fedora/Nobara
sudo dnf install python3-devel gcc gcc-c++

# Arch/Manjaro
sudo pacman -S base-devel
```

Depois execute novamente:
```bash
./install.sh
```

### Erro ao compilar PyQt5-sip

**Causa**: Faltam compiladores ou bibliotecas de desenvolvimento.

**Solução**:

```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# Fedora/Nobara  
sudo dnf install gcc gcc-c++ python3-devel

# Arch/Manjaro
sudo pacman -S base-devel
```

### PyQt5 não instala

**Alternativa**: Use a versão do repositório do sistema:

```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5

# Fedora/Nobara
sudo dnf install python3-qt5

# Arch/Manjaro
sudo pacman -S python-pyqt5
```

Depois, use o Python do sistema sem venv:
```bash
python3 main.py
```

## Problemas com ADB

### ADB não detecta dispositivo

**Verificações**:

1. **Depuração USB ativada?**
   - Configurações → Opções do desenvolvedor → Depuração USB

2. **Dispositivo autorizado?**
   ```bash
   adb devices
   # Deve mostrar "device", não "unauthorized"
   ```
   
   Se mostrar "unauthorized", desbloqueie o telefone e aceite.

3. **Servidor ADB travado?**
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

4. **Cabo USB funcionando?**
   - Tente outro cabo
   - Teste outra porta USB
   - Alguns cabos são apenas para carregamento

5. **Regras udev (Linux)?**
   ```bash
   # Crie arquivo de regras
   sudo nano /etc/udev/rules.d/51-android.rules
   
   # Adicione (substitua XXXX pelo vendor ID do seu dispositivo):
   SUBSYSTEM=="usb", ATTR{idVendor}=="XXXX", MODE="0666", GROUP="plugdev"
   
   # Recarregue regras
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   
   # Reconecte o dispositivo
   ```
   
   Vendor IDs comuns:
   - Google: 18d1
   - Samsung: 04e8
   - Xiaomi: 2717
   - Motorola: 22b8
   - LG: 1004

### Permissão negada ao usar ADB

**Solução**:

```bash
# Adicione seu usuário ao grupo plugdev
sudo usermod -aG plugdev $USER

# Faça logout e login novamente
```

### ADB muito lento

**Soluções**:

1. Reinicie o servidor ADB:
   ```bash
   adb kill-server
   adb start-server
   ```

2. Use outro cabo USB (prefira USB 3.0)

3. Desative outras ferramentas que usam ADB

## Problemas com scrcpy

### Tela preta no scrcpy

**Causas e soluções**:

1. **Tela do dispositivo bloqueada**
   - Desbloqueie a tela

2. **Protetor de tela ativo**
   - Desative temporariamente

3. **Aplicativo em primeiro plano bloqueando**
   - Volte para a tela inicial

4. **Codec não suportado**
   ```bash
   # Tente com codec diferente
   scrcpy --video-codec=h264
   ```

5. **Resolução muito alta**
   - Use uma resolução menor:
   ```bash
   scrcpy -m 1024
   ```

### scrcpy travando/lagado

**Soluções**:

1. **Reduza a resolução**:
   - No AndView: use preset "Performance"
   - Ou defina resolução máxima: 720

2. **Reduza o bitrate**:
   - Tente 4M ou 2M

3. **Reduza FPS**:
   - Defina para 30 FPS

4. **Use cabo USB**:
   - Conexão sem fio tem mais latência

5. **Feche outros aplicativos**:
   - Libere recursos do PC e do telefone

### Áudio não funciona

**Nota**: Áudio no scrcpy requer versão 2.0+

**Verificação**:
```bash
scrcpy --version
```

**Se versão < 2.0**:
```bash
# Ubuntu/Debian (pode precisar de PPA)
sudo add-apt-repository ppa:sicklylife/scrcpy
sudo apt update
sudo apt install scrcpy

# Fedora/Nobara
sudo dnf update scrcpy

# Arch
sudo pacman -Syu scrcpy
```

### scrcpy não conecta via WiFi

**Passos**:

1. **Conecte primeiro via USB**

2. **Configure porta TCP/IP**:
   ```bash
   adb tcpip 5555
   ```

3. **Encontre IP do dispositivo**:
   - Configurações → Sobre → Status → Endereço IP
   - Ou: `adb shell ip addr show wlan0`

4. **Conecte**:
   ```bash
   adb connect 192.168.1.XXX:5555
   ```

5. **Desconecte USB e use scrcpy**

**Problemas**:
- Computador e telefone devem estar na mesma rede
- Alguns roteadores bloqueiam comunicação entre dispositivos
- Firewall pode estar bloqueando

## Problemas na Interface Gráfica

### AndView não abre

**Verificações**:

1. **PyQt5 instalado?**
   ```bash
   python3 -c "import PyQt5"
   ```

2. **Ambiente virtual ativado?**
   ```bash
   source venv/bin/activate
   python3 main.py
   ```

3. **Execute com debug**:
   ```bash
   ./dev.sh --debug
   ```

### Erro: "cannot import name 'MainWindow'"

**Solução**:
```bash
# Limpe arquivos compilados
./dev.sh --clean

# Ou manualmente
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Execute novamente
./dev.sh
```

### Interface gráfica muito pequena/grande

**Solução**: Edite `main.py` e ajuste o tamanho da janela:

```python
self.setGeometry(100, 100, 1400, 800)  # Largura, altura
```

### Fonte muito pequena

**Solução**: Ajuste o DPI no Qt:

```python
# No main.py, antes de criar a janela
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1.5"  # Ajuste conforme necessário
```

## Problemas no AppImage

### "cannot open shared object file"

**Causa**: Biblioteca do sistema faltando.

**Solução**:
```bash
# Instale FUSE para AppImage
sudo apt install fuse libfuse2  # Ubuntu/Debian
sudo dnf install fuse fuse-libs  # Fedora/Nobara
```

### AppImage não executa

**Verificações**:

1. **É executável?**
   ```bash
   chmod +x AndView-*.AppImage
   ```

2. **FUSE instalado?**
   ```bash
   sudo apt install fuse libfuse2
   ```

3. **Execute manualmente**:
   ```bash
   ./AndView-*.AppImage --appimage-extract-and-run
   ```

### AppImage muito grande

**Para reduzir o tamanho**:

1. Edite `build_appimage.sh`
2. Adicione compressão:
   ```bash
   appimagetool --comp gzip AndView.AppDir
   ```

## Problemas de Performance

### Alto uso de CPU

**Causas**:

1. **Atualização automática de dispositivos**
   - Normal, atualiza a cada 5 segundos
   - Para desabilitar, edite `main_window.py` e comente:
   ```python
   # self.update_timer.start(5000)
   ```

2. **scrcpy em alta qualidade**
   - Use preset "Performance"
   - Reduza resolução e FPS

### Alto uso de memória

**Soluções**:

1. Feche e reabra o aplicativo periodicamente
2. Não mantenha múltiplas janelas abertas
3. Use resolução menor no scrcpy

## Outros Problemas

### Mudanças no código não aparecem

```bash
# Limpe cache Python
./dev.sh --clean

# Recrie o ambiente virtual
rm -rf venv
./install.sh
```

### Erro de importação

```bash
# Certifique-se de estar no diretório correto
cd /home/panda/Projects/satodu/AndView

# Ative o ambiente virtual
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt
```

### AndView congela

**Possíveis causas**:

1. **Operação ADB longa**
   - Instalação de APK grande
   - Normal, aguarde

2. **scrcpy travou**
   - Feche o scrcpy manualmente
   - Clique em "Parar"

3. **Dispositivo desconectou**
   - Reconecte
   - Clique em "Atualizar"

## Conseguindo Mais Ajuda

Se o problema persistir:

1. **Veja os logs**:
   ```bash
   ./dev.sh --debug 2>&1 | tee andview.log
   ```

2. **Teste componentes individualmente**:
   ```bash
   adb devices       # Testa ADB
   scrcpy --version  # Testa scrcpy
   python3 -c "import PyQt5"  # Testa PyQt5
   ```

3. **Abra uma issue** no GitHub com:
   - Descrição do problema
   - Passos para reproduzir
   - Log de erro completo
   - Sistema operacional e versões:
     ```bash
     uname -a
     python3 --version
     adb version
     scrcpy --version
     ```

4. **Pergunte na comunidade**:
   - Reddit: r/linux
   - Fóruns da sua distro
   - Stack Overflow


# 🔧 Como Ativar o Modo Debug no Android

Para usar o AndView, você **DEVE** ativar o modo debug no seu dispositivo Android. Este guia mostra como fazer isso passo a passo.

## ⚠️ Importante

**Sem o modo debug ativado, o AndView não conseguirá:**
- ❌ Detectar seu dispositivo
- ❌ Conectar via USB ou WiFi
- ❌ Espelhar a tela
- ❌ Executar comandos ADB

## 📱 Passo a Passo

### 1. Ativar as Opções do Desenvolvedor

1. **Abra as Configurações** do Android
2. **Vá para "Sobre o telefone"** ou "Sobre o dispositivo"
3. **Encontre "Número da versão"** ou "Versão do software"
4. **Toque 7 vezes** no número da versão
5. Você verá a mensagem: **"Você agora é um desenvolvedor!"**

### 2. Ativar a Depuração USB

1. **Volte para as Configurações**
2. **Procure por "Opções do desenvolvedor"** ou "Para desenvolvedores"
3. **Ative a opção** (pode estar em Configurações avançadas)
4. **Ative "Depuração USB"** (USB Debugging)

### 3. Autorizar o Computador

1. **Conecte o dispositivo via USB** ao computador
2. **Aparecerá uma notificação** no Android
3. **Toque na notificação**
4. **Marque "Sempre permitir deste computador"**
5. **Toque em "OK"** ou "Permitir"

## 🔍 Como Verificar se Está Funcionando

### Via Terminal (Linux):

```bash
# Verificar se o dispositivo aparece
adb devices

# Deve mostrar algo como:
# List of devices attached
# ABC123DEF456    device
```

### Via AndView:

1. **Abra o AndView**
2. **Vá para a aba "Dispositivos"**
3. **Clique em "Atualizar"**
4. **Seu dispositivo deve aparecer** na lista

## 🚨 Problemas Comuns

### ❌ "Dispositivo não aparece"

**Soluções:**
- Verifique se a depuração USB está ativada
- Reconecte o cabo USB
- Tente outro cabo USB
- Reinicie o dispositivo Android
- Reinicie o serviço ADB: `sudo adb kill-server && adb start-server`

### ❌ "Dispositivo aparece como 'unauthorized'"

**Soluções:**
- Desconecte e reconecte o USB
- No Android, toque na notificação e autorize novamente
- Marque "Sempre permitir deste computador"

### ❌ "ADB não encontrado"

**Soluções:**
- Use o AppImage (inclui ADB)
- Ou instale manualmente:
  ```bash
  # Ubuntu/Debian
  sudo apt install android-tools-adb
  
  # Fedora
  sudo dnf install android-tools
  
  # Arch Linux
  sudo pacman -S android-tools
  ```

## 📶 Conexão WiFi (Opcional)

Após configurar via USB, você pode conectar via WiFi:

1. **Conecte via USB primeiro** (para configurar)
2. **No AndView, vá para a aba "WiFi"**
3. **Configure a conexão WiFi**
4. **Desconecte o USB**
5. **Continue usando via WiFi**

## 🔐 Segurança

### ⚠️ Avisos Importantes:

- **Depuração USB** permite acesso total ao dispositivo
- **Só autorize computadores confiáveis**
- **Desative quando não estiver usando** o AndView
- **Nunca deixe a depuração ativada** em dispositivos de produção

### 🛡️ Como Desativar:

1. **Configurações → Opções do desenvolvedor**
2. **Desative "Depuração USB"**
3. **Ou desative completamente "Opções do desenvolvedor"**

## 📱 Diferentes Versões do Android

### Android 11+ (mais recente):
- As opções podem estar em **"Configurações do sistema"**
- Procure por **"Opções para desenvolvedores"**

### Android 10 e anteriores:
- Geralmente em **"Sobre o telefone"**
- Depois em **"Opções do desenvolvedor"**

### Samsung:
- Pode estar em **"Configurações do desenvolvedor"**
- Ou em **"Informações do software"**

### Xiaomi/MIUI:
- Procure por **"Configurações adicionais"**
- Ou **"Para desenvolvedores"**

## 🆘 Ainda Não Funciona?

Se mesmo seguindo este guia não funcionar:

1. **Verifique se o cabo USB suporta dados** (não apenas carregamento)
2. **Tente outro cabo USB**
3. **Reinicie o dispositivo Android**
4. **Reinicie o computador**
5. **Verifique se há drivers específicos** para seu dispositivo
6. **Consulte a documentação específica** do seu dispositivo

## 📞 Suporte

- **Issues no GitHub:** [AndView Issues](https://github.com/satodu/AndView/issues)
- **Documentação completa:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**💡 Dica:** Mantenha este guia salvo! Você precisará dele sempre que conectar um novo dispositivo ou após atualizações do Android.

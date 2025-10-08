# 🚀 Comece Aqui - AndView

Bem-vindo ao **AndView** - Interface Gráfica para scrcpy e ADB!

## ⚡ Início Rápido

### 1️⃣ Primeiro, instale as dependências do sistema

Como você está no **Nobara/Fedora**, execute:

```bash
# Instale ferramentas de desenvolvimento (NECESSÁRIO!)
sudo dnf install python3-devel gcc gcc-c++

# Instale ADB e scrcpy
sudo dnf install android-tools scrcpy
```

### 2️⃣ Execute a instalação do projeto

```bash
cd /home/panda/Projects/satodu/AndView
./scripts/install.sh
```

Isso irá:
- ✅ Criar ambiente virtual Python
- ✅ Instalar PyQt5 e dependências
- ✅ Criar script de execução
- ✅ (Opcional) Criar atalho no menu

### 3️⃣ Execute o aplicativo

```bash
./andview
```

## 🛠️ Modo Desenvolvimento

Para testar e desenvolver:

```bash
# Execução normal em modo dev
./dev.sh

# Com debug ativado (mostra mais informações)
./dev.sh --debug

# Com saída verbose
./dev.sh --verbose

# Verificar código (instala pylint se necessário)
./dev.sh --lint

# Formatar código (instala black se necessário)
./dev.sh --format

# Limpar arquivos temporários
./dev.sh --clean

# Instalar ferramentas de desenvolvimento
./dev.sh --install-dev

# Ver todas as opções
./dev.sh --help
```

## 📦 Criar AppImage (No Futuro)

Quando quiser distribuir o aplicativo como AppImage:

### 1. Instale o appimagetool

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### 2. Construa o AppImage

```bash
./scripts/build_appimage.sh
```

### 3. Teste o AppImage

```bash
./build/AppImage/AndView-1.0.0-x86_64.AppImage
```

Veja [APPIMAGE.md](APPIMAGE.md) para detalhes completos.

## 📚 Documentação

Criamos vários guias para ajudá-lo:

### Para Usuários Finais
- **[README.md](README.md)** - Visão geral do projeto
- **[QUICKSTART.md](QUICKSTART.md)** - Guia rápido de uso
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solução de problemas

### Para Desenvolvedores
- **[DEV_GUIDE.md](DEV_GUIDE.md)** - Guia completo de desenvolvimento
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Como contribuir
- **[APPIMAGE.md](APPIMAGE.md)** - Como criar AppImage

### Outros
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões
- **[LICENSE](LICENSE)** - Licença MIT

## 🎯 Estrutura do Projeto

```
AndView/
├── main.py                    # ← Inicia o aplicativo
├── src/
│   ├── adb_manager.py         # Gerencia comandos ADB
│   ├── scrcpy_manager.py      # Gerencia scrcpy
│   └── ui/
│       ├── main_window.py     # Janela principal
│       └── widgets/
│           ├── device_list.py    # Lista de dispositivos
│           └── control_panel.py  # Painel de controle
│
├── dev.sh                     # ← Script de desenvolvimento
├── install.sh                 # ← Script de instalação
├── build_appimage.sh          # ← Cria AppImage
│
└── [Documentação em .md]
```

## 🔧 Funcionalidades Principais

✅ **Detecção Automática** de dispositivos Android
✅ **Espelhamento de Tela** com scrcpy (múltiplos presets)
✅ **Instalação de APKs** via interface gráfica
✅ **Captura de Screenshots**
✅ **Console ADB Shell** integrado
✅ **Informações Detalhadas** do dispositivo

## 🎨 Presets de Qualidade

- **Padrão**: Configuração balanceada (8M bitrate)
- **Alta Qualidade**: Melhor visual (16M, 60 FPS, H265)
- **Performance**: Melhor desempenho (720p, 4M, 30 FPS)
- **Baixa Latência**: Menor delay (1024p, 8M, 60 FPS, sem áudio)
- **Gravação**: Para gravar vídeos (16M, 60 FPS)

## 🐛 Problemas Comuns

### Erro ao instalar PyQt5
```bash
# Instale ferramentas de desenvolvimento
sudo dnf install python3-devel gcc gcc-c++
```

### Dispositivo não aparece
```bash
# Verifique se depuração USB está ativada
adb devices

# Reinicie servidor ADB se necessário
adb kill-server
adb start-server
```

### scrcpy com tela preta
- Desbloqueie a tela do dispositivo
- Volte para tela inicial (saia de apps)

Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para mais soluções.

## 📱 Preparando o Dispositivo Android

1. **Ative Opções do Desenvolvedor**:
   - Configurações → Sobre o telefone
   - Toque 7 vezes em "Número da versão"

2. **Ative Depuração USB**:
   - Configurações → Opções do desenvolvedor
   - Ative "Depuração USB"

3. **Conecte via USB**:
   - Use um cabo USB de dados (não apenas carregamento)
   - Autorize o computador quando solicitado
   - Marque "Sempre permitir"

## 💡 Dicas

### Desenvolvimento
```bash
# Sempre use o script de dev para testar
./dev

# Limpe cache antes de testar mudanças importantes
./dev --clean
./dev

# Verifique qualidade do código periodicamente
./dev --lint
./dev --format
```

### Performance
- Use preset "Performance" para dispositivos mais lentos
- Conecte via USB para melhor qualidade (WiFi tem mais latência)
- Feche outros apps no Android para liberar recursos

### Produtividade
- Use `F5` para atualizar lista de dispositivos
- Use `Ctrl+S` para screenshot rápido
- Mantenha comandos frequentes salvos para executar no console

## 🤝 Contribuindo

Quer melhorar o AndView?

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Faça suas alterações
4. Teste com `./dev.sh --debug`
5. Commit (`git commit -m 'Adiciona MinhaFeature'`)
6. Push (`git push origin feature/MinhaFeature`)
7. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📞 Precisa de Ajuda?

1. **Leia a documentação** nos arquivos `.md`
2. **Veja o troubleshooting** em [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. **Execute com debug** para ver erros: `./dev.sh --debug`
4. **Abra uma issue** no GitHub com detalhes do problema

## 🎉 Próximos Passos

Agora que você está configurado:

1. ✅ Execute `./scripts/install.sh` para configurar tudo
2. ✅ Conecte seu dispositivo Android
3. ✅ Execute `./andview` e divirta-se!
4. ✅ Para desenvolvimento, use `./dev`
5. ✅ No futuro, crie AppImage com `./scripts/build_appimage.sh`

**Divirta-se codificando! 🚀**

---

*AndView - Interface Gráfica para scrcpy e ADB*  
*Desenvolvido com ❤️ usando Python e PyQt5*


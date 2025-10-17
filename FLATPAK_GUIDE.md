# Guia para Publicar AndView no Flathub

## 📋 Pré-requisitos

1. **Conta no GitHub** (você já tem)
2. **Conta no Flathub** (você já tem)
3. **Flatpak instalado** no seu sistema
4. **Repositório Git** configurado

## 🚀 Passo a Passo

### 1. Preparar o Repositório Git

```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Prepare for Flathub submission"
git push origin main
```

### 2. Instalar Ferramentas Necessárias

```bash
# Instalar flatpak-builder
sudo apt install flatpak-builder

# Adicionar repositório Flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Instalar SDK do KDE
flatpak install flathub org.kde.Sdk//5.15-22.08
```

### 3. Testar o Build Localmente

```bash
# Executar o script de build
./scripts/build_flatpak.sh
```

### 4. Criar Fork do Flathub

1. Acesse: https://github.com/flathub/flathub
2. Clique em "Fork" no canto superior direito
3. Clone seu fork:
```bash
git clone https://github.com/SEU_USUARIO/flathub.git
cd flathub
```

### 5. Criar Branch para o AndView

```bash
git checkout -b com.satodu.AndView
```

### 6. Adicionar Arquivos do AndView

Crie a estrutura de diretórios:
```bash
mkdir -p com.satodu.AndView
```

Copie os arquivos necessários:
```bash
# Do seu projeto AndView
cp com.satodu.AndView.yml flathub/com.satodu.AndView/
cp com.satodu.AndView.metainfo.xml flathub/com.satodu.AndView/
```

### 7. Adicionar Screenshots

Crie uma pasta para screenshots:
```bash
mkdir -p flathub/com.satodu.AndView/screenshots
```

Adicione screenshots da aplicação (formato PNG, 1280x720 ou 1920x1080):
- `1.png` - Tela principal
- `2.png` - Lista de dispositivos
- `3.png` - Configurações

### 8. Commit e Push

```bash
git add com.satodu.AndView/
git commit -m "Add AndView application"
git push origin com.satodu.AndView
```

### 9. Criar Pull Request

1. Acesse seu fork no GitHub
2. Clique em "Compare & pull request"
3. Preencha o título: "Add AndView - Android Device Manager"
4. Na descrição, inclua:
   - Resumo da aplicação
   - Funcionalidades principais
   - Link para o repositório original
   - Screenshots anexados

### 10. Aguardar Revisão

A equipe do Flathub irá:
- Revisar o manifest
- Testar o build
- Verificar se atende aos critérios
- Aprovar ou solicitar mudanças

## 📝 Critérios do Flathub

### ✅ Obrigatórios
- [x] Manifest válido (com.satodu.AndView.yml)
- [x] Arquivo AppData (metainfo.xml)
- [x] Screenshots da aplicação
- [x] Licença clara (MIT)
- [x] Código fonte público

### ✅ Recomendados
- [x] Documentação clara
- [x] Issues e pull requests abertos
- [x] Releases versionadas
- [x] Descrição detalhada

## 🔧 Troubleshooting

### Erro de Build
```bash
# Verificar logs detalhados
flatpak-builder --verbose --install-deps-from=flathub --repo=repo build com.satodu.AndView.yml
```

### Problemas de Permissão
```bash
# Verificar finish-args no manifest
# Adicionar permissões necessárias
```

### Dependências
```bash
# Verificar se todas as dependências estão no manifest
# Usar versões estáveis das dependências
```

## 📞 Suporte

- **Flathub Issues**: https://github.com/flathub/flathub/issues
- **Flathub Wiki**: https://github.com/flathub/flathub/wiki
- **Flatpak Docs**: https://docs.flatpak.org/

## 🎯 Próximos Passos

1. Execute o build local para testar
2. Crie o fork do Flathub
3. Adicione os arquivos necessários
4. Submeta o pull request
5. Aguarde a aprovação

Boa sorte! 🚀

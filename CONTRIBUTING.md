# 🤝 Contribuindo para o AndView

Obrigado por considerar contribuir para o AndView! Este documento fornece diretrizes e informações para contribuidores.

## 🚀 Como Contribuir

### 1. Fork do Repositório
1. Faça um **fork** deste repositório clicando no botão "Fork" no canto superior direito
2. Clone seu fork localmente:
   ```bash
   git clone https://github.com/SEU_USUARIO/AndView.git
   cd AndView
   ```

### 2. Configurar Ambiente de Desenvolvimento
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o projeto em modo de desenvolvimento:
   ```bash
   ./dev
   ```

### 3. Criar uma Branch
```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b bugfix/corrigir-problema
```

### 4. Fazer Mudanças
- Escreva código limpo e bem documentado
- Siga as convenções de nomenclatura Python
- Adicione comentários quando necessário
- Teste suas mudanças

### 5. Commit e Push
```bash
git add .
git commit -m "feat: adicionar nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### 6. Abrir Pull Request
1. Vá para o repositório original no GitHub
2. Clique em "Compare & pull request"
3. Preencha o template do PR
4. Aguarde a revisão

## 📋 Diretrizes de Contribuição

### 🎯 Tipos de Contribuição
- **🐛 Bug fixes**: Corrigir problemas existentes
- **✨ Novas funcionalidades**: Adicionar recursos
- **📚 Documentação**: Melhorar docs e exemplos
- **🎨 UI/UX**: Melhorar interface
- **🧪 Testes**: Adicionar ou melhorar testes
- **🔧 Build**: Melhorar scripts de build

### 📝 Convenções de Commit
Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adicionar suporte a múltiplos dispositivos
fix: corrigir problema de conexão WiFi
docs: atualizar README
style: formatar código
refactor: reorganizar estrutura de arquivos
test: adicionar testes para ADB manager
```

### 🐍 Padrões de Código Python
- Use **PEP 8** para estilo de código
- Máximo de 88 caracteres por linha (Black formatter)
- Use type hints quando possível
- Documente funções e classes com docstrings

### 🧪 Testando
Antes de submeter um PR:
1. Teste suas mudanças localmente
2. Verifique se não quebrou funcionalidades existentes
3. Execute o aplicativo e teste a funcionalidade

## 🏗️ Estrutura do Projeto

```
AndView/
├── src/                    # Código fonte
│   ├── adb_manager.py     # Gerenciador ADB
│   ├── scrcpy_manager.py  # Gerenciador scrcpy
│   └── ui/               # Interface gráfica
├── scripts/              # Scripts de build e desenvolvimento
├── docs/                # Documentação
└── .github/             # Templates e workflows
```

## 🐛 Reportando Bugs

1. Verifique se o bug já foi reportado
2. Use o template de bug report
3. Inclua informações do ambiente
4. Adicione passos para reproduzir
5. Inclua logs de erro se disponível

## ✨ Sugerindo Funcionalidades

1. Verifique se a funcionalidade já foi sugerida
2. Use o template de feature request
3. Explique o problema que resolve
4. Descreva a solução proposta
5. Considere alternativas

## 📋 Processo de Revisão

1. **Automatizado**: Verificações de CI/CD
2. **Revisão de código**: Mantenedores revisam o código
3. **Testes**: Funcionalidade é testada
4. **Merge**: Após aprovação, o PR é mergeado

## 🏷️ Labels

- `bug`: Problema que precisa ser corrigido
- `enhancement`: Nova funcionalidade
- `documentation`: Mudanças na documentação
- `good first issue`: Bom para iniciantes
- `help wanted`: Precisa de ajuda da comunidade
- `question`: Pergunta ou discussão

## 💬 Comunidade

- **Discussions**: Para perguntas e discussões
- **Issues**: Para bugs e feature requests
- **Pull Requests**: Para contribuições de código

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).

## 🙏 Agradecimentos

Obrigado a todos os contribuidores que ajudam a tornar o AndView melhor!

---

**Precisa de ajuda?** Abra uma [discussão](https://github.com/satodu/AndView/discussions) ou entre em contato!

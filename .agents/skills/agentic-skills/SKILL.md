---
name: agentic-skills
description: Gerencia e busca no catálogo de mais de 2.690 skills locais do Agentic Awesome Skills (AAS). Permite buscar, ler e instalar qualquer skill instantaneamente no projeto (.agents/skills) ou globalmente (~/.gemini/config/skills).
---

# Agentic Awesome Skills (AAS) - Catálogo Local

Esta skill dá acesso ao acervo local com mais de 2.690 skills de inteligência artificial e engenharia de software para o Antigravity.

## Estrutura do Acervo
- **Diretório Raiz**: `C:\Users\lexke\.gemini\agentic-awesome-skills`
- **Índice de Skills**: `C:\Users\lexke\.gemini\agentic-awesome-skills\skills_index.json`
- **Pastas de Skills**: `C:\Users\lexke\.gemini\agentic-awesome-skills\skills\<skill-id>`
- **Helper CLI**: `C:\Users\lexke\.gemini\agentic-awesome-skills\aas-helper.js` (ou `aas.bat`)

## Como Buscar e Instalar Skills

### 1. Pelo Assistente / Terminal
- **Buscar por palavra-chave ou tecnologia**:
  ```bash
  node "C:\Users\lexke\.gemini\agentic-awesome-skills\aas-helper.js" search "<termo>"
  ```
- **Instalar em escopo Global** (`~/.gemini/config/skills/`):
  ```bash
  node "C:\Users\lexke\.gemini\agentic-awesome-skills\aas-helper.js" install <skill-id> --global
  ```
- **Instalar no Projeto Atual** (`.agents/skills/`):
  ```bash
  node "C:\Users\lexke\.gemini\agentic-awesome-skills\aas-helper.js" install <skill-id>
  ```
- **Listar Categorias Disponíveis**:
  ```bash
  node "C:\Users\lexke\.gemini\agentic-awesome-skills\aas-helper.js" categories
  ```

## Boas Práticas
- Evite instalar todas as 2.690 skills simultaneamente no diretório de monitoramento contínuo para economizar tokens de contexto do modelo.
- Instale e ative as skills sob demanda conforme a necessidade de cada projeto (ex: desenvolvimento web, segurança, debugging, gamedev, backend, devops).

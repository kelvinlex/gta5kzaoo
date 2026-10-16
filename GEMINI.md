# Diretrizes do Projeto no Antigravity IDE

## Idioma Obrigatório
- Sempre responder em português do Brasil (pt-BR).

## Otimização de Tokens e Contexto (tokenleak & context-pruning)
1. **Respostas Diretas**: Seja direto ao ponto, sem enrolação e sem explicações desnecessárias que gastem tokens à toa.
2. **Localizar antes de ler**: Nunca leia arquivos gigantes inteiros. Use busca cirúrgica (`grep`, `sed`) e leia apenas o trecho necessário.
3. **Não reler**: Nunca releia arquivos ou logs que já estão no contexto da conversa.
4. **Comandos limitados**: Saídas de comandos devem ser concisas e limitadas (evitar despejar milhares de linhas no terminal).
5. **Edições cirúrgicas**: Use ferramentas de substituição pontual (`replace_file_content`) em vez de reescrever arquivos inteiros.

## Gamedev & Gráficos 3D
- Aplicar as melhores práticas das skills `game-development`, `gamedev`, `threejs-skills` e `shader-programming-glsl`.
- Focar em alta taxa de quadros (60 FPS), baixo consumo de VRAM e compatibilidade WebGPU/WebGL para PC e dispositivos móveis.

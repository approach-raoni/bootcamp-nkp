# BOOT CAMP NKP | COMECE AQUI
Material do instrutor · Versão 1.1 · 21/10/2026
## Arquivos principais
- Apresentacao_BootCamp_NKP_Approach.pptx: apresentação completa, com notas de condução.
- Guia_BootCamp_NKP_Approach.pdf / .docx: roteiro do instrutor.
- Caderno_Aluno_NKP.pdf / .docx: exercícios da turma.
- repositorio: aplicação, manifests, scripts e procedimentos para publicar no Git.
## Preparação do instrutor
1. Escolha o cluster de trabalho; confira capacidade, Flux e permissões.
2. Reserve um IP de LoadBalancer por aluno e teste o acesso pela rede dos participantes.
3. Publique o conteúdo de repositorio na raiz de um Git compartilhado, branch main.
4. Substitua a URL de exemplo pela real e gere os arquivos da turma.
5. Aplique admin.yaml por aluno e associe sua identidade ao papel bootcamp-aluno.
6. Ensaie deploy v1, exposição, GitOps, atualização v2 e reversão.
## Gerar a turma
Na bastion Linux, dentro da raiz do repositório:
```bash
python3 ferramentas/preparar_turma.py --alunos 10 \
  --repositorio https://github.com/SUA-ORG/bootcamp-nkp.git
```
O script apenas gera arquivos. Ajuste a quantidade à capacidade do ambiente.
## Modelo da aula
Todos usam main / loja; cada instalação fica em app-aluno01, app-aluno02 etc. Os alunos fazem o deploy inicial. O instrutor ativa GitOps e publica a v2 para toda a turma.
A loja usa código estático em ConfigMap com hash, sem build de imagem. O guia explica o mecanismo e os comandos de validação.
## Conferência final
Nós e pods Ready; imagem disponível; Flux observando os namespaces; IPs acessíveis; permissões individuais; v1 no Git. Consulte VALIDACAO.md para o escopo dos testes locais e faça o ensaio no NKP antes do evento.

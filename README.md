# Boot Camp NKP | Approach
Repositorio compartilhado, branch main e pasta loja/.
Cada aluno utiliza app-aluno01, app-aluno02, etc.
Somente o instrutor publica as atualizacoes no Git.

1. Instrutor publica este conteudo em um repositorio Git acessivel pelo cluster.
2. Instrutor gera os manifests por aluno:
   python3 ferramentas/preparar_aluno.py --aluno 01 --repositorio https://github.com/SUA-ORG/bootcamp-nkp.git
3. Instrutor aplica gerados/app-aluno01/admin.yaml e vincula a identidade real ao Role bootcamp-aluno.
4. Aluno, autenticado no cluster de trabalho, executa:
   kubectl apply -k loja -n app-aluno01
5. Instrutor ativa o GitOps aplicando gerados/app-aluno01/gitops.yaml.
6. Instrutor publica a v2 com:
   cp atualizacoes/v2/index.html loja/site/index.html
   git add loja/site/index.html
   git commit -m "Loja v1.1.0: cupom e novo produto"
   git push origin main

Leia docs/GUIA_BOOTCAMP.md para o procedimento completo, pre-requisitos,
resultados esperados, isolamento, validacao, reversao e limpeza.

A aplicacao e uma simulacao estatica com carrinho no navegador, sem banco,
pagamento ou autenticacao. A v2 habilita o cupom NKP10, adiciona um produto
e altera a identidade visual. A v1 possui catalogo e carrinho. A v2 acrescenta o campo de cupom,
a logica de desconto e um produto, alem de alterar a identificacao da versao.

O Kustomize gera um ConfigMap com hash do conteudo e atualiza a referencia
no Deployment, disparando um rollout. Nao ha build de imagem neste laboratorio.
Para aplicacoes compiladas, adicione CI, publique imagem imutavel e altere
a referencia de imagem no Git.

Nao execute flux bootstrap, flux install ou troca dos controladores gerenciados
pelo NKP. Verifique se o Flux do cluster de trabalho observa estes namespaces.
O fluxo deste kit usa recursos Flux diretamente no cluster, sem criar um
GitopsRepository de Project no Kommander. Evite dupla gestao do mesmo workload.

Os arquivos gerados sao locais e estao ignorados pelo Git. Nenhum script deste
kit se conecta ao cluster, publica commits ou envia credenciais automaticamente.

Materiais adicionais: docs/CADERNO_ALUNO.md e docs/COMECE_AQUI.md.
Gere varios namespaces com ferramentas/preparar_turma.py.
Validacao opcional: ferramentas/validar_aluno.py --help.

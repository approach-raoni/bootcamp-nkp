# BOOT CAMP NKP | APPROACH
## Guia do instrutor e laboratório dos participantes
Versão 1.1 · 21/10/2026 · Raoni Santana
Modelo: repositório compartilhado / branch main / pasta loja / namespaces app-alunoNN.

## 1. Resultado que o cliente deve experimentar
Ao final, cada aluno terá uma loja acessível pelo navegador, executando no seu namespace. O instrutor publicará uma única atualização no Git; todas as instalações que acompanham a mesma origem receberão a nova versão automaticamente. O aluno identificará a versão, o pod e o commit aplicado, e acompanhará uma reversão controlada.
A loja é uma simulação estática, sem banco, autenticação ou pagamentos. O carrinho fica na memória do navegador e é reiniciado quando a página é recarregada. O exercício não depende de PVC, banco ou construção de imagem.
Neste laboratório, o código HTML/JavaScript é entregue por ConfigMap. A alteração do conteúdo gera um nome com hash e muda o template do Deployment, provocando a troca gradual dos pods. Em uma aplicação compilada, uma esteira de CI construiria a imagem e publicaria uma referência imutável no Git.
O procedimento usa recursos Flux diretamente no cluster de trabalho. Ele não cria um GitopsRepository de Project no Kommander. A demonstração de Workspaces/Projects é complementar; não cadastre a mesma aplicação nos dois fluxos ao mesmo tempo.

## 2. Mensagem de abertura e posicionamento
Fala sugerida: “Hoje vamos sair de um cluster pronto e chegar a uma aplicação publicada, atualizada e recuperável. O objetivo é entender como o NKP ajuda a operar Kubernetes com consistência.”
O NKP é uma plataforma Kubernetes. Scheduling, Deployment, Service e recuperação de pods pertencem ao Kubernetes. Flux e GitOps também existem em outras plataformas. O argumento comercial deve conectar integração, validação da stack, gestão centralizada, ciclo de vida e suporte ao esforço que o cliente teria para integrar e manter esses componentes.
Evite prometer que outras plataformas não têm GitOps ou que o NKP torna qualquer aplicação automaticamente mais rápida. Para comparar com uma plataforma empresarial concorrente, valide os mesmos critérios no contexto do cliente.
| Necessidade do cliente | O que demonstrar | Mensagem de valor |
| --- | --- | --- |
| Padronizar ambientes | Mesmo Git em namespaces ou clusters distintos | Uma origem de configuração, repetível |
| Reduzir trabalho operacional | Kommander, ciclo de vida e apps da plataforma | Menos integrações mantidas isoladamente |
| Organizar equipes | Workspaces/Projects, identidades, RBAC e quotas | Acesso e consumo com governança |
| Acompanhar operação | Métricas, eventos e logs disponíveis | Diagnóstico com contexto |
| Controlar mudanças | Git, reconciliação e reversão | Histórico e recuperação reproduzíveis |
NKP Ultimate é o contexto comercial do evento. Catálogo, custos, observabilidade, Insights e demais módulos só devem ser demonstrados se estiverem licenciados, instalados e operacionais no ambiente. Não inferir ativação apenas pela edição.

## 3. Agenda sugerida
O laboratório principal dura cerca de 3 horas. Acrescente de 30 a 60 minutos se a turma for criar clusters; o provisionamento deve ser ensaiado previamente.
| Bloco | Tempo | Marco |
| --- | --- | --- |
| Abertura e posicionamento | 15 min | Entender o objetivo e o valor |
| Fundamentos e navegação no Kommander | 25 min | Cluster, namespace, pod e Service |
| Acesso e preparação por aluno | 20 min | Permissões e contexto corretos |
| Deploy e LoadBalancer | 30 min | Loja v1 acessível |
| Ativação e atualização por GitOps | 35 min | Loja v2 aplicada em toda a turma |
| Recuperação, drift e reversão | 30 min | Estado desejado restaurado |
| Observabilidade e encerramento | 25 min | Evidências e próximos passos |

## 4. Organização da turma
| Participante | Namespace | Git | Aplicação |
| --- | --- | --- | --- |
| Aluno 01 | app-aluno01 | Mesmo repositório / main / loja | Deployment loja + Service loja |
| Aluno 02 | app-aluno02 | Mesmo repositório / main / loja | Deployment loja + Service loja |
| Aluno 03 | app-aluno03 | Mesmo repositório / main / loja | Deployment loja + Service loja |
Cada namespace tem duas réplicas, um Service LoadBalancer e um GitRepository/Kustomization próprios. Os nomes dos recursos podem se repetir em namespaces diferentes. Reserve um IP de LoadBalancer disponível por aluno.
Uma alteração na pasta loja afeta todos os alunos; a reconciliação é assíncrona e não acontece no mesmo instante. Namespace separa recursos, mas não separa o código publicado na origem compartilhada.
Só o instrutor precisa publicar no Git. Os alunos precisam de acesso de leitura ao repositório e de credenciais individuais para seus namespaces. Leitura pública simplifica a turma; um repositório privado exige credenciais de leitura do Flux em cada namespace, preparadas previamente e sem segredos no Git.
Namespaces e RBAC não equivalem a isolamento de rede. Se o evento exigir bloqueio entre equipes, preparar e validar NetworkPolicies com o CNI. Não entregar kubeconfig administrativo aos participantes.
Para limitar privilégios, o instrutor cria namespace, quota, RBAC e os objetos Flux. Os alunos fazem o deploy inicial da loja e acompanham o GitOps; o papel fornecido não permite alterar reconciliações privilegiadas.

## 5. Preparação do instrutor — antes do evento
Use uma bastion Linux com Bash, Git, Python 3 e kubectl compatível com o cluster. Os comandos deste guia são para esse terminal; não são comandos PowerShell. Os exemplos usam app-aluno01. Cada aluno substitui apenas pelo namespace que recebeu.
Preencha: URL de clone ____________________; cluster de trabalho ____________________; versão NKP ____________________; número de alunos ______; pool de IPs ____________________; conta de cada aluno ____________________.
A referência conceitual é NKP 2.18 e APIs Flux v1. Confirmar as versões e as políticas efetivamente instaladas antes da turma. Não usar o cluster de gestão para a carga do laboratório quando houver cluster de trabalho disponível.
Confira conectividade, nós, recursos Flux e seus controladores:
```bash
kubectl config current-context
kubectl cluster-info
kubectl get nodes
kubectl get deployments -A
kubectl get crd gitrepositories.source.toolkit.fluxcd.io
kubectl get crd kustomizations.kustomize.toolkit.fluxcd.io
```
Resultado esperado: contexto de trabalho correto; nós Ready; source-controller e kustomize-controller disponíveis e configurados para observar os namespaces app-alunoNN. A existência das CRDs, sozinha, não prova que os controladores estão em execução.
Inspecione a configuração e o escopo de observação dos controladores usando o namespace e os nomes reais retornados pelo ambiente. Se esse cluster não tiver reconciliação Flux disponível para os namespaces da turma, preparar o fluxo suportado de Project do NKP antes do evento ou escolher outro cluster. Não instalar um segundo Flux nem executar flux bootstrap/flux install sobre a stack gerenciada pelo NKP.
Confirme o balanceamento:
```bash
kubectl get ipaddresspools.metallb.io -A
kubectl get l2advertisements.metallb.io -A
kubectl get services -A
```
Em cloud pública, valide o controlador LoadBalancer do provedor. No laboratório Nutanix on-premises com MetalLB, confirme pool livre, anúncio L2 ou BGP e alcance do cliente ao IP. O VIP da API Kubernetes, o IP do Kommander e os IPs das aplicações têm funções distintas.
Se já houver pool gerenciado e funcional, reutilize-o. O arquivo extras/metallb.yaml.example é apenas documental: exige namespace real, IPs reservados e validação de rede. Não sobrescrever a configuração existente durante a turma.
Valide acesso HTTPS do Flux ao Git, resolução DNS, proxy/CA e download da imagem nginxinc/nginx-unprivileged:1.28-alpine pelos workers. Antes do evento, confirmar a disponibilidade da tag; em ambiente restrito, espelhar a imagem e alterar o manifesto no Git. Para repetibilidade maior, fixar o digest aprovado após o ensaio.
Capacidade apenas da loja: por aluno, 2 pods solicitam 100m de CPU e 128Mi de memória; durante rollout com surge 1, até 3 pods solicitam 150m e 192Mi. Os limites durante esse pico somam 750m e 384Mi. Isso não inclui plataforma, sistema, VMs nem outros workloads. Dimensionar para atualizações simultâneas e manter folga.
Faça o ensaio completo com um aluno: deploy v1, IP, GitOps Ready, atualização v2, validação dos dois pods e reversão. Não iniciar a aula com v2 já publicada.

## 6. Publicar o repositório compartilhado
Extraia o diretório repositorio do kit e use-o como raiz do repositório. A pasta loja e a pasta atualizacoes precisam ficar diretamente na raiz. Os arquivos templates não são manifests prontos para aplicar.
No provedor Git, crie previamente um repositório vazio chamado bootcamp-nkp. Substitua SUA-ORG pela organização real e configure sua autenticação de escrita; nenhum token deve entrar nos arquivos do projeto.
```bash
git init -b main
git add .
git commit -m "Bootcamp NKP: loja v1"
git remote add origin https://github.com/SUA-ORG/bootcamp-nkp.git
git push -u origin main
```
Resultado esperado: branch main publicada com loja/site/index.html na versão 1.0.0. Esse endereço é um exemplo, não um repositório já criado.
O diretório atualizacoes contém as duas versões para facilitar a demonstração; somente loja é reconciliada pelo Flux. Não apontar o Flux para a raiz inteira nem para atualizacoes.

## 7. Preparar os namespaces — instrutor
Gere os arquivos do aluno 01 e repita para cada número. O script só escreve manifests locais; ele não acessa o cluster.
```bash
python3 ferramentas/preparar_aluno.py --aluno 01 \
  --repositorio https://github.com/SUA-ORG/bootcamp-nkp.git
kubectl apply -f gerados/app-aluno01/admin.yaml
```
O arquivo admin.yaml cria o namespace app-aluno01, quota, ServiceAccount e papéis. O reconciliador pode gerenciar apenas ConfigMaps, Services e Deployments do seu namespace e ler os recursos necessários para saúde.
Vincule a identidade exata do aluno ao papel fornecido. IDENTIDADE_REAL_DO_ALUNO é o nome autenticado pelo IdP/kubeconfig, não necessariamente o e-mail digitado pelo participante.
```bash
kubectl create rolebinding acesso-aluno -n app-aluno01 \
  --role=bootcamp-aluno --user=IDENTIDADE_REAL_DO_ALUNO
```
Para grupos, use a identificação real do IdP e --group no lugar de --user. Se o RoleBinding já existir, revisar antes de atualizar; não criar vínculos administrativos genéricos.
Entregue ao aluno o kubeconfig individual/contexto do cluster de trabalho, o namespace e a URL de clone. Ainda não aplique gitops.yaml: a turma fará primeiro o deploy inicial para entender os recursos.
Como aluno, validar:
```bash
kubectl config current-context
kubectl auth can-i create deployments -n app-aluno01
kubectl auth can-i create deployments -n app-aluno02
```
Resultado esperado para o aluno 01: yes no próprio namespace e no no namespace do colega. Se a segunda resposta for yes, corrigir permissões antes da aula. O teste é do usuário aluno, não da credencial administrativa.

## 8. Criação de clusters — opcional, com limite de tempo
Com Kommander pronto, o instrutor apresenta Workspace e cluster de trabalho. Havendo recursos, divide a turma em grupos para criar alguns clusters. Reservar um cluster pronto como alternativa para que todos concluam o laboratório.
Definir previamente nome, infraestrutura, versão suportada, imagem de nó, rede, VIP da API, pool de LoadBalancer e tamanhos compatíveis. Usar o assistente da versão instalada do NKP; os nomes das telas podem mudar. Não habilitar aplicativos adicionais sem dimensionar a capacidade.
Validar nós e aplicações da plataforma antes de distribuir acessos. Cada grupo usa o kubeconfig do seu cluster e os mesmos namespaces app-alunoNN. Um control plane único pode ser uma concessão de laboratório, mas não deve ser apresentado como alta disponibilidade.
Fala sugerida: “O gerenciamento permanece central, enquanto as aplicações podem estar em clusters diferentes. O exercício de GitOps será o mesmo em cada destino.”

## 9. Deploy inicial — alunos
No terminal individual, clonar o repositório e entrar na pasta:
```bash
git clone https://github.com/SUA-ORG/bootcamp-nkp.git
cd bootcamp-nkp
kubectl config current-context
kubectl kustomize loja
kubectl apply -k loja -n app-aluno01
kubectl rollout status deployment/loja -n app-aluno01 --timeout=180s
kubectl get pods -n app-aluno01 -l app=loja -o wide
```
Resultado esperado: dois pods Running e Ready. Os manifests da loja não fixam namespace; -n define o destino neste primeiro apply. A preferência de anti-afinidade distribui os pods quando houver nós disponíveis, mas não garante isso em um cluster com apenas um worker.
Explicar: Deployment declara duas réplicas; ConfigMap contém o site; Service encontra os pods por label app=loja. Abrir loja/kustomization.yaml e mostrar os nomes com hash produzidos no build.
Ponto de controle: todos os alunos precisam de dois pods prontos antes da publicação da v2.

## 10. Expor via LoadBalancer e abrir a loja — alunos
O manifesto loja/service.yaml já solicita type: LoadBalancer, porta 80, destino 8080. Em um pool funcional, o controlador atribui o endereço.
```bash
kubectl get service loja -n app-aluno01 -w
```
Quando EXTERNAL-IP tiver um valor, encerrar a observação com Ctrl+C. Abrir http://IP_DO_SEU_LOADBALANCER no navegador. É HTTP no laboratório interno; TLS pode ser uma extensão posterior.
```bash
curl -fsS http://IP_DO_SEU_LOADBALANCER/healthz
curl -fsS http://IP_DO_SEU_LOADBALANCER/runtime.json
```
Resultado esperado: healthz retorna ok; runtime.json identifica um pod; a página mostra VERSÃO 1.0.0, três produtos e carrinho funcional. Cada aluno anota namespace, IP e nome de um pod.
Se o IP ficar pending, investigar pool/controlador. Se o IP existir sem acesso, conferir anúncio, rotas, VLAN, firewall e endpoints. IP atribuído não prova conectividade.
Explicar os slides de exposição do PPT: NodePort oferece uma porta em cada nó; LoadBalancer fornece o ponto de entrada; um controlador Ingress pode compartilhar esse ponto entre vários hosts HTTP. Para esta turma, a trilha principal é LoadBalancer direto. Requisições repetidas não garantem alternância visível de pod por causa das conexões mantidas.

## 11. Ativar GitOps por namespace — instrutor e alunos
Instrutor: revisar URL, branch main, path ./loja, namespace e serviceAccountName no arquivo gerado. Aplicar uma vez em cada destino:
```bash
kubectl apply -f gerados/app-aluno01/gitops.yaml
```
Alunos: observar a origem e a reconciliação:
```bash
kubectl get gitrepositories -n app-aluno01
kubectl get kustomizations -n app-aluno01
kubectl describe gitrepository loja -n app-aluno01
kubectl describe kustomization loja -n app-aluno01
```
Resultado esperado: ambos Ready=True, com revisão main@sha1:... ou formato equivalente da versão instalada. GitRepository disponibiliza o conteúdo; Kustomization constrói a pasta loja e aplica no namespace indicado.
O instrutor deve manter os objetos Flux fora das permissões de escrita dos alunos. serviceAccountName limita as alterações do reconciliador; apenas targetNamespace não é um mecanismo de autorização.
Fala sugerida: “A partir daqui, o Git descreve o estado desejado. O comando manual foi o primeiro contato; as próximas mudanças virão da origem versionada.”

## 12. Publicar a versão 2 — somente instrutor
Em sua cópia atualizada da branch main:
```bash
git switch main
git pull --ff-only
cp atualizacoes/v2/index.html loja/site/index.html
git diff -- loja/site/index.html
git add loja/site/index.html
git commit -m "Loja v1.1.0: cupom e novo produto"
git push origin main
git rev-parse HEAD
```
Anotar o SHA do commit v2. A atualização modifica o HTML e o JavaScript: acrescenta o campo de cupom, a lógica de desconto, o quarto produto e a identificação da nova versão. A versão inicial não contém o campo nem o código de aplicação de cupom.
Não executar novo kubectl apply, rollout restart ou edição de pod para provocar a atualização. Aguardar a observação do Git. O intervalo configurado é 1 minuto; download, construção e rollout acrescentam tempo.
O Kustomize produz um novo ConfigMap e muda a referência do volume no template do Deployment. A estratégia maxUnavailable=0 e maxSurge=1 busca manter as réplicas disponíveis durante a troca, desde que haja capacidade e os novos pods fiquem saudáveis.
Fala sugerida: “Fizemos uma publicação na origem. Cada destino está convergindo para essa mesma versão, sem repetir o deploy manual.”

## 13. Validar a atualização — cada aluno
Primeiro, acompanhar a nova revisão. Não usar apenas rollout status imediatamente após o push: ele pode informar a conclusão da versão anterior.
```bash
kubectl get gitrepositories -n app-aluno01 -w
```
Conferir que a revisão da origem corresponde ao SHA v2 anotado. Sair com Ctrl+C, acompanhar a Kustomization e confirmar também a revisão aplicada:
```bash
kubectl get kustomizations -n app-aluno01 -w
```
Quando Ready=True para a revisão nova, sair com Ctrl+C. O describe detalha Last Applied Revision, condições e mensagens quando necessário.
```bash
kubectl describe kustomization loja -n app-aluno01
kubectl rollout status deployment/loja -n app-aluno01 --timeout=180s
kubectl get pods -n app-aluno01 -l app=loja -o wide
kubectl get replicasets -n app-aluno01
```
Conferir a versão no arquivo servido por cada um dos dois pods novos. Substituir NOME_DO_POD pelo nome real e repetir para o outro pod:
```bash
kubectl exec -n app-aluno01 NOME_DO_POD -- \
  grep data-version /usr/share/nginx/html/index.html
```
Resultado esperado: ambos contêm data-version="1.1.0". No navegador, atualizar a página; se necessário, usar Ctrl+F5. Verificar quatro sinais: VERSÃO 1.1.0, faixa laranja, produto Fone DevOps e campo de cupom.
Adicionar um produto de R$ 79,90 e aplicar NKP10: o total deve ser R$ 71,91. Atualizar a página reinicia o carrinho, pois o estado é apenas do navegador.
Critério de sucesso: novo SHA observado e aplicado, rollout concluído, dois pods servindo v2 e comportamento esperado no navegador. Confirmar apenas a versão em uma página não prova que todos os pods foram atualizados.

Validação automatizada opcional: ferramentas/validar_aluno.py aceita --namespace, --versao, --sha e --url. Ele usa kubectl somente para consultar o estado e ler o arquivo servido em cada pod; exige o SHA completo anotado. Consulte --help para o formato.

## 14. Recuperação de pod e correção de drift — extensão
No próprio namespace de laboratório, listar os pods e excluir apenas um deles pelo nome:
```bash
kubectl get pods -n app-aluno01 -l app=loja
kubectl delete pod NOME_DE_UM_POD -n app-aluno01
kubectl get pods -n app-aluno01 -l app=loja -w
```
Resultado esperado: o Deployment repõe a réplica. Pode existir um breve período de convergência; o acesso depende de haver outra réplica pronta. Isso demonstra comportamento Kubernetes, não um recurso exclusivo do NKP.
Para demonstrar correção de uma alteração manual:
```bash
kubectl scale deployment loja -n app-aluno01 --replicas=3
kubectl get deployment loja -n app-aluno01 -w
```
O Git continua declarando duas réplicas. Na reconciliação seguinte, esperar o retorno a duas. Não fazer esse exercício se houver HPA ou outra automação concorrente; o kit não instala HPA.

## 15. Reverter a atualização — instrutor
Substituir SHA_DO_COMMIT_V2 pelo commit registrado na etapa 12. Não usar force push.
```bash
git switch main
git pull --ff-only
git revert --no-edit SHA_DO_COMMIT_V2
git push origin main
git rev-parse HEAD
```
Cada aluno repete a validação do novo SHA de reversão, rollout e dois pods. Ao recarregar a loja, a versão deve voltar a 1.0.0, com três produtos e sem campo de cupom.
A reversão afeta toda a turma, pois todos seguem a mesma origem. Preferir reversão no Git ao kubectl rollout undo, que seria uma alteração no cluster sujeita à reconciliação.

## 16. Navegação no Kommander e fechamento comercial
Selecionar o cluster de trabalho e os recursos do namespace do aluno. Mostrar estado dos pods, eventos, logs e métricas quando esses aplicativos estiverem disponíveis. Mostrar Workspaces/Projects como organização e governança da plataforma.
Explicar a fronteira: o namespace criado por este kit não se torna automaticamente um Project do Kommander. A trilha nativa de Project deve ser preparada de acordo com a versão instalada e a política de tenant, sem duplicar a gestão desta loja.
Perguntas para o cliente: quem administra os clusters hoje? Como aprovam uma mudança? Como identificam versões entre ambientes? Quem integra e atualiza a stack? Qual evidência precisam para auditoria? Quais workloads precisam de dados persistentes?
Fala sugerida: “O laboratório usou componentes abertos e APIs Kubernetes. O valor da plataforma está em integrar a operação desses componentes e organizar seu uso em escala.”
Não demonstrar um upgrade real do NKP durante a aula principal; mostrar o fluxo e os pré-requisitos é suficiente. Armazenamento, backup, restauração e custos podem ser encontros adicionais, com dependências e licenças próprias.

## 17. Troubleshooting rápido
| Sintoma | Verificar primeiro | Próximo passo |
| --- | --- | --- |
| Forbidden | Contexto e identidade do aluno | Rever RoleBinding do próprio namespace |
| GitRepository não fica Ready | URL, branch, DNS, TLS e autenticação | describe gitrepository; corrigir a origem |
| Kustomization não fica Ready | path, YAML, RBAC e condições | describe kustomization; revisar eventos |
| Flux não reage em nenhum aluno | Controladores e escopo de observação | Instrutor confirma preparação do cluster |
| EXTERNAL-IP pending | Controlador, pool e quota de LB | Conferir IPs livres e eventos do Service |
| IP atribuído sem acesso | Anúncio L2/BGP, rota e firewall | Conferir endpoints e caminho do cliente |
| ImagePullBackOff | Imagem, registry, proxy e limite de pull | describe pod e validar espelho da imagem |
| Pod Pending | Requests, quota e capacidade de surge | Conferir eventos e nós |
| CrashLoopBackOff | Nginx, volumes e permissões | Logs atuais/anteriores do container |
| Flux mostra v2, página mostra v1 | SHA aplicado, pods e endereço aberto | Conferir ambos os pods e recarregar sem cache |
Comandos curtos de apoio:
```bash
kubectl describe service loja -n app-aluno01
kubectl get endpointslices -n app-aluno01
kubectl get events -n app-aluno01 --sort-by=.lastTimestamp
kubectl describe pod NOME_DO_POD -n app-aluno01
kubectl logs NOME_DO_POD -n app-aluno01
kubectl logs NOME_DO_POD -n app-aluno01 --previous
kubectl get resourcequota -n app-aluno01
```
O aluno pode usar kubectl port-forward service/loja 8080:80 -n app-aluno01 e abrir http://127.0.0.1:8080 para separar falha da aplicação de falha do caminho externo. Esse é um diagnóstico, não a conclusão do exercício de LoadBalancer.
O instrutor pode solicitar reconciliação antecipada com Flux CLI, se já disponível e autorizado. A trilha principal não depende dessa CLI; não substituir a demonstração automática por acionamento manual sem explicar.

## 18. Limpeza e preparação para a próxima turma
Somente o instrutor, depois do encerramento e da coleta de evidências, remove os recursos dos namespaces dedicados. Deletar a Kustomization com prune=true elimina os recursos sob sua gestão.
```bash
kubectl delete -f gerados/app-aluno01/gitops.yaml
kubectl delete -f gerados/app-aluno01/admin.yaml
```
Repetir por aluno e cluster correto. A exclusão do namespace remove tudo que estiver nele; não executar em namespaces reutilizados para outras aplicações. Não remover controladores Flux, pools MetalLB ou componentes da plataforma.
Para novo evento, publicar uma reversão/commit que mantenha loja na v1, confirmar main e repetir o ensaio. Não limpar o histórico do Git.

## 19. Roteiro de slides e falas para ampliar o PPT
A apresentação completa incorpora os 12 slides originais e o roteiro de laboratório, com notas do apresentador. As grafias “Kubernets” e “Plataform” foram corrigidas nos textos editáveis. O deck complementar permite repetir somente a parte prática.
| Slide complementar | Mensagem principal | Ação do instrutor |
| --- | --- | --- |
| Objetivo do laboratório | Do Git ao navegador | Mostrar o resultado esperado |
| Agenda e papéis | Um instrutor publica; alunos operam destinos | Identificar as etapas |
| NKP e Kubernetes | Integração e gestão são o foco | Evitar alegações de exclusividade |
| Topologia da turma | Mesmo Git, namespaces app-alunoNN | Distribuir a ficha de cada aluno |
| Pré-requisitos | Flux, rede, imagem e capacidade prontos | Conferir o ensaio |
| Contexto e acesso | Cada aluno no seu destino | Validar RBAC |
| Deploy da loja v1 | Deployment, ConfigMap e Service | Acompanhar dois pods Ready |
| Exposição LoadBalancer | Um endereço por instalação | Abrir a loja |
| GitOps por namespace | GitRepository + Kustomization | Instrutor ativa a reconciliação |
| Publicar v2 | Uma mudança alcança a turma | Fazer commit e push |
| O que muda nos pods | Hash do ConfigMap muda o template | Acompanhar rollout |
| Validar a entrega | SHA, saúde, pods e navegador | Testar cupom NKP10 |
| Recuperação e drift | Estado real converge ao desejado | Excluir um pod e corrigir escala |
| Reversão | Git também registra o retorno | Reverter o commit v2 |
| Diagnóstico | Separar origem, cluster e rede | Mostrar eventos e logs |
| Encerramento | Evidências e próximos passos | Relacionar com a operação do cliente |

## 20. Ficha de conclusão e critérios de aceite
| Item | Preencher / confirmar |
| --- | --- |
| Participante / namespace | ____________________ / app-aluno____ |
| Cluster e contexto | ____________________ |
| IP da loja | ____________________ |
| SHA aplicado da v2 | ____________________ |
| Dois pods v2 Ready | Sim / Não |
| Página 1.1.0 e quarto produto | Sim / Não |
| NKP10: R$ 79,90 para R$ 71,91 | Sim / Não |
| Recuperação de pod observada | Sim / Não |
| Reversão para v1 confirmada | Sim / Não |
Entregar as evidências sem tokens, kubeconfigs ou informações de outros clientes. O instrutor encerra quando todos alcançarem o núcleo do exercício: v1 acessível, v2 automática e validação do resultado.

## 21. Referências oficiais e limites da validação
Conteúdo conferido em fontes oficiais em 20/10/2026 e revisado em 21/10/2026. Os arquivos do kit precisam do ensaio no NKP de destino: este material não implica que um deploy foi executado no ambiente do cliente.
- Nutanix NKP — plataforma e capacidades: https://www.nutanix.com/products/kubernetes-management-platform
- Nutanix — GitOps e operação declarativa: https://www.nutanix.dev/2026/04/01/avoid-these-kubernetes-anti-patterns-a-guide-for-virtualization-professionals/
- Flux GitRepository: https://fluxcd.io/flux/components/source/gitrepositories/
- Flux Kustomization e controle de acesso: https://fluxcd.io/flux/components/kustomize/kustomizations/
- Kubernetes Kustomize: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- Kubernetes Deployment: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- MetalLB — pool e anúncio de endereços: https://metallb.io/configuration/
- NGINX sem privilégios: https://github.com/nginx/docker-nginx-unprivileged

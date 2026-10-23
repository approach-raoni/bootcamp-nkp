# BOOT CAMP NKP | CADERNO DO ALUNO
Versão 1.1 · 21/10/2026 · Approach
## Sua ficha
| Informação | Valor informado pelo instrutor |
| --- | --- |
| Seu nome | ____________________ |
| Namespace | app-aluno____ |
| Contexto do cluster | ____________________ |
| URL de clone | ____________________ |
| IP da sua loja | ____________________ |
Todos usam o mesmo repositório, branch main e pasta loja. Cada namespace tem sua instalação. Somente o instrutor publica mudanças no Git. Os exemplos abaixo são para o aluno 01: troque app-aluno01 pelo seu namespace.
## 1. Conferir o acesso
Abra o terminal individual com o kubeconfig entregue pelo instrutor.
```bash
kubectl config current-context
kubectl auth can-i create deployments -n app-aluno01
```
Espere o contexto correto e a resposta yes. Não use a credencial administrativa da turma. Se houver divergência, solicite a correção antes de continuar.
## 2. Clonar e publicar a loja
Substitua SUA-ORG pela organização real informada pelo instrutor.
```bash
git clone https://github.com/SUA-ORG/bootcamp-nkp.git
cd bootcamp-nkp
kubectl apply -k loja -n app-aluno01
kubectl rollout status deployment/loja -n app-aluno01 --timeout=180s
kubectl get pods -n app-aluno01 -l app=loja -o wide
```
Resultado: dois pods Running e Ready. O Deployment controla as réplicas, os ConfigMaps levam o site e o Service direciona o tráfego.
## 3. Obter seu endereço
```bash
kubectl get service loja -n app-aluno01 -w
```
Quando o EXTERNAL-IP estiver preenchido, pressione Ctrl+C. Anote o endereço e abra http://IP_DA_SUA_LOJA no navegador.
Resultado: VERSÃO 1.0.0, três produtos e carrinho. Adicione a camiseta e observe R$ 79,90. O pedido é apenas uma simulação; não há pagamento.
## 4. Acompanhar o GitOps
O instrutor ativa a integração uma vez por namespace. Depois disso:
```bash
kubectl get gitrepositories -n app-aluno01
kubectl get kustomizations -n app-aluno01
```
Espere Ready=True. O GitRepository acompanha o Git; a Kustomization aplica a pasta loja ao seu namespace. Você não precisa instalar Flux nem publicar sua própria cópia do repositório.
## 5. Observar a atualização da turma
Quando o instrutor publicar v2, anote o SHA informado: ____________________.
```bash
kubectl get gitrepositories -n app-aluno01 -w
```
Espere o novo SHA na origem e pressione Ctrl+C.
```bash
kubectl get kustomizations -n app-aluno01 -w
```
Espere a mesma revisão aplicada com Ready=True. Pressione Ctrl+C e confira:
```bash
kubectl describe kustomization loja -n app-aluno01
kubectl rollout status deployment/loja -n app-aluno01 --timeout=180s
kubectl get pods -n app-aluno01 -l app=loja -o wide
```
Não execute novo apply nem rollout restart para disparar a mudança. Aguarde a reconciliação. O intervalo é de 1 minuto, além do tempo de aplicação e troca de pods.
## 6. Conferir a versão nos dois pods
Copie um nome real da listagem e repita para o outro pod:
```bash
kubectl exec -n app-aluno01 NOME_DO_POD -- \
  grep data-version /usr/share/nginx/html/index.html
```
Resultado: os dois arquivos mostram 1.1.0. Recarregue a página, usando Ctrl+F5 se necessário.
| Evidência visual da v2 | Confirmar |
| --- | --- |
| VERSÃO 1.1.0 | Sim / Não |
| Faixa laranja com mensagem GitOps | Sim / Não |
| Produto Fone DevOps | Sim / Não |
| Campo de cupom NKP10 | Sim / Não |
Adicione uma camiseta e aplique NKP10: o total deve passar de R$ 79,90 para R$ 71,91. O carrinho fica na memória do navegador e reinicia ao recarregar a página.
## 7. Recuperação de uma réplica — com o instrutor
No seu namespace de laboratório, exclua somente um pod pelo nome real:
```bash
kubectl delete pod NOME_DE_UM_POD -n app-aluno01
kubectl get pods -n app-aluno01 -l app=loja -w
```
Observe a nova réplica e retorne a dois pods Ready. Esse comportamento pertence ao Kubernetes. Não exclua o Deployment ou o namespace.
## 8. Reversão da turma
O instrutor fará um git revert do commit v2. Repita a validação da origem, revisão aplicada e pods. Ao recarregar a página, espere a versão 1.0.0, três produtos e ausência do campo de cupom.
## 9. Se algo falhar
```bash
kubectl get events -n app-aluno01 --sort-by=.lastTimestamp
kubectl describe service loja -n app-aluno01
kubectl describe kustomization loja -n app-aluno01
```
Registre a mensagem e informe o instrutor. Forbidden indica acesso/contexto; EXTERNAL-IP pending envolve balanceamento; GitRepository não Ready exige revisão da origem; Kustomization não Ready exige ler as condições.
## Sua conclusão
| Marco | Concluído |
| --- | --- |
| V1 no navegador | Sim / Não |
| Novo SHA aplicado automaticamente | Sim / Não |
| Dois pods com v2 | Sim / Não |
| Cupom com resultado correto | Sim / Não |
| Reversão confirmada | Sim / Não |

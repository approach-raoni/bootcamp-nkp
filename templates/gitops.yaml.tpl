apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: loja
  namespace: {{NAMESPACE}}
spec:
  interval: 1m
  timeout: 60s
  url: {{REPO_URL}}
  ref:
    branch: main
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: loja
  namespace: {{NAMESPACE}}
spec:
  interval: 1m
  retryInterval: 30s
  timeout: 3m
  path: ./loja
  prune: true
  serviceAccountName: loja-reconciler
  sourceRef:
    kind: GitRepository
    name: loja
  targetNamespace: {{NAMESPACE}}
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: loja
      namespace: {{NAMESPACE}}

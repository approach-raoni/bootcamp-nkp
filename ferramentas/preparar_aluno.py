#!/usr/bin/env python3
"""Gera os manifests do instrutor. Nao altera o cluster nem publica no Git."""
from pathlib import Path
import argparse
import json
from urllib.parse import urlparse

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--aluno", required=True, help="Numero do aluno, por exemplo 01")
p.add_argument("--repositorio", required=True, help="URL HTTPS de clone do repositorio compartilhado")
a = p.parse_args()
if not a.aluno.isdigit() or int(a.aluno) < 1:
    p.error("--aluno deve ser um inteiro positivo")
u = urlparse(a.repositorio)
if u.scheme != "https" or not u.netloc or u.username or u.password or u.query or u.fragment:
    p.error("Use uma URL HTTPS de clone sem credenciais, query ou fragmento")
ns = f"app-aluno{int(a.aluno):02d}"
root = Path(__file__).resolve().parents[1]
dest = root / "gerados" / ns
dest.mkdir(parents=True, exist_ok=True)
for name in ("admin", "gitops"):
    text = (root / "templates" / f"{name}.yaml.tpl").read_text(encoding="utf-8")
    text = text.replace("{{NAMESPACE}}", ns).replace("{{REPO_URL}}", json.dumps(a.repositorio))
    (dest / f"{name}.yaml").write_text(text, encoding="utf-8", newline="\n")
print(f"Arquivos gerados em {dest}")
print("Revise antes de aplicar. Execute como instrutor no contexto do cluster de trabalho:")
print(f"kubectl apply -f gerados/{ns}/admin.yaml")
print(f"kubectl apply -f gerados/{ns}/gitops.yaml")

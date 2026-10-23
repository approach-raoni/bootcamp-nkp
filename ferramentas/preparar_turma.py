#!/usr/bin/env python3
"""Gera os arquivos de uma turma. Nao aplica recursos e nao publica no Git."""
from pathlib import Path
import argparse, subprocess, sys, csv
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--alunos",type=int,required=True)
p.add_argument("--repositorio",required=True)
a=p.parse_args()
if not 1 <= a.alunos <= 200:
    p.error("--alunos deve estar entre 1 e 200; dimensione a capacidade separadamente")
root=Path(__file__).resolve().parents[1]
for n in range(1,a.alunos+1):
    subprocess.run([sys.executable,str(root/"ferramentas/preparar_aluno.py"),"--aluno",str(n),"--repositorio",a.repositorio],check=True)
roster=root/"gerados"/"controle_turma.csv"
with roster.open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.writer(f,delimiter=";")
    writer.writerow(["aluno","namespace","identidade_idp","cluster","ip_loja","sha_v2","concluido"])
    writer.writerows([[f"{n:02d}",f"app-aluno{n:02d}","","","","",""] for n in range(1,a.alunos+1)])
print(f"Controle da turma: {roster}")
print("Revise e aplique admin.yaml por namespace antes da aula; gitops.yaml entra na etapa de ativacao.")

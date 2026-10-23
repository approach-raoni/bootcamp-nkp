#!/usr/bin/env python3
"""Verifica a entrega por kubectl e, opcionalmente, HTTP. Somente leitura."""
import argparse,json,re,subprocess,sys,urllib.request
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--namespace",required=True)
p.add_argument("--versao",required=True,choices=["1.0.0","1.1.0"])
p.add_argument("--sha",required=True,help="SHA completo do commit esperado")
p.add_argument("--url",help="Endereco HTTP(S) da loja, opcional")
a=p.parse_args()
if not re.fullmatch(r"app-aluno[0-9]{2,}",a.namespace):p.error("Namespace esperado: app-alunoNN")
if not re.fullmatch(r"[a-fA-F0-9]{40}",a.sha):p.error("--sha deve ser o SHA completo com 40 caracteres")
def k(*args):
    r=subprocess.run(["kubectl","-n",a.namespace,*args],capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r.stdout
def get(kind,name):return json.loads(k("get",kind,name,"-o","json"))
def ready(obj):return any(c.get("type")=="Ready" and c.get("status")=="True" for c in obj.get("status",{}).get("conditions",[]))
def require(ok,message):
    print(("OK " if ok else "FALHA ")+message)
    if not ok:raise RuntimeError(message)
try:
    source=get("gitrepository","loja")
    app=get("kustomization","loja")
    require(ready(source),"Origem Git Ready")
    require(ready(app),"Kustomization Ready")
    require(a.sha.lower() in source.get("status",{}).get("artifact",{}).get("revision","").lower(),"SHA esperado na origem")
    require(a.sha.lower() in app.get("status",{}).get("lastAppliedRevision","").lower(),"SHA esperado aplicado")
    d=get("deployment","loja");s=d.get("status",{});desired=d["spec"].get("replicas",1)
    require(s.get("observedGeneration",0)>=d["metadata"]["generation"],"Geracao observada")
    require(desired==2 and s.get("updatedReplicas",0)==2 and s.get("availableReplicas",0)>=2,"Duas replicas atualizadas e disponiveis")
    pods=json.loads(k("get","pods","-l","app=loja","-o","json"))["items"]
    pods=[v for v in pods if not v["metadata"].get("deletionTimestamp")]
    require(len(pods)==2,"Exatamente dois pods ativos")
    for pod in pods:
        name=pod["metadata"]["name"]
        require(pod.get("status",{}).get("phase")=="Running" and ready(pod),"Pod pronto: "+name)
        served=k("exec",name,"--","cat","/usr/share/nginx/html/index.html")
        require(('data-version="'+a.versao+'"') in served,"Versao no pod "+name)
    if a.url:
        if not re.match(r"^https?://",a.url):raise RuntimeError("URL deve comecar com http:// ou https://")
        req=urllib.request.Request(a.url,headers={"Cache-Control":"no-cache"})
        with urllib.request.urlopen(req,timeout=15) as response:page=response.read().decode("utf-8")
        require(('data-version="'+a.versao+'"') in page,"Versao pelo endereco externo")
    print("VALIDACAO CONCLUIDA: "+a.namespace)
except (RuntimeError,OSError,ValueError) as e:
    print("VALIDACAO INCOMPLETA: "+str(e),file=sys.stderr)
    sys.exit(1)

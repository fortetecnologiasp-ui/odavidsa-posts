"""Renderiza os dias de um lote direto em ../series/<dia>/<slug>/01..06.jpg
Uso: python3 gerar_dias.py serie_lote4"""
import os, sys, shutil, importlib, tempfile, subprocess
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
mod = importlib.import_module(sys.argv[1])
tmp = tempfile.mkdtemp()
slugs = [c["slug"] for v in mod.DIAS.values() for c in v]
env = dict(os.environ, CONTEUDO=sys.argv[1], OUT_DIR=tmp)
subprocess.run([sys.executable, os.path.join(AQUI, "render.py"), *slugs], env=env, check=True, cwd=AQUI)
for dia, lista in mod.DIAS.items():
    for c in lista:
        dst = os.path.join(AQUI, "..", "series", dia, c["slug"])
        if os.path.exists(dst): shutil.rmtree(dst)
        shutil.copytree(os.path.join(tmp, c["slug"]), dst)
print("ok", len(slugs), "carrosséis em", ", ".join(mod.DIAS))

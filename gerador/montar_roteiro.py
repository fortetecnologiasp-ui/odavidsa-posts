"""Gera roteiro-series.html (página do roteiro) com todos os dias de hoje-3 em diante.
Uso: python3 montar_roteiro.py  -> grava ../roteiro-series.html"""
import json, re, datetime, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import serie_todos as s
auto = json.load(open(os.path.join(AQUI, "auto.json")))
HORAS = ['12:30','14:00','16:00','17:00','19:00','20:00']
SEM = ['seg','ter','qua','qui','sex','sáb','dom']
hoje = datetime.date.today(); corte = hoje - datetime.timedelta(days=3)
data = []
for dia in sorted(s.DIAS):
    dt = datetime.date.fromisoformat(dia)
    if dt < corte: continue
    posts = []
    for h, c in zip(HORAS, s.DIAS[dia]):
        a = auto.get(c['slug'])
        posts.append(dict(id=c['slug'], hora=(a['hora'] if a else h), auto=bool(a),
            serie="Marketing" if c['serie']=='mkt' else "Relacionamento",
            tema=c['tema'], titulo=re.sub(r'<[^>]+>','',c['titulo']),
            pasta=f"series/{dia}/{c['slug']}",
            link=f"https://github.com/fortetecnologiasp-ui/odavidsa-posts/tree/main/series/{dia}/{c['slug']}",
            legenda=c['legenda']))
    posts.sort(key=lambda p: p['hora'])
    data.append(dict(id=dia, dia=f"{SEM[dt.weekday()]}, {dt.day:02d}/{dt.month:02d}", posts=posts))
ini, fim = data[0]['id'], data[-1]['id']
fmt = lambda d: f"{d[8:10]}/{d[5:7]}"
intro = (f"Carrosséis de {fmt(ini)} a {fmt(fim)}, seis por dia. Os marcados como automáticos saem sozinhos pelo "
         "Metricool; os outros você posta no app do Instagram.")
t = open(os.path.join(AQUI, "roteiro2_template.html")).read()
t = t.replace("__INTRO__", intro).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
out = os.path.join(AQUI, "..", "roteiro-series.html")
open(out, "w").write(t)
print("roteiro:", ini, "a", fim, "->", os.path.abspath(out))

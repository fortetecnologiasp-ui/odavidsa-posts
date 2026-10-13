import base64, os, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(__file__))
import importlib
CARROSSEIS = importlib.import_module(os.environ.get('CONTEUDO','conteudo')).CARROSSEIS

OUT = os.environ.get("OUT_DIR") or os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CSS = f"""
@font-face {{ font-family: I; src: url('file://{FONT}Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: I; src: url('file://{FONT}Inter-Medium.otf'); font-weight: 500; }}
@font-face {{ font-family: I; src: url('file://{FONT}Inter-Bold.otf'); font-weight: 700; }}
@font-face {{ font-family: I; src: url('file://{FONT}Inter-ExtraBold.otf'); font-weight: 800; }}
@font-face {{ font-family: I; src: url('file://{FONT}Inter-Black.otf'); font-weight: 900; }}
:root {{ --glow1:rgba(217,165,74,.14); --glow2:rgba(217,165,74,.18); --bg:#0f0d0a; --gold:#d9a54a; --gold2:#f0c878; --ink:#f6f1e8; --mute:#a99f8f; --line:#2c2620; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1350px; background:var(--bg); font-family:'Inter', sans-serif; color:var(--ink); }}
.s {{ position:relative; width:1080px; height:1350px; overflow:hidden; }}
em {{ font-style:normal; color:var(--gold2); }}
b {{ color:var(--gold2); font-weight:700; }}

/* capa */
.cover img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.cover .shade {{ position:absolute; inset:0;
  background: linear-gradient(180deg, rgba(10,8,6,.55) 0%, rgba(10,8,6,0) 22%, rgba(10,8,6,0) 42%, rgba(10,8,6,.88) 66%, rgba(10,8,6,.98) 100%); }}
.top {{ position:absolute; top:56px; left:64px; right:64px; display:flex; justify-content:space-between; align-items:center; }}
.pill {{ font-size:22px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:var(--bg);
  background:var(--gold); padding:12px 22px; border-radius:999px; }}
.handle {{ font-size:26px; font-weight:700; color:var(--ink); }}
.cover .txt {{ position:absolute; left:64px; right:64px; bottom:120px; }}
.kicker {{ font-size:34px; font-weight:700; color:var(--gold); margin-bottom:22px; }}
.cover h1 {{ font-size:84px; line-height:1.02; font-weight:900; letter-spacing:-.025em; }}
.swipe {{ position:absolute; left:64px; right:64px; bottom:52px; display:flex; justify-content:space-between;
  font-size:22px; color:var(--mute); font-weight:500; letter-spacing:.06em; text-transform:uppercase; }}

/* conteúdo */
.c {{ padding:64px; background:
  radial-gradient(900px 600px at 100% 0%, var(--glow1), transparent 60%), var(--bg); }}
.bar {{ display:flex; justify-content:space-between; align-items:center; font-size:22px; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:var(--mute); padding-bottom:28px; border-bottom:2px solid var(--line); }}
.bar .t {{ color:var(--gold); }}
.num {{ margin-top:70px; font-size:170px; font-weight:900; line-height:1; color:transparent;
  -webkit-text-stroke:3px var(--gold); letter-spacing:-.03em; }}
.c h2 {{ margin-top:30px; font-size:84px; line-height:1.05; font-weight:900; letter-spacing:-.02em; }}
.c ul {{ list-style:none; margin-top:64px; }}
.c li {{ position:relative; padding-left:48px; font-size:46px; line-height:1.3; font-weight:500; margin-bottom:42px; color:#e9e2d6; }}
.c li::before {{ content:''; position:absolute; left:0; top:24px; width:26px; height:7px; background:var(--gold); border-radius:3px; }}
.mv {{ display:inline-block; font-family:I, sans-serif; font-weight:900; font-size:34px; letter-spacing:.08em; padding:6px 18px; border-radius:10px; margin-right:6px; vertical-align:3px; }}
.mv.m {{ background:#4a1d17; color:#ffb7a8; }}
.mv.v {{ background:#173d27; color:#9fe8bb; }}
.mv.p {{ background:#45351a; color:#f3d08a; }}
.c h2.q {{ font-size:66px; font-weight:800; }}
.foot {{ position:absolute; left:64px; right:64px; bottom:56px; display:flex; justify-content:space-between;
  font-size:22px; color:var(--mute); font-weight:500; }}
.foot .h {{ color:var(--ink); font-weight:700; }}

/* final */
.f {{ padding:64px; display:flex; flex-direction:column; background:
  radial-gradient(1000px 700px at 50% 0%, var(--glow2), transparent 65%), var(--bg); }}
.av {{ margin-top:110px; width:200px; height:200px; border-radius:50%; overflow:hidden; border:4px solid var(--gold); }}
.av img {{ width:100%; height:100%; object-fit:cover; transform:scale(var(--z)); transform-origin:var(--fo); }}
.f .q {{ margin-top:56px; font-size:74px; line-height:1.06; font-weight:900; letter-spacing:-.02em; }}
.f .cta {{ margin-top:44px; font-size:38px; line-height:1.35; font-weight:500; color:#e9e2d6; }}
.f .src {{ margin-top:auto; padding-top:32px; border-top:2px solid var(--line); font-size:24px; line-height:1.45; color:var(--mute); }}
.f .src strong {{ color:var(--ink); font-weight:700; }}
.f .ai {{ margin-top:14px; font-size:20px; color:#7d7466; }}
"""

def page(body, c=None):
    extra = c.get("css","") if c else ""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{body}</body></html>"

def cover(c, total):
    img = b64(c["foto"])
    return page(f"""
<div class="s cover">
  <img src="data:image/jpeg;base64,{img}" style="object-position:{c['foco']}; transform:scale({c.get('zoom',1)}); transform-origin:{c['foco']}">
  <div class="shade"></div>
  <div class="top"><span class="pill">{c.get('pill', 'Plano de governo · ' + c['tema'])}</span><span class="handle">@odavidsa</span></div>
  <div class="txt"><div class="kicker">{c['kicker']}</div><h1>{c['titulo']}</h1></div>
  <div class="swipe"><span>{c.get('rodape', 'Flávio Bolsonaro · 2º turno')}</span><span>Arraste →</span></div>
</div>""", c)

def content(c, i, title, bullets, total):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return page(f"""
<div class="s c">
  <div class="bar"><span class="t">{c['tema']}</span><span>{i+1}/{total}</span></div>
  <div class="num">{i:02d}</div>
  <h2>{title}</h2>
  <ul>{lis}</ul>
  <div class="foot"><span class="h">@odavidsa</span><span>{c.get('fc','Fonte: plano registrado no TSE')}</span></div>
</div>""", c)

def final(c, total):
    img = b64(c["foto"])
    return page(f"""
<div class="s f">
  <div class="bar"><span class="t">{c['tema']}</span><span>{total}/{total}</span></div>
  <div class="av"><img src="data:image/jpeg;base64,{img}" style="object-position:{c['foco']}; --fo:{c['foco']}; --z:{1.9*c.get('zoom',1)}"></div>
  <div class="q">{c['pergunta']}</div>
  <div class="cta">{c.get('cta', 'Comenta aqui embaixo e manda esse post para alguém que ainda não decidiu o voto.')}</div>
  <div class="src">{c.get('fl','<strong>Fonte:</strong> plano de governo “Para o Brasil Vencer o Atraso”, registrado por Flávio Bolsonaro (PL) no TSE.<br>Resumo informativo em linguagem simples. Leia o documento completo no portal do TSE.')}</div>
  {c.get('ai', '<div class="ai">Conteúdo produzido com auxílio de inteligência artificial · @odavidsa</div>')}
</div>""", c)

def main(only=None):
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width":1080, "height":1350})
        for c in CARROSSEIS:
            if only and c["slug"] not in only: continue
            total = len(c["slides"]) + 2
            htmls = [cover(c, total)]
            htmls += [content(c, i+1, t, b, total) for i, (t, b) in enumerate(c["slides"])]
            htmls.append(final(c, total))
            d = os.path.join(OUT, c["slug"]); os.makedirs(d, exist_ok=True)
            for n, h in enumerate(htmls, 1):
                pg.set_content(h, wait_until="load")
                pg.wait_for_timeout(150)
                pg.screenshot(path=os.path.join(d, f"{n:02d}.jpg"), type="jpeg", quality=92)
            print(c["slug"], len(htmls))
        br.close()

if __name__ == "__main__":
    main(sys.argv[1:] or None)

"""Renderiza carrosséis tipográficos do Viva Voz Casamentos (1080x1350, JPEG 95).
Uso: python3 vv_render.py [slug ...]   (CONTEUDO=vv_conteudo por padrão)"""
import base64, os, sys, importlib
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
CARROSSEIS = importlib.import_module(os.environ.get("CONTEUDO", "vv_conteudo")).CARROSSEIS
OUT = os.environ.get("OUT_DIR") or os.path.join(AQUI, "out")

def b64(p):
    with open(os.path.join(AQUI, p), "rb") as f:
        return base64.b64encode(f.read()).decode()
LOGO, LOGO_CLARO = b64("logo.png"), b64("logo-claro.png")

CSS = """
:root { --gold:#C3A034; --gold2:#D9BC5C; --ink:#141210; --ivory:#F7F4EE; --paper:#FBF9F5; --mute:#8A8277; --line:#E4DED3; }
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1350px; font-family:'Inter',sans-serif; }
.s { position:relative; width:1080px; height:1350px; overflow:hidden; }
.serif { font-family:'Lora',serif; }
em { font-style:normal; color:var(--gold); }
/* anéis decorativos */
.rings { position:absolute; width:620px; height:400px; opacity:.07; }
.rings i { position:absolute; top:0; width:400px; height:400px; border:34px solid currentColor; border-radius:50%; }
.rings i:last-child { left:220px; }

/* capa: preta */
.cover { background:var(--ink); color:var(--ivory); padding:80px 76px; }
.cover .rings { color:var(--gold); right:-210px; top:-90px; opacity:.16; }
.tag { display:inline-block; font-size:24px; font-weight:700; letter-spacing:.18em; text-transform:uppercase;
  color:var(--ink); background:var(--gold); padding:13px 24px; border-radius:999px; }
.cover .kicker { margin-top:300px; font-family:'Lora',serif; font-size:46px; font-style:italic; color:var(--gold2); }
.cover h1 { margin-top:26px; font-size:124px; line-height:.98; font-weight:900; letter-spacing:-.03em; text-transform:uppercase; }
.cover .sub { margin-top:40px; font-size:40px; line-height:1.35; color:#CFC8BC; font-weight:500; max-width:860px; }
.cover .logo { position:absolute; left:76px; bottom:72px; height:190px; }
.cover .swipe { position:absolute; right:76px; bottom:88px; font-size:24px; letter-spacing:.16em; text-transform:uppercase; color:var(--gold2); font-weight:700; }

/* conteúdo: claro */
.c { background:var(--paper); color:var(--ink); padding:72px 76px; }
.c .rings { color:var(--gold); right:-260px; bottom:-150px; opacity:.09; }
.bar { display:flex; justify-content:space-between; align-items:center; padding-bottom:26px; border-bottom:2px solid var(--line);
  font-size:22px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--mute); }
.bar .t { color:var(--gold); }
.num { margin-top:64px; font-family:'Lora',serif; font-style:italic; font-size:120px; line-height:1; color:var(--gold); }
.c h2 { margin-top:18px; font-size:72px; line-height:1.04; font-weight:900; letter-spacing:-.025em; }
.c p.lead { margin-top:44px; font-size:46px; line-height:1.42; color:#3A352F; font-weight:500; }
.songs { position:absolute; left:76px; right:76px; top:470px; bottom:170px; display:flex; flex-direction:column; justify-content:center; }
.song { display:flex; align-items:center; gap:40px; padding:44px 0; border-bottom:2px solid var(--line); }
.song:last-child { border-bottom:none; }
.song .n { font-family:'Lora',serif; font-style:italic; font-size:110px; line-height:1; color:var(--gold); width:90px; }
.song .ti { font-size:62px; font-weight:800; line-height:1.12; letter-spacing:-.01em; }
.song .ar { margin-top:10px; font-family:'Lora',serif; font-size:42px; color:var(--mute); font-style:italic; }
.pill { display:inline-block; margin-top:18px; font-size:24px; font-weight:800; letter-spacing:.14em; text-transform:uppercase;
  padding:9px 20px; border-radius:8px; }
.pill.gospel { background:#F1E6C4; color:#7A5D0E; } .pill.popular { background:#E9E4DC; color:#4C463E; }
.pill.classica { background:#141210; color:#E8D9A8; } .pill.mpb { background:#E3EBDF; color:#35532C; }
ul.lst { list-style:none; margin-top:50px; }
ul.lst li { position:relative; padding-left:58px; font-size:46px; line-height:1.34; font-weight:500; margin-bottom:34px; color:#2C2823; }
ul.lst li::before { content:''; position:absolute; left:0; top:20px; width:28px; height:28px; border-radius:50%; border:6px solid var(--gold); }
ul.lst li b { font-weight:800; color:var(--ink); }
.foot { position:absolute; left:76px; right:76px; bottom:60px; display:flex; justify-content:space-between; align-items:center;
  font-size:22px; color:var(--mute); font-weight:600; letter-spacing:.04em; }
.foot img { height:90px; }

/* final: preto */
.f { background:var(--ink); color:var(--ivory); padding:72px 76px; text-align:center; }
.f .rings { color:var(--gold); left:50%; margin-left:-310px; top:120px; opacity:.10; }
.f .logo { margin-top:70px; height:330px; }
.f .q { margin-top:70px; font-size:68px; line-height:1.08; font-weight:900; letter-spacing:-.02em; }
.f .cta { margin:34px auto 0; max-width:860px; font-size:36px; line-height:1.4; color:#CFC8BC; font-weight:500; }
.f .handle { position:absolute; left:0; right:0; bottom:76px; font-family:'Lora',serif; font-style:italic; font-size:40px; color:var(--gold2); }
"""

FIT = r"""<script>(()=>{
const h=document.querySelector('.cover h1'), sub=document.querySelector('.cover .sub'), k=document.querySelector('.cover .kicker');
let fs=124, mt=300;
const limite=1350-72-190-50;
function ok(){ const r=sub.getBoundingClientRect(); return r.bottom<=limite && h.scrollWidth<=h.clientWidth+2; }
while(!ok() && (fs>78 || mt>140)){ if(mt>140){mt-=20;k.style.marginTop=mt+'px';} else {fs-=4;h.style.fontSize=fs+'px';} }
while(!ok() && fs>60){ fs-=4; h.style.fontSize=fs+'px'; }
})();</script>"""

RINGS = '<div class="rings"><i></i><i></i></div>'

def page(body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"

def cover(c):
    return page(f"""<div class="s cover">{RINGS}
  <span class="tag">{c['tema']}</span>
  <div class="kicker">{c['kicker']}</div>
  <h1>{c['titulo']}</h1>
  <div class="sub">{c.get('sub','')}</div>
  <img class="logo" src="data:image/png;base64,{LOGO_CLARO}">
  <div class="swipe">Arraste →</div></div>
{FIT}""")

def corpo(sl):
    if "songs" in sl:
        rows = "".join(
            f'<div class="song"><div class="n">{i}</div><div><div class="ti">{t}</div><div class="ar">{a}</div>'
            f'<span class="pill {k}">{ {"gospel":"Gospel","popular":"Popular","classica":"Clássica","mpb":"MPB"}[k] }</span></div></div>'
            for (i, t, a, k) in sl["songs"])
        return f'<div class="songs">{rows}</div>'
    out = ""
    if sl.get("p"): out += f'<p class="lead">{sl["p"]}</p>'
    if sl.get("li"): out += '<ul class="lst">' + "".join(f"<li>{x}</li>" for x in sl["li"]) + "</ul>"
    return out

def content(c, i, sl, total):
    num = f'<div class="num">{sl["num"]}</div>' if sl.get("num") else '<div style="height:40px"></div>'
    return page(f"""<div class="s c">{RINGS}
  <div class="bar"><span class="t">{c['tema']}</span><span>{i}/{total}</span></div>
  {num}<h2>{sl['h']}</h2>{corpo(sl)}
  <div class="foot"><span>@vivavozcasamentos</span><img src="data:image/png;base64,{LOGO}"></div></div>""")

def final(c, total):
    return page(f"""<div class="s f">{RINGS}
  <img class="logo" src="data:image/png;base64,{LOGO_CLARO}">
  <div class="q">{c['pergunta']}</div>
  <div class="cta">{c.get('cta') or 'Salve este post para o planejamento do seu casamento e envie para quem vai casar.'}</div>
  <div class="handle">@vivavozcasamentos</div></div>""")

def main(only=None):
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width":1080, "height":1350})
        for c in CARROSSEIS:
            if only and c["slug"] not in only: continue
            total = len(c["slides"]) + 2
            htmls = [cover(c)] + [content(c, i+2, s, total) for i, s in enumerate(c["slides"])] + [final(c, total)]
            d = os.path.join(OUT, c["dia"], c["slug"]); os.makedirs(d, exist_ok=True)
            for n, h in enumerate(htmls, 1):
                pg.set_content(h, wait_until="load"); pg.wait_for_timeout(120)
                pg.screenshot(path=os.path.join(d, f"{n:02d}.jpg"), type="jpeg", quality=95)
            print(c["dia"], c["slug"], len(htmls))
        br.close()

if __name__ == "__main__":
    main(sys.argv[1:] or None)

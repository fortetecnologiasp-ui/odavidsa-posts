"""Gera Reel 1080x1920 (MP4) a partir de um carrossel da série (mesmo conteúdo).
Uso: CONTEUDO=serie_eleicao python3 reel.py m104 [m105 ...]  -> out_reels/<slug>.mp4 + capa.jpg"""
import base64, os, sys, subprocess, importlib, shutil
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
CARROSSEIS = importlib.import_module(os.environ.get("CONTEUDO", "serie_eleicao")).CARROSSEIS
OUT = os.environ.get("OUT_DIR") or os.path.join(AQUI, "out_reels")
F = AQUI + "/fonts/"
def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()
CSS = f"""
@font-face {{ font-family:I; src:url('file://{F}Inter-Medium.otf'); font-weight:500; }}
@font-face {{ font-family:I; src:url('file://{F}Inter-Bold.otf'); font-weight:700; }}
@font-face {{ font-family:I; src:url('file://{F}Inter-Black.otf'); font-weight:900; }}
:root {{ --bg:#0f0d0a; --gold:#d9a54a; --gold2:#f0c878; --ink:#f6f1e8; --mute:#a99f8f; }}
.rel {{ --gold:#d98f86; --gold2:#f3b9b0; }}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:var(--bg);font-family:I,sans-serif;color:var(--ink)}}
.s{{position:relative;width:1080px;height:1920px;overflow:hidden;background:radial-gradient(1100px 800px at 100% 0%,rgba(217,165,74,.16),transparent 60%),var(--bg)}}
em{{font-style:normal;color:var(--gold2)}} b{{color:var(--gold2);font-weight:700}}
.photo{{position:absolute;left:0;top:0;width:1080px;height:auto}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,8,6,.35) 0%,rgba(10,8,6,0) 18%,rgba(10,8,6,0) 45%,rgba(10,8,6,.92) 68%,var(--bg) 84%)}}
.pill{{position:absolute;top:150px;left:80px;font-size:28px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--bg);background:var(--gold);padding:14px 26px;border-radius:999px}}
.ctxt{{position:absolute;left:80px;right:80px;bottom:330px}}
.kicker{{font-size:42px;font-weight:700;color:var(--gold);margin-bottom:26px}}
h1{{font-size:104px;line-height:1.02;font-weight:900;letter-spacing:-.025em}}
.handle{{position:absolute;left:80px;bottom:250px;font-size:32px;font-weight:700;color:var(--mute)}}
.c{{display:flex;flex-direction:column;justify-content:center;padding:220px 80px 380px}}
.num{{font-size:220px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:4px var(--gold)}}
h2{{margin-top:40px;font-size:96px;line-height:1.04;font-weight:900;letter-spacing:-.02em}}
ul{{list-style:none;margin-top:80px}}
li{{position:relative;padding-left:60px;font-size:56px;line-height:1.3;font-weight:500;margin-bottom:50px;color:#e9e2d6}}
li::before{{content:'';position:absolute;left:0;top:32px;width:32px;height:9px;background:var(--gold);border-radius:4px}}
.f{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:220px 90px 380px}}
.av{{width:300px;height:300px;border-radius:50%;overflow:hidden;border:6px solid var(--gold)}}
.av img{{width:100%;height:100%;object-fit:cover}}
.q{{margin-top:80px;font-size:92px;line-height:1.06;font-weight:900}}
.cta{{margin-top:60px;font-size:52px;line-height:1.35;font-weight:500;color:#e9e2d6}}
.h2b{{margin-top:70px;font-size:56px;font-weight:900;color:var(--gold2)}}
"""
def page(body, serie): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body class='{serie}'>{body}</body></html>"

def cenas(c):
    img = b64(c["foto"]); s = c["serie"]
    yield page(f"""<div class="s"><img class="photo" src="data:image/jpeg;base64,{img}" style="object-position:{c['foco']}">
<div class="shade"></div><span class="pill">{c['pill']}</span>
<div class="ctxt"><div class="kicker">{c['kicker']}</div><h1>{c['titulo']}</h1></div><div class="handle">@odavidsa</div></div>""", s)
    for i, (t, bs) in enumerate(c["slides"], 1):
        lis = "".join(f"<li>{x}</li>" for x in bs)
        yield page(f"""<div class="s c"><div class="num">{i:02d}</div><h2>{t}</h2><ul>{lis}</ul></div>""", s)
    yield page(f"""<div class="s f"><div class="av"><img src="data:image/jpeg;base64,{img}" style="object-position:{c['foco']}"></div>
<div class="q">{c['pergunta']}</div><div class="cta">Comenta aqui e salva pra não esquecer.</div><div class="h2b">Siga @odavidsa</div></div>""", s)

DUR = [3.5, 4.5, 4.5, 4.5, 4.5, 4.0]   # capa, 4 tópicos, final
FADE = 0.5

def video(frames, out):
    n = len(frames); durs = DUR[:n-1] + [DUR[-1]]
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f, d in zip(frames, durs): args += ["-loop", "1", "-t", str(d), "-framerate", "30", "-i", f]
    flt = []; prev = "[0:v]"; off = 0.0
    for i in range(1, n):
        off += durs[i-1] - FADE
        lab = f"[x{i}]"
        flt.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}{lab}")
        prev = lab
    flt.append(f"{prev}format=yuv420p[v]")
    args += ["-filter_complex", ";".join(flt), "-map", "[v]", "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
             "-movflags", "+faststart", out]
    subprocess.run(args, check=True)

def main(slugs):
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width":1080, "height":1920})
        for c in CARROSSEIS:
            if c["slug"] not in slugs: continue
            d = os.path.join(OUT, c["slug"]); os.makedirs(d, exist_ok=True); frames = []
            for k, h in enumerate(cenas(c), 1):
                pg.set_content(h, wait_until="load"); pg.wait_for_timeout(150)
                fp = os.path.join(d, f"cena{k}.png"); pg.screenshot(path=fp); frames.append(fp)
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",frames[0],"-q:v","2",os.path.join(d,"capa.jpg")], check=True)
            video(frames, os.path.join(d, "reel.mp4")); print(c["slug"], "ok")
        br.close()

if __name__ == "__main__":
    main(sys.argv[1:])

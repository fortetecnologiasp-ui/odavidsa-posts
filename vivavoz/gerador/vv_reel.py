"""Reels da @vivavozcasamentos (1080x1920, 1 por dia às 18:00).

Três modos:
  aovivo  VIDEO INICIO saida.mp4 --gancho "..."           corte de 13 s da banda tocando ao vivo (som original)
  ab      VIDEO_A INICIO_A VIDEO_B INICIO_B saida.mp4 --pergunta "..." --rotulo-a "..." --rotulo-b "..."
  dica    PASTA_SLIDES MUSICA.m4a saida.mp4               slides do carrossel de dica + música da Viva Voz

Regras visuais (iguais às da fotografia):
- CAPA LIMPA: os primeiros 2 s são só a imagem (no "ab", 1,5 s).
- Texto numa faixa sem rosto (YuNet em davidsa/modelos/), dentro da área segura do Reels (y 260–1460).
- Final (últimos 3 s): "@vivavozcasamentos" + "Solicite um orçamento sem compromisso".
"""
import argparse, os, subprocess, tempfile, json
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
AQUI = os.path.dirname(os.path.abspath(__file__))
YUNET = os.path.join(AQUI, "..", "..", "davidsa", "modelos", "yunet_n_dynamic.onnx")
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
INTER_S = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
DOURADO = (232, 205, 150)
SEGURA, FAIXA = (260, 1460), 380
DUR = 13.0
CTA = "Solicite um orçamento sem compromisso"


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *map(str, a)], check=True)


def frames(video, ini, dur, n=5):
    out = []
    with tempfile.TemporaryDirectory() as t:
        for k in range(n):
            p = f"{t}/{k}.png"
            ff("-ss", ini + dur * (k + 0.5) / n, "-i", video, "-frames:v", 1, "-vf", f"scale={W}:{H}", p)
            out.append(Image.open(p).convert("RGB"))
    return out


def faixa_livre(imgs):
    """y da faixa de texto: sem rosto em nenhum dos quadros e com menos detalhe."""
    prot = np.zeros(H); det_b = np.zeros(H)
    for im in imgs:
        a = np.array(im)[:, :, ::-1].copy()
        s = 640 / H
        sm = cv2.resize(a, (round(W * s), round(H * s)))
        d = cv2.FaceDetectorYN.create(YUNET, "", (sm.shape[1], sm.shape[0]), 0.6)
        r = d.detect(sm)[1]
        for x in ([] if r is None else r):
            y, h = x[1] / s, x[3] / s
            peso = 1.0 if h > 70 else 0.3
            y0, y1 = max(0, int(y - 0.6 * h - 60)), min(H, int(y + 1.6 * h + 60))
            prot[y0:y1] = np.maximum(prot[y0:y1], peso)
        g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
        det_b += cv2.Canny(g, 60, 160).mean(1) / 255
    melhor = None
    for y in range(SEGURA[0], SEGURA[1] - FAIXA + 1, 20):
        c = prot[y:y + FAIXA].mean() * 10 + det_b[y:y + FAIXA].mean() / len(imgs)
        if melhor is None or c < melhor[0]:
            melhor = (c, y)
    return melhor[1]


def quebra(d, txt, fonte, larg=940):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if d.textlength(t, font=fonte) > larg and atual:
            linhas.append(atual); atual = p
        else:
            atual = t
    return linhas + [atual]


def painel(yb, blocos, path):
    """PNG transparente com faixa escura suave e blocos de texto [(texto, fonte, cor)]."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(FAIXA):
        borda = min(k, FAIXA - k) / 70
        d.line((0, yb + k, W, yb + k), fill=(0, 0, 0, int(125 * min(1, borda))))
    import re
    sem_emoji = lambda t: re.sub(r"[🀀-🿿☀-➿️]", "", t).strip()
    linhas = [(l, f, c) for (t, f, c) in blocos for l in quebra(d, sem_emoji(t), f)]
    alt = sum(f.size * 1.3 for (_, f, _) in linhas)
    y = yb + (FAIXA - alt) / 2
    for (l, f, c) in linhas:
        w = d.textlength(l, font=f); x = (W - w) / 2
        d.text((x + 3, y + 3), l, font=f, fill=(0, 0, 0, 150))
        d.text((x, y), l, font=f, fill=c + (255,))
        y += f.size * 1.3
    im.save(path)


def fim_png(yb, path):
    painel(yb, [("@vivavozcasamentos", ImageFont.truetype(LORA, 64), (255, 255, 255)),
                (CTA, ImageFont.truetype(INTER_S, 38), DOURADO)], path)


def gancho_png(yb, txt, path):
    painel(yb, [(txt, ImageFont.truetype(LORA, 62), (255, 255, 255))], path)


def compoe(base_args, dur, overlays, saida, audio_filter=None, audio_map="0:a"):
    """overlays: [(png, inicio, fim)] com fade de 0,4 s."""
    args = list(base_args)
    for (png, _, _) in overlays:
        args += ["-loop", 1, "-t", dur, "-i", png]
    fc = ["[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,setsar=1,fps=30[v0]"]
    last = "v0"
    nb = sum(1 for x in base_args if x == "-i")
    for i, (png, a, b) in enumerate(overlays, nb):
        fo = f"fade=out:st={b - 0.4}:d=0.4:alpha=1," if b < dur else ""
        fc.append(f"[{i}:v]format=rgba,fade=in:st={a}:d=0.4:alpha=1,{fo}null[o{i}]")
        fc.append(f"[{last}][o{i}]overlay=0:0:enable='between(t,{a},{b})'[v{i}]")
        last = f"v{i}"
    af = audio_filter or f"loudnorm=I=-14:TP=-1.5,afade=t=in:d=0.4,afade=t=out:st={dur - 1.5}:d=1.5"
    fc.append(f"[{audio_map}]{af}[a]")
    ff(*args, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "[a]", "-t", dur,
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", 23, "-preset", "slow", "-c:a", "aac", "-b:a", "192k", "-ar", 44100,
       "-movflags", "+faststart", saida)


def aovivo(video, ini, saida, gancho):
    yb = faixa_livre(frames(video, ini, DUR))
    with tempfile.TemporaryDirectory() as t:
        gancho_png(yb, gancho, f"{t}/g.png"); fim_png(yb, f"{t}/f.png")
        compoe(["-ss", ini, "-t", DUR, "-i", video], DUR,
               [(f"{t}/g.png", 2.0, 5.4), (f"{t}/f.png", DUR - 3.0, DUR)], saida)
    return yb


def ab(va, ia, vb, ib, saida, pergunta, ra, rb, metade=7.0):
    dur = metade * 2
    with tempfile.TemporaryDirectory() as t:
        ff("-ss", ia, "-t", metade, "-i", va, "-ss", ib, "-t", metade, "-i", vb, "-filter_complex",
           "[0:v]scale=1080:1920,setsar=1,fps=30[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];"
           f"[0:a]afade=t=out:st={metade - 0.4}:d=0.4[x];[1:a]afade=t=in:d=0.4[y];"
           "[a][x][b][y]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]",
           "-c:v", "libx264", "-crf", 16, "-c:a", "aac", f"{t}/ab.mp4")
        yb = faixa_livre(frames(va, ia, metade, 3) + frames(vb, ib, metade, 3))
        fq = ImageFont.truetype(LORA, 56); fl = ImageFont.truetype(INTER_B, 120); fr = ImageFont.truetype(INTER_S, 38)
        painel(yb, [("A", fl, DOURADO), (ra, fr, (255, 255, 255)), (pergunta, fq, (255, 255, 255))], f"{t}/A.png")
        painel(yb, [("B", fl, DOURADO), (rb, fr, (255, 255, 255)), (pergunta, fq, (255, 255, 255))], f"{t}/B.png")
        painel(yb, [("A ou B?", fl, DOURADO), ("Comenta aqui embaixo! " + CTA, fr, (255, 255, 255)),
                    ("@vivavozcasamentos", fq, (255, 255, 255))], f"{t}/F.png")
        compoe(["-i", f"{t}/ab.mp4"], dur,
               [(f"{t}/A.png", 1.5, metade), (f"{t}/B.png", metade, dur - 3.0), (f"{t}/F.png", dur - 3.0, dur)],
               saida, audio_filter="loudnorm=I=-14:TP=-1.5,afade=t=out:st=12.5:d=1.5")
    return yb


def dica(pasta, musica, saida, por_slide=3.2, fim=3.0):
    slides = sorted(f for f in os.listdir(pasta) if f.lower().endswith((".jpg", ".png")))
    dur = round(por_slide * len(slides) + fim, 2)
    with tempfile.TemporaryDirectory() as t:
        for i, s_ in enumerate(slides):
            sl = Image.open(os.path.join(pasta, s_)).convert("RGB")
            bg = sl.resize((W, H)).filter(ImageFilter.GaussianBlur(50))
            bg = ImageEnhance.Brightness(bg).enhance(0.35)
            if i == len(slides) - 1:
                bg.save(f"{t}/fim.png")  # tela final: só o fundo, para o CTA não brigar com o slide
            fg = sl.resize((1000, round(1000 * sl.height / sl.width)), Image.LANCZOS)
            bg.paste(fg, ((W - 1000) // 2, (H - fg.height) // 2 - 60))
            bg.save(f"{t}/{i:02d}.png")
        lista = "".join(f"file '{t}/{i:02d}.png'\nduration {por_slide}\n" for i in range(len(slides)))
        lista += f"file '{t}/fim.png'\nduration {fim}\nfile '{t}/fim.png'\n"
        open(f"{t}/l.txt", "w").write(lista)
        ff("-f", "concat", "-safe", 0, "-i", f"{t}/l.txt", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", 16,
           f"{t}/s.mp4")
        ff("-stream_loop", -1, "-i", musica, "-t", dur, "-c:a", "aac", f"{t}/m.m4a")
        fim_png((H - FAIXA) // 2 - 100, f"{t}/f.png")
        compoe(["-i", f"{t}/s.mp4", "-i", f"{t}/m.m4a"], dur, [(f"{t}/f.png", dur - fim, dur)], saida,
               audio_map="1:a")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["aovivo", "ab", "dica"]); ap.add_argument("args", nargs="+")
    ap.add_argument("--gancho", default=""); ap.add_argument("--pergunta", default="Qual você escolheria para a sua cerimônia?")
    ap.add_argument("--rotulo-a", default=""); ap.add_argument("--rotulo-b", default="")
    a = ap.parse_args()
    if a.modo == "aovivo":
        v, i, s = a.args; print("faixa", aovivo(v, float(i), s, a.gancho))
    elif a.modo == "ab":
        va, ia, vb, ib, s = a.args; print("faixa", ab(va, float(ia), vb, float(ib), s, a.pergunta, a.rotulo_a, a.rotulo_b))
    else:
        p, m, s = a.args; dica(p, m, s)

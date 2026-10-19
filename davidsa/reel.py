"""Transforma UMA foto em Reels 1080x1920 (zoom lento + música da Viva Voz).

uso: python3 davidsa/reel.py FOTO.jpg MUSICA.m4a saida.mp4 [--inicio 0] [--dur 12]
       [--gancho "Frase curta"] [--legenda "Stephanie & Alisson · Paraibuna"]

Regras visuais:
- CAPA LIMPA: os primeiros 2 s são só a foto (a capa do Reels é a própria foto).
- Gancho aparece de 2,0 s a 5,2 s; "@davidsafotografia" + legenda nos últimos 2,6 s.
- O texto NUNCA fica no rosto/destaque: detecta rostos (OpenCV YuNet, davidsa/modelos/) e
  escolhe, dentro da área segura do Reels (y 260–1460), a faixa sem rosto e com menos
  detalhe (fundo, céu, parede, desfoque).
- Vertical: preenche a tela. Horizontal: fundo desfocado + foto inteira.
- Música: arquivos em davidsa/musicas/ (trechos de 13 s já normalizados).
"""
import argparse, os, subprocess, tempfile
import numpy as np, cv2
cv2.setLogLevel(2) if hasattr(cv2, 'setLogLevel') else None
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
AQUI = os.path.dirname(os.path.abspath(__file__))
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
CAPA_LIMPA, GANCHO_FIM, FIM_CARD = 2.0, 5.2, 2.6
ZOOM = 0.12
SEGURA = (260, 1460)   # fora da barra de cima e da interface de baixo do Reels
FAIXA = 360            # altura da faixa de texto


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))


def base(foto):
    """Quadro 'mestre' em 2x para o zoom ficar nítido."""
    im = ImageOps.exif_transpose(Image.open(foto)).convert("RGB")
    W2, H2 = W * 2, H * 2
    if im.width < im.height:
        return cover(im, W2, H2)
    bg = cover(im, W2, H2).filter(ImageFilter.GaussianBlur(60))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    s = (W2 * 0.94) / im.width
    fg = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    bg.paste(fg, ((W2 - fg.width) // 2, (H2 - fg.height) // 2 - 460))  # foto mais alta: faixa de texto fica no fundo desfocado
    return bg


def rostos(img):
    """Rostos (x, y, w, h) na tela 1080x1920 sem zoom — YuNet (davidsa/modelos/yunet_n_dynamic.onnx)."""
    im = np.array(img.resize((W, H)))[:, :, ::-1].copy()
    s = 640 / H
    im = cv2.resize(im, (round(W * s), round(H * s)))
    det = cv2.FaceDetectorYN.create(os.path.join(AQUI, "modelos", "yunet_n_dynamic.onnx"), "",
                                    (im.shape[1], im.shape[0]), 0.6)
    r = det.detect(im)[1]
    return [] if r is None else [tuple(v / s for v in x[:4]) for x in r]


def escolhe_faixa(img, faces):
    """Topo (y) da faixa de texto: sem rosto e com menos detalhe."""
    g = cv2.cvtColor(np.array(img.resize((W, H))), cv2.COLOR_RGB2GRAY)
    bordas = cv2.Canny(g, 60, 160).astype(float) / 255
    # área protegida: rosto ampliado (cabelo, pescoço) + folga para o zoom de 12%
    prot = np.zeros(H)
    for (x, y, w, h) in faces:
        peso = 1.0 if h > 90 else 0.25   # rosto grande = destaque; rostinhos ao fundo pesam menos
        y0 = max(0, int(y - 0.6 * h - 0.07 * H)); y1 = min(H, int(y + 1.8 * h + 0.07 * H))
        prot[y0:y1] = np.maximum(prot[y0:y1], peso)
    melhor = None
    for y in range(SEGURA[0], SEGURA[1] - FAIXA + 1, 20):
        rosto = prot[y:y + FAIXA].mean()
        detalhe = bordas[y:y + FAIXA].mean()
        custo = rosto * 10 + detalhe
        if melhor is None or custo < melhor[0]:
            melhor = (custo, y)
    return melhor[1]


def texto_central(d, y, txt, fonte, cor=(255, 255, 255), alpha=255, larg=940):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if d.textlength(t, font=fonte) > larg and atual:
            linhas.append(atual); atual = p
        else:
            atual = t
    linhas.append(atual)
    for ln in linhas:
        w = d.textlength(ln, font=fonte)
        x = (W - w) / 2
        d.text((x + 3, y + 3), ln, font=fonte, fill=(0, 0, 0, int(alpha * 0.6)))
        d.text((x, y), ln, font=fonte, fill=cor + (alpha,))
        y += fonte.size * 1.3
    return y


def faixa(d, y, a):
    """Faixa escura com bordas suaves (gradiente) atrás do texto."""
    for k in range(FAIXA):
        borda = min(k, FAIXA - k) / 70
        d.line((0, y + k, W, y + k), fill=(0, 0, 0, int(115 * a * min(1, borda))))


def quadros(foto, dur, gancho, legenda, pasta):
    m = base(foto)
    yb = escolhe_faixa(m, rostos(m))
    n = int(dur * FPS)
    f_gancho = ImageFont.truetype(LORA, 62)
    f_marca = ImageFont.truetype(LORA, 62)
    f_leg = ImageFont.truetype(INTER, 32)
    for i in range(n):
        t = i / (n - 1)
        e = t * t * (3 - 2 * t)
        z = 1.0 + ZOOM * e
        cw, ch = m.width / z, m.height / z
        l, tp = (m.width - cw) / 2, (m.height - ch) / 2
        fr = m.resize((W, H), Image.BICUBIC, box=(l, tp, l + cw, tp + ch))
        sec = i / FPS
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        if gancho and CAPA_LIMPA <= sec < GANCHO_FIM:
            a = min(1, (sec - CAPA_LIMPA) / 0.5, (GANCHO_FIM - sec) / 0.5)
            faixa(d, yb, a)
            texto_central(d, yb + 110, gancho, f_gancho, alpha=int(255 * a))
        ini = dur - FIM_CARD
        if sec > ini:
            a = min(1, (sec - ini) / 0.6)
            faixa(d, yb, a)
            y = texto_central(d, yb + 115, "@davidsafotografia", f_marca, alpha=int(255 * a))
            if legenda:
                texto_central(d, y + 10, legenda.upper(), f_leg, cor=(232, 205, 150), alpha=int(255 * a))
        fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
        fr.save(os.path.join(pasta, f"{i:04d}.jpg"), quality=92)
    return yb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto"); ap.add_argument("audio"); ap.add_argument("saida")
    ap.add_argument("--inicio", type=float, default=0); ap.add_argument("--dur", type=float, default=12)
    ap.add_argument("--gancho", default=""); ap.add_argument("--legenda", default="")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        yb = quadros(a.foto, a.dur, a.gancho, a.legenda, tmp)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%04d.jpg"]
        if a.audio and a.audio != "-":
            cmd += ["-ss", str(a.inicio), "-t", str(a.dur), "-i", a.audio,
                    "-af", f"afade=t=in:d=0.4,afade=t=out:st={a.dur - 1.5}:d=1.5", "-c:a", "aac", "-b:a", "192k",
                    "-map", "0:v", "-map", "1:a", "-shortest"]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
                "-movflags", "+faststart", a.saida]
        subprocess.run(cmd, check=True)
    print("faixa de texto y =", yb)


if __name__ == "__main__":
    main()

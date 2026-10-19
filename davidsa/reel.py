"""Transforma UMA foto em Reels 1080x1920 (zoom lento + música da Viva Voz).

uso: python3 davidsa/reel.py FOTO.jpg AUDIO_OU_VIDEO saida.mp4 [--inicio 30] [--dur 12]
       [--gancho "Texto dos 3 primeiros segundos"] [--legenda "Stephanie & Alisson · Paraibuna"]

- Vertical: preenche a tela e faz zoom-in lento.
- Horizontal: fundo com a própria foto desfocada + foto inteira centralizada, zoom suave.
- Gancho opcional nos primeiros ~3 s; "@davidsafotografia" + legenda no final.
- Textos na faixa y 1080-1460: fora do rosto (terço de cima) e fora da área da interface do Reels (embaixo).
- Áudio: trecho de --dur s a partir de --inicio, extraído de qualquer áudio/vídeo, com fade.
"""
import argparse, os, subprocess, tempfile
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))


def base(foto):
    """Quadro 'mestre' em 2x para o zoom ficar nítido."""
    im = ImageOps.exif_transpose(Image.open(foto)).convert("RGB")
    W2, H2 = W * 2, H * 2
    if im.width < im.height:  # vertical
        return cover(im, W2, H2)
    bg = cover(im, W2, H2).filter(ImageFilter.GaussianBlur(60))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    s = (W2 * 0.94) / im.width
    fg = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    bg.paste(fg, ((W2 - fg.width) // 2, (H2 - fg.height) // 2 - 80))
    return bg


def texto_central(d, y, txt, fonte, cor=(255, 255, 255), alpha=255, larg=940):
    # quebra simples de linha
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


def quadros(foto, dur, gancho, legenda, pasta):
    m = base(foto)
    n = int(dur * FPS)
    f_gancho = ImageFont.truetype(LORA, 64)
    f_marca = ImageFont.truetype(LORA, 62)
    f_leg = ImageFont.truetype(INTER, 32)
    for i in range(n):
        t = i / (n - 1)
        e = t * t * (3 - 2 * t)  # ease in-out
        z = 1.0 + 0.12 * e      # zoom 1.00 -> 1.12
        cw, ch = m.width / z, m.height / z
        l = (m.width - cw) / 2
        tp = (m.height - ch) / 2 - (m.height * 0.02) * e  # leve subida
        fr = m.resize((W, H), Image.BICUBIC, box=(l, tp, l + cw, tp + ch))
        sec = i / FPS
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        if gancho and sec < 3.2:
            a = min(1, sec / 0.4, (3.2 - sec) / 0.4)
            d.rectangle((0, 1080, W, 1460), fill=(0, 0, 0, int(120 * a)))
            texto_central(d, 1150, gancho, f_gancho, alpha=int(255 * a))
        fim = dur - 2.6
        if sec > fim:
            a = min(1, (sec - fim) / 0.6)
            d.rectangle((0, 1120, W, 1440), fill=(0, 0, 0, int(120 * a)))
            y = texto_central(d, 1200, "@davidsafotografia", f_marca, alpha=int(255 * a))
            if legenda:
                texto_central(d, y + 10, legenda.upper(), f_leg, cor=(232, 205, 150), alpha=int(255 * a))
        fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
        fr.save(os.path.join(pasta, f"{i:04d}.jpg"), quality=92)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto"); ap.add_argument("audio"); ap.add_argument("saida")
    ap.add_argument("--inicio", type=float, default=0); ap.add_argument("--dur", type=float, default=12)
    ap.add_argument("--gancho", default=""); ap.add_argument("--legenda", default="")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        quadros(a.foto, a.dur, a.gancho, a.legenda, tmp)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%04d.jpg"]
        if a.audio and a.audio != "-":
            cmd += ["-ss", str(a.inicio), "-t", str(a.dur), "-i", a.audio,
                    "-af", f"afade=t=in:d=0.6,afade=t=out:st={a.dur - 1.8}:d=1.8", "-c:a", "aac", "-b:a", "192k",
                    "-map", "0:v", "-map", "1:a", "-shortest"]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
                "-movflags", "+faststart", a.saida]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()

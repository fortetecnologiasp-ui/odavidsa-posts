"""Transforma os slides (1080x1350) de um carrossel do Viva Voz em stories 1080x1920."""
import sys,os,glob
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
W,H=1080,1920
LORA='/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
def story(src,dst):
    im=Image.open(src).convert('RGB')
    s=max(W/im.width,H/im.height); bg=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    l=(bg.width-W)//2; t=(bg.height-H)//2
    bg=bg.crop((l,t,l+W,t+H)).filter(ImageFilter.GaussianBlur(50))
    bg=ImageEnhance.Brightness(bg).enhance(0.35)
    k=1000/im.width; fg=im.resize((1000,round(im.height*k)),Image.LANCZOS)
    x=(W-fg.width)//2; y=(H-fg.height)//2-40
    bg.paste(fg,(x,y))
    d=ImageDraw.Draw(bg); f=ImageFont.truetype(LORA,48); f.set_variation_by_axes([500])
    d.text((W//2,y+fg.height+70),"@vivavozcasamentos",font=f,fill=(232,205,150),anchor='mm')
    bg.save(dst,quality=90)
def carrossel(pasta,saida):
    os.makedirs(saida,exist_ok=True)
    for f in sorted(glob.glob(pasta+'/*.jpg')): story(f,os.path.join(saida,os.path.basename(f)))
if __name__=='__main__': carrossel(sys.argv[1],sys.argv[2])

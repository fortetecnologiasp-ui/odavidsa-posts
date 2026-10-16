import sys,os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont
W,H=1080,1920
LORA='/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
INTER='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
def story(src,dst,legenda="Stephanie & Alisson · Paraibuna"):
    im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    # fundo: a própria foto ampliada, desfocada e escurecida
    s=max(W/im.width,H/im.height); bg=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    l=(bg.width-W)//2; t=(bg.height-H)//2; bg=bg.crop((l,t,l+W,t+H)).filter(ImageFilter.GaussianBlur(45))
    bg=ImageEnhance.Brightness(bg).enhance(0.45)
    # foto inteira, sem corte
    maxw,maxh=940,1300
    k=min(maxw/im.width,maxh/im.height); fg=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
    x=(W-fg.width)//2
    y=250 if fg.height>fg.width else (H-(fg.height+130))//2
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((x+8,y+14,x+fg.width+8,y+fg.height+14),fill=(0,0,0,140))
    bg=Image.alpha_composite(bg.convert('RGBA'),sh.filter(ImageFilter.GaussianBlur(18))).convert('RGB')
    bg.paste(fg,(x,y))
    d=ImageDraw.Draw(bg)
    f1=ImageFont.truetype(LORA,54); f1.set_variation_by_axes([500])
    f2=ImageFont.truetype(INTER,30)
    ty=y+fg.height+65
    d.text((W//2,ty),"@davidsafotografia",font=f1,fill=(245,236,220),anchor='mm')
    d.text((W//2,ty+62),legenda.upper(),font=f2,fill=(220,200,160),anchor='mm',spacing=4)
    bg.save(dst,quality=90)
if __name__=='__main__': story(sys.argv[1],sys.argv[2])

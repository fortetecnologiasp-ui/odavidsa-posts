import json, datetime as dt
fotos=[l.split() for l in open('fotos_ste_alisson.txt') if l.strip()]
fotos=[f for f in fotos if f[0]!='DAVI3523']  # já publicada 15/10 16h
L=[
"Tem dia que a gente não vive, a gente guarda. O de Stephanie & Alisson ficou guardado assim. 🤍",
"Stephanie & Alisson: o amor que transforma um dia comum no dia mais importante da vida.",
"Paraibuna foi testemunha. Stephanie & Alisson disseram sim. 🤍",
"Antes do sim, o coração já sabia. Stephanie & Alisson.",
"Cada olhar conta uma parte da história. Esta é de Stephanie & Alisson.",
"O tempo passa, a foto fica. E com ela, tudo o que Stephanie & Alisson sentiram.",
"Não é só uma foto. É a lembrança que Stephanie & Alisson vão mostrar para os netos.",
"Amor de verdade não precisa de pose. Stephanie & Alisson. 🤍",
"Um capítulo escrito a dois, em Paraibuna. Stephanie & Alisson.",
"Tem emoção que só cabe numa fotografia. Stephanie & Alisson.",
"Daqui a vinte anos, essa imagem ainda vai arrepiar. Stephanie & Alisson.",
"Os detalhes também contam a história de Stephanie & Alisson.",
"Quando duas histórias viram uma só: Stephanie & Alisson.",
"O dia passou rápido. As memórias de Stephanie & Alisson vão durar para sempre.",
"Sorrisos que dizem tudo. Stephanie & Alisson. 🤍",
"Família, amigos, amor. Tudo o que importa reunido no dia de Stephanie & Alisson.",
"Fotografar casamento é eternizar o que não volta. Obrigado, Stephanie & Alisson.",
"Paraibuna, um sim e duas vidas que agora caminham juntas. Stephanie & Alisson.",
"Cada segundo desse dia foi único. Stephanie & Alisson.",
"O amor mora nos pequenos gestos. Stephanie & Alisson.",
"Há encontros que estavam escritos. Stephanie & Alisson. 🤍",
"Uma imagem, mil sentimentos. Stephanie & Alisson.",
"Para Stephanie & Alisson, o para sempre começou em Paraibuna.",
"A gente fotografa o que o coração não quer esquecer. Stephanie & Alisson.",
"Leveza, verdade e muito amor. Assim foi o dia de Stephanie & Alisson.",
"Quem vive um amor assim merece guardar cada momento. Stephanie & Alisson.",
"Tem foto que a gente sente antes de ver. Stephanie & Alisson.",
"O sim mais bonito de Paraibuna. Stephanie & Alisson. 🤍",
"Memórias não se repetem. Por isso a gente guarda. Stephanie & Alisson.",
"Juntos é o lugar favorito de Stephanie & Alisson.",
"Um dia para lembrar a vida inteira. Stephanie & Alisson.",
"A emoção estava em todo lugar no casamento de Stephanie & Alisson.",
"Casamento é sobre pessoas. E sobre o amor entre elas. Stephanie & Alisson.",
"Histórias reais, sentimentos reais. Stephanie & Alisson.",
"Mais um capítulo da história de Stephanie & Alisson. 🤍",
"Cada clique, um pedaço do dia mais especial de Stephanie & Alisson.",
"O amor de Stephanie & Alisson em uma imagem.",
]
S=[
"Conta pra gente nos comentários: qual momento do seu casamento você mais quer eternizar?",
"Marca aqui quem vai casar e precisa ver essa história. 💍",
"Salve este post para se inspirar no seu grande dia.",
"Essa é uma das muitas fotos dessa história. Acompanhe as próximas.",
]
CTA="📸 Siga @davidsafotografia e acompanhe mais histórias de amor.\n🎶 E para a trilha sonora do seu grande dia, conheça a @vivavozcasamentos."
TAGS="#casamento #fotografiadecasamento #noivos #paraibuna #weddingphotography #davidsafotografia"
slots=["08:00","09:30","11:00","12:30","14:00","15:30","17:00","18:30","20:00","21:30"]
datas=[("2026-10-15",s) for s in ["17:00","18:30","20:00","21:30"]]
d=dt.date(2026,10,16)
while len(datas)<len(fotos):
    for s in slots: datas.append((d.isoformat(),s))
    d+=dt.timedelta(days=1)
out=[]
for i,(f,(dia,h)) in enumerate(zip(fotos,datas)):
    txt=f"{L[i%len(L)]}\n\n{S[i%len(S)]}\n\n{CTA}\n\n{TAGS}"
    out.append({"foto":f[0],"id":f[1],"dia":dia,"hora":h,"text":txt})
json.dump(out,open('agenda_ste.json','w'),ensure_ascii=False,indent=1)
print(len(out), out[-1]['dia'], out[-1]['hora'], max(len(o['text']) for o in out))

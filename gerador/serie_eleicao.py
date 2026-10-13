#  Marketing + relacionamento intercalados com a série de política (13 a 24/10).
#  13/10: 19:45, 20:30, 21:15, 22:00. 14 a 24/10: 10h, 14h, 18h marketing; 12h, 16h, 20h relacionamento.
import sys, os
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(__file__))
from serie_base import UP
from serie_eleicao_mkt import MKT
from serie_eleicao_rel import REL

# Fotos novas (12/10), só as profissionais. Sem camiseta-amarela (exclusiva da política), sem palestra, sem selfie.
FOTOS = [("moeda","50% 30%"),("estudio-celular","50% 25%"),("blazer-preto","50% 20%"),("camera","50% 8%"),
         ("blazer-escritorio","50% 20%"),("jardim","42% 0%"),("parede-cinza","50% 25%"),("blazer-oculos","50% 20%"),
         ("camiseta-azul","50% 22%"),("camiseta-marrom","50% 22%"),("mao-no-queixo","50% 25%"),("piscina","42% 15%")]

AGENDA = [("2026-10-13", ["19:45","20:30","21:15","22:00"])]
for d in range(11):
    AGENDA.append(((date(2026,10,14)+timedelta(days=d)).isoformat(), ["10:00","12:00","14:00","16:00","18:00","20:00"]))

CARROSSEIS = []
mi = ri = k = 0
for dia, horas in AGENDA:
    for j, h in enumerate(horas):
        if j % 2 == 0: c = MKT[mi]; mi += 1
        else: c = REL[ri]; ri += 1
        f, foco = FOTOS[k % len(FOTOS)]; k += 1
        c.update(foto=UP + f + ".jpg", foco=foco, zoom=1.0, inteira=False, dia=dia, hora=h)
        CARROSSEIS.append(c)
assert mi == len(MKT) and ri == len(REL), (mi, ri)

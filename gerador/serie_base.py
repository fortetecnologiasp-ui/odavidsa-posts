#  Base das séries de marketing e relacionamento (a partir de 26/10).
import itertools

import os
UP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos") + "/"
FOTOS = [
    (UP + "1001343507.jpg", "50% 20%", 1.0),   # blazer
    (UP + "1001343512.jpg", "50% 25%", 1.0),   # intenso
    (UP + "1001343509.jpg", "49% 30%", 1.0),   # fala
    (UP + "1001343506.jpg", "45% 30%", 1.0),   # sorri
    (UP + "1001343510.jpg", "50% 30%", 1.0),   # pensa
    (UP + "1001343508.jpg", "50% 30%", 1.0),   # café
]

# Fotos enviadas em 12/10 (usadas a partir do lote 4). Os lotes 1 a 3 continuam com FOTOS.
# Só fotos com cara profissional: selfies, frames de vídeo e fotos de celular ficam de fora (o David é fotógrafo).
NOVAS = [
    ("moeda", "50% 30%", 1.0),
    ("estudio-celular", "50% 25%", 1.0), ("blazer-preto", "50% 20%", 1.0), ("camera", "50% 8%", 1.0),
    ("blazer-escritorio", "50% 20%", 1.0), ("jardim", "42% 0%", 1.0), ("parede-cinza", "50% 25%", 1.0), ("blazer-oculos", "50% 20%", 1.0),
    ("camiseta-azul", "50% 22%", 1.0), ("camiseta-marrom", "50% 22%", 1.0),
    ("mao-no-queixo", "50% 25%", 1.0), ("moeda-cinza", "50% 25%", 1.0), ("mao-no-queixo-pb", "50% 30%", 1.0), ("palestra-tela", "inteira", 1.0), ("piscina", "42% 15%", 1.0),
    ("palestra-casal", "inteira", 1.0), ("palestra-iluminacao", "inteira", 1.0),
    ("amarela-bandeira", "50% 28%", 1.0), ("amarela-mesa", "50% 28%", 1.0), ("preta-mesa", "50% 28%", 1.0),
    ("cafe-falando", "50% 40%", 1.0), ("cafe-olhando", "50% 42%", 1.0), ("cafe-bebendo", "50% 42%", 1.0),
]
FOTOS_TODAS = FOTOS + [(UP + n + ".jpg", f, z) for n, f, z in NOVAS]

SERIES = {
    "mkt": dict(
        pill="Marketing · {tema}", rodape="Marketing e negócios",
        cta="Salva esse post e manda pra alguém que precisa ver isso.",
        fl="<strong>@odavidsa</strong> · Marketing, negócios e relacionamento.<br>Conteúdo novo todos os dias.",
        fc="@odavidsa · Marketing",
        css="",
        tags_base="#marketing #empreendedorismo #negociolocal",
    ),
    "rel": dict(
        pill="Relacionamento · {tema}", rodape="Relacionamento a dois",
        cta="Manda esse post pra quem divide a vida com você.",
        fl="<strong>@odavidsa</strong> · Marketing, negócios e relacionamento.<br>Conteúdo novo todos os dias.",
        fc="@odavidsa · Relacionamento",
        css=":root{--gold:#d98f86;--gold2:#f3b9b0;--glow1:rgba(217,143,134,.14);--glow2:rgba(217,143,134,.18);}",
        tags_base="#relacionamento #casal #casamento",
    ),
}

CTA_LEGENDA = "👉 Siga @odavidsa para mais conteúdo sobre marketing e relacionamento."

_rot = itertools.count()

# Versão em inglês (só marketing): ver serie_en.py. Carrossel fica com 6 slides PT + 6 EN.
try:
    from serie_en import EN as _EN
except ImportError:
    _EN = {}

CTA_EN = "👉 Follow @odavidsa for marketing tips every day."
TAGS_EN = "#smallbusiness #marketingtips"
LIMITE_LEGENDA = 500  # limite do Threads

def legenda_bilingue(gancho, chamada, en, tags):
    """Legenda PT + EN, no máximo 500 caracteres (Threads). Corta hashtags extras se passar."""
    tags = list(tags) + [t for t in TAGS_EN.split() if t not in tags]
    def monta(tg):
        return (f"🇧🇷 {gancho}\n{chamada} 👇\n\n"
                f"🇺🇸 {en['gancho']}\n{en['chamada']} 👇\n\n"
                f"Arrasta pro lado · English version inside ➡️\n\n"
                f"{CTA_LEGENDA}\n{CTA_EN}\n\n{' '.join(tg)}")
    txt = monta(tags)
    while len(txt) > LIMITE_LEGENDA and len(tags) > 3:
        tags = tags[:-1]; txt = monta(tags)
    return txt

def X(serie, slug, tema, kicker, titulo, slides, pergunta, gancho, chamada, tags):
    s = SERIES[serie]
    f, foco, zoom = FOTOS[next(_rot) % len(FOTOS)]
    _t = []
    for t in (s['tags_base'] + " " + tags).split():
        if t not in _t: _t.append(t)
    legenda = (f"{gancho}\n\nArrasta pro lado e salva pra não esquecer.\n\n{chamada} 👇\n\n"
               f"{CTA_LEGENDA}\n\n{' '.join(_t)}")
    en = _EN.get(slug) if serie == "mkt" else None
    if en:
        legenda = legenda_bilingue(gancho, chamada, en, _t)
    return {
        "slug": slug, "serie": serie, "foto": f, "foco": foco, "zoom": zoom, "tema": tema,
        "kicker": kicker, "titulo": titulo, "slides": slides, "pergunta": pergunta,
        "pill": s["pill"].format(tema=tema), "rodape": s["rodape"], "cta": s["cta"],
        "fl": s["fl"], "fc": s["fc"], "css": s["css"], "ai": "", "legenda": legenda, "en": en,
    }

def montar(mkt, rel, inicio, ndias, offset=0, fotos=None):
    """Distribui 3 de marketing + 3 de relacionamento por dia e alterna as 6 fotos sem repetir no mesmo dia."""
    from datetime import timedelta
    fotos = fotos or FOTOS
    dias = {}
    for d in range(ndias):
        dia = (inicio + timedelta(days=d)).isoformat()
        lista = [mkt[3*d], rel[3*d], mkt[3*d+1], rel[3*d+1], mkt[3*d+2], rel[3*d+2]]
        for i, c in enumerate(lista):
            f, foco, zoom = fotos[(6 * d + i + offset) % len(fotos)] if len(fotos) > 6 else fotos[(i + d + offset) % len(fotos)]
            inteira = foco == "inteira"
            c.update(foto=f, foco=("50% 40%" if inteira else foco), zoom=zoom, inteira=inteira)
        dias[dia] = lista
    return dias

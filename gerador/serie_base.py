#  Base das séries de marketing e relacionamento (a partir de 26/10).
import itertools

import os
UP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos") + "/"
FOTOS = [
    (UP + "1001343507.jpg", "50% 20%", 1.0),   # blazer
    (UP + "1001343512.jpg", "50% 25%", 1.0),   # intenso
    (UP + "1001343509.jpg", "49% 38%", 1.7),   # fala
    (UP + "1001343506.jpg", "45% 30%", 1.0),   # sorri
    (UP + "1001343510.jpg", "50% 44%", 1.7),   # pensa
    (UP + "1001343508.jpg", "50% 44%", 1.7),   # café
]

# Fotos enviadas em 12/10 (usadas a partir do lote 4). Os lotes 1 a 3 continuam com FOTOS.
NOVAS = [
    ("moeda", "50% 30%", 1.0), ("risada-mesa", "50% 28%", 1.0), ("carro-oculos", "50% 30%", 1.0),
    ("estudio-celular", "50% 25%", 1.0), ("blazer-preto", "50% 20%", 1.0), ("camera", "50% 8%", 1.0),
    ("blazer-escritorio", "50% 20%", 1.0), ("carro-selfie", "50% 30%", 1.0), ("jardim", "42% 0%", 1.0),
    ("carro-oculos2", "50% 32%", 1.0), ("parede-cinza", "50% 25%", 1.0), ("blazer-oculos", "50% 20%", 1.0),
    ("camiseta-azul", "50% 22%", 1.0), ("camiseta-marrom", "50% 22%", 1.0), ("perfil-fone", "50% 30%", 1.0),
    ("mao-no-rosto", "50% 35%", 1.0),
    ("mao-no-queixo", "50% 25%", 1.0), ("palestra-tela", "inteira", 1.0), ("piscina", "42% 15%", 1.0),
    ("palestra-casal", "inteira", 1.0), ("palestra-iluminacao", "inteira", 1.0),
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

def X(serie, slug, tema, kicker, titulo, slides, pergunta, gancho, chamada, tags):
    s = SERIES[serie]
    f, foco, zoom = FOTOS[next(_rot) % len(FOTOS)]
    _t = []
    for t in (s['tags_base'] + " " + tags).split():
        if t not in _t: _t.append(t)
    legenda = (f"{gancho}\n\nArrasta pro lado e salva pra não esquecer.\n\n{chamada} 👇\n\n"
               f"{CTA_LEGENDA}\n\n{' '.join(_t)}")
    return {
        "slug": slug, "serie": serie, "foto": f, "foco": foco, "zoom": zoom, "tema": tema,
        "kicker": kicker, "titulo": titulo, "slides": slides, "pergunta": pergunta,
        "pill": s["pill"].format(tema=tema), "rodape": s["rodape"], "cta": s["cta"],
        "fl": s["fl"], "fc": s["fc"], "css": s["css"], "ai": "", "legenda": legenda,
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

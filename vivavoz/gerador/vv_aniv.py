from vv_conteudo import C, CTA
c = C("2026-10-15", "engaja", "22-anos-viva-voz", "22 anos", "Legado · 15 de outubro",
  "22 anos de <em>história</em>", "Desde 2004 fazendo a trilha sonora do “sim” de muitos casais.",
  [dict(num="2004", h="Onde tudo começou", p="Em 15 de outubro de 2004 nascia a Viva Voz Casamentos, com um propósito: transformar cada cerimônia em um momento inesquecível através da música."),
   dict(num="22", h="Anos de emoção", li=["Entradas que arrepiaram igrejas inteiras", "Alianças trocadas ao som da música certa", "Saídas em festa, sob aplausos"]),
   dict(num="600+", h="Um repertório que cresceu com a gente", p="Hoje são mais de 600 músicas, separadas por momento da cerimônia e por estilo, do gospel ao popular."),
   dict(num="♥", h="Obrigado", p="Aos casais que confiaram o dia mais importante da vida a nós, aos músicos que fazem parte dessa história e a quem acompanha o nosso trabalho. Que venham muitos outros anos de música e amor.")],
  "Casou com a Viva Voz? Conta pra gente!",
  "Hoje a Viva Voz Casamentos completa 22 anos de história. 🎶",
  "São 22 anos fazendo a trilha sonora do “sim” de tantos casais. Obrigado a cada noivo, noiva e família que confiou esse momento a nós. Casou com a Viva Voz? Conta nos comentários 👇",
  cta="Obrigado por fazer parte dos nossos 22 anos. Que venham muitos outros!")
c["hora"] = "20:00"
c["legenda"] = c["legenda"].rsplit("\n\n",1)[0] + "\n\n#vivavozcasamentos #22anos #musicaparacasamento #casamento #cerimonia"
CARROSSEIS = [c]

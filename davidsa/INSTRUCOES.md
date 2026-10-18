# @davidsafotografia — posts automáticos de fotos de casamento

## Metricool
- brand/blogId **7449099**, fuso America/Sao_Paulo, autoPublish true.
- providers `[{"network":"instagram"},{"network":"facebook"}]`
- instagramData `{"type":"POST","collaborators":[],"showReelOnFeed":true}`, facebookData `{"type":"POST"}`
- media = URL do Google Drive da foto (`https://drive.google.com/file/d/<ID>/view?usp=drivesdk`). O Drive está ligado ao Metricool.

## Ritmo
- **10 posts por dia**: 08:00, 09:30, 11:00, 12:30, 14:00, 15:30, 17:00, 18:30, 20:00, 21:30.
- **1 foto = 1 post único. Nunca repetir.** Antes de agendar, leia `publicadas.txt`: nenhum ID listado pode virar post único de novo. Depois de agendar, acrescente cada foto nova em `publicadas.txt` e faça commit.
- Ordem: por número do arquivo (DAVIxxxx crescente), casal por casal.
- Não mexer no tamanho: a foto vai como está (sem corte/zoom). Formatos fora de 4:5 a 1,91:1 o Instagram pode ajustar.

## Onde estão as fotos
- **SOMENTE** as subpastas de casal dentro da pasta "David Sá Fotografia - Instagram" (cada uma com info.txt/info.rtf: nomes, local, detalhes). **Nunca use fotos de nenhuma outra pasta do Drive**, mesmo que pareçam do mesmo casal. Se a subpasta estiver vazia, não poste nada desse casal.
- Use só o que estiver no info; nunca invente detalhes da foto ou do casamento.
- A paginação do Drive pode repetir resultados: se passar de 100 fotos, liste por janelas de `createdTime`.

## Legenda
Frase emocional com os nomes do casal (sem descrever o que a foto mostra), chamada para comentar/marcar/salvar, depois:
```
📸 Siga @davidsafotografia e acompanhe mais histórias de amor.
🎶 E para a trilha sonora do seu grande dia, conheça a @vivavozcasamentos.
```
Hashtags: #casamento #fotografiadecasamento #noivos #<cidade> #weddingphotography #davidsafotografia
Exemplo de legendas já usadas: `agenda_stephanie_alisson.json` (não repita as mesmas frases em sequência).

## Carrosséis
Quando TODAS as fotos de um casal já tiverem sido agendadas como post único, criar carrosséis desse casal (até 10 fotos cada, separando horizontais de verticais; fotos podem se repetir nos carrosséis), nos mesmos horários.

## Stories (só Instagram)
- Todo dia, **as mesmas 10 fotos do feed daquele dia** viram 10 stories em sequência: **10:00, 10:01, 10:02 … 10:09**, na ordem do feed. Em dia de carrossel, use a 1ª foto de cada carrossel.
- Arte 1080x1920 gerada por `davidsa/story.py` (foto inteira sem corte sobre fundo desfocado da própria foto, "@davidsafotografia" + "NOIVOS · CIDADE" embaixo). Para outro casal, passe a legenda: `story(src, dst, "Nome & Nome · Cidade")`.
- Salve em `davidsa/stories/AAAA-MM-DD/NN_FOTO.jpg`, commit + push e use a URL raw fixada no hash do commit.
- Metricool: providers `[{"network":"instagram"}]`, instagramData `{"type":"STORY","collaborators":[],"showReelOnFeed":true}`, sem campo text.
- Já agendados: 17/10 a 21/10. (18/10: sem fotos novas nas pastas; feed e stories cobertos só até 21/10.)

## Como saber se a foto é horizontal ou vertical
O Drive não informa as dimensões. Baixe cada foto com `download_file_content` (o resultado grande é salvo num arquivo .txt em JSON com o campo `content` em base64), decodifique com Python + PIL (`ImageOps.exif_transpose`) e leia largura x altura. Apague os arquivos depois. Dimensões já medidas ficam em `dimensoes_fotos.json`.
Fotos verticais 2:3 são ajustadas pelo Instagram para 4:5 (limite da rede); horizontais 3:2 entram inteiras.

## Situação (15/10/2026)
- Stephanie & Alisson: 55 posts únicos (15/10 17h → 21/10 08h) + 9 carrosséis em 21/10 (09h30 → 21h30), separados por orientação, em ordem do dia (noivo, entrada, cerimônia, altar, saída, família, festa, favoritas, detalhes). Ver `carrosseis_stephanie_alisson.json`. Esse casal está concluído.
- 22/10 em diante: livre para o próximo casal (Marcela & Felipe, Laura & Renan quando tiverem fotos).
- Rascunhos com o texto "APAGAR - foto da pasta errada" no Metricool (15/10 16h e 22/10) são lixo: ignore.

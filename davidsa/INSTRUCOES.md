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
Gerador de exemplo: `gerar_ste.py`.

## Carrosséis
Quando TODAS as fotos de um casal já tiverem sido agendadas como post único, criar carrosséis desse casal (até 10 fotos cada, separando horizontais de verticais; fotos podem se repetir nos carrosséis), nos mesmos horários.

## Situação (15/10/2026)
- Stephanie & Alisson (subpasta "Stephanie & Alisson", info: Paraibuna): as 55 fotos da pasta já estão agendadas como post único (15/10 17h até 21/10 08h). Próximo passo: carrosséis desse casal a partir de 21/10 09:30, a menos que o David suba fotos novas na pasta (aí as novas entram primeiro como post único).
- Rascunhos com o texto "APAGAR - foto da pasta errada" no Metricool (15/10 16h e 21/10 09:30 a 22/10 21:30) são lixo: ignore e não reaproveite.

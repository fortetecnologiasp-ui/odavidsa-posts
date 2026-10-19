# Viva Voz Casamentos — carrosséis automáticos (@vivavozcasamentos)

## Ritmo
- **3 carrosséis por dia, todos os dias**, só no Instagram @vivavozcasamentos.
- Metricool: blogId/brandId **7401168**, fuso America/Sao_Paulo, autoPublish true, draft false.
- Horários fixos: **10:00 música**, **15:00 dica para noivos**, **20:00 engajamento**.
- Na tarefa semanal: descubra o último dia já agendado (getScheduledPosts no brand 7401168, janelas de 2 dias) e gere os **7 dias seguintes** (21 carrosséis). Nunca duplique um dia que já tem posts.

## Conteúdo
- Tipos:
  - `musica`: músicas por momento (entradas, alianças, assinaturas, saída, homenagens, primeira dança) e gospel x popular. Só músicas reais, com título e artista corretos; marque cada uma como gospel, popular, classica ou mpb. Nunca reproduza letras.
  - `dica`: dicas práticas para noivos sobre a música da cerimônia e da festa (planejamento, roteiro, tempo, contratação, som, ensaio).
  - `engaja`: enquetes A/B/C/D, "isso ou aquilo", "marca quem vai casar", perguntas sobre a história do casal.
- Não repita temas: veja os slugs já usados nas pastas `vivavoz/AAAA-MM-DD/`.
- Sem política, sem preços ou valores.
- Capas só com texto (tipográficas) até o David mandar fotos de casamento. Não use banco de imagens.

## Legenda
Descrição própria do post (2 parágrafos curtos, o segundo com a chamada para comentar), depois o CTA fixo e as hashtags. O CTA e as hashtags já saem prontos da função `C()` de `gerador/vv_conteudo.py`:

```
👉 Siga @vivavozcasamentos e salve este post para o seu casamento.
Quer música ao vivo na sua cerimônia? Chama no direct.
📸 E para eternizar cada momento, conheça a @davidsafotografia.
```

## Como gerar
1. Crie `vivavoz/gerador/vv_semana_AAAA-MM-DD.py` (data do primeiro dia) no mesmo formato de `vv_conteudo.py`:
   `from vv_conteudo import C` e uma lista `CARROSSEIS = [C(dia, tipo, slug, tema, kicker, titulo, sub, slides, pergunta, abertura, chamada), ...]`.
   - slides: 3 ou 4 dicts com `num`, `h` e um de `songs=[(n, titulo, artista, tipo)]`, `p="texto"` ou `li=["item", ...]` (aceita `<b>`).
   - título da capa com uma palavra em `<em>` (fica dourada). Slug sem acento.
2. Renderize: `cd vivavoz/gerador && CONTEUDO=vv_semana_AAAA-MM-DD OUT_DIR=../ python3 vv_render.py` (gera `vivavoz/AAAA-MM-DD/slug/01..06.jpg`). Fontes Inter e Lora já instaladas no sistema; logos em `logo.png`/`logo-claro.png`.
3. Confira as capas numa folha de contato: nenhum título pode encostar no logo nem sair da largura.
4. Commit + push e use URLs raw fixadas no hash do commit:
   `https://raw.githubusercontent.com/fortetecnologiasp-ui/odavidsa-posts/<hash>/vivavoz/<dia>/<slug>/NN.jpg`
5. Agende com createScheduledPost: providers `[{"network":"instagram"}]`, instagramData `{"type":"POST","collaborators":[],"showReelOnFeed":true}`, text = legenda.

## Datas comemorativas
Antes de escrever os temas da semana, consulte `DATAS_COMEMORATIVAS.md` (raiz do repo): nas datas listadas, um post do dia vira o post temático.

## Stories (Instagram)
- Os slides de cada carrossel do dia também viram stories, em sequência, 5 min depois do post do feed:
  carrossel das 10h → stories 10:05, 10:06, …; 15h → 15:05…; 20h → 20:05… (um story por slide, na ordem).
- Gerar com `python3 vivavoz/gerador/vv_story.py` (função `carrossel(pasta_slides, saida)`): 1080x1920, fundo = slide desfocado/escurecido, slide centralizado, "@vivavozcasamentos" embaixo.
- Arquivos em `vivavoz/stories/AAAA-MM-DD/<slug>/NN.jpg`; commitar e usar a URL raw fixada no hash do commit.
- Metricool (brand 7401168): providers `[{"network":"instagram"}]`, `instagramData {"type":"STORY","collaborators":[],"showReelOnFeed":true}`, sem texto.
- Status: stories já agendados de 16/10 a 27/10 (199 stories); carrosséis do feed até 27/10.

## Reels (Instagram) — 1 por dia às 18:00
- Gerador: `python3 vivavoz/gerador/vv_reel.py` (1080x1920, capa limpa nos 2 primeiros segundos, texto numa faixa sem rosto, final com "@vivavozcasamentos" + "Solicite um orçamento sem compromisso").
- Mistura por semana (7 dias): **5 "aovivo"** (corte de 13 s da banda tocando, som original), **1 "ab"** (dois cortes, "A ou B? comenta"), **1 "dica"** (slides de um carrossel de dica já publicado ANTES, com música de `davidsa/musicas/`).
  - aovivo: `vv_reel.py aovivo VIDEO INICIO saida.mp4 --gancho "..."`
  - ab: `vv_reel.py ab VIDEO_A INICIO_A VIDEO_B INICIO_B saida.mp4 --pergunta "..." --rotulo-a "..." --rotulo-b "..."`
  - dica: `vv_reel.py dica vivavoz/AAAA-MM-DD/<slug> davidsa/musicas/<trecho>.m4a saida.mp4`
- Cortes: SOMENTE os aprovados em `vivavoz/reels/cortes.json` (sem conversa, aprovados pelo David). Cada corte é usado UMA vez (preencha `usado_em`). Vídeos de origem em `vivavoz/videos/`.
- Se sobrarem menos de 7 cortes livres, avise o David para mandar vídeos novos dos casamentos (os cortes de vídeo novo precisam ser aprovados por ele antes de usar).
- Gancho: frase curta e verdadeira sobre o que aparece no vídeo (voz, violino, piano, noiva, altar). Nunca inventar nomes ou fatos.
- Legenda: gancho + 1–2 frases + "💬 Solicite um orçamento sem compromisso: chama a gente no direct!" + hashtags (#casamento #musicaparacasamento #musicaaovivo #cerimonia #noivas #vivavozcasamentos + 1 específica).
- Salvar em `vivavoz/reels/AAAA-MM-DD.mp4`, registrar em `vivavoz/reels/plano.json`, commit + push, URL raw fixada no hash do commit.
- Metricool (brand 7401168): providers `[{"network":"instagram"}]`, instagramData `{"type":"REEL","collaborators":[],"showReelOnFeed":true}`. Testado e aceito em 18/10/2026.
- Status: Reels agendados de 19/10 a 27/10/2026.

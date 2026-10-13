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

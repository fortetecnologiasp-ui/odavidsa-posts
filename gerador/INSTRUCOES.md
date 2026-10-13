# Tarefa semanal: carrosséis de marketing e relacionamento do @odavidsa

Dono: David Sá (@odavidsa). Instagram ligado ao Metricool, blogId **7381311**, fuso **America/Sao_Paulo**.
Todo o gerador está nesta pasta (`gerador/`), e as imagens prontas ficam em `series/<AAAA-MM-DD>/<slug>/01..06.jpg`.

## Quando gerar

1. `git pull` no repositório.
2. Veja a última data em `series/` (a maior pasta). Se ela já estiver **10 dias ou mais à frente de hoje**, não gere nada. Só avise o David de que o conteúdo já está garantido até essa data e termine.
3. Senão, gere os **7 dias seguintes** à última data.

## Conteúdo (6 carrosséis por dia)

São 3 de marketing e 3 de relacionamento por dia, intercalados (m, r, m, r, m, r). Quem monta essa ordem e distribui as fotos é o `montar()`.

- **Marketing (`"mkt"`):** misture marketing para negócio local (loja, serviço, atendimento, Instagram, WhatsApp, Google, vendas, preço, indicação) e marca pessoal (posicionamento, constância, vídeo, autoridade).
- **Relacionamento (`"rel"`):** vida a dois, ou seja, comunicação, rotina, dinheiro do casal, família, brigas, carinho, casamento, namoro.
- **Proibido:**
  - política;
  - estatística ou número inventado, ou "pesquisa diz";
  - promessa de resultado;
  - conselho médico ou psicológico de diagnóstico;
  - conteúdo íntimo/sexual explícito.
- **Não repita temas nem títulos** já usados. Antes de escrever, leia os títulos de todos os `serie_lote*.py`.
- **Tom e idioma:** português do Brasil, direto, prático, frases curtas. Use o mesmo estilo dos lotes anteriores (copie a estrutura de `serie_lote3.py`).

### Como escrever o lote

Crie `gerador/serie_loteN.py`, com N sendo o próximo número.

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from serie_base import X, montar
from datetime import date
MKT = [ X("mkt","m0NN","Tema","Kicker curto","Título com <em>destaque</em>",
          [("Subtítulo 1",["frase"]),("Subtítulo 2",["frase"]),("Subtítulo 3",["frase"]),("Subtítulo 4",["frase"])],
          "Pergunta final do slide 6?",
          "Gancho da legenda (1 ou 2 frases).",
          "Chamada para comentar","#tag1 #tag2"), ... 21 itens ]
REL = [ ... 21 itens com "rel" e slugs r0NN ... ]
DIAS = montar(MKT, REL, date(AAAA, M, D), 7, offset=N)
```

Regras de cada carrossel:

- **Slugs:** continue a numeração do último lote (m091, m092… e r091, r092…).
- **Slides:** sempre 4, cada um como `(subtítulo, [1 ou 2 frases curtas])`.
- **Subtítulos:** **não** comece com número ("1.", "01"), porque o slide já mostra o número grande.
- **Título:** no máximo ~45 caracteres, com uma palavra-chave em `<em>`.
- **Hashtags:** só letras e números, sem hífen e sem acento. As de base (`#marketing...` / `#relacionamento...`) já entram sozinhas. Coloque 1 ou 2 extras.
- **Legenda:** o `X()` já monta a legenda com o CTA "👉 Siga @odavidsa…". Não remova esse CTA.

Depois de escrever o lote:

1. Acrescente o nome do lote em `LOTES` dentro de `serie_todos.py`.
2. Renderize com `cd gerador && python3 gerar_dias.py serie_loteN`. Isso grava as imagens em `series/`.
3. **Confira visualmente:**
   - Abra com Read a capa (`01.jpg`), um slide do meio e o `06.jpg` de pelo menos 4 carrosséis.
   - Procure texto cortado ou estourando, numeração duplicada e foto repetida no mesmo dia.
   - Corrija e renderize de novo se precisar.
4. Faça commit e push para `main`, terminando a mensagem com as linhas de atribuição pedidas pela sessão.

## Agendamento no Metricool

O plano gratuito permite **20 posts publicados por mês**. Rascunhos não contam.

1. Use `getScheduledPosts` (blogId 7381311) para contar os posts **não rascunho** do mês de cada dia novo, já publicados ou pendentes.
2. Para cada dia novo, em ordem de data, se ainda houver cota no mês, agende **1 post automático**:
   - **dia par do mês:** o 5º carrossel do dia (marketing), às **19:00**;
   - **dia ímpar do mês:** o 6º carrossel do dia (relacionamento), às **20:00**.
3. Se não houver cota, esse dia fica todo manual. **Nunca** passe de 20 por mês.
4. Se o Metricool recusar por limite, pare de agendar.
5. Payload de `createScheduledPost`:
   - `date` = `"AAAA-MM-DDTHH:MM:00-03:00"`;
   - `info` = `{"autoPublish":true,"descendants":[],"draft":false,"firstCommentText":"","hasNotReadNotes":false,"media":[6 URLs],"mediaAltText":[],"providers":[{"network":"instagram"}],"publicationDate":{"dateTime":"AAAA-MM-DDTHH:MM:00","timezone":"America/Sao_Paulo"},"shortener":false,"smartLinkData":{"ids":[]},"text":<legenda do carrossel>,"instagramData":{"type":"POST","collaborators":[],"showReelOnFeed":true}}`;
   - as URLs de mídia são `https://raw.githubusercontent.com/fortetecnologiasp-ui/odavidsa-posts/main/series/<dia>/<slug>/0N.jpg`, de 01 a 06. Faça o push **antes** de agendar.
6. Registre cada post agendado em `gerador/auto.json` como `"slug": {"dia": "...", "hora": "HH:MM"}`, depois faça commit e push.

Se o David tiver assinado um plano pago e o limite não existir mais, ele vai avisar. Até lá, siga a regra acima.

## Roteiro (página de postagem manual)

1. Rode `python3 gerador/montar_roteiro.py`. Ele grava `roteiro-series.html` na raiz do repositório e não deve ser commitado.
2. Leia o artifact `https://claude.ai/artifact/QbDitqymz8rsW5Qc5ixjSZ` com a ação read.
3. Publique o arquivo novo nesse mesmo `url`, mantendo o mesmo link.

## Aviso final ao David

Mande uma mensagem curta em português para o David, por SendUserMessage e na resposta final, com:

- os dias gerados;
- quais posts ficaram automáticos;
- o lembrete de que os outros estão no roteiro.

Se algo falhar (push, Metricool, render), diga claramente o que ficou pendente.

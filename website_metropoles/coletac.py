#%%
import json
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

url_feed = "https://www.metropoles.com/ultimas-noticias/feed"
feed = feedparser.parse(url_feed)


lista_noticias = []

for noticia in feed.entries[:20]:
    descricao = noticia.summary  
    if not descricao or descricao.isspace():
        if 'content' in noticia:
            html_bruto = noticia.content[0].value
            descricao = BeautifulSoup(html_bruto, "html.parser").text[:500] + "..."
        else:
            descricao = "Descrição não disponível."
    lista_noticias.append({
        "titulo": noticia.title,
        "descricao": descricao.strip(),
        "link": noticia.link,
        "data_publicacao": noticia.published
    })
data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"ultimas_noticias_{data_atual}.json"
with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
    json.dump(lista_noticias, arquivo, indent=4, ensure_ascii=False)

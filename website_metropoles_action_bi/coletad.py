#%%
import json
import feedparser
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,key)

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
json_string = json.dumps(lista_noticias, indent=4, ensure_ascii=False)
dados_em_memoria = json_string.encode("utf-8")
supabase.storage.from_("upsert").upload(
    file=dados_em_memoria,
    path="ultimas_noticias.json",
    file_options={"x-upsert": "true"}
)

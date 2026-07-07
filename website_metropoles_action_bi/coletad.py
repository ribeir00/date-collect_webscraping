#%%
import json
import feedparser
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")
EMAIL_SENHA = os.environ.get("EMAIL_SENHA")
EMAIL_DESTINATARIO = os.environ.get("EMAIL_DESTINATARIO")

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
if lista_noticias:
    print("Preparando envio de e-mail...")
        
    html_corpo = """
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #d32f2f;">Resumo Diário de Notícias - Metrópoles</h2>
            <p>Aqui estão as últimas notícias coletadas hoje:</p>
            <hr style="border: 0; border-top: 1px solid #ccc; margin-bottom: 20px;">
    """
    
    for idx, noticia in enumerate(lista_noticias, 1):
        html_corpo += f"""
        <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px dashed #eee;">
            <h3 style="margin: 0 0 5px 0;"><a href="{noticia['link']}" style="color: #1a73e8; text-decoration: none;">{idx}. {noticia['titulo']}</a></h3>
            <p style="margin: 5px 0; font-size: 14px; color: #555;">{noticia['descricao']}</p>
            <span style="font-size: 12px; color: #999;">Publicado em: {noticia['data_publicacao']}</span>
        </div>
        """
        
    html_corpo += """
        </body>
    </html>
    """
   
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Resumo Diário: Últimas Notícias'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    
    msg.attach(MIMEText(html_corpo, 'html'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_REMETENTE, EMAIL_SENHA)
            server.send_message(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
else:
    print("Nenhuma notícia encontrada para enviar.")
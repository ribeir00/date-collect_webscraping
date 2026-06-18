# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'pt-BR,pt;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Brave";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    }

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_info(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
    return data

def get_aparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content").find("h4").find_next().find_all("li"))
    aparicoes = [i.text for i in lis]
    return aparicoes
def get_personagem_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possível obter dados!!!")
        return {}
    else:
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = get_basic_info(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data
    
def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div",class_ = "td-page-content").find_all("a"))
    links = [i["href"] for i in ancoras]
    return links
# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d["link"] = i
    nome = i.strip("/").split("/")[-1].replace("-"," ").title()
    d["Nome"] = nome
    data.append(d)
# %%
df = pd.DataFrame(data)
df.to_parquet("dados_re.parquet", index=False)
df.to_pickle("dados_re.pkl")

# Projetos de Web Scraping e Extração de Dados

Este repositório contém scripts em Python focados em coleta, extração e estruturação de dados de diferentes fontes na web. O objetivo é demonstrar habilidades práticas em manipulação de dados e automação de processos.

---

## Tecnologias e Bibliotecas Utilizadas

* **Linguagem:** Python
* **Bibliotecas Principais:**
  * `pandas`: Manipulação, limpeza e exportação de dados em múltiplos formatos.
  * `requests`: Realização de requisições HTTP para acessar o conteúdo das páginas.
  * `BeautifulSoup` (bs4): Parseamento e extração de informações de estruturas HTML.
  * `feedparser`: Leitura e processamento de feeds RSS.
  * `datetime` e `json`: Manipulação de dados temporais e geração de arquivos JSON.

---

## Visão Geral dos Scripts

### 1. `coletaa.py` (Raspagem de Páginas Web)
* **O que faz:** Acessa o site *Resident Evil Database*, extrai dinamicamente as informações e aparições dos personagens, e salva o conjunto de dados em formatos estruturados e otimizados (`.parquet` e `.pkl`).

### 2. `coletab.py` (Extração de Dados Oficiais)
* **O que faz:** Obtém o arquivo de fechamento diário de cotações de moedas diretamente do Banco Central do Brasil (BCB), seleciona as informações mais relevantes e exporta tudo formatado para uma planilha Excel (`.xlsx`).

### 3. `coletac.py` (Consumo de Feed RSS)
* **O que faz:** Conecta-se ao feed de notícias do portal *Metrópoles*, coleta o título, resumo, data e link das publicações mais recentes (limpando o texto de resíduos HTML), e armazena os resultados em um arquivo `.json`.

### 4. `coletad.py` (Consumo de Feed RSS, Supabase e Automação de E-mail)
* **O que faz:** Conecta-se ao feed de notícias do portal *Metrópoles*, coleta o título, resumo, data e link das publicações mais recentes (limpando o texto de resíduos HTML). Os dados são estruturados e exportados como um arquivo `.json` diretamente para o bucket de Storage do **Supabase**.
* **Automação:** O script é executado diariamente de forma 100% autônoma através do **GitHub Actions** em um horário pré-definido, consolidando um resumo dessas notícias em um layout HTML e realizando o envio automático por e-mail utilizando SMTP seguro.
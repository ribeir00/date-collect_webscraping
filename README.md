# Multi-Target Web Scrapers Collection 

Este repositório reúne uma coleção de scripts de **Web Scraping** desenvolvidos em Python. O objetivo principal é extrair, estruturar e armazenar dados de múltiplos alvos na web (HTML e endpoints de APIs JavaScript), utilizando uma abordagem leve, rápida e sem a necessidade de emulação de navegadores pesados.

Ideal para fins de portfólio, automação de dados e integração de pipelines.

Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Extração de Dados:** `Requests` — Requisições HTTP eficientes para páginas estáticas e consumo de APIs internas estruturadas em JavaScript.
* **Manipulação de Dados:** `Pandas` — Limpeza, transformação e estruturação dos dados coletados.
* **Gestão Temporal:** `Datetime` — No caso específico evitar coleta em datas que não sejam úteis, API quebra.

## 📂 Estrutura do Repositório

```text
├── scrapers/
│   ├── html_sites/         # Scrapers focados na extração de páginas HTML
│   │   └── exemplo_html.py
│   └── js_api_sites/       # Scrapers que consomem APIs carregadas via JS
│       └── exemplo_api.py
└── README.md

#%%
import pandas as pd
from datetime import datetime, timedelta

def ultimo_d_util():
    hoje = datetime.now()
    dia_semana = hoje.weekday()
    
    if dia_semana == 0:
        hoje -= timedelta(days=3)
    elif dia_semana == 6:
        hoje -= timedelta(days=2)
    elif dia_semana == 5:
        hoje -= timedelta(days=1)
    else:
        hoje -= timedelta(days=1)
        
    # O formato exigido para baixar o arquivo do BCB
    return hoje.strftime('%Y%m%d')

data_consulta = 20260603
url_csv = f"https://www4.bcb.gov.br/Download/fechamento/{data_consulta}.csv"

colunas = [
    'data', 'cod_moeda', 'tipo', 'simbolo', 
    'taxa_compra', 'taxa_venda', 
    'paridade_compra', 'paridade_venda'
]

try:
    df = pd.read_csv(
        url_csv, 
        sep=';', 
        names=colunas, 
        decimal=',', 
        encoding='latin1'
    )
    
    df = df[['simbolo', 'tipo', 'taxa_compra', 'taxa_venda', 'paridade_compra', 'paridade_venda']]
    df.to_string(index=False)
    #Defina o formato que deseja salvar 
    df.to_excel("Todas_Cotacoes.xlsx", index=False)
    
except Exception as e:
    print(f"\nErro ao processar o arquivo. Detalhe: {e}")
    print("Possível causa: A data solicitada pode ser um feriado ou o BCB ainda não gerou o arquivo de hoje.")


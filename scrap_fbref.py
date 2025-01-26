import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# ids do fbref no formato https://fbref.com/en/squads/{time['id']}/{time['nome']
times = [
    {"nome": "Botafogo-RJ", "id": "d9fdd9d9"},
    {"nome": "Palmeiras", "id": "abdce579"},
    {"nome": "Flamengo", "id": "639950ae"},
    {"nome": "Fortaleza", "id": "a9d0ab0e"},
    {"nome": "Internacional", "id": "6f7e1f03"},
    {"nome": "São Paulo", "id": "5f232eb1"},
    {"nome": "Corinthians", "id": "bf4acd28"},
    {"nome": "Bahia", "id": "157b7fee"},
    {"nome": "Cruzeiro", "id": "03ff5eeb"},
    {"nome": "Vasco da Gama", "id": "83f55dbe"},
    {"nome": "Vitória", "id": "33f95fe0"},
    {"nome": "Atlético Mineiro", "id": "422bb734"},
    {"nome": "Fluminense", "id": "84d9701c"},
    {"nome": "Grêmio", "id": "d5ae3703"},
    {"nome": "Juventude", "id": "d081b697"},
    {"nome": "Red Bull Bragantino", "id": "f98930d1"},
    {"nome": "Athletico Paranaense", "id": "2091c619"},
    {"nome": "Criciúma", "id": "3f7595bb"},
    {"nome": "Atlético Goianiense", "id": "32d508ca"},
    {"nome": "Cuiabá", "id": "f0e6fb14"}
]

def coletar_dados_time(time):
    url = f"https://fbref.com/en/squads/{time['id']}/{time['nome'].replace(' ', '-')}-Stats"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    div = soup.find('div', id='div_stats_standard_24')

    if div:
        df = pd.read_html(StringIO(str(div)))[0]

        if isinstance(df.columns, pd.core.indexes.multi.MultiIndex):
            df.columns = [' '.join(col).strip() for col in df.columns.values]

        nome_arquivo = f"tabela_{time['nome'].replace(' ', '_')}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"Dados de {time['nome']} salvos em '{nome_arquivo}'")
    else:
        print(f"Tabela não encontrada para {time['nome']}.")


for time in times:
    coletar_dados_time(time)
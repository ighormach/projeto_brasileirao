import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = 'https://fbref.com/en/squads/639950ae/Flamengo-Stats'

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

    print(df.iloc[:, :6])

    df.to_excel('tabela_flamengo.xlsx', index=False)
    print("Tabela salva em 'tabela_flamengo.xlsx'")
else:
    print("Tabela não encontrada.")
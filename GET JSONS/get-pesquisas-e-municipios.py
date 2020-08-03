import requests
import json
import pandas as pd

url_municipio = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
url_pesquisas = "https://servicodados.ibge.gov.br/api/v1/pesquisas"

response1 = requests.get(url_pesquisas)
response2 = requests.get(url_municipio)
data2 = response2.json()
data = response1.json()
with open('pesquisas.json', 'w') as json_file:
    json.dump(data, json_file)
with open('municipios.json', 'w') as json_file:
    json.dump(data2, json_file)

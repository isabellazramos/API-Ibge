import requests
import json
import pandas as pd
from flatten_json import flatten

def main():

    url = "https://servicodados.ibge.gov.br/api/v1/pesquisas"
    output = "indicadores.csv"

    response = requests.get(url)
    data1 = response.text

    df_pesquisa = pd.read_json(data1)

    get_id = df_pesquisa['id'].values

    for i in get_id:

        number = str(i)
        response = requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/'+number+'/indicadores/')

        if(response.status_code) == 200:
            data = response.json()
            endereco = str('indicadores-da-pesquisa-'+str(i)+'.json')
            with open(endereco,'w') as f:
                f.write(json.dumps(data))
            #with open(endereco, 'w') as json_file:
            #    json.dump(data, json_file)


if __name__ == '__main__':
	main()

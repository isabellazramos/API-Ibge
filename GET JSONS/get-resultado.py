
import requests
import json
import pandas as pd
from flatten_json import flatten

def main():

    url1 = "https://servicodados.ibge.gov.br/api/v1/pesquisas"
    url2 = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"


    response2 = requests.get(url2)
    response1 = requests.get(url1)

    data2 = response2.text
    data1 = response1.text

    #parsed = json.loads(data)

    df_pesquisa = pd.read_json(data1)
    df_municipios = pd.read_json(data2)

    get_id_pesquisa = df_pesquisa['id'].values
    get_id_municipios = df_municipios['id'].values

    pesquisas = [11,19,20,21,22,23,24,29,30,31,32,33,34,35,36,37,38,39,40,42,43,44,
    45,46,47,48,49,50,51,52,53,10053,10054,10055,10056,10057,10058,10059,10060,10061,
    10062,10063,10064,10065,10066,10070,10071,10072,10073,
    10074,10075,10076,10077,10078,10079,10080,10081,10082,10083,10084,10085,10086,10087,
    10088,10089,10090,10091,10092,10093,10094]

    #for i in get_id_pesquisa:
    #number_pesquisa = str(i)

    for i in pesquisas:
        array = []
        df = pd.DataFrame()
        number_pesquisa = str(i)
        print("pesquisa:",number_pesquisa)
        for j in get_id_municipios:
            print("pesquisa:",number_pesquisa,"id",j)
            number_municipio = str(j)
            #https://servicodados.ibge.gov.br/api/v1/pesquisas/14/resultados/1100023
            response = requests.get('https://servicodados.ibge.gov.br/api/v1/pesquisas/'+number_pesquisa+'/resultados/'+number_municipio)


            if(response.status_code) == 200:
                data = response.json()
                dict = {j : data}
                print(dict)
                array.append(dict)
               # for d in data:
               #     dict[str(d['id'])] = d['res'][0]['res']
                #flatten(dict)
                #df = df.append(dict, ignore_index = True)

            else:
                break

        with open('resultado'+str(i)+'.json','w') as f:
            f.write(json.dumps(array))
#def statuscode():

if __name__ == '__main__':
	main()

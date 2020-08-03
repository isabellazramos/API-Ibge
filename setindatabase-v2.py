import pandas as pd
import numpy as np
import gzip
import ast
from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import Session

def main():

    #conectando com o Banco de Dados
    Base = automap_base()
    engine = create_engine("mysql+pymysql://api:api@localhost:3306/api") #COLOCAR O 'ENDEREÇO' DO SEU BANCO
    Base.prepare(engine, reflect=True)
    ResultadoV2 = Base.classes.resultadov2
    #Resultado = Base.classes.resultado

    connection = engine.connect()
    tables = engine.table_names()

    #engine.echo = True
    metadata= MetaData(engine)

    session = sessionmaker()
    session.configure(bind=engine)

    #periodo = Table('periodo',metadata,autoload = True) #recuperando tabelas do banco
    #indicador_pesquisa_periodo = Table('indicador_pesquisa_periodo',metadata,autoload = True)
    #print(Base.classes)
    #Resultadov2 = Table('resultadov2',metadata,autoload = True)
    

    pesquisas = [11,13,14,15,16,17,18,19,20,21,22,23,231,233,234,235,232,29,30,31,32,33,34,35,36,37,38,39,40,42,43,
    10075,10077,10078,10084,10087]

    for j in pesquisas:
        #recuperando o dataframe
        s = session()
        
        print("pesquisa: ",j)
        with open('RESULTADOS/pesquisa'+str(j)+'.csv', 'rb') as fd:
            gzip_fd = gzip.GzipFile(fileobj=fd)
            df = pd.read_csv(gzip_fd,index_col=0)

        #isolando a coluna do id do municipio
        id_municipio  = df['id']
        df = df.drop(columns=['id'])

        colunas = df.columns

        df = df.dropna()
        df = df.reset_index()

        #exe = resultado.insert()
        for col in colunas:
            #print(col,"\n")
            objects = []
            for i in range(len(df)):
                dict = df[col][i]
                dict = ast.literal_eval(dict)
                ano = dict.keys()
                #print("id municipio:",id_municipio[i])

                for d in ano:

                    if(dict[d] != None):
                        #print(d)
                        #print(d,":",dict[d]) #ano e resultado
                        #id_periodo = select([periodo.c.id]).where(periodo.c.ano == d)
                        #id_indicador_pesquisa_periodo = select([indicador_pesquisa_periodo.c.id]).where(indicador_pesquisa_periodo.c.id_pesquisa == str(j)).where(indicador_pesquisa_periodo.c.id_indicador == col).where(indicador_pesquisa_periodo.c.id_periodo == id_periodo)

                        ##conn = engine.connect()
                        #result = connection.execute(id_indicador_pesquisa_periodo)
                        #for row in result:
                        #    a = row[0] #id indicador pesquisa periodo
                            #print("id indicador_pesquisa_periodo",int(a))
                        #print(a)
                        ##exe.execute(id_cidade = int(id_municipio[i]),id_indicador_pesquisa_periodo = int(a), resultado = str(dict[d]))
                        objects.append({'id_cidade': int(id_municipio[i]),'id_pesquisa': int(j), 'periodo': int(d), 'id_indicador': int(col), 'resultado': str(dict[d])})
                        #objects.append({'id_cidade': int(id_municipio[i]),'id_indicador_pesquisa_periodo': int(a), 'resultado': str(dict[d])})
            #s.bulk_save_objects(objects)
            #s.add_all(objects)
            s.bulk_insert_mappings(ResultadoV2, objects)
            #s.bulk_insert_mappings(Resultado, objects)
            s.commit()


if __name__ == '__main__':
	main()

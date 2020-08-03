------------------------------------------------------------------------
				EXECUTANDO
------------------------------------------------------------------------


O banco de dados está relativamente pronto, falta apenas colocar as respostas
no banco. Por esse motivo, estou disponibilizando o 'backup.sql' para disponibilizar
o banco com mais facilidade, dê um restore no seu gerenciador de banco de dados para 
o banco estar disponível.

Estão disponíveis também os csvs que foram convertidos de jsons, pois quando peguei os dados
logo converti para csv pois para mim seria mais fácil de manipular dessa forma. Os csvs estão 
dentro do arquivo zipado.

Você precisará do python e dos seguintes pacotes:
-pandas
-numpy
-gzip
-ast
-sqlalchemy


Mas voltando, fiz um código para fazer inserts na tabela 'resultado' no banco de dados,
utilizei o pacote SLQALCHEMY para isso, que faz com que eu consiga manipular o banco de dados através
do python. O programa é o 'setindatabase.py'.

-> O programa tem um array com todos os números de pesquisas dos csvs de resultado para executar, caso queira executar apenas
um resultado de pesquisa, é só retirar os outros desse array.

-> Temos também que colocar o "endereço do seu banco no código" para conectar o sqlalchemy com o seu banco.
Para isso, pesquise a linha que contém o comentário "COLOQUE O ENDEREÇO DO SEU BANCO", e substitua com a que
está lá.

-> Depois disso é só executar o comando do python para rodar o programa, faça isso dentro dessa pasta pois 
utilizo a pasta RESULTADOS com os csvs para colocar no banco.



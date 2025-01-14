# SafeMask 
Ferramenta de anonimização de dados através de mascaramento em bases de dados.

### Requisitos

- Python 3 instalado e configurado;
- Biblioteca mysql-connector-python instalada;
- Adicionar suas credenciais no seguinte trecho de código:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/36905abd-8869-4a03-b38c-c0afcdd68965/image.png)

### Instalação

- Baixar o arquivo .zip do repositório;
- git clone

### Parâmetros

Obrigatórios:

- -c, recebe a coluna que será aplicada o mascaramento, o formato correto é database.tabela.coluna (obrigatório somente em tabelas mysql);
- -q, indica quantos caractéres serão substituidos;
- -m, indica qual caracterére será utilizado na substituição;

Opcionais: 

- -s, ativa o modo de simulação, onde nenhuma substituição é feita (somente com tabelas mysql);
- -b, ativa o backup incremental, onde as atlerações feitas são salvas em um arquivo .csv (somente com tabelas mysql);
- -i, aplica o mascaramento da esquerda para a direita
- -csv, indica que o mascaramento será feito em um arquivo .csv
- -csv-coluna, indica o nome da coluna que será mascarada no csv (obrigatório com arquivos .csv)

### Exemplos de uso

Base de dados  simulada utilizada nos testes:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/ba579167-4bda-4d3c-a237-6b045862f7b4/image.png)

- Utilizando em modo simulação;

python masksafe.py -c teste_anonimizacao.pessoa.cpf -q 5 -m '@' -s

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/9c91d363-281e-4070-ae64-ec98f557c7da/image.png)

- Utilizando na base de testes mysql;

python [masksafe.py](http://masksafe.py/) -c teste_anonimizacao.pessoa.cpf -q 5 -m '@' -b 'backup.csv'

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/0b33f78e-8345-40e9-8d69-6b35de969da6/image.png)

Arquivo de backup gerado:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/adada76a-9875-4a44-abd0-aa73d8213335/image.png)

Base alterada:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/bc126aca-21b0-4652-a8fb-40b007ef725c/image.png)

- Utilizando com arquivo .csv;

Arquivo utilizado nos testes:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/7f6e7d27-5df9-4c84-b09a-84f1305ff4fb/image.png)

python [safemask.py](http://safemask2.py/) -csv 'teste.csv' -csv-coluna 'cpf' -q 6 -m '*'

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/8c93913d-e0b7-4e32-bac2-5147d4134223/image.png)

Resultado final do arquivo:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/b01af394-dbce-457a-9287-9a177e4d12ea/b36b4a6a-37f9-4e04-8b49-20af7455dc89/image.png)

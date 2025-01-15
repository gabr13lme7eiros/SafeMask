# SafeMask 
Ferramenta de anonimização de dados através de mascaramento em bases de dados.

### Requisitos

- Python 3 instalado e configurado;
- Biblioteca mysql-connector-python instalada;
- Adicionar suas credenciais no seguinte trecho de código (Somente MySQL):

![image](https://github.com/user-attachments/assets/43dcdfbd-9ac4-434a-aa10-e9ee7f35549e)

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

![image](https://github.com/user-attachments/assets/418aa8d3-1392-4f46-83e1-924ca3d35b36)


- Utilizando em modo simulação;

python safemask.py -c teste_anonimizacao.pessoa.cpf -q 5 -m '@' -s

![image](https://github.com/user-attachments/assets/1d028907-b1e5-4b3c-9f65-5ec48c45f671)

- Utilizando na base de testes mysql;

python safemask.py -c teste_anonimizacao.pessoa.cpf -q 5 -m '@' -b 'backup.csv'

![image](https://github.com/user-attachments/assets/04497640-6699-4ec3-b957-a20be11e647b)

Arquivo de backup gerado:

![image](https://github.com/user-attachments/assets/ee6617fb-7578-4ee0-8e4e-35913297becf)

Base alterada:

![image](https://github.com/user-attachments/assets/8231ebf8-b017-47ed-8839-b2bc1afcbb69)

- Utilizando com arquivo .csv;

Arquivo utilizado nos testes:

![image](https://github.com/user-attachments/assets/fae155f2-f28e-494d-8f58-a6e74ec9e2cc)

python safemask.py -csv 'teste.csv' -csv-coluna 'cpf' -q 6 -m '*'

![image](https://github.com/user-attachments/assets/80acd615-2d2a-49f5-abf5-fee962cdfafa)

Resultado final do arquivo:

![image](https://github.com/user-attachments/assets/b480a69f-a1cc-49ec-95b3-5e93afe0b6e1)





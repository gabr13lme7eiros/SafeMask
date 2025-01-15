import mysql.connector
from mysql.connector import Error
import argparse
import csv
import os

# Parâmetros da conexão
host = '127.0.0.1' 
port = 3306  # Porta padrão do MySQL
user = 'root'
password = 'NoJD&OJ3'

# Função para criar o backup em CSV
def criar_backup_incremental(coluna, registros_anteriores, registros_atualizados, arquivo_backup):
    # Cria o cabeçalho do CSV se o arquivo não existir
    if not os.path.exists(arquivo_backup):
        with open(arquivo_backup, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')  # Certifique-se de usar o delimitador correto
            writer.writerow(['coluna', 'valor_antigo', 'valor_novo'])

    # Adiciona os dados alterados ao arquivo CSV
    with open(arquivo_backup, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')  # Certifique-se de usar o delimitador correto
        for antigo, novo in zip(registros_anteriores, registros_atualizados):
            writer.writerow([coluna, antigo, novo])

    print(f"Backup incremental criado em {arquivo_backup}.")

# Função para conectar ao banco de dados 
def anonimizar(coluna, quantidade, mascara, simulacao, backup_arquivo, arquivo_csv=None, csv_coluna=None):
    connection = None  # Inicializando a variável connection como None
    cursor = None  # Inicializando a variável cursor

    try:
        if arquivo_csv:
            # Lendo o arquivo CSV
            print(f"Lendo o arquivo CSV: {arquivo_csv}")
            with open(arquivo_csv, mode='r', newline='') as file:
                reader = csv.DictReader(file, delimiter=';')  # Usando o delimitador correto
                colunas = reader.fieldnames

                if csv_coluna not in colunas:
                    print(f"Erro: A coluna '{csv_coluna}' não foi encontrada no arquivo CSV.")
                    return

                registros_anteriores = []
                registros_atualizados = []
                linhas_modificadas = []  # Lista para armazenar as linhas modificadas

                # Processar as linhas do CSV
                for row in reader:
                    valor_original = row[csv_coluna]
                    if valor_original is not None and len(valor_original) > quantidade:
                        nova_string = valor_original[:-quantidade] + mascara * quantidade
                        print(f"Alteração proposta: '{valor_original}' será substituído por '{nova_string}'")

                        if not simulacao:
                            # Atualizando o valor no CSV
                            row[csv_coluna] = nova_string

                            # Adicionando os valores anteriores e os novos para backup
                            registros_anteriores.append(valor_original)
                            registros_atualizados.append(nova_string)

                    # Adicionando a linha (modificada ou não) à lista
                    linhas_modificadas.append(row)

                # Caso esteja em modo de simulação ou se não quiser atualizar os dados no arquivo original
                if not simulacao:
                    # Reescrevendo o arquivo com as modificações
                    with open(arquivo_csv, mode='w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=colunas, delimiter=';')
                        writer.writeheader()
                        writer.writerows(linhas_modificadas)
                    print(f"Arquivo CSV atualizado com sucesso em {arquivo_csv}.")
                
                if backup_arquivo:
                    criar_backup_incremental(csv_coluna, registros_anteriores, registros_atualizados, backup_arquivo)
            
            return

        # Caso o arquivo .CSV não seja fornecido, o processo segue para banco de dados MySQL
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        if connection.is_connected():
            print("Conexão bem-sucedida ao banco de dados MySQL.")
            
            # Criando um cursor para executar comandos SQL
            cursor = connection.cursor()
            
            # Extraindo nome do banco, tabela e coluna
            parts = coluna.split('.')
            if len(parts) != 3:
                print("Erro: O formato da coluna deve ser 'database.tabela.coluna'")
                return
            
            db, tabela, coluna_nome = parts
            
            # Comando para selecionar os dados da coluna especificada
            select_query = f"SELECT {coluna_nome} FROM {db}.{tabela}"
            cursor.execute(select_query)
            
            # Recuperando e exibindo os dados da coluna
            registros = cursor.fetchall()

            registros_anteriores = []
            registros_atualizados = []
            
            for registro in registros:
                valor_original = registro[0]
                if valor_original is not None and len(valor_original) > quantidade:
                    # Substituindo caracteres a partir do final pelo caractere da máscara
                    nova_string = valor_original[:-quantidade] + mascara * quantidade
                    print(f"Alteração proposta: '{valor_original}' será substituído por '{nova_string}'")
                    
                    # Se não for simulação, realiza a atualização na tabela
                    if not simulacao:
                        # Atualizando o valor na tabela
                        update_query = f"UPDATE {db}.{tabela} SET {coluna_nome} = %s WHERE {coluna_nome} = %s"
                        cursor.execute(update_query, (nova_string, valor_original))
                        
                        # Adicionando os valores anteriores e os novos para backup
                        registros_anteriores.append(valor_original)
                        registros_atualizados.append(nova_string)
            
            # Se o modo de simulação não foi ativado, faz o commit e cria o backup incremental
            if not simulacao:
                connection.commit()
                print(f"A substituição foi realizada com sucesso na coluna {coluna_nome} da tabela {tabela}.")
                
                if backup_arquivo:
                    criar_backup_incremental(coluna_nome, registros_anteriores, registros_atualizados, backup_arquivo)
            else:
                print("Modo de simulação ativado. Nenhuma alteração foi feita.")

    except mysql.connector.Error as err:
        print(f"Erro ao executar o script SQL: {err}")
        
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    
    finally:
        if cursor:
            cursor.close()
        
        if connection and connection.is_connected():
            connection.close()
            print("Conexão fechada.")

# Função principal 
def main():
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Anonimizar dados de uma coluna no MySQL ou CSV.")
    parser.add_argument('-c', '--coluna', type=str, help="A coluna no formato 'database.tabela.coluna'.")
    parser.add_argument('-q', '--quantidade', type=int, required=True, help="A quantidade de caracteres a serem substituídos.")
    parser.add_argument('-m', '--mascara', type=str, required=True, help="O caractere a ser usado na máscara.")
    parser.add_argument('-s', '--simulacao', action='store_true', help="Ativa o modo de simulação (dry run), sem realizar alterações.")
    parser.add_argument('-b', '--backup', type=str, help="Ativa o backup incremental e salva as alterações em um arquivo CSV.")
    parser.add_argument('-csv', '--csv', type=str, help="Caminho para o arquivo CSV a ser anonimizado.")
    parser.add_argument('-csv-coluna', '--csv-coluna', type=str, help="Nome da coluna no arquivo CSV a ser anonimizada.")
    
    # Parse dos argumentos
    args = parser.parse_args()

    if args.csv:
        anonimizar(
            coluna=None, 
            quantidade=args.quantidade, 
            mascara=args.mascara, 
            simulacao=args.simulacao, 
            backup_arquivo=args.backup, 
            arquivo_csv=args.csv, 
            csv_coluna=args.csv_coluna
        )
    else:
        anonimizar(
            coluna=args.coluna, 
            quantidade=args.quantidade, 
            mascara=args.mascara, 
            simulacao=args.simulacao, 
            backup_arquivo=args.backup
        )

# Chama a função main se o script for executado diretamente
if __name__ == "__main__":
    main()

'''
SafeMask
Autor: Gabriel Medeiros https://www.linkedin.com/in/gabriel-medeiros-a90b42260/
GitHub: https://github.com/gabr13lme7eiros
Versão: 1.0
'''
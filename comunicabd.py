import psycopg2
import datetime
from datetime import date

import json, os

import logging

def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)

def init():
    logging.basicConfig(level=logging.DEBUG)
    # Update connection string information
    host = os.environ['JDBC_HOST']
    dbname = os.environ["JDBC_NAME"]
    user = os.environ["JDBC_USER"]
    password = os.environ["JDBC_PASS"]

    sslmode = "require"

    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()

    print("Buscando dados...")

    def query_db(query, args=(), one=False):
        cursor.execute(query, args)
        r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
        return (r[0] if r else None) if one else r

    def date_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    
    #query = query_db("select alias from noticia where removido = false order by id")
    query = query_db("select p.nomeurl as url from produto_valor pv left join produto p on (p.id = pv.idproduto) left join lojista l on (pv.idlojista = l.id) where pv.removido = false and pv.idproduto is not null and p.ativo = true and l.removido = false order by p.nomeurl asc")

    json_union = {}
    data_atual = date.today()
    hoje = f'{data_atual.day}/{data_atual.month}/{data_atual.year}'

    json_union['data_criacao'] = hoje
    json_union['artigos']= query
    
    links = []
    filtro = 'produto'

    #Concatenando URL
    print('lista links!')
    for item in query:
        # if item["url"][0] != "'":
        links.append(f'https://staging.suprevida.com.br/{filtro}/{item["url"]}')

    links.sort()

    links_ordenados = ','.join(str(e) for e in links)
    
    print('Convertendo para json e formatando!')
    result = json.dumps(links_ordenados, default = date_converter, indent=4, ensure_ascii=False)

    # Clean up
    cursor.close()
    conn.close()

    # Create a file in the local data directory to upload and download
    local_file_name = "result.json"

    try:
        with open(local_file_name, "w", encoding="utf-8") as myfile:
            myfile.write(result)
    except Exception as e:
        print(e)
        print(f"falha ao escrever no arquivo:\n\t{local_file_name}!")
        
    return result

if __name__ == "__main__":
    init()
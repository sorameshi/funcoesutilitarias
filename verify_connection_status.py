import psycopg2
import datetime
import urllib.parse


import json, os

import logging
import azure.functions as func

def init():
    logging.basicConfig(level=logging.DEBUG)
    # Update connection string information
    host = os.environ["JDBC_HOST"]
    dbname = os.environ["JDBC_NAME"]
    user = os.environ["JDBC_USER"]
    password = os.environ["JDBC_PASS"]

    
    # DOMAIN = os.environ["DOMAIN"]

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

    print("Carregando produtos...")
    query_produtos_ativos = query_db("SELECT count(*), state FROM pg_stat_activity GROUP BY 2")    
    # ids_produtos=[]
    # print('Populando a lista de ids das categorias principais!')
    # for item in query_produtos_ativos:
    #     ids_produtos.append(item["id"])
        
    print('Concluindo sitemap.txt')
    urls = query_produtos_ativos
    print(f'listagem concluida, resultado em formato lista de strings separado por virgula: \n{urls}')


    
    output = json.dumps(urls, indent=4)
    
    f = open("duplicacoes.txt", "a")
    f.write(str(output))
    f.close()
    
    
    print('\n\n'+output)
    
    # Clean up
    cursor.close()
    conn.close()

    return urls

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if init():
        return func.HttpResponse(json.dumps({'message': init()}), status_code=201, mimetype="application/json")
    else:
        return func.HttpResponse(
            "Algo deu errado!",
            status_code=400, 
            mimetype="application/json"
        )

if __name__ == "__main__":
    init()
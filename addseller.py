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
        
    print("ola");
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
    query_produtos_ativos = query_db("select distinct(idproduto) from produto_valor where idlojista <> 52 and idproduto is not null and idproduto not in(select distinct(idproduto) from produto_valor where idlojista = 52) order by idproduto asc")    
    ids_produtos=[]
    print('Populando a lista de ids a serem inseridos o seller!')
    for item in query_produtos_ativos:
        ids_produtos.append(item['idproduto'])
        
  
    idseller = 52    
    count = query_db('select max(id) from produto_valor')
    qtd = int(count[0]['max'])+1
    
    for idproduto in ids_produtos:        
        
        
        query_add_seller = f"INSERT INTO produto_valor (id, ativo, removido, estoque, estoquecomprometido, precodescontocampanha, precofachada, valor, valordesconto, idproduto, idlojista, skulojista, dtype, vendatipopessoa) VALUES ({qtd}, true, false, 0, 0, 0, 0, 2, 0, {idproduto}, {idseller}, null, 'ProdutoValorETO', 'fisica/juridica')"        
        print("Query da vez: "+query_add_seller)
        query_db(query_add_seller)        
        
        qtd += 1
    
    
    # Clean up
    cursor.close()
    conn.close()

    return True

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
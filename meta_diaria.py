from Configuration.DbConection.queries import dayli_selers_sales_query, dayli_store_sales_query
from Configuration.DbConection.DbConnect import DbConnection
from dotenv import load_dotenv
import time
import os

def meta_batida(vendedor):
    if int(list(vendedor.values())[0]) > int(list(vendedor.values())[1]):
        vendedor['metabatida'] = '✔️'
    else:
        vendedor['metabatida'] = '❌'

def main():
    load_dotenv()    
    db_conn = DbConnection(
        host=os.environ.get('HOST', False), 
        port=os.environ.get('PORT', False), 
        dbname=os.environ.get('DBNAME', False), 
        user=os.environ.get('USER', False), 
        password=os.environ.get('PASSWD', False)
        )

    if not db_conn.connect(): 
        raise db_conn.error

    breno_sales_code = '000054'
    kathleen_sales_code = '000095'
    arthur_sales_code = '000090'
    marcelo_sales_code = '000019'

    breno_goal = 5000
    kathleen_goal = 5000
    arthur_goal = 3750
    marcelo_goal = 5000

    breno_sales = db_conn.sqlquery(dayli_selers_sales_query, (breno_sales_code,))[0]
    kathleen_sales = db_conn.sqlquery(dayli_selers_sales_query, (kathleen_sales_code,))[0]
    arthur_sales = db_conn.sqlquery(dayli_selers_sales_query, (arthur_sales_code,))[0]
    marcelo_sales = db_conn.sqlquery(dayli_selers_sales_query, (marcelo_sales_code,))[0]
    store_sales = db_conn.sqlquery(dayli_store_sales_query)[0]

    if db_conn.error: 
        raise db_conn.error
    
    scores = [
        {'MARCELO': marcelo_sales['total'], 'meta': marcelo_goal},
        {'BRENO': breno_sales['total'], 'meta': breno_goal}, 
        {'ARTHUR': arthur_sales['total'], 'meta': arthur_goal}, 
        {'KATHLEEN': kathleen_sales['total'], 'meta': kathleen_goal}
    ]

    scores.sort(key=lambda score: list(score.values())[0], reverse=True)
    for score in scores:
        meta_batida(score)
    first, second, third, fourth = scores
    
    message = f"""
Atualização:
1° {list(first.keys())[0]} Atual: R${int(list(first.values())[0])} Meta: R${int(list(first.values())[1])} {list(first.values())[2]}\n
2° {list(second.keys())[0]} Atual: R${int(list(second.values())[0])} Meta: R${int(list(second.values())[1])} {list(second.values())[2]}\n
3° {list(third.keys())[0]} Atual: R${int(list(third.values())[0])} Meta: R${int(list(third.values())[1])} {list(third.values())[2]}\n
4° {list(fourth.keys())[0]} Atual: R${int(list(fourth.values())[0])} Meta: R${int(list(fourth.values())[1])} {list(fourth.values())[2]}\n
Loja {float(store_sales['total']):.2f} unidades
    """


    with open('resultado_dia.txt', 'w+', encoding='utf-8') as txt:
        txt.write(message)
    
if __name__ == '__main__':
    while True:
        main()
        time.sleep(30)
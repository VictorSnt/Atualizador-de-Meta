from Configuration.DbConection.queries import selers_sales_query, store_sales_query
from Configuration.DbConection.DbConnect import DbConnection
from dotenv import load_dotenv
import time
import os


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

    breno_sales = db_conn.sqlquery(selers_sales_query, (breno_sales_code,))[0]
    kathleen_sales = db_conn.sqlquery(selers_sales_query, (kathleen_sales_code,))[0]
    arthur_sales = db_conn.sqlquery(selers_sales_query, (arthur_sales_code,))[0]
    marcelo_sales = db_conn.sqlquery(selers_sales_query, (marcelo_sales_code,))[0]
    store_sales = db_conn.sqlquery(store_sales_query)[0]

    if db_conn.error: 
        raise db_conn.error
    
    scores = [
        {'MARCELO': marcelo_sales['total']},
        {'BRENO': breno_sales['total']}, 
        {'ARTHUR': arthur_sales['total']}, 
        {'KATHLEEN': kathleen_sales['total']}
    ]

    scores.sort(key=lambda score: list(score.values())[0], reverse=True)
    first, second, third, fourth = scores
    message = f"""
Atualização:

1° {list(first.keys())[0]} {int(list(first.values())[0])} und 🥇= R${float(list(first.values())[0]) * 0.15:.2f}
2° {list(second.keys())[0]} {int(list(second.values())[0])} und 🥈= R${float(list(second.values())[0]) * 0.15:.2f}
3° {list(third.keys())[0]} {int(list(third.values())[0])} und 🥉= R${float(list(third.values())[0]) * 0.15:.2f}
4° {list(fourth.keys())[0]} {int(list(fourth.values())[0])} und = R${float(list(fourth.values())[0]) * 0.15:.2f}
Loja {float(store_sales['total']):.2f} 
    """


    with open('resultado_cimento.txt', 'w+', encoding='utf-8') as txt:
        txt.write(message)
    
if __name__ == '__main__':
    while True:
        main()
        time.sleep(30)
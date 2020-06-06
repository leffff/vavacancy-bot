import psycopg2
import json

# считываем конфиг
with open('config.json') as f:
    config = json.loads(f.read())
    PASSWORD = config["PASSWORD"]
    DBNAME = config["DBNAME"]
    USER = config["USER"]
    HOST = config["HOST"]
    PORT = config["PORT"]
# Первое создание базы данных
'''
Первое создание базы данных.
return {"result": "ok"}
return {"result": "database already exists"}
return {"result": "unknown error"}
'''


def first_db_creation():
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER,
                              password=PASSWORD, host=HOST, port=PORT) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE TABLE users ("
                               "user_id SERIAL PRIMARY KEY NOT NULL, "
                               "tg_nickname VARCHAR(30) NOT NULL UNIQUE, "
                               "name VARCHAR(30) NOT NULL, "
                               "surname VARCHAR(30) NOT NULL, "
                               "qualification text NOT NULL, "
                               "experience INT NOT NULL, "
                               "qualities text NOT NULL,"
                               "city VARCHAR(30) NOT NULL);")
                cursor.execute("CREATE TABLE orders ("
                               "order_id SERIAL PRIMARY KEY NOT NULL, "
                               "employer_id SERIAL REFERENCES users(user_id) NOT NULL,"
                               "worker_id SERIAL REFERENCES users(user_id),"
                               "title VARCHAR(40) NOT NULL, "
                               "description TEXT NOT NULL, "
                               "payment REAL NOT NULL, "
                               "active BOOLEAN DEFAULT True NOT NULL, "
                               "done BOOLEAN DEFAULT False NOT NULL, "
                               "start_time INT,"
                               "finish_time INT,"
                               "mark INT,"
                               "feedback TEXT,"
                               "cancellation VARCHAR(30),"
                               "result INT,"
                               "active_orders INT)")
    except Exception as ex:
        return {"status": f"unknown error: {ex.args[0]}"}
    else:
        return {"status": "ok"}
    finally:
        conn.close()
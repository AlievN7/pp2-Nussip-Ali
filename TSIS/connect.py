import psycopg2
from config import load_config

# Подключение к БД, параметры из database.ini

def connect():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)
        return None

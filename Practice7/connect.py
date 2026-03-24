import psycopg2
from config import load_config

def connect(config):
    """Connect to the PostgreSQL database server using psycopg v3"""
    try:
        conn = psycopg2.connect(
            host=config['host'],
            dbname=config['database'],  
            user=config['user'],
            password=config['password'],
            port=config.get('port', 5432)
        )
        print('Connected to the PostgreSQL server.')
        return conn
    except Exception as error:  
        print('Connection error:', error)

if __name__ == '__main__':
    config = load_config()
    conn = connect(config)

    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print("PostgreSQL version:", cur.fetchone()[0])
        conn.close()
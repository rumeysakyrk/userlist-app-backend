import psycopg2
import os

# Veritabanı bağlantısı
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return conn
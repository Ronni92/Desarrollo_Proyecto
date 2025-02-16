import psycopg2

# Función para obtener una conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="calendario_db",
        user="postgres",
        password="123456789*",
        host="localhost",
        port="5433"
    )
import os
import psycopg2.pool
import psycopg2.extras

pool = psycopg2.pool.SimpleConnectionPool(
    2,
    3,
    host=os.environ['DB_HOST'],
    database=os.environ['DB'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    port=os.environ['DB_PORT'],
)


# def cursor_factory():
#     return psycopg2.extras.RealDictCursor


# def run_sql(sql_statement):
#     conn = pool.getconn()
#     cursor = conn.cursor(cursor_factory=cursor_factory())
#     cursor.execute(sql_statement)
#     results = cursor.fetchall()
#     release_connection(conn)
#
#     return results


# def get_connection():
#     return pool.getconn()


def get_connection():
    conn = pool.getconn()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return conn, cursor


def release_connection(connection):
    pool.putconn(connection)
import psycopg2.extensions
import psycopg2

conn = psycopg2.connect("host=localhost dbname=rbdm user=m")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE users(
    id integer PRIMARY KEY,
    email text,
    name text,
    address text
)
""")
# DATABASES = {
#     # ...
#     'OPTIONS': {
#         'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
#     },
# }
# one = cur.fetchone()
# all = cur.fetchall()

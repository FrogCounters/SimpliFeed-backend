import os
import psycopg2

# If using database from Render
if os.environ.get('DATABASE_URL'):
    postgres_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(postgres_url, sslmode='require')
# If using local database
else:
    conn = psycopg2.connect("dbname=fintechmonth "
                            "port=5433 "
                            "user=postgres "
                            "password=admin")
conn.autocommit = True
db = conn.cursor()

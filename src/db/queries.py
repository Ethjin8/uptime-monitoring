import psycopg    # library connecting Python to Postgres
from psycopg.rows import dict_row   # labels each row value and returns it as a dictionary

# default user -> postgres; default database name -> postgres
DB_URL = "postgresql://postgres:dev@localhost:5435/postgres"

def list_targets():
  # row_factory -> setting on the connection that says dict_row should build every row
  with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
    rows = conn.execute("SELECT id, url, owner_label FROM targets ORDER BY id").fetchall()

  return rows

print(list_targets())
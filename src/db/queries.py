import psycopg    # library connecting Python to Postgres
from psycopg.rows import dict_row   # labels each row value and returns it as a dictionary

# default user -> postgres; default database name -> postgres
DB_URL = "postgresql://postgres:dev@localhost:5435/postgres"

def list_targets():
  # row_factory -> setting on the connection that says dict_row should build every row
  with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
    rows = conn.execute("SELECT id, url, owner_label FROM targets ORDER BY id").fetchall()

  return rows

def save_result(target_id, probe_info):
  status_code = probe_info["status_code"]
  latency_ms = probe_info["latency_ms"]
  error = probe_info["error"]

  with psycopg.connect(DB_URL) as conn:
    conn.execute(
      # use a parameterized SQL query so the values are treated as inserted data, rather than direct code (prevents SQL injection)
      "INSERT INTO probe_results (target_id, status_code, latency_ms, error) VALUES (%s, %s, %s, %s)",    
      (target_id, status_code, latency_ms, error)
    )
    
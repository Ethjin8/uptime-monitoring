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


def fetch_probe_results():
  """
  Query to fetch information from the most recent probe to a target website
  """

  with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
    return conn.execute("""
        SELECT DISTINCT ON (probe_results.target_id) targets.owner_label, targets.id, targets.url, probe_results.status_code, probe_results.latency_ms, probe_results.error
        FROM probe_results
        JOIN targets ON targets.id = probe_results.target_id
        ORDER BY probe_results.target_id DESC, probe_results.probed_at DESC
    """).fetchall()


def fetch_uptime_24h():
  """
  Query to gather 24-hour uptime percentage
  """
  with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
    rows = conn.execute("""
      SELECT target_id,
        COUNT(*) AS total_probes,
        COUNT(*) FILTER (WHERE status_code BETWEEN 200 and 299) AS successful_probes
      FROM probe_results
      WHERE probed_at > now() - interval '24 hours'
      GROUP BY target_id
    """).fetchall()

  uptime_24h = {}
  for row in rows:
    uptime_percentage = row["successful_probes"] / row["total_probes"] * 100
    uptime_24h[row["target_id"]] = round(uptime_percentage, 1)

  return uptime_24h


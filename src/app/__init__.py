from flask import Flask, render_template, abort
app = Flask(__name__)


status_table = [
  {
    "id": 1234,
    "owner": "user",
    "status": "DOWN",
    "uptime_24h": 85,
    "p95_ms": 100,
  },
  {
    "id": 2345,
    "owner": "user",
    "status": "DOWN",
    "uptime_24h": 85,
    "p95_ms": 100,
  },
  {
    "id": 3456,
    "owner": "user",
    "status": "DOWN",
    "uptime_24h": 85,
    "p95_ms": 100,
  },
]


@app.route("/")
@app.route("/home")
def index():
  return render_template('index.html', status_table=status_table)

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/site/<int:site_id>")
def site(site_id):
  row = next((r for r in status_table if r["id"] == site_id), None)
  if row is None:
    abort(404)
  return render_template('site.html', site=row)
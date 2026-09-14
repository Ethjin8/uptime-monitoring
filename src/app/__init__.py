from flask import Flask, render_template
app = Flask(__name__)


status_table = [
  {
    "owner": "user",
    "status": "DOWN",
    "uptime_24h": 85,
    "p95_ms": 100,
  },
  {
    "owner": "user",
    "status": "DOWN",
    "uptime_24h": 85,
    "p95_ms": 100,
  },
  {
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
from flask import Flask, render_template, abort
from db.queries import fetch_probe_results
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
  status_table = fetch_probe_results()
  return render_template('index.html', status_table=status_table)

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/site/<int:site_id>")
def site(site_id):
  status_table = fetch_probe_results()    # temporary fix for now
  
  row = next((r for r in status_table if r["id"] == site_id), None)
  if row is None:
    abort(404)
  return render_template('site.html', site=row)
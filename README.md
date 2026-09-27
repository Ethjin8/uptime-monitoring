# Argus — An Uptime Monitoring Service

A lightweight monitoring application to help you track your website's status, with visualizations and notification-based alerts.

## Running Locally

The database runs in Docker. The Flask app currently runs directly on your machine via `uv`.

**Prerequisites:** [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python packages, and [Docker Desktop](https://docs.docker.com/desktop/) for the database.

### 1. Clone the repo

```bash
git clone https://github.com/Ethjin8/uptime-monitoring.git
cd uptime-monitoring
uv sync
```

### 2. Start the database

First time only — this creates the container and the `argus-data` volume where the data actually lives:

```bash
docker run --name argus-database -d \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  -v argus-data:/var/lib/postgresql \
  postgres:18
```

Every time after that, just switch it back on:

```bash
docker start argus-database
```

To open a SQL prompt (password `dev`):

```bash
docker exec -it argus-database psql -U postgres
```

The container is disposable; `argus-data` is not. You can delete and recreate the container without losing your tables.

### 3. Run the web app

```bash
PYTHONPATH=src uv run flask --app app run --debug --port 5055
```

Then open <http://127.0.0.1:5055>. `--debug` reloads the app automatically when you edit a file.

### Troubleshooting

- **`port 5432 already in use`** — another Postgres is running on your machine. Stop it, or change `-p 5432:5432` to `-p 5433:5432`.
- **Port 5055 already in use** — pass any other port to `--port`.
- **`Could not locate a Flask application`** — `PYTHONPATH=src` is missing. There is no `app.py`; the app lives in `src/app/__init__.py`.


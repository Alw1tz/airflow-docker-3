# Apache Airflow 3.0.6 Docker Setup with Snowflake

Production-ready Apache Airflow 3.0.6 setup using Docker Compose with LocalExecutor and Snowflake integration.

## Prerequisites

- **Docker Desktop** (with at least 4GB memory allocated, 8GB recommended)
- **Docker Compose** v2.14.0 or newer
- **Snowflake account** (optional, for Snowflake integration)

### Check Docker Resources

Ensure Docker has enough resources:
- **Memory**: At least 4GB (8GB recommended)
- **CPUs**: At least 2

On Docker Desktop: Settings > Resources > Advanced

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/airflow-docker-3.git
cd airflow-docker-3
```

### 2. Initialize Environment (Linux/Mac only)

```bash
# Set your user ID (Linux only - Windows users skip this)
echo "AIRFLOW_UID=$(id -u)" >> .env
```

### 3. Build and Start Airflow

```bash
# Build the custom image with Snowflake provider
docker compose build

# Start all services (init runs automatically)
docker compose up -d
```

### 4. Access Airflow

Wait about 1 minute for initialization, then open your browser:

- **Airflow UI**: http://localhost:8080
- **Username**: `airflow`
- **Password**: `airflow`

## Configure Snowflake Connection

1. Go to **Admin** > **Connections** > **+** (Add a new record)

2. Fill in the connection details:

| Field | Value |
|-------|-------|
| Connection Id | `conn_id_snowflake` |
| Connection Type | `Snowflake` |
| Account | `your-account-identifier` (e.g., `abc12345` - NO region needed) |
| Login | `your_username` |
| Password | `your_password` |
| Schema | `PUBLIC` |

3. Add **Extra** (JSON format):

```json
{
  "warehouse": "COMPUTE_WH",
  "database": "YOUR_DATABASE",
  "role": "SYSADMIN"
}
```

4. Click **Save**

**Important**: For the Account field, use only your account identifier (e.g., `xjasplf-dfb59392`). Do NOT include the region or `.snowflakecomputing.com` - Snowflake routes automatically.

### Test the Connection

1. Find the `test_snowflake_connection` DAG in the DAGs list
2. Toggle the DAG ON
3. Click the play button to trigger a run
4. Check the logs to verify the connection works

## Project Structure

```
airflow-docker-3/
├── docker-compose.yaml     # Main Docker Compose configuration
├── Dockerfile              # Custom image with Snowflake provider
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── dags/                   # Your DAG files go here
│   ├── test_snowflake.py   # Snowflake test DAG
│   └── simple_test.py      # Simple test DAG
├── logs/                   # Task execution logs (auto-generated)
├── plugins/                # Custom Airflow plugins
└── config/                 # Custom Airflow configuration (auto-generated)
```

## Services Overview

| Service | Description | Port |
|---------|-------------|------|
| airflow-apiserver | Web UI and REST API | 8080 |
| airflow-scheduler | Monitors and triggers tasks | - |
| airflow-dag-processor | Parses DAG files | - |
| airflow-triggerer | Handles deferrable tasks | - |
| postgres | Metadata database | - |

This setup uses **LocalExecutor** (no Redis/Celery needed) for simpler deployment.

## Useful Commands

### Start/Stop Services

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f airflow-scheduler
docker compose logs -f airflow-apiserver
```

### Access Container Shell

```bash
# Access the scheduler container
docker compose exec airflow-scheduler bash

# Run Airflow CLI commands
docker compose exec airflow-scheduler airflow dags list
docker compose exec airflow-scheduler airflow tasks list test_snowflake_connection
```

### Rebuild After Changes

```bash
# Rebuild image after Dockerfile/requirements.txt changes
docker compose build --no-cache

# Rebuild and restart
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

## Adding New DAGs

1. Create your Python DAG file in the `dags/` directory
2. Airflow will automatically detect and load it within a few seconds
3. Refresh the Airflow UI to see your new DAG

Example minimal DAG:

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def my_task():
    print("Hello from Airflow!")

with DAG(
    'my_first_dag',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id='hello_task',
        python_callable=my_task,
    )
```

## Troubleshooting

### "Not enough memory"

Increase Docker Desktop memory allocation to at least 4GB (8GB recommended).

### Port 8080 already in use

Change the port in `docker-compose.yaml`:
```yaml
ports:
  - "8081:8080"  # Use port 8081 instead
```

### "Incorrect username or password" (Snowflake)

- Use account identifier only (e.g., `abc12345`), NOT the full URL
- Do NOT include region in the account field
- Ensure the role has appropriate permissions

### SSL Certificate Error (Snowflake)

If you see "hostname doesn't match certificate":
- Remove any region from the Account field
- Use just the account identifier (e.g., `xjasplf-dfb59392`)

### DAGs not appearing

1. Check for syntax errors: `docker compose exec airflow-scheduler python /opt/airflow/dags/your_dag.py`
2. View DAG processor logs: `docker compose logs airflow-dag-processor`
3. Ensure the file has `.py` extension

### Tasks fail with "Connection refused" or no logs

This usually means internal API communication issues. Ensure all services are healthy:
```bash
docker compose ps
```

If services keep restarting, check the logs and do a fresh start:
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker compose down -v

# Remove built images (optional)
docker compose down --rmi local -v

# Start fresh
docker compose build --no-cache
docker compose up -d
```

## Environment Variables

Key variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `AIRFLOW_UID` | User ID for file permissions | `50000` |
| `_AIRFLOW_WWW_USER_USERNAME` | Admin username | `airflow` |
| `_AIRFLOW_WWW_USER_PASSWORD` | Admin password | `airflow` |

## Configuration Details

This setup uses:
- **Airflow 3.0.6** - Stable version
- **LocalExecutor** - Simple, no Redis/Celery required
- **FAB Auth Manager** - Traditional Flask-AppBuilder authentication
- **PostgreSQL 13** - Metadata database

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Snowflake Provider Documentation](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html)
- [Docker Hub - Apache Airflow](https://hub.docker.com/r/apache/airflow)

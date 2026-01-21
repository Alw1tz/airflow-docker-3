# Apache Airflow 3.1.6 Docker Setup with Snowflake

Production-ready Apache Airflow 3.1.6 setup using Docker Compose with Snowflake integration.

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

### 2. Initialize Environment (Linux/Mac)

```bash
# Set your user ID (Linux only)
echo "AIRFLOW_UID=$(id -u)" >> .env
```

### 3. Build and Start Airflow

```bash
# Build the custom image with Snowflake provider
docker compose build

# Initialize the database and create admin user
docker compose up airflow-init

# Start all services in detached mode
docker compose up -d
```

### 4. Access Airflow

Open your browser and navigate to:

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
| Host | `your-account.region.snowflakecomputing.com` |
| Login | `your_username` |
| Password | `your_password` |
| Schema | `PUBLIC` |

3. Add **Extra** (JSON format):

```json
{
  "account": "your_account_id",
  "warehouse": "your_warehouse",
  "database": "your_database",
  "role": "your_role"
}
```

4. Click **Save**

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
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── dags/                   # Your DAG files go here
│   └── test_snowflake.py   # Example Snowflake test DAG
├── logs/                   # Task execution logs (auto-generated)
├── plugins/                # Custom Airflow plugins
└── config/                 # Custom Airflow configuration
```

## Services Overview

| Service | Description | Port |
|---------|-------------|------|
| airflow-api-server | Web UI and REST API | 8080 |
| airflow-scheduler | Monitors and triggers tasks | - |
| airflow-dag-processor | Parses DAG files | - |
| airflow-worker | Executes tasks | - |
| airflow-triggerer | Handles deferrable tasks | - |
| postgres | Metadata database | 5432 |
| redis | Message broker | 6379 |
| flower | Celery monitoring (optional) | 5555 |

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
docker compose logs -f airflow-worker
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
# Rebuild image after Dockerfile changes
docker compose build

# Rebuild and restart
docker compose up -d --build
```

### Enable Flower (Celery Monitoring)

```bash
docker compose --profile flower up -d
# Access at http://localhost:5555
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

- Verify your Snowflake credentials
- Use account ID only, not the full URL
- Ensure the role has appropriate permissions

### "externalbrowser not supported" (Snowflake)

SSO/MFA authentication isn't supported in Docker. Use username/password authentication instead.

### DAGs not appearing

1. Check for syntax errors: `docker compose exec airflow-scheduler python /opt/airflow/dags/your_dag.py`
2. View DAG processor logs: `docker compose logs airflow-dag-processor`
3. Ensure the file has `.py` extension

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker compose down -v

# Remove built images
docker compose down --rmi all -v

# Start fresh
docker compose build
docker compose up airflow-init
docker compose up -d
```

## Environment Variables

Key variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `AIRFLOW_UID` | User ID for file permissions | `50000` |
| `_AIRFLOW_WWW_USER_USERNAME` | Admin username | `airflow` |
| `_AIRFLOW_WWW_USER_PASSWORD` | Admin password | `airflow` |
| `_PIP_ADDITIONAL_REQUIREMENTS` | Extra pip packages | (empty) |

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Snowflake Provider Documentation](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html)
- [Docker Hub - Apache Airflow](https://hub.docker.com/r/apache/airflow)

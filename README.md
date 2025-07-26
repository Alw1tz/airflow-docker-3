# Airflow 3.0 + Snowflake Docker Setup

Quick setup for Apache Airflow 3.0 with Snowflake integration using Docker.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/your-username/airflow-snowflake-setup.git
cd airflow-snowflake-setup

# Build and start
docker-compose build
docker-compose up airflow-init
docker-compose up -d

# Access Airflow at http://localhost:8080
# Username: airflow | Password: airflow
```

## Configure Snowflake Connection

1. Go to **Admin** → **Connections** → **+**
2. Fill in:

```
Connection Id: conn_id_snowflake
Connection Type: Snowflake
Host: your-account.region.snowflakecomputing.com
Login: your_username
Password: your_password
Schema: PUBLIC
```

3. **Extra Fields JSON**:
```json
{
  "account": "your_account_id",
  "warehouse": "your_warehouse", 
  "database": "your_database",
  "role": "your_role"
}
```

## Test Connection

The included DAG `test_snowflake_connection` will automatically appear. Activate and run it to test your Snowflake connection.

## Project Structure

```
├── docker-compose.yaml     # Main Docker configuration
├── Dockerfile              # Custom image with Snowflake provider
├── .env                    # Environment variables
└── dags/
    └── test_snowflake.py   # Example DAG
```

## Useful Commands

```bash
# Stop services
docker-compose down

# View logs
docker-compose logs airflow-scheduler

# Access container
docker exec -it airflow-airflow-scheduler-1 bash
```

## Common Issues

**"Incorrect username or password"**
- Verify your Snowflake credentials
- Use account ID, not full URL

**"externalbrowser not supported"**
- Use username/password instead of SSO in Docker

**Port 8080 in use**
- Change port in `docker-compose.yaml`: `"8081:8080"`

## Requirements

- Docker Desktop
- Snowflake account credentials

---

That's it! Your Airflow 3.0 + Snowflake setup is ready to use.
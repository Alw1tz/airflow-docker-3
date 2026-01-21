# Custom Apache Airflow 3.1.6 Docker Image with Snowflake Provider
FROM apache/airflow:3.1.6

# Switch to root to install system dependencies if needed
USER root

# Install any system dependencies (uncomment if needed)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install Snowflake provider and other useful packages
RUN pip install --no-cache-dir \
    apache-airflow-providers-snowflake \
    snowflake-connector-python[pandas]

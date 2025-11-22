# Use the latest stable Airflow image (currently based on Debian Bookworm)
FROM apache/airflow:latest

# Switch to root to install system dependencies (Java is required for Spark)
USER root

# Install OpenJDK 17 (standard for modern Spark versions) and procps (for process monitoring)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    procps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Switch back to the airflow user to install Python packages
USER airflow

# Install Apache Spark provider and PySpark
# This allows you to run Spark locally within Airflow tasks
RUN pip install --no-cache-dir \
    "apache-airflow-providers-apache-spark" \
    "pyspark" \
    "openmeteo-requests" \
    "requests-cache"
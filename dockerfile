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

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow-providers-apache-spark" \
    "pyspark" \
    "openmeteo-requests" \
    "requests-cache" \
    "urllib3==1.26.18" \
    "pipdeptree"
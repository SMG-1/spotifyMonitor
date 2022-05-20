# syntax=docker/dockerfile:1

FROM apache/airflow:2.3.0
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
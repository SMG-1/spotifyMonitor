import json
from datetime import datetime, timedelta

from pipeline import top_tracks_to_df, top_artists_to_df

from airflow import DAG
from airflow.contrib.operators.emr_add_steps_operator import (
    EmrAddStepsOperator,
)
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator

# DAG definition
default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime(2021, 5, 23),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "user_behaviour",
    default_args=default_args,
    schedule_interval="*/2 * * * *",
    max_active_runs=1,
)

pull_tracks_save_df = PythonOperator(
    dag=dag,
    task_id="pull_tracks_save_df",
    python_callable=top_tracks_to_df,
    op_kwargs={
        "limit": 50,
        "time_range": 'short_term'
    },
)

pull_artists_save_df = PythonOperator(
    dag=dag,
    task_id="pull_artists_save_df",
    python_callable=top_artists_to_df,
    op_kwargs={
        "limit": 50,
        "time_range": 'short_term'
    }
)

(
    pull_tracks_save_df >> pull_artists_save_df
)


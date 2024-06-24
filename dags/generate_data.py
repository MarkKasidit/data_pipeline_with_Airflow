from airflow import DAG
from datetime import datetime
import os
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator

with DAG (
    dag_id = "generate_data",
    start_date = datetime(2024, 1, 1),
    schedule_interval = "@daily",
    catchup = False
):
    start = DummyOperator(task_id="start")
    run_sampledata_script = BashOperator(task_id="run_sampledata_script", 
                                         bash_command="python /opt/airflow/sampledata_new.py") 
    end = DummyOperator(task_id="end")


    start >> run_sampledata_script >> end


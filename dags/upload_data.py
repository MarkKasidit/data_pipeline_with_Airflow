from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
import os
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import pandas as pd
import logging

# Function to upload Parquet data to PostgreSQL
def upload_parquet_to_postgres(parquet_folder, postgres_conn_id, batch_size=1440):

    parquet_files = [os.path.join(parquet_folder, f) for f in os.listdir(parquet_folder) if f.endswith('.parquet')]
    engine = create_engine(postgres_conn_id)
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Process files in batches
    for i in range(0, len(parquet_files), batch_size):
        batch_files = parquet_files[i:i+batch_size]

        for parquet_file in batch_files:
            table = pq.ParquetFile(parquet_file)
            table_name = "master"  # Define your target table name

            # Process each file
            df = table.read().to_pandas()
            df = df.drop_duplicates()

            # Save to temporary CSV file
            temp_csv = '/tmp/temp_data.csv'
            df.to_csv(temp_csv, index=False)

            # Bulk insert using COPY command
            copy_sql = f"""
                COPY {table_name} FROM STDIN WITH CSV HEADER
                DELIMITER AS ','
            """
            with open(temp_csv, 'r') as f:
                cursor.copy_expert(sql=copy_sql, file=f)
            
            os.remove(temp_csv)  # Remove the temporary CSV file after loading
        logging.info(f"Uploaded batch {i//batch_size + 1} to master table")

    conn.commit()
    cursor.close()
    conn.close()
    engine.dispose()
        

with DAG (
    dag_id = "upload_data",
    start_date = datetime(2024, 1, 1),
    schedule_interval = "@daily",
    catchup = False
):
    start = DummyOperator(task_id="start")
    create_table = PostgresOperator(
        task_id="create_table", 
        postgres_conn_id="postgres_local",
        sql = '''
            CREATE TABLE if not exists master(
            department_name varchar(128),
            sensor_serial varchar(128),
            create_at date,
            product_name varchar(128),
            product_expire date
            )
        '''
    ) 
    load_to_master = PythonOperator(
        task_id="load_to_master",
        python_callable=upload_parquet_to_postgres,
        op_kwargs={
        'parquet_folder': '/opt/airflow/data_sample',
        'postgres_conn_id': 'postgresql://postgres:mypostgres@host.docker.internal:5432/postgres',
        'batch_size': 1440
    }
    )
    end = DummyOperator(task_id="end")


    start >> create_table >> load_to_master >> end


# Create a data pipeline for uploading Parquet Data to PostgreSQL using Airflow

<p>This project contains an Apache Airflow DAG for uploading Parquet data from a local folder to a PostgreSQL database. The DAG reads Parquet files in batches, combines the data, removes duplicates, and uploads the data to a specified PostgreSQL table.</p>

## Prerequisites
- Python
- Docker
- Docker Compose
- Apache Airflow
- PostgreSQL

## Initial step: Generate parquet data
<ol>
  <li><strong>Setup virtual environment for the project</strong></li>
      
      pip install venv
      python -m venv [venv_name]
      [venv_name]\Scripts\activate
      
  <li><strong>Generate the data</strong></li>

      pip install -r requirements.txt
      python sampledata_new.py
      
</ol>

## Setup Apache Airflow with Docker
<ol>
  <li><strong>Download docker-compose.yml</strong></li>
    <p> The provided file is the version used in the project. If you want to build from scratch, you can run the script below: </p> 

    curl -LfO https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml

  <li><strong>Prepare the workplace</strong></li>
    <p> Create <strong>logs</strong> folder for contains logs from task execution and scheduler, and <strong>plugins</strong> folder for the custom plugins</p>

    mkdir -p ./logs ./plugins

  <li><strong>Start docker-compose</strong></li>

    docker-compose up -d

# Create a data pipeline for uploading Parquet Data to PostgreSQL using Airflow

<p>This project contains an Apache Airflow DAG for uploading Parquet data from a local folder to a PostgreSQL database. The DAG reads Parquet files in batches, combines the data, removes duplicates, and uploads the data to a specified PostgreSQL table.</p>

## Prerequisites
- Python
- Docker
- Docker Compose
- Apache Airflow
- PostgreSQL

## Initial step: Prepare data
<ol>
  <li><strong>Setup virtual environment for the project</strong></li>
      
      pip install venv
      python -m venv [venv_name]
      [venv_name]\Scripts\activate
      
  <li><strong>Generate data</strong></li>

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

</ol>

## Usage
<ol>
  <li><strong>Access Airflow Web UI</strong></li>
    <p>Open your browser and go to http://localhost:8080. Use the default credentials (username: airflow, password: airflow) to log in.</p>

  <li><strong>Trigger the DAG</strong></li>
    <p>Find the <strong>upload_data</strong> DAG and toggle it to "On".</p>
</ol>


## (Optional) Install python requirements via extending airflow docker image
<p> This step occur due to the need to run <strong>sampledata_new.py</strong> via Airflow.</p>
  <ol>
    <li><strong>Create Dockerfile</strong></li>
      <p> For this project, I build the Dockerfile as the script below </p>

        FROM apache/airflow:2.5.1-python3.8
        USER airflow
        COPY requirements.txt .
        RUN pip install --upgrade pip
        RUN pip install --no-cache-dir -r requirements.txt
        
  <li><strong>Build Docker Image from Dockerfile</strong></li>

      docker build . --tag extending_airflow:latest

  <li><strong>Change Airflow Image</strong></li>
    <p>Open <strong>docker-compose.yaml</strong> and change the Airflow Image to <strong>extending_airflow:latest</strong></p>
</ol>
      

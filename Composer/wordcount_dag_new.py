from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from datetime import datetime

default_args = {
    'owner': 'flopeza',
    'start_date': datetime(2026, 4, 8),
    'retries': 1
}

with DAG(
    dag_id='wordcount_dataflow',
    default_args=default_args,
    description='Ejecutar job de Dataflow desde template',
    schedule='@hourly',
    catchup=False
) as dag:

    dataflow_task = DataflowTemplatedJobStartOperator(
        task_id='ejecutar_wordcount',
        template='gs://flopeza-composer-demo/templates/wordcount_template',
        location='us-central1',
        project_id='flopeza-demo-composer',

        parameters={
    "input": "gs://dataflow-samples/shakespeare/kinglear.txt",
    "output": "gs://flopeza-composer-demo/wordcount/{{ ts_nodash }}/result",
    "temp_location": "gs://flopeza-composer-demo/temp"
}
    )
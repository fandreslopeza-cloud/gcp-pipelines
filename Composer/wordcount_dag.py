from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from datetime import datetime

#DAG
default_args = {
    'owner': 'flopeza',
    'start_date': datetime(2026,4,7),
    'retries': 1
}

dag = DAG(
    'wordcount_dataflow',
    default_args = default_args,
    description = 'Ejecutar job de Dataflow desde template',
    schedule_interval = None,
    catchup = False
)

dataflow_task = DataflowTemplatedJobStartOperator(
    task_id = 'ejecutar_wordcount',
    template = 'gs://flopeza-composer-demo/templates/wordcount_template',
    location = 'us-central1',
    project_id = 'flopeza-demo-composer',
    dag=dag
)
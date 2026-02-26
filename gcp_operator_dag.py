import pendulum
from airflow.models import Variable
from airflow.sdk import DAG, task
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator

default_args = dict(
    owner = 'jaeminjjung',
    email = ['jaeminjjung@gmail.com'],
    email_on_failure = False,
    retries = 3
    )

with DAG(
    dag_id="gcp_operator_dag",
    start_date=pendulum.datetime(2026, 1, 1, tz='Asia/Seoul'),
    schedule="30 10 * * *", # cron 표현식
    tags = [''],
    default_args = default_args,
    catchup=False
):  
    list_objects = GCSListObjectsOperator(
        task_id='list_objects',
        gcp_conn_id='gcp_conn',
        bucket='bonaventura',  
        prefix='source'        
    )    


list_objects 
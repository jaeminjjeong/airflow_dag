import pendulum
from airflow.sdk import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator


default_args = dict(
    owner = 'hyunsoo',
    email = ['hyunsoo@airflow.com'],
    email_on_failure = False,
    retries = 3
    )

with DAG(
    dag_id="18_bigquery_job_dag",
    start_date=pendulum.datetime(2025, 6, 1, tz='Asia/Seoul'),
    schedule="30 10 * * *", # cron 표현식
    tags = ['20250726'],
    default_args = default_args,
    catchup=False
):  
    # trainer 테이블에서 레벨이 'Advanced' 인 것들만 추출!
    SQL_QUERY = """
    CREATE TABLE bq_dataset.adv_trainer AS
    SELECT * FROM bq_dataset.trainer WHERE achievement_level='Advanced'
    """
    bq_job = BigQueryInsertJobOperator(
        task_id='bq_job',
        gcp_conn_id='gcp_connection',
        project_id=Variable.get('PROJECT_ID'), # GCP PROJECT ID
        location=Variable.get('LOCATION'),
        configuration={
            "query": {
                "query": SQL_QUERY,
                "useLegacySql": False,
                "priority": "BATCH",
            }
        }
    )
    
    bq_job
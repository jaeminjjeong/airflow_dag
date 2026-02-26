import pendulum
import pandas as pd
from airflow.sdk import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

"""
빅쿼리 dataset 생성, table 생성!
"""

default_args = dict(
    owner = 'codeit',
    email = ['codeit@airflow.com'],
    email_on_failure = False,
    retries = 3
    )

with DAG(
    dag_id="bigquery_operator_dag",
    start_date=pendulum.datetime(2025, 6, 1, tz='Asia/Seoul'),
    schedule="30 10 * * *", # cron 표현식
    tags = ['20250726'],
    default_args = default_args,
    catchup=False
):  
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_dataset',
        gcp_conn_id='gcp_connection', # gcp에 대한 airflow connection
        project_id=Variable.get('PROJECT_ID'), # GCP PROJECT ID
        dataset_id='airflow', # 생성할 dataset 이름
        location=Variable.get('LOCATION'),
        if_exists='ignore'
    )
    
    bigquery_hook = BigQueryHook(
        gcp_conn_id='gcp_connection',
        location=Variable.get('LOCATION')
    ).get_sqlalchemy_engine()
    
    # bigquery에서 trainer 테이블 읽어오기
    @task(task_id='read_bigquery_data')
    def read_bigquery_data():
        df = pd.read_sql_table(
            table_name='bq_dataset.trainer',
            con=bigquery_hook
        )
        return df
    
    # achievement_level = Advanced 인 것만 필터링!
    @task(task_id='transform')
    def transform(df):
        
        tdf = df[df['achievement_level'] == 'Advanced']
        return tdf
    
    # 필터링 된 dataframe을 bigquery에 저장!
    @task(task_id='load_to_bigquery')
    def load_to_bigquery(df):
    
        df.to_sql(
            name='bq_dataset.adv_trainer',
            con=bigquery_hook,
            if_exists='replace'
        )
        
    df = read_bigquery_data()
    tdf = transform(df)
    load_to_bigquery(tdf)
    
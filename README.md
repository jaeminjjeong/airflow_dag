# airflow_dag
Automation of airflow script - airflow + Google cloud storage bucket + BigQuery

## GCP storage:
#### https://console.cloud.google.com/storage/browser/bonaventura

## Documentation
Google Cloud Storage Transfer Operator to BigQuery¶
Google Cloud Storage (GCS) is a managed service for storing unstructured data. Google Cloud BigQuery is Google Cloud’s serverless data warehouse offering. This operator can be used to populate BigQuery tables with data from files stored in a Cloud Storage bucket.

Prerequisite Tasks¶
To use these operators, you must do a few things:

Select or create a Cloud Platform project using the Cloud Console.

Enable billing for your project, as described in the Google Cloud documentation.

Enable the API, as described in the Cloud Console documentation.

Install API libraries via pip.

pip install 'apache-airflow[google]'
Detailed information is available for Installation.

Setup a Google Cloud Connection.

Operator¶
File transfer from GCS to BigQuery is performed with the GCSToBigQueryOperator operator.

Use Jinja templating with bucket, source_objects, schema_object, schema_object_bucket, destination_project_dataset_table, impersonation_chain, src_fmt_configs to define values dynamically.

You may load multiple objects from a single bucket using the source_objects parameter. You may also define a schema, as well as additional settings such as the compression format. For more information, please refer to the links above.

Transferring files¶
The following Operator transfers one or more files from GCS into a BigQuery table.

tests/system/google/cloud/gcs/example_gcs_to_bigquery.py

load_csv = GCSToBigQueryOperator(
    task_id="gcs_to_bigquery_example",
    bucket="cloud-samples-data",
    source_objects=["bigquery/us-states/us-states.csv"],
    destination_project_dataset_table=f"{DATASET_NAME}.{TABLE_NAME}",
    schema_fields=[
        {"name": "name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "post_abbr", "type": "STRING", "mode": "NULLABLE"},
    ],
    write_disposition="WRITE_TRUNCATE",
)
Also you can use GCSToBigQueryOperator in the deferrable mode:

tests/system/google/cloud/gcs/example_gcs_to_bigquery_async.py

load_string_based_csv = GCSToBigQueryOperator(
    task_id="gcs_to_bigquery_example_str_csv_async",
    bucket="cloud-samples-data",
    source_objects=["bigquery/us-states/us-states.csv"],
    destination_project_dataset_table=f"{DATASET_NAME_STR}.{TABLE_NAME_STR}",
    write_disposition="WRITE_TRUNCATE",
    external_table=False,
    autodetect=True,
    max_id_key="string_field_0",
    deferrable=True,
)

load_date_based_csv = GCSToBigQueryOperator(
    task_id="gcs_to_bigquery_example_date_csv_async",
    bucket="cloud-samples-data",
    source_objects=["bigquery/us-states/us-states-by-date.csv"],
    destination_project_dataset_table=f"{DATASET_NAME_DATE}.{TABLE_NAME_DATE}",
    write_disposition="WRITE_TRUNCATE",
    external_table=False,
    autodetect=True,
    max_id_key=MAX_ID_DATE,
    deferrable=True,
)

load_json = GCSToBigQueryOperator(
    task_id="gcs_to_bigquery_example_date_json_async",
    bucket="cloud-samples-data",
    source_objects=["bigquery/us-states/us-states.json"],
    source_format="NEWLINE_DELIMITED_JSON",
    destination_project_dataset_table=f"{DATASET_NAME_JSON}.{TABLE_NAME_JSON}",
    write_disposition="WRITE_TRUNCATE",
    external_table=False,
    autodetect=True,
    max_id_key=MAX_ID_STR,
    deferrable=True,
)

load_csv_delimiter = GCSToBigQueryOperator(
    task_id="gcs_to_bigquery_example_delimiter_async",
    bucket="big-query-samples",
    source_objects=["employees-tabular.csv"],
    source_format="csv",
    destination_project_dataset_table=f"{DATASET_NAME_DELIMITER}.{TABLE_NAME_DELIMITER}",
    write_disposition="WRITE_TRUNCATE",
    external_table=False,
    autodetect=True,
    field_delimiter="\t",
    quote_character="",
    max_id_key=MAX_ID_STR,
    deferrable=True,
)
Reference¶
For further information, look at:

Google Cloud Storage Documentation

Google Cloud BigQuery Documentation




## Reference
####

https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/transfer/gcs_to_bigquery.html

https://www.youtube.com/watch?v=LmQhHcueJs0

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Airflow로 Google Cloud 서비스 완벽 공략: BigQuery, GCS 다루기 실전 가이드
https://www.youtube.com/watch?v=l_qZXGQwhk8

https://github.com/Hyunsoo-Ryan-Lee/Apache_Airflow_Tutorial_DAG


https://www.youtube.com/watch?v=WOk0RrmArPQ&sttick=1


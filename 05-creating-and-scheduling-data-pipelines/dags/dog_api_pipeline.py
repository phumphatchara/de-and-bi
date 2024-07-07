from airflow import DAG
from airflow.utils import timezone
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import requests
import json
import logging
#from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOprator
def _get_don_api():
    response=requests.get(" https://dog.ceo/api/breeds/image/random Fetch!")
    data=response.json()
    logging.info(data)
    with open("/opt/airflow/dags/dog.json","w") as f:   
        json.dump(data,f)
    #เปลี่ยน "w" เป็น "a" appen


with DAG(
    "dog_api_pipeline",
    start_date=timezone.datetime(2024, 7, 7),
    schedule="@daily", #cron expression
    tags=["DS525"],
):

    start = EmptyOperator(task_id="start")

    get_don_api = PythonOperator(
        task_id="get_don_api",
        python_callable=_get_don_api,
    )


    #upload_to_gcs=LocalFilesystemToGCSOprator(
    #    task_id="",
    #    src="",
    #    dst="dog.json",
    #    bucket="",
    #    gcp_comm_id=""
    #)
    


    end = EmptyOperator(task_id="end")

    start >> get_don_api >> end
    
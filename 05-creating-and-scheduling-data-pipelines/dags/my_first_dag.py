from airflow import DAG
from airflow.utils import timezone
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import logging


def _say_hello():
    logging.debug("This is DEBUG log")
    logging.info("my_first_dag")


with DAG(
    "my_first_dag",
    start_date=timezone.datetime(2024, 7, 7),
    schedule=None,
    tags=["DS525"],
):

    start = EmptyOperator(task_id="start")

    echo_hello = BashOperator(
        task_id="echo_hello",
        bash_command="echo 'my_first_dag'",
    )

    say_hello = PythonOperator(
        task_id="say_hello",
        python_callable=_say_hello,
    )


    end = EmptyOperator(task_id="end")

    start >> echo_hello >> say_hello >> end
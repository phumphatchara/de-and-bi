import json
import glob
import os
from typing import List

from airflow import DAG
from airflow.utils import timezone
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

def _query():
    hook = PostgresHook(postgres_conn_id="neon_pj")   #ดึงข้อมูลpostgres
    conn = hook.get_conn()
    cur = conn.cursor()
    sql="select * from chickens"
    cur.execute(sql)
    rows=cur.fetchall()
    for each in rows:
        print(each)

with DAG(
    "neon_pj",
    start_date=timezone.datetime(2024, 7, 22),
    schedule=None,
    tags=["workshop"],
    catchup=False,
):  
 
    
    query = PythonOperator(
        task_id="query",
        python_callable=_query,
        
    )

    rename_column = PostgresOperator(
        task_id="rename_column",
        postgres_conn_id="neon_pj",
        sql="""
            create or replace view staging_chickens
            as
                select
                    year,
                    province,
                    value as number_of_chickens
            from chickens
            """,
    
    )

    summarize = PostgresOperator(
        task_id="summarize",
        postgres_conn_id="neon_pj",
        sql="""
            create or replace view chickens_summary
            as
                select
                    year,
                    
                    avg(number_of_chickens) as avg_number_of_chickens
            from staging_chickens
            group by year
            """,
    
    )
    

    
    query >> rename_column >> summarize
    
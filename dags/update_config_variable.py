import json
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from airflow.models import Variable

def update_dag_config():
    postgres_hook = PostgresHook(postgres_conn_id="airflow_db")
    df = postgres_hook.get_pandas_df(sql="select * from public.dag_config;")
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    final = json.dumps(parsed, indent=4)
    print(final)

    try:
        Variable.update(key="dag_config", value=final)
    except:
        Variable.set(key="dag_config", value=final)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1),
    'catchup': False
}

with DAG(
        dag_id='update_config_variable',
        schedule_interval=None,
        default_args=default_args,
        template_searchpath="/usr/local/airflow/include/update_config_variable/",
        catchup=False,
    ) as dag:

    start = DummyOperator(
        task_id="start"
    )

    finish = DummyOperator(
        task_id="finish"
    )

    t1 = PostgresOperator(
        task_id="initialize_config",
        sql="initialize_config.sql",
        postgres_conn_id='airflow_db'
    )

    t2 = PythonOperator(
        task_id='update_dag_config',
        python_callable=update_dag_config,
    )

    start >> t1 >> t2 >> finish
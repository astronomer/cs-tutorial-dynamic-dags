import json
from datetime import datetime
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable


def create_dag(dag_id, schedule, sql_query, default_args):

    with DAG(dag_id=dag_id, schedule_interval=schedule, default_args=default_args, catchup=False) as dag:

        start = DummyOperator(task_id='start')
        finish = DummyOperator(task_id='finish')

        t1 = PostgresOperator(
                task_id='postgres_query',
                postgres_conn_id='my_postgres_conn',
                sql=sql_query
        )

        with TaskGroup('dynamic_tasks') as dyn_tasks:
            for i in range(10):
                DummyOperator(task_id=f"dummy_task_{i}")

        start >> t1 >> dyn_tasks >> finish


    return dag


for dag in json.loads(Variable.get('dag_config')):
    dag_id = '{}'.format(str(dag["dagid"]))

    default_args = {
        'owner': 'airflow',
        'start_date': datetime(2018, 1, 1),
        'catchup': False
    }

    globals()[dag_id] = create_dag(
        dag_id=dag["dagid"],
        schedule=dag["schedule"],
        sql_query=dag["query"],
        default_args=default_args
    )
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def imprimir_hora():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("La hora actual es:", current_time)

default_args = {
    'owner': 'tu_nombre',
    'start_date': datetime(2023, 7, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'mi_dag',
    description='DAG para imprimir la hora cada minuto',
    schedule_interval='*/1 * * * *',
    default_args=default_args,
)

tarea = PythonOperator(
    task_id='imprimir_hora',
    python_callable=imprimir_hora,
    dag=dag,
)
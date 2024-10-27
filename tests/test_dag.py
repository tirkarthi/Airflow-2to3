import datetime

from airflow import DAG, settings, models
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.timetables.events import EventsTimetable


with DAG(
    dag_id="my_dag_name",
    default_view="tree",
    start_date=datetime.datetime(2021, 1, 1),
    schedule_interval="@daily",
    concurrency=2,
):
    op = EmptyOperator(
        task_id="task", task_concurrency=1, trigger_rule="none_failed_or_skipped"
    )


@dag(
    default_view="graph",
    start_date=datetime.datetime(2021, 1, 1),
    schedule_interval=EventsTimetable(event_dates=[datetime.datetime(2022, 4, 5)]),
    max_active_tasks=2,
    full_filepath="/tmp/test_dag.py"
)
def my_decorated_dag():
    op = EmptyOperator(task_id="task")


my_decorated_dag()

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator

schedule_interval = "@daily"
start_date = days_ago(1)
default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id="reddit_india_pipeline",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=False,
    max_active_runs=1,
) as dag:

    scrape_reddit = BashOperator(
        task_id="scrape_reddit",
        bash_command="python /opt/airflow/tasks/scraper.py",
    )

    validate_sanitize_bronze = BashOperator(
        task_id="validate_sanitize_bronze",
        bash_command="python /opt/airflow/tasks/validate_and_transform.py",
    )

(
    scrape_reddit
    >> validate_sanitize_bronze
)

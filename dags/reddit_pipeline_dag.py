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

    push_bronze = BashOperator(
        task_id="push_bronze",
        bash_command="python /opt/airflow/tasks/s3_push.py bronze",
    )

    validate_sanitize_bronze = BashOperator(
        task_id="validate_sanitize_bronze",
        bash_command="python /opt/airflow/tasks/validate_and_transform.py",
    )

    push_silver = BashOperator(
        task_id="push_silver",
        bash_command="python /opt/airflow/tasks/s3_push.py silver",
    )

    push_redshift = BashOperator(
        task_id="push_redshift",
        bash_command="python /opt/airflow/tasks/redshift_push.py",
    )

(
    scrape_reddit
    >> push_bronze
    >> validate_sanitize_bronze
    >> push_silver
    >> push_redshift
)

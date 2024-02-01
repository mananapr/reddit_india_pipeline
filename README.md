# Reddit India Pipeline
Pipeline that scrapes data from [r/india](https://old.reddit.com/r/india) subreddit and finalizes data for the visual layer.

## Architecture
- **Infra Provisioning:** Terraform (with AWS)
- **Containerization:** Docker
- **Orchestration:** Airflow
- **Visual Layer:** Not sure yet, maybe Metabase

### DAG Tasks:

1. Scrape data from r/india to generate bronze data
2. Validate using Pydantic and load data to S3
3. Generate and valiate silver data and load to S3
4. Load silver data into Redshift


## Requirements

1. AWS CLI and Terraform for infra provisioning
2. Docker for Airflow and DAG execution

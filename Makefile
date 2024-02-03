help:
	@echo "init   Initializes airflow"
	@echo "infra  Create AWS infrastructure and sets up env config"
	@echo "up     Runs airflow"

init:
	@echo -e "AIRFLOW_UID=$$(id -u)" > .env
	docker-compose up airflow-init

infra:
	terraform -chdir=terraform/ init -input=false
	terraform -chdir=terraform/ apply
	terraform -chdir=terraform/ output > ./tasks/configuration.env
	cat $$HOME/.aws/credentials >> ./tasks/configuration.env

up:
	docker-compose up

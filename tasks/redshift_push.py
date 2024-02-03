import pathlib
import psycopg2
from dotenv import dotenv_values

## Read env file
script_path = pathlib.Path(__file__).parent.resolve()
config = dotenv_values(f"{script_path}/configuration.env")

def get_connection() -> psycopg2.extensions.connection:
    """
        Connects to RDS and returns connection object
    """
    conn = psycopg2.connect(
        host=config["redshift_host"].split(":")[0],
        port=config["redshift_port"],
        user=config["redshift_user"],
        password=config["redshift_password"],
        dbname=config["redshift_database"],
    )
    return conn

def get_query_by_filename(filename: str) -> str:
    """
        Returns query in filename as string
    """
    with open(f"{script_path}/queries/{filename}.sql", "r") as f:
        query = f.read()
        return query

if __name__ == '__main__':
    conn = get_connection()
    cursor = conn.cursor()

    ## Creates main table if does not exists
    table_init_query = get_query_by_filename("1_table_init")

    ## Create intermediate temp table
    intermediate_table_query = get_query_by_filename("2_temp_table").format(
        bucket_name=config["bucket_name"],
        region=config["aws_region"],
        aws_access_id=config["aws_access_key_id"],
        aws_secret_key=config["aws_secret_access_key"]
    )

    ## Insert data into main table and cleanup temp table
    final_insert_query = get_query_by_filename("3_final_insert")

    ## Execute Queries
    cursor.execute(table_init_query)
    cursor.execute(intermediate_table_query)
    cursor.execute(final_insert_query)

    ## Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()

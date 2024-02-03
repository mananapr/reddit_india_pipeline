CREATE TEMP TABLE Post_temp (LIKE Post);

COPY Post_temp
FROM
    's3://{bucket_name}/silver.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

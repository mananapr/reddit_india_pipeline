output "aws_region" {
  description = "AWS Region"
  value       = var.aws_region
}

output "bucket_name" {
  description = "S3 Bucket Name"
  value       = aws_s3_bucket.reddit-bucket.id
}

output "redshift_password" {
  description = "Redshift Cluster Password"
  value       = var.redshift_password
}

output "redshift_user" {
  description = "Redshift Cluster Username"
  value       = aws_redshift_cluster.reddit_cluster.master_username
}

output "redshift_port" {
  description = "Redshift Cluster Port"
  value       = aws_redshift_cluster.reddit_cluster.port
}

output "redshift_host" {
  description = "Redshift Cluster Hostname"
  value       = aws_redshift_cluster.reddit_cluster.endpoint
}

output "redshift_database" {
  description = "Redshift Cluster Database Name"
  value       = aws_redshift_cluster.reddit_cluster.database_name
}

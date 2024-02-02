output "aws_region" {
  description = "AWS Region"
  value       = var.aws_region
}

output "bucket_name" {
  description = "S3 Bucket Name"
  value       = aws_s3_bucket.reddit-bucket.id
}

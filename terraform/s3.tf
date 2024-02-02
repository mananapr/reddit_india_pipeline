## Create S3 Bucket
resource "aws_s3_bucket" "reddit-bucket" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}

## Enable Versioning
resource "aws_s3_bucket_versioning" "reddit_bucket_versioning" {
  bucket = aws_s3_bucket.reddit-bucket.id
  versioning_configuration {
    status = var.versioning
  }
}

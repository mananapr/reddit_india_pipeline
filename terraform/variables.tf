variable "aws_region" {
  description = "Region for the AWS services to run in."
  type        = string
  default     = "us-east-2"
}

variable "bucket_prefix" {
  description = "S3 Bucket Prefix"
  type        = string
  default     = "reddit-india-pipeline-"
}

variable "versioning" {
  type    = string
  default = "Enabled"
}

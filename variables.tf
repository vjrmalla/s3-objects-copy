variable "aws_region" {
    default = "us-east-1"
    description = "AWS Region to deploy to"
}

variable "env_name" {
    default = "s3-to-s3-copy-example"
    description = "Terraform environment name"
}
provider "aws" {
  allowed_account_ids = ["571725821101"]
  region = "${var.aws_region}"
  profile = "iamadmin-general"
}

data "archive_file" "my_lambda_function" {
  source_dir  = "${path.module}/lambda/"
  output_path = "${path.module}/lambda.zip"
  type        = "zip"
}
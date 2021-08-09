resource "aws_s3_bucket" "destination_bucket" {
   bucket = "${var.env_name}-lambda-dest-bucket"
   force_destroy = true
}
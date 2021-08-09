resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.env_name}_lambda_s3copy_policy"
  description = "${var.env_name}_lambda_s3copy_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:CopyObject",
        "s3:HeadObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.env_name}-lambda-src-bucket",
        "arn:aws:s3:::${var.env_name}-lambda-src-bucket/*"
      ]
    },
    {
      "Action": [
        "s3:ListBucket",
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:CopyObject",
        "s3:HeadObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.env_name}-lambda-dest-bucket",
        "arn:aws:s3:::${var.env_name}-lambda-dest-bucket/*"
      ]
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "s3_copy_function" {
    name = "app_${var.env_name}_lambda"

    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "terraform_lambda_iam_policy_basic_execution" {
 role = "${aws_iam_role.s3_copy_function.id}"
 policy_arn = "${aws_iam_policy.lambda_policy.arn}"
}

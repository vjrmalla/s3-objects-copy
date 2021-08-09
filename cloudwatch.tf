resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.s3_copy.function_name}"
  retention_in_days = 14
}
resource "aws_lambda_function" "s3_copy" {
   filename = "lambda.zip"
   source_code_hash = data.archive_file.my_lambda_function.output_base64sha256
   #source_code_hash = filebase64sha256("lambda.zip")
   function_name = "${var.env_name}_s3_copy_lambda"
   role = "${aws_iam_role.s3_copy_function.arn}"
   handler = "index.handler"
   runtime = "python3.8"

   environment {
       variables = {
           SRC_BUCKET = "${var.env_name}-lambda-src-bucket",
           DST_BUCKET = "${var.env_name}-lambda-dest-bucket",
           REGION = "${var.aws_region}"
       }
   }
}
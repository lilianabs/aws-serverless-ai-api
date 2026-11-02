# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

There is no build, lint, or test tooling in this repo. The only workflow is Terraform plus the AWS CLI, run from `infra/`:

```bash
cd infra
terraform init
terraform apply
terraform output -raw base_url                # API Gateway base URL
curl --get "$(terraform output -raw base_url)/chat" \
  --data-urlencode "prompt=Explain briefly what is AWS lambda"
```

Invoke the Lambda directly, bypassing API Gateway:

```bash
aws lambda invoke --region=us-east-1 \
  --function-name=$(terraform output -raw function_name) response.json
```

## Architecture

The system is a single synchronous path: API Gateway (HTTP API) → Lambda → Amazon Bedrock Converse API.

- **Lambda code** lives in `code/lambda_function.py`. Its handler reads `prompt` from `event["queryStringParameters"]`, calls `bedrock.converse` with the model from the `MODEL_ID` env var, and returns `{message, success}` as JSON. Errors return a 500 with `details`. The handler assumes the query parameter exists; a request without `prompt` raises a `KeyError` that is caught and returned as a 500.
- **Packaging is done by Terraform, not by hand.** `infra/main.tf` uses the `archive` provider to zip the whole `code/` directory into `code.zip` at the repo root, uploads it to a random-named S3 bucket, and points the Lambda at that S3 object. Changing anything under `code/` changes `source_code_hash` and triggers a redeploy on the next `terraform apply`. `code.zip` is a build artifact; don't edit it directly.
- **Model and region config** are set in the `aws_lambda_function.ai_api` environment block in `infra/main.tf` (`MODEL_ID`, `BEDROCK_REGION`), not in code. The `bedrock-runtime` client is created at module load, outside the handler, so it is reused across warm invocations.
- **Routing:** the only route is `POST /chat` on the `serverless_lambda_gw` HTTP API, using `AWS_PROXY` integration. The stage auto-deploys.
- **IAM:** the Lambda role (`serverless_lambda`) has `AWSLambdaBasicExecutionRole` plus `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on `Resource = "*"`. Tighten the resource if you touch this.
- **Terraform state** is in `infra/terraform.tfstate` and is currently tracked by git. It holds resource IDs and may hold other sensitive values, so avoid committing changes to it.

Everything in `infra/` targets `us-east-1` by default (`var.aws_region`). The Bedrock region is set separately to `us-east-1` in the Lambda environment.

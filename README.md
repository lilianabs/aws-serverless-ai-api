# aws-serverless-ai-api

This repository contains template code to create the infrastructure and code for an AI API in AWS.

## Prerequisites

- Install AWS CLI
- Install Terraform

## To run this project

1. cd into infra
2. run terraform init
3. run terraform apply
4. run aws s3 ls $(terraform output -raw lambda_bucket_name)
5. run aws lambda invoke --region=us-east-1 --function-name=$(terraform output -raw function_name) response.json
6. run curl "$(terraform output -raw base_url)/chat"

To test the API run the following command:
curl --get "$(terraform output -raw base_url)/chat" \
  --data-urlencode "prompt=Explain briefly what is AWS lambda"

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
5. 

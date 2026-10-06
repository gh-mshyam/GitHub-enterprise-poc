terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Configure backend as needed for your deployment
  # backend "s3" {
  #   bucket         = "your-bucket"
  #   key            = "your-key"
  #   region         = "us-east-1"
  #   dynamodb_table = "terraform-lock"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Repository  = "repository-name"
      ManagedBy   = "Terraform"
    }
  }
}

# Add your infrastructure resources here

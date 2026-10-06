################################################################################
# ⚠️  TEMPLATE MANAGED FILE
# Terraform Configuration
################################################################################

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # Configure this with your S3 bucket
    # bucket         = "your-terraform-state"
    # key            = "repo-name/terraform.tfstate"
    # region         = "us-east-1"
    # encrypt        = true
    # dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Repository  = "repo-name"
    }
  }
}

# Add your infrastructure resources here
# Example:
# resource "aws_s3_bucket" "example" {
#   bucket = "my-bucket"
# }

################################################################################
# ⚠️  TEMPLATE MANAGED FILE
# Terraform Variables
################################################################################

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for resources"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment (dev, staging, prod)"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  type        = string
  description = "Project name for resource naming"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Additional tags for resources"
}

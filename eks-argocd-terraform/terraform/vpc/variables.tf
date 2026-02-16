variable "region" {
  description = "AWS region to deploy resources to."
  type        = string
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "project_name" {
  description = "The name prefix for all created resources."
  type        = string
}
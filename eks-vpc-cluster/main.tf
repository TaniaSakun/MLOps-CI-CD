provider "aws" {
  region = var.region
}

locals {
  region          = var.region
  vpc_name        = var.vpc_name
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
}

module "vpc" {
  source = "./vpc"

  vpc_name     = local.vpc_name
  cluster_name = local.cluster_name
  region       = local.region
}

module "eks" {
  source = "./eks"

  cluster_name    = local.cluster_name
  cluster_version = local.cluster_version
  region          = local.region

  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets
}
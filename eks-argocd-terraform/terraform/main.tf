# terraform/main.tf

# 1. VPC Module
module "vpc" {
  source = "./vpc"
  project_name = var.project_name
  region       = var.aws_region
}

# 2. EKS Module
module "eks" {
  source = "./eks"
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnet_ids 
}

# 3. ArgoCD Module
module "argocd" {
  source = "./argocd"
 
  cluster_name = module.eks.cluster_name
  cluster_endpoint = module.eks.cluster_endpoint
  cluster_ca = module.eks.cluster_ca_certificate
}

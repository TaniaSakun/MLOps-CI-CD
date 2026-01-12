data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket = "ts-terraform-states-bucket"
    key    = "eks-vpc/vpc/terraform.tfstate"
    region = "eu-central-1"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"

  vpc_id     = data.terraform_remote_state.vpc.outputs.vpc_id
  subnet_ids = data.terraform_remote_state.vpc.outputs.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    cpu = {
      min_size     = 1
      max_size     = 3
      desired_size = 2

      instance_types = ["t3.micro"]
      capacity_type  = "ON_DEMAND"

      labels = {
        node-type = "cpu"
      }
    }
  }

authentication_mode = "API"
  access_entries = {
    admin = {
      principal_arn = "arn:aws:iam::{iam-identifier}:user/{user-name}"

      policy_associations = {
        admin = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}

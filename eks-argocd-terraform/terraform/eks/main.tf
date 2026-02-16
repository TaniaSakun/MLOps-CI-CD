module "eks" {
    source = "terraform-aws-modules/eks/aws"
    version = "~> 20.0"

    cluster_name = "eks-cluster"
    cluster_version = "1.30"
    vpc_id = var.vpc_id
    subnet_ids = var.subnet_ids

    eks_managed_node_groups = {
        default = {
            desired_size = 2
      max_size     = 4
      min_size     = 1
      instance_types =["t3.medium"]
        }
    }

    tags = {
        Project = "eks-argocd"
    }
}

terraform {
  backend "s3" {
    bucket = "ts-terraform-states-bucket"
    key    = "eks-vpc/eks/terraform.tfstate"
    region = "eu-central-1"
  }
}

terraform {
  backend "s3" {
    bucket = "my-terraform-states-eu"
    key    = "argocd/terraform.tfstate"
    region = "eu-central-1"
  }
}

output "eks_cluster_name" {
    value = module.eks.cluster_name
}

output "argocd_server_url" {
    value = module.argocd.argocd_server_url
}

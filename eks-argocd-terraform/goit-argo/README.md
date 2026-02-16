# EKS + ArgoCD + Helm (Terraform Deployment)

This project demonstrates:

- Deploying ArgoCD into an existing EKS cluster using Terraform
- Managing Kubernetes applications via ArgoCD
- Deploying a Helm chart using ArgoCD Application
- Automated sync and self-healing

---

## 📁 Project Structure

### Terraform (ArgoCD installation)
```
terraform/
└── argocd/
├── main.tf
├── variables.tf
├── provider.tf
├── outputs.tf
├── backend.tf
├── terraform.tf
└── values/
└── argocd-values.yaml
```

## GitOps Repository
```
goit-argo
├── namespaces
│ ├── application
│ │ ├── nginx.yaml
│ │ └── ns.yaml
│ └── infra-tools
│ └── ns.yaml
└── README.md
```

---

## 1. Deploy ArgoCD using Terraform

### Step 1 — Initialize Terraform

```
cd terraform/argocd
terraform init
Step 2 — Validate configuration
terraform validate
Step 3 — Apply infrastructure
terraform apply
Confirm with yes.
```

Verify ArgoCD Installation
Check namespace:

```kubectl get ns```

Check pods:

```kubectl get pods -n infra-tools```

You should see pods like:

```argocd-server-xxxx
argocd-repo-server-xxxx
argocd-application-controller-xxxx
argocd-dex-server-xxxx
```

Access ArgoCD UI
Option 1 — Port Forward

```kubectl port-forward svc/argocd-server -n infra-tools 8080:443```

Open in browser:

```https://localhost:8080```

Get Initial Admin Password

```
kubectl -n infra-tools get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
Username: admin
```

2. ArgoCD Application Deployment
ArgoCD automatically deploys applications defined in Git.

Application definition is stored in:

```namespaces/application/nginx.yaml```

Verify Application
Check ArgoCD applications:

```kubectl get applications -n infra-tools```

Expected:

```NAME     SYNC STATUS   HEALTH STATUS
nginx    Synced        Healthy
```

### Verify Workload Deployment
Check target namespace:
```
kubectl get pods -n application
```
You should see nginx pods running.

### Automated Sync
The Application is configured with:
```
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
```
This means:

- Automatically sync on Git changes
- Automatically remove deleted resources
- Automatically fix manual cluster drift
- Automatically create namespace if missing

### How ArgoCD Application Works
ArgoCD pulls:
- Helm chart from external Helm repository
- Values overrides (inline or from file)
- Deploys into target namespace
- Continuously monitors drift

### Useful Commands
Check all resources

```kubectl get all -n infra-tools
kubectl get all -n application
```

Delete everything

```terraform destroy```
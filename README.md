# MLOps-CI-CD
The repository for the MLOps CI/CD homeworks
# Terraform EKS + VPC Project

## Огляд

Цей проєкт демонструє модульне використання Terraform для автоматичного створення:

- **VPC** з приватними та публічними субнетами, NAT Gateway, маршрутизаторами і Security Group.
- **EKS кластер** з двома node group-ами (CPU та GPU).
- Підключення до кластера через `kubectl` після виконання `terraform apply`.

Мета — показати базовий шаблон продакшн-проєкту на AWS з використанням модульної структури Terraform.

⚠️ **Увага:** Після тестування обов’язково видаляйте створені ресурси командою `terraform destroy`, щоб уникнути непередбачених витрат.

---

## Структура проєкту

```text
eks-vpc-cluster/
├── main.tf                # Кореневий виклик модулів
├── variables.tf           # Глобальні змінні
├── outputs.tf             # Глобальні output-и
├── terraform.tf           # Конфігурація Terraform
├── backend.tf             # Конфігурація S3 backend
├── vpc/                   # Модуль VPC
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── backend.tf
├── eks/                   # Модуль EKS
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── backend.tf
└── README.md
```
## Встановлення та вимоги

- Terraform >= 1.5
- AWS CLI
- Kubectl
- Доступ до AWS з IAM користувачем або роллю, яка має права на: 
   - VPC (EC2, Subnets, Security Groups, IGW, NAT)
   -  EKS (CreateCluster, NodeGroup, IAM Roles)
   - S3 (для Terraform state)
   - STS (для отримання токену)

## Налаштування backend

У кожному модулі (```vpc/``` та ```eks/```) використовується S3 backend для збереження state:
```
terraform {
  backend "s3" {
    bucket = "ts-terraform-states-bucket"
    key    = "eks-vpc/vpc/terraform.tfstate" # або eks/terraform.tfstate
    region = "eu-central-1"
  }
}
```

В корені проєкту можна залишити окремий ```terraform.tf``` для глобальних конфігурацій.

## Змінні

Приклад ```variables.tf``` у корені:
```
variable "region" {
  default = "eu-central-1"
}

variable "cluster_name" {
  default = "eks-cluster"
}
```

У модулів ```vpc``` та ```eks``` оголошені власні змінні для CIDR, AZs, instance types та node group конфігурацій.

## Розгортання інфраструктури

1. VPC:
```
cd vpc
terraform init
terraform plan
terraform apply
```
2. EKS кластер:
```
cd ../eks
terraform init
terraform plan
terraform apply
```
Під час apply Terraform підключиться до state VPC через terraform_remote_state і використає VPC ID та subnet-и.

## Підключення до кластера

Після успішного створення кластера виконайте:
```
aws eks update-kubeconfig --region eu-central-1 --name eks-cluster
kubectl get nodes
```
Ви повинні побачити всі ноди, наприклад:
```
ip-10-0-1-120.eu-central-1.compute.internal   Ready
ip-10-0-2-92.eu-central-1.compute.internal    Ready
```

Додавання користувачів та ролей
```
access_entries = {
  aws_cli_user = {
    principal_arn = "arn:aws:iam::<iam-identifier>:user/<user-name>"
    policy_associations = {
      admin = {
        policy_arn   = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
        access_scope = { type = "cluster" }
      }
    }
  }
}
```
Це дозволяє підключатися до кластера через kubectl. Варто лише змінити на коректні наступні дані: ```iam-identifier``` та ```user-name``` в ```eks/main.tf``` файлі

## Видалення ресурсів
Щоб уникнути витрат, після тестування:
```
cd eks
terraform destroy

cd ../vpc
terraform destroy
```
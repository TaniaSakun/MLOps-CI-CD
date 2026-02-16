output "vpc_id" {
  description = "The ID of the created VPC."
  # Посилання на вихідне значення vpc_id, яке повертає модуль VPC
  value       = module.vpc.vpc_id 
}

output "public_subnet_ids" {
  description = "List of IDs of the public subnets."
  # Посилання на вихідне значення public_subnets, яке повертає модуль VPC
  value       = module.vpc.public_subnets 
}

output "private_subnet_ids" {
  description = "List of IDs of the private subnets."
  # Посилання на вихідне значення private_subnets, яке повертає модуль VPC
  value       = module.vpc.private_subnets 
}
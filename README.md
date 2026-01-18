# MLOps-CI-CD
The repository for the MLOps CI/CD homeworks
# MLOps Train Automation (AWS Step Functions + Terraform + GitLab CI)

## Мета роботи

Метою цієї роботи є побудова автоматизованого пайплайну тренування моделі з використанням **AWS Step Functions**, **AWS Lambda**, **Terraform** та **GitLab CI**.
Цей проєкт демонструє модульне використання Terraform для автоматичного створення:

Пайплайн складається з кількох етапів:
- валідація даних;
- логування метрик / результатів.

Уся інфраструктура описана як код (Infrastructure as Code) за допомогою Terraform, а запуск пайплайну автоматизований через GitLab CI при `push` у репозиторій.

---

## Структура проєкту

```text
mlops-train-automation/
├── terraform/
│  ├── main.tf
│  ├── variables.tf
│  └── lambda/
│    ├── validate.py
│    ├── log_metrics.py
│    ├── validate.zip
│    └── log_metrics.zip
├── .gitlab-ci.yml
├── README.md
```
---
## Lambda-функції

`validate.py`
Виконує умовну валідацію даних.
```
def handler(event, context):
    print("Validating data...")
    return {"status": "validated"}
```

`log_metrics.py`
Імітує логування метрик.
```
def handler(event, context):
    print("Logging metrics...")
    return {"status": "logged"}
```
---
## Збірка Lambda-архівів

Перед застосуванням Terraform необхідно зібрати `.zip` архіви для Lambda-функцій.
```
cd terraform/lambda
zip validate.zip validate.py
zip log_metrics.zip log_metrics.py
```
---
## Розгортання інфраструктури через Terraform

1. Перейдіть у директорію terraform:
```
cd terraform/
```
2. Ініціалізуйте Terraform:
```
terraform init
```
3. Застосуйте конфігурацію:
```
terraform apply
```

Після виконання буде створено:

- IAM роль для Lambda;
- IAM роль для Step Function;
- 2 Lambda-функції (`validate`, `log_metrics`);
- Step Function mlops-train-pipeline.
---
## AWS Step Function

Архітектура пайплайну
```
ValidateData → LogMetrics → Succeeded
```

Ручний запуск Step Function

1. AWS Console → Step Functions
2. Вибрати `mlops-train-pipeline`
3. Натиснути Start execution
4. Передати JSON:
```
{
  "source": "manual",
  "run": "test"
}
```
5. Запустити виконання

---
## GitLab CI

Опис

GitLab CI автоматично запускає Step Function при `push` у репозиторій.

`.gitlab-ci.yml`
```
train-model:
  stage: train
  image: amazon/aws-cli:2.15.0
  script:
    - aws stepfunctions start-execution \
        --state-machine-arn arn:aws:states:REGION:ACCOUNT_ID:stateMachine:mlops-train-pipeline \
        --name "train-$(date +%s)" \
        --input '{"source":"gitlab-ci","commit":"'$CI_COMMIT_SHORT_SHA'"}'
```
---
## Змінні середовища GitLab CI

У GitLab CI необхідно додати:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
---
## Перевірка результатів

- Статус виконання перевіряється у AWS Step Functions
- Логи Lambda доступні у CloudWatch:
    - `/aws/lambda/validate`
    - `/aws/lambda/log_metrics`
---
## Результати виконання
<img width="1440" height="737" alt="Screenshot 2026-01-17 at 15 00 42" src="https://github.com/user-attachments/assets/a5a513ea-86e4-4f4f-b2ee-3b4e7cdf68a3" />
<img width="1147" height="679" alt="Screenshot 2026-01-17 at 15 02 53" src="https://github.com/user-attachments/assets/f7d6dc3d-00fc-4c90-9d30-1f81bfb6c02e" />
<img width="1401" height="578" alt="Screenshot 2026-01-17 at 15 02 43" src="https://github.com/user-attachments/assets/c5a3ccc7-7b4f-49c7-b2e5-2d9bf8ee7d0f" />

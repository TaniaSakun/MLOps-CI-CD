# MLOps-CI-CD
The repository for the MLOps CI/CD homeworks

# AIOps Quality Monitoring Project

## Опис проєкту

Цей проєкт демонструє end-to-end MLOps pipeline для ML-моделі з використанням Kubernetes, GitOps та інструментів моніторингу.

Реалізовано:

- inference-сервіс на FastAPI;
- деплой у Kubernetes через Helm;
- GitOps-керування через ArgoCD;
- моніторинг метрик через Prometheus + Grafana;
- логування подій та дрейфу;
- підготовлений CI-пайплайн для retrain моделі.

Проєкт фокусується не на складності моделі, а на інфраструктурі, спостережуваності та автоматизації.

---

## Структура проєкту

```text
aiops-quality-project/
├── app/
│   └── main.py                  # FastAPI inference сервіс
├── model/
│   └── train.py                 # Скрипт retrain моделі
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/               # Deployment, Service, ServiceAccount
├── argocd/
│   ├── application.yaml         # ArgoCD app для сервісу
│   └── prometheus-app.yaml      # ArgoCD app для Prometheus
├── prometheus/
│   └── additionalScrapeConfigs.yaml
├── grafana/
│   └── dashboards.json          # Grafana dashboard
├── .gitlab-ci.yml               # CI пайплайн (retrain)
└── README.md
```
---

## Архітектура (логічно)

```arduino
Client → FastAPI → ML model
               ↘ logs
                ↘ /metrics → Prometheus → Grafana
                               ↑
                           ArgoCD (GitOps)
```
---

## Як запустити проєкт

### 1. Деплой через ArgoCD

ArgoCD підʼєднаний до Git-репозиторію і автоматично деплоїть:
- inference-сервіс (`aiops-quality`);
- Prometheus;
- Grafana.
Перевірка:
```bash
kubectl get applications -n argocd
```
Очікувано:

```text
aiops-quality   Synced   Healthy
prometheus      Synced   Healthy
grafana         Synced   Healthy
```
---

### 2. Перевірка API

```bash
kubectl port-forward svc/aiops-quality -n aiops-quality 8000:8000
```
Swagger:
```bash
kubectl get applications -n argocd
```
---

### Як протестувати запит

Приклад запиту:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[5.1,3.5,1.4,0.2]}'
```
Очікувана відповідь: 
```json
{
  "prediction": 0,
  "drift": false
}
```
<img width="1433" height="549" alt="Screenshot 2026-01-17 at 16 24 35" src="https://github.com/user-attachments/assets/3b042775-9b53-4f45-8abd-adcc5e5a4b1c" />
<img width="1440" height="889" alt="Screenshot 2026-01-17 at 16 24 07" src="https://github.com/user-attachments/assets/dbad3445-37ff-4562-a2ee-e67ba7b7fc91" />

---

### Як перевірити логування

Логи inference-сервісу:
```bash
kubectl logs -n aiops-quality deployment/aiops-quality
```
У логах видно:
- вхідні дані;
- результат прогнозу;
- повідомлення про дрейф (якщо спрацьовує).
Приклад:
```less
Incoming request: [5.1, 3.5, 1.4, 0.2]
Prediction result: 0
[DRIFT] Drift detected
```
---

### Як перевірити спрацювання детектора дрейфу

Drift-детекція реалізована на рівні inference-сервісу.
Механізм:
- аналізуються статистики вхідних даних;
- при перевищенні порогу логуються події дрейфу.
Для перевірки:
- Надіслати серію нетипових запитів;
- Перевірити логи сервісу.
```bash
kubectl logs -n aiops-quality deployment/aiops-quality | grep DRIFT
```
---
### Моніторинг у Grafana
Grafana доступна через `port-forward`:
```bash
kubectl port-forward svc/grafana -n monitoring 3000:3000
```
```bash
http://localhost:3000
```
Dashboard показує:
- Requests per minute;
- Latency;
- Активність сервісу.
<img width="1440" height="631" alt="Screenshot 2026-01-18 at 13 13 54" src="https://github.com/user-attachments/assets/0a55c6cd-1f03-4417-9e37-d1c93bae398e" />

---

### Як перевірити retrain-пайплайн

Файл `model/train.py`:
- тренує модель;
- зберігає новий артефакт `model/model.pkl`.
- CI-пайплайн (`.gitlab-ci.yml`) передбачає:
  - запуск retrain-job;
  - генерацію нової моделі;
  - можливість подальшого деплою.
Retrain може бути:
- ручним;
- тригереним зовнішнім сигналом (наприклад, дрейф).
---

### Як оновити модель

- Запустити retrain (`train.py` або CI job);
- Отримати новий `model.pkl`;
- Оновити Docker-image або версію чарта;
- Закомітити зміни;
- ArgoCD автоматично оновить деплой.
---

## Результати

- Inference-сервіс стабільно працює в Kubernetes;
- Метрики збираються Prometheus;
- Трафік візуалізується у Grafana;
- Дрейф логуються;
- GitOps-деплой через ArgoCD працює.
Проєкт демонструє повний життєвий цикл ML-моделі в продакшн-оточенні.
---

## Висновок

Цей проєкт показує, як ML-модель:
- стає сервісом,
- моніториться,
- аналізується на якість,
- автоматично оновлюється через CI/CD і GitOps.

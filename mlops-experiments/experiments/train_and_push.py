import os
import mlflow
import mlflow.sklearn
import joblib
import shutil

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

MLFLOW_TRACKING_URI = "http://localhost:5000"
PUSHGATEWAY_URL = "http://pushgateway.monitoring.svc.cluster.local:9091"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("iris-experiment")

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

params_grid = [
    {"C": 0.1, "max_iter": 100},
    {"C": 1.0, "max_iter": 200},
    {"C": 10.0, "max_iter": 300},
]

best_accuracy = 0
best_run_id = None
best_model_path = None

for params in params_grid:
    with mlflow.start_run() as run:
        model = LogisticRegression(**params)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)

        acc = accuracy_score(y_test, preds)
        loss = log_loss(y_test, probs)

        mlflow.log_params(params)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("loss", loss)
        mlflow.sklearn.log_model(model, "model")

        # Push metrics to PushGateway
        registry = CollectorRegistry()
        g_acc = Gauge("mlflow_accuracy", "Accuracy from MLflow run", ["run_id"], registry=registry)
        g_loss = Gauge("mlflow_loss", "Loss from MLflow run", ["run_id"], registry=registry)

        g_acc.labels(run_id=run.info.run_id).set(acc)
        g_loss.labels(run_id=run.info.run_id).set(loss)

        push_to_gateway(PUSHGATEWAY_URL, job="mlflow_training", registry=registry)

        if acc > best_accuracy:
            best_accuracy = acc
            best_run_id = run.info.run_id
            best_model_path = mlflow.artifacts.download_artifacts(
                run_id=best_run_id,
                artifact_path="model"
            )

# Save best model locally
os.makedirs("best_model", exist_ok=True)
shutil.copytree(best_model_path, "best_model/model", dirs_exist_ok=True)

print(f"Best run: {best_run_id}, accuracy={best_accuracy}")

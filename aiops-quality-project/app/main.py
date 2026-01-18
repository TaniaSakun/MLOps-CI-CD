from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
import numpy as np
import joblib
import os
import time
import logging


# ======================
# App init
# ======================
app = FastAPI(title="AIOps Quality Service")

# ======================
# Metrics
# ======================
REQUEST_COUNT = Counter(
    "http_requests_total", "Total number of HTTP requests", ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "Latency of HTTP requests", ["endpoint"]
)

PREDICTIONS_TOTAL = Counter(
    "model_predictions_total", "Total number of model predictions"
)

DRIFT_COUNT = Counter("drift_detected_total", "Number of detected drift events")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aiops-quality")

# ======================
# Model loading
# ======================
MODEL_PATH = os.getenv("MODEL_PATH", "model/model.pkl")

print("Loading model...")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully")


# ======================
# Request schema
# ======================
class PredictRequest(BaseModel):
    features: list[float]


class PredictResponse(BaseModel):
    prediction: float
    drift_detected: bool


# ======================
# Drift detector (simple / mock)
# ======================
def check_drift(features: list[float]) -> bool:
    mean_value = np.mean(features)

    if mean_value > 0.7:
        print(f"[DRIFT] Drift detected! mean={mean_value}")
        DRIFT_COUNT.inc()
        return True

    return False


# ======================
# Endpoints
# ======================
@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    start_time = time.time()

    if len(data.features) != 4:
        return {
            "prediction": None,
            "drift_detected": False
        }

    logger.info(f"Incoming request: {data.features}")

    prediction = model.predict([data.features])[0]

    drift = check_drift(data.features)

    logger.info(f"Prediction result: {prediction}, drift={drift}")

    REQUEST_COUNT.labels(method="POST", endpoint="/predict").inc()
    PREDICTIONS_TOTAL.inc()
    REQUEST_LATENCY.labels(endpoint="/predict").observe(time.time() - start_time)

    return {
        "prediction": int(prediction),
        "drift_detected": drift
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.get("/health")
def health():
    return {"status": "ok"}

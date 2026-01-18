import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

print("Training model...")

X, y = load_iris(return_X_y=True)

model = LogisticRegression(max_iter=200)
model.fit(X, y)

joblib.dump(model, "model/model.pkl")

print("Model saved to model/model.pkl")

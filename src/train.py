import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

import os
import joblib

# Load data
data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlflow.set_experiment("iris-classification")

with mlflow.start_run() as run:

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("Accuracy:", acc)

    # Log metrics
    mlflow.log_metric("accuracy", acc)
    mlflow.log_param("model", "RandomForest")

    # Log model to MLflow
    mlflow.sklearn.log_model(model, "model")

    run_id = run.info.run_id

    # Register model
    mlflow.register_model(
        f"runs:/{run_id}/model",
        "iris-model"
    )

    # Save fallback model
    os.makedirs("models", exist_ok=True)
    joblib.dump({
        "model": model,
        "features": list(X.columns)
    }, "models/model.pkl")

print("Training completed + model registered")
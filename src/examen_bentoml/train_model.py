import bentoml
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

from examen_bentoml.params import PROCESSED_DATA_PATH


# Load processed data
# ===================

X_train = pd.read_pickle(PROCESSED_DATA_PATH / "X_train.pkl")
X_test = pd.read_pickle(PROCESSED_DATA_PATH / "X_test.pkl")
y_train = pd.read_pickle(PROCESSED_DATA_PATH / "y_train.pkl")
y_test = pd.read_pickle(PROCESSED_DATA_PATH / "y_test.pkl")

# Train model on train set with grid search cv
# ============================================

# Estimator with min max scaler
estimator = make_pipeline(
    MinMaxScaler(),
    ElasticNet(random_state=42)
)

# Params grid
grid = {
    "elasticnet__alpha": np.linspace(0.01, 1, 10),
    "elasticnet__l1_ratio": np.linspace(0.01, 1, 10)
}

# Instanciate the grid search
grid_search = GridSearchCV(
    estimator=estimator,
    param_grid=grid,
    cv=5,
    scoring="r2"
)

# Train
grid_search.fit(X_train, y_train)

# Print results
print("Best parameters:", grid_search.best_params_)
print("Best CV score (R2):", grid_search.best_score_)
print("R2 score on the test set:", grid_search.score(X_test, y_test)) # Score on the test set


# Save the model with the best params
# ===================================

# Instanciate best model
best_model = grid_search.best_estimator_

# Save into BentoML model store
bento_model = bentoml.sklearn.save_model("elasticnet-bento-exam", best_model)

# Print model tag
print(f"Model saved as {bento_model} in the model store.")
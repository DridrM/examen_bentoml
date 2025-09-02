import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from examen_bentoml.params import RAW_DATA_PATH, PROCESSED_DATA_PATH


# Load raw data
# =============
raw_data = pd.read_csv(RAW_DATA_PATH / "admission.csv")

# Clean data
# ==========

# Split between features and target
X = raw_data.drop(["Serial No.", "Chance of Admit "], axis=1) # Drop the 'Serial No.' col because this is an ID col
y = raw_data[["Chance of Admit "]]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)

# Save processed data
# ===================

pd.to_pickle(X_train, PROCESSED_DATA_PATH / "X_train.pkl")
pd.to_pickle(X_test, PROCESSED_DATA_PATH / "X_test.pkl")
pd.to_pickle(y_train, PROCESSED_DATA_PATH / "y_train.pkl")
pd.to_pickle(y_test, PROCESSED_DATA_PATH / "y_test.pkl")

print("Raw data successfully processed and saved into /data/processed.")


if __name__ == "__main__":
    pass
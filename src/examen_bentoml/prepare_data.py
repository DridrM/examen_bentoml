import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from params import RAW_DATA_PATH, PROCESSED_DATA_PATH


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

# Min-max scale the continuous variable as we want to use a linear model
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = pd.DataFrame(scaler.transform(X_train), columns=scaler.get_feature_names_out())
X_test = pd.DataFrame(scaler.transform(X_test), columns=scaler.get_feature_names_out())

# Save processed data
# ===================

pd.to_pickle(X_train, PROCESSED_DATA_PATH / "X_train.pkl")
pd.to_pickle(X_test, PROCESSED_DATA_PATH / "X_test.pkl")
pd.to_pickle(y_train, PROCESSED_DATA_PATH / "y_train.pkl")
pd.to_pickle(y_test, PROCESSED_DATA_PATH / "y_test.pkl")

print("Raw data successfully processed and saved into /data/processed.")


if __name__ == "__main__":
    pass
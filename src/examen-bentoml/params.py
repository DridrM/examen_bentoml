from pathlib import Path


# Raw data URL
RAW_DATA_URL = "https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv"

# Root project path
ROOT_PROJECT_PATH = Path(__file__).resolve().parents[2]

# Raw data path
RAW_DATA_PATH = ROOT_PROJECT_PATH / "data" / "raw"

# Processed data path
PROCESSED_DATA_PATH = ROOT_PROJECT_PATH / "data" / "processed"
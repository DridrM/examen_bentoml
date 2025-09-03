import os
from pathlib import Path


# Root project path
ROOT_PROJECT_PATH = Path(__file__).resolve().parents[2]


########
# Data #
########

# Raw data URL
RAW_DATA_URL = "https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv"

# Raw data path
RAW_DATA_PATH = ROOT_PROJECT_PATH / "data" / "raw"

# Processed data path
PROCESSED_DATA_PATH = ROOT_PROJECT_PATH / "data" / "processed"

# Local models folder
SAVED_MODEL_PATH = ROOT_PROJECT_PATH / "models"


###################
# BentoML service #
###################

# Duration of the token
JWT_EXP_DELTA_MINUTES = 120

# Encoding algorithm
JWT_ALGORITHM = "HS256"

# Encoding secret
JWT_SECRET = os.environ.get("JWT_SECRET")
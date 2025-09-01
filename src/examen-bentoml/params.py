from pathlib import Path


# Root project path
ROOT_PROJECT_PATH = Path(__file__).resolve().parents[2]

# Raw data path
RAW_DATA_PATH = ROOT_PROJECT_PATH / "data" / "raw"

# Processed data path
PROCESSED_DATA_PATH = ROOT_PROJECT_PATH / "data" / "processed"
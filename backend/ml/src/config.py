from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

PROCESSED_DIR = DATA_DIR / "processed"

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "calibration_model.pkl"

# ==========================================================
# Model Settings
# ==========================================================

RANDOM_STATE = 42

CONFIDENCE_THRESHOLD = 0.75
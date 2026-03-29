"""
Cashew Disease Detection - Centralized Configuration
All configuration constants in one place
"""

import os

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "static", "uploads")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "cashew_micro_pt.pth")

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

IMG_SIZE = 224  # Updated for PyTorch Micro-Model
LABELS = ['Anthracnose', 'Dieback', 'Healthy', 'Leaf Spot', 'Powdery Mildew']
NUM_CLASSES = len(LABELS)

# ============================================================================
# UPLOAD CONFIGURATION
# ============================================================================

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'cashew-disease-detection-secret-key-2026')
DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///cashew_diagnostics.db')

# ============================================================================
# MODEL METADATA
# ============================================================================

MODEL_METADATA = {
    "version": "PyTorch Micro-AI V2 (Active)",
    "accuracy": "94.2%",
    "dataset_size": "~1200 images",
    "framework": "PyTorch 2.11"
}

# ============================================================================
# THRESHOLDS
# ============================================================================

CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for predictions
BIAS_THRESHOLD = 0.8  # Threshold for bias detection

# ============================================================================
# MODELS TO CHECK (Priority order)
# ============================================================================

MODELS_TO_CHECK = [
    os.path.join(PROJECT_ROOT, "models", "cashew_micro_pt.pth"),
]

"""
Cashew AI Neural Engine
Provides a unified interface for multiple AI model frameworks.
"""
import time
from loguru import logger

# Safe imports for optional backends
try:
    import torch
except ImportError:
    torch = None

# ============================================================================
# CASHEW AI NEURAL ENGINE (V11.0 - HYBRID FALLBACK)
# ============================================================================

class AINeuralEngine:
    """
    The central AI core that orchestrates multi-framework inference.
    """

    def __init__(self, active_engine="PyTorch"):
        """Initialize engine state and load default backend."""
        self.active_engine = active_engine
        self.pt_model = None
        self.labels_pt = []  # Managed dynamically to prevent mismatches
        
        logger.info("[ENGINE] Initializing neural orchestration layer...")
        self._load_pytorch()
        self._load_onnx()
        self._auto_select_engine()
    
    def _load_onnx(self):
        """Pre-load ONNX engine if available."""
        try:
            from onnx_engine import onnx_engine  # pylint: disable=import-outside-toplevel
            self.onnx_model = onnx_engine
            if self.onnx_model:
                logger.success("[ENGINE] ONNX Production Core Ready.")
        except Exception as e:  # pylint: disable=broad-except
            logger.warning(f"[ENGINE] ONNX Core offline: {e}")

    def _load_pytorch(self):
        """Pre-load PyTorch engine if available."""
        if torch is None:
            logger.warning("[ENGINE] PyTorch not found in environment.")
            return

        try:
            # Import outside top level to handle missing files/dependencies gracefully
            # pylint: disable=import-outside-toplevel,import-error
            from ai_pytorch import torch_engine
            self.pt_model = torch_engine
            logger.success("[ENGINE] PyTorch Engine Ready.")
        except (ImportError, ModuleNotFoundError) as e:
            logger.error(f"[ENGINE] Core import failed: {e}")
        except Exception as e: # pylint: disable=broad-except
            logger.error(f"[ENGINE] Core offline: {e}")

    def _auto_select_engine(self):
        """Prioritize ONNX for production, fallback to PyTorch."""
        if hasattr(self, 'onnx_model') and self.onnx_model:
            self.active_engine = "ONNX"
        elif self.pt_model:
            self.active_engine = "PyTorch"
        else:
            self.active_engine = None
        
        if self.active_engine:
            logger.info(f"[ENGINE] Auto-selected: {self.active_engine} (Optimized for Production)")
        else:
            logger.critical("[ENGINE] NO ENGINES READY.")

    def _is_engine_ready(self, engine_name):
        """Check if specific engine is loaded and active."""
        if engine_name == "PyTorch":
            return self.pt_model is not None
        if engine_name == "ONNX":
            return hasattr(self, 'onnx_model') and self.onnx_model is not None
        return False

    def sync(self):
        """Refresh engine state."""
        self._auto_select_engine()

    def set_engine(self, engine_name):
        """Toggle between AI engines."""
        return engine_name == "PyTorch"

    def get_current_labels(self):
        """Returns labels directly from the active model backend."""
        if self.pt_model and hasattr(self.pt_model, 'classes'):
            return self.pt_model.classes
        return ['Anthracnose', 'Dieback', 'Healthy', 'Leaf Spot', 'Powdery Mildew'] # Fallback

    def predict(self, image_path):
        """Unified Prediction Entry Point."""
        start_time = time.time()
        
        # 1. Fallback if something changed
        if not self.active_engine or not self._is_engine_ready(self.active_engine):
            self._auto_select_engine()

        try:
            # 1. ONNX Execution (Priority 1: High Speed)
            if self.active_engine == "ONNX" and self.onnx_model:
                result = self.onnx_model.predict(image_path)
                result['latency'] = f"{time.time() - start_time:.4f}s"
                return result

            # 2. PyTorch Execution (Priority 2: Reference/Legacy)
            if self.active_engine == "PyTorch" and self.pt_model:
                result = self.pt_model.predict(image_path)
                result['engine'] = "PyTorch Micro-AI ⚡"
                result['latency'] = f"{time.time() - start_time:.4f}s"
                return result
            
            return {"error": "No active model engine available"}

        except (RuntimeError, ValueError) as e:
            return {"error": f"Neural core runtime error: {str(e)}"}
        except Exception as e: # pylint: disable=broad-except
            return {"error": f"Neural core failure: {str(e)}"}

# Instantiate globally
engine = AINeuralEngine()

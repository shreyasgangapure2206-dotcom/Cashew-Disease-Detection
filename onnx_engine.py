"""
Cashew AI - High-Performance ONNX Production Engine (V3 PRO)
Optimized for ultra-fast, multi-threaded CPU inference.
"""
import os
import time
import json
import logging
from typing import Dict, Any

import numpy as np
import cv2  # pylint: disable=no-member

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    import onnxruntime as ort
except ImportError:
    ort = None
def softmax(x):
    """Numerically stable softmax implementation for NumPy."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

class CashewONNXEngine:
    """
    Enterprise-grade ONNX Engine with thread optimization and latency telemetry.
    """
    def __init__(self, model_path: str = "models/cashew_micro.onnx"):
        self.session = None
        self.classes = ['Anthracnose', 'Dieback', 'Healthy', 'Leaf Spot', 'Powdery Mildew']
        
        if ort is None:
            print("[ONNX] [FAIL] onnxruntime not installed.")
            return
        # 1. Load Classes from External Config if available
        classes_path = "models/classes.json"
        if os.path.exists(classes_path):
            try:
                with open(classes_path, 'r', encoding='utf-8') as f:
                    self.classes = json.load(f)
                    print(f"[ONNX] [OK] Classes synchronized from {classes_path}")
            except Exception as e:  # pylint: disable=broad-except
                print(f"[ONNX] [WARN] Failed to load classes.json: {e}")

        # 2. Optimized Session Initialization
        if os.path.exists(model_path):
            try:
                so = ort.SessionOptions()
                so.intra_op_num_threads = 4
                
                self.session = ort.InferenceSession(
                    model_path,
                    sess_options=so,
                    providers=["CPUExecutionProvider"]
                )
                
                # 3. Engine Warming (Cold Start Mitigation)
                input_name = self.session.get_inputs()[0].name
                dummy = np.zeros((1, 3, 224, 224), dtype=np.float32)
                self.session.run(None, {input_name: dummy})
                
                print(f"[ONNX] [OK] V3 PRO Engine Ignited: {model_path} (4 Threads)")
            except Exception as e:  # pylint: disable=broad-except
                print(f"[ONNX] [FAIL] Engine ignition failed: {e}")
            print(f"[ONNX] [WARN] Production model missing at {model_path}")
    def preprocess(self, image_path: str):
        """Standard Forensic Image Preprocessing."""
        img = cv2.imread(image_path)  # pylint: disable=no-member
        if img is None:
            raise ValueError(f"CRITICAL: Specimen at {image_path} is unreachable or corrupt.")
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member
        img = cv2.resize(img, (224, 224))  # pylint: disable=no-member
        
        # Normalize (Reference: ImageNet mean/std)
        img = img.astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img = (img - mean) / std
        
        # HWC -> NCHW
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def _calculate_metrics(self, image_path: str, prediction: str) -> dict:
        """
        High-Performance Colorimetric Bridge (Intelligence V4).
        Identical signature detection to PyTorch engine for cross-validation reliability.
        """
        if prediction == "Healthy":
            return {"area_pct": 0.0, "severity": "Healthy (निरोगी)", "nci": 99.1}
            
        try:
            img = cv2.imread(image_path)
            if img is None:
                return {"area_pct": 0.0, "severity": "Unknown", "nci": 0.0}

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, leaf_mask = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
            total_leaf_px = cv2.countNonZero(leaf_mask)
            
            if total_leaf_px < 500:
                return {"area_pct": 0.0, "severity": "Invalid", "nci": 0.0}

            # Signature Detection
            mask_brown = cv2.inRange(hsv, np.array([10, 50, 20]), np.array([30, 255, 200]))
            mask_white = cv2.inRange(hsv, np.array([0, 0, 160]), np.array([180, 40, 255]))
            
            disease_mask = cv2.bitwise_and(cv2.bitwise_or(mask_brown, mask_white), leaf_mask)
            disease_px = cv2.countNonZero(disease_mask)
            pct = (disease_px / total_leaf_px) * 100.0
            
            # Neural Consistency Bridge
            nci = 100.0
            if prediction in ["Anthracnose", "Dieback"] and disease_px < (total_leaf_px * 0.01):
                nci = 42.0
            elif prediction == "Healthy" and disease_px > (total_leaf_px * 0.18):
                nci = 28.0

            # Standardized Severity
            if pct > 45:
                sev = "Critical (अति-गंभीर)"
            elif pct > 25:
                sev = "High (गंभीर)"
            elif pct > 10:
                sev = "Moderate (मध्यम)"
            elif pct > 2:
                sev = "Low (सुरुवात)"
            else:
                sev = "Minimal (किमान)"

            return {"area_pct": round(pct, 2), "severity": sev, "nci": round(nci, 1)}
        except Exception:
            return {"area_pct": 0.0, "severity": "Engine Error", "nci": 0.0}

    def predict(self, image_path: str) -> Dict[str, Any]:
        """Diagnostic Pipeline with Latency Breakdown."""
        if not self.session:
            return {"error": "ONNX engine offline"}

        start_time = time.time()
        try:
            # 1. PREPROCESS
            pre_start = time.time()
            input_tensor = self.preprocess(image_path)
            pre_time = time.time() - pre_start
            
            # 2. INFERENCE
            infer_start = time.time()
            input_name = self.session.get_inputs()[0].name
            outputs = self.session.run(None, {input_name: input_tensor})
            infer_time = time.time() - infer_start
            
            # 3. POSTPROCESS (Diagnostic Synthesis)
            post_start = time.time()
            logits = outputs[0][0]
            probs = softmax(logits)
            
            idx = np.argmax(probs)
            prediction = self.classes[idx]
            confidence = float(probs[idx] * 100)
            
            # Multi-ranking
            prob_dict = {self.classes[i]: float(probs[i] * 100) for i in range(len(self.classes))}
            sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
            top3 = [{"label": k, "conf": round(v, 2)} for k, v in sorted_probs[:3]]

            # Intelligence V4 Metric Injection
            metrics = self._calculate_metrics(image_path, prediction)
            inf_area = metrics['area_pct']
            severity = metrics['severity']
            nci_score = metrics['nci']
            
            # Hybrid Risk Logic (Calibration V4)
            if inf_area > 40 or (inf_area > 20 and nci_score < 60):
                risk_level = "CRITICAL"
            elif inf_area > 20:
                risk_level = "MODERATE"
            elif inf_area > 5:
                risk_level = "LOW"
            else:
                risk_level = "MINIMAL"
            
            # Expert Advice Hub (Intelligence V4)
            advice_hub = {
                "Anthracnose": [
                    "Isolate specimen locally",
                    "Apply rapid copper treatment",
                    "Prune at 45 degree angle"
                ],
                "Dieback": [
                    "Prune heavily into healthy wood",
                    "Sterilize blade after every cut",
                    "Burn infected prunings"
                ],
                "Leaf Spot": [
                    "Remove affected leaves",
                    "Increase tree spacing",
                    "Irrigate at base only"
                ],
                "Powdery Mildew": [
                    "Apply sulfur dust",
                    "Prune for maximum light",
                    "Check surrounding trees"
                ],
                "Healthy": [
                    "Standard monitoring",
                    "Ensure balanced N-K levels",
                    "Inspect monthly"
                ]
            }
            advice = advice_hub.get(prediction, ["Professional agronomist consultation suggested"])

            post_time = time.time() - post_start
            total_time = time.time() - start_time

            return {
                "prediction": prediction,
                "confidence": confidence,
                "top3": top3,
                "risk_level": risk_level,
                "advice": advice,
                "infection_area": inf_area,
                "severity": severity,
                "nci": nci_score,
                "engine": "ONNX Quantized Engine V4 (Ultra)",
                "latency": f"{total_time:.4f}s",
                "latency_breakdown": {
                    "preprocess": f"{pre_time:.4f}s",
                    "inference": f"{infer_time:.4f}s",
                    "postprocess": f"{post_time:.4f}s"
                },
                "probabilities": prob_dict
            }
        except Exception as e:  # pylint: disable=broad-except
            return {"error": f"Diagnostic Runtime Fault: {str(e)}"}
# Global Instance
onnx_engine = None
if os.path.exists("models/cashew_micro.onnx"):
    onnx_engine = CashewONNXEngine("models/cashew_micro.onnx")

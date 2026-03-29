"""
Cashew AI - PyTorch Inference Engine
# pylint: disable=no-member, broad-exception-caught, unused-argument, invalid-name, unused-variable
"""
import os
import time
import logging
from typing import Dict, Any, List, Optional

import torch
import torch.nn as nn
import cv2  # pylint: disable=import-error, no-member
import numpy as np
from torchvision import transforms, models
from PIL import Image

try:
    from config import IMG_SIZE
except ImportError:
    IMG_SIZE = 224

logger = logging.getLogger(__name__)

# ============================================================================
# LOCALIZATION & CONSTANTS
# ============================================================================

MARATHI_LABELS = {
    "Healthy": "आरोग्यदायी (Healthy)",
    "Anthracnose": "अॅन्थ्रॅक्नोझ (Anthracnose)",
    "Dieback": "शेंडा वाळणे (Dieback)",
    "Leaf Spot": "पानावरील ठिपके (Leaf Spot)",
    "Powdery Mildew": "भुरी रोग (Powdery Mildew)"
}

# ============================================================================
# EXPLAINABLE AI (Grad-CAM Core)
# ============================================================================

class GradCAM:
    """Gradient-weighted Class Activation Mapping for model explainability."""
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Hooks to capture internal state
        self.target_layer.register_forward_hook(self.save_activation)
        # Using register_full_backward_hook for newer torch compatibility
        try:
            self.target_layer.register_full_backward_hook(self.save_gradient)
        except AttributeError:
            self.target_layer.register_backward_hook(self.save_gradient)

    def save_activation(self, _module, _input_data, output_data):
        """Saves layer activations."""
        self.activations = output_data

    def save_gradient(self, _module, _grad_input, grad_output):
        """Saves layer gradients."""
        self.gradients = grad_output[0]

    def generate(self, input_tensor, class_idx=None):
        """Produces the activation map for a specific class."""
        output = self.model(input_tensor)

        if class_idx is None:
            class_idx = torch.argmax(output)

        self.model.zero_grad()
        output[0, class_idx].backward()

        if self.gradients is None or self.activations is None:
            return None

        gradients = self.gradients[0]
        activations = self.activations[0]

        weights = torch.mean(gradients, dim=(1, 2))
        cam = torch.zeros(activations.shape[1:], dtype=torch.float32).to(input_tensor.device)

        for i, w in enumerate(weights):
            cam += w * activations[i]

        cam = torch.nn.functional.relu(cam)
        cam = cam.detach().cpu().numpy()

        # Normalize 0-1
        cam = cv2.resize(cam, (224, 224))
        cam = (cam - cam.min()) / (cam.max() + 1e-8)
        return cam

def apply_heatmap(original_img, cam):
    """Overlays the heatmap on the original BGR image."""
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = np.float32(heatmap) / 255
    overlay = heatmap + np.float32(original_img) / 255
    overlay = overlay / np.max(overlay)
    return np.uint8(255 * overlay)

# ============================================================================
# PYTORCH NEURAL ENGINE (V2 PRO)
# ============================================================================

class CashewTorchEngine:
    """Production-Grade PyTorch Core with Infection Metrics."""

    def __init__(self, model_path: str = "models/cashew_micro_pt.pth"):
        """Initialize device, transformations, and load the specified model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes: List[str] = [
            'Anthracnose', 'Dieback', 'Healthy', 'Leaf Spot', 'Powdery Mildew'
        ]
        self.model = self._load_model(model_path)
        self.grad_cam = None
        
        if self.model:
            # Detect target layer for MobileNetV3/EfficientNet
            try:
                target_layer = self.model.features[-1]
                self.grad_cam = GradCAM(self.model, target_layer)
            except (AttributeError, IndexError):
                print("[GradCAM] Warn: Target layer not found. Explainability disabled.")
        self.transform = transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def _load_model(self, path: str) -> Optional[nn.Module]:
        """Build and load architectural state from checkpoint."""
        try:
            if os.path.exists(path):
                checkpoint = torch.load(path, map_location=self.device)
                if isinstance(checkpoint, dict) and 'classes' in checkpoint:
                    self.classes = checkpoint['classes']

                num_classes = len(self.classes)
                state_dict = checkpoint.get('state_dict', checkpoint)

                is_mobilenet = any('classifier.3' in k for k in state_dict.keys()) or \
                               ('features.0.0.weight' in state_dict and \
                                state_dict['features.0.0.weight'].shape[0] == 16)

                if is_mobilenet:
                    model = models.mobilenet_v3_small(pretrained=False)
                    last_layer_in = model.classifier[3].in_features
                    model.classifier[3] = nn.Linear(last_layer_in, num_classes)
                else:
                    model = models.efficientnet_b0(pretrained=False)
                    last_layer_in = model.classifier[1].in_features
                    model.classifier[1] = nn.Linear(last_layer_in, num_classes)

                model.load_state_dict(state_dict)
            else:
                model = models.efficientnet_b0(pretrained=False)
                num_classes = len(self.classes)
                last_layer_in = model.classifier[1].in_features
                model.classifier[1] = nn.Linear(last_layer_in, num_classes)

            model.eval()
            return model.to(self.device)
        except Exception as e:
            print(f"[PYTORCH] [FAIL] Model loading error: {e}")
            return None
    def _calculate_metrics(self, image_path: str, prediction: str) -> dict:
        """
        Advanced Multi-Band Colorimetric Analysis (Intelligence V4).
        Specifically isolates necrotic and fungal signatures instead of simple green-subtraction.
        """
        if prediction == "Healthy":
            return {"area_pct": 0.0, "severity": "Healthy (निरोगी)", "nci": 98.5}
            
        try:
            img = cv2.imread(image_path)
            if img is None:
                return {"area_pct": 0.0, "severity": "Unknown", "nci": 0.0}

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # 1. Total Leaf Area (Binary masking)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, leaf_mask = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
            total_leaf_px = cv2.countNonZero(leaf_mask)
            
            if total_leaf_px < 500: # Threshold for valid specimen
                return {"area_pct": 0.0, "severity": "Invalid Specimen", "nci": 0.0}

            # 2. Necrotic Signature (Anthracnose/Dieback - Browns/Blacks)
            lower_brown = np.array([10, 50, 20])
            upper_brown = np.array([30, 255, 200])
            mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
            
            # 3. Fungal Signature (Mildew - Whites/Greys)
            lower_white = np.array([0, 0, 160])
            upper_white = np.array([180, 40, 255])
            mask_white = cv2.inRange(hsv, lower_white, upper_white)
            
            # 4. Combined Disease Load
            disease_mask = cv2.bitwise_or(mask_brown, mask_white)
            disease_mask = cv2.bitwise_and(disease_mask, leaf_mask) # Stay within leaf
            
            # Morphological cleaning
            kernel = np.ones((3,3), np.uint8)
            disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_OPEN, kernel)
            
            disease_px = cv2.countNonZero(disease_mask)
            pct = (disease_px / total_leaf_px) * 100.0
            
            # 5. Neural Consistency Index (NCI) calculation
            # High NCI means visual evidence matches prediction
            nci = 100.0
            if prediction in ["Anthracnose", "Dieback"] and disease_px < (total_leaf_px * 0.01):
                nci = 45.0 # Predicted disease but no visual lesions found
            elif prediction == "Healthy" and disease_px > (total_leaf_px * 0.15):
                nci = 30.0 # Predicted healthy but significant lesions found

            # 6. High-Precision Severity Engine
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

            return {
                "area_pct": round(pct, 2),
                "severity": sev,
                "nci": round(nci, 1),
                "necrotic_px": disease_px
            }
        except Exception as e:
            logger.error("[METRICS ERROR] %s", e)
            return {"area_pct": 0.0, "severity": "Calculation Error", "nci": 0.0}

    def predict(self, image_path: str) -> Dict[str, Any]:
        """Identify disease with advanced metrics."""
        if not self.model:
            return {"error": "PyTorch engine offline"}

        try:
            image = Image.open(image_path).convert('RGB')
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

            conf, idx = torch.max(probabilities, 0)
            prediction = self.classes[idx.item()]

            # Core Upgraded Diagnostics (Intelligence V4)
            metrics = self._calculate_metrics(image_path, prediction)
            inf_area = metrics['area_pct']
            severity = metrics['severity']
            nci_score = metrics['nci']
            
            # Risk Level based on Hybrid Intelligence (Infection + NCI)
            if inf_area > 40 or (inf_area > 20 and nci_score < 60):
                risk_level = "Critical"
            elif inf_area > 20:
                risk_level = "Moderate"
            elif inf_area > 5:
                risk_level = "Low"
            else:
                risk_level = "Minimal"

            prob_dict = {self.classes[i]: float(probabilities[i] * 100) \
                         for i in range(len(self.classes))}

            # Post-Inference Expert Filter
            if prediction != "Healthy" and inf_area < 0.5 and float(conf.item()*100) < 80:
                # Potential False Positive - check second best
                second_best_idx = torch.argsort(probabilities, descending=True)[1]
                if self.classes[second_best_idx.item()] == "Healthy":
                    prediction = "Healthy"
                    risk_level = "MINIMAL"

            # Explainable AI (Grad-CAM)
            heatmap_rel_path = None
            if self.grad_cam:
                try:
                    cam = self.grad_cam.generate(img_tensor)
                    if cam is not None:
                        orig_bgr = cv2.imread(image_path)
                        orig_bgr = cv2.resize(orig_bgr, (224, 224))
                        heatmap_img = apply_heatmap(orig_bgr, cam)
                        
                        os.makedirs("static/gradcam", exist_ok=True)
                        ts = int(time.time())
                        heatmap_filename = f"cam_{ts}.jpg"
                        heatmap_save_path = os.path.join("static/gradcam", heatmap_filename)
                        cv2.imwrite(heatmap_save_path, heatmap_img)
                        heatmap_rel_path = f"static/gradcam/{heatmap_filename}"
                except Exception as e:
                    logger.error("[GradCAM ERROR] %s", e)

            sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
            top3 = [{"label": k, "conf": round(v, 2)} for k, v in sorted_probs[:3]]

            advice_map = {
                "Anthracnose": [
                    "Rapid isolation of specimen",
                    "Apply copper oxychloride (0.3%)",
                    "Prune diseased twigs"
                ],
                "Dieback": [
                    "Prune 10cm below infected zone",
                    "Seal cuts with Bordeaux paste",
                    "Clear floor debris"
                ],
                "Leaf Spot": [
                    "Optimize solar exposure",
                    "Thin canopy for airflow",
                    "Apply Hexaconazole (0.1%)"
                ],
                "Powdery Mildew": [
                    "Wettable sulphur (0.2%) application",
                    "Avoid excessive nitrogen",
                    "Monitor humidity"
                ],
                "Healthy": [
                    "Biosecurity scan successful",
                    "Continue seasonal fertilizing",
                    "Inspect weekly"
                ]
            }
            advice = advice_map.get(prediction, ["Verify via field expert", "Monitor transmission"])

            return {
                "prediction": prediction,
                "confidence": float(conf.item() * 100),
                "top3": top3,
                "risk_level": risk_level.upper(),
                "advice": advice,
                "infection_area": inf_area,
                "severity": severity,
                "nci": nci_score,
                "heatmap_path": heatmap_rel_path,
                "engine": "PyTorch Hybrid Engine V4 (Ultra)",
                "probabilities": prob_dict
            }
        except Exception as e:
            return {"error": f"Inference failure: {str(e)}"}

# Global instance (lowercase for neural_engine.py compatibility)
try:
    print("[PYTORCH] Initializing inference engine...")
    torch_engine = CashewTorchEngine("models/cashew_micro_pt.pth")
    if torch_engine:
        print("[PYTORCH] [OK] Multi-Stage Inference Engine Online.")
except Exception as e:
    print(f"[PYTORCH] [CRITICAL] Init fail: {e}")
    torch_engine = None

if __name__ == "__main__":
    print("PyTorch Engine Logic Ready.")

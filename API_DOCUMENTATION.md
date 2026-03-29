# 📡 API DOCUMENTATION

## Base URL
```
http://127.0.0.1:5000
```

---

## 🔬 PREDICTION APIs

### 1. Predict Disease
**Endpoint**: `POST /predict`

**Description**: Upload image and get disease prediction

**Request**:
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -F "file=@leaf_image.jpg"
```

**Response**:
```json
{
  "id": 123,
  "prediction": "Anthracnose",
  "confidence": 87.5,
  "probabilities": {
    "Anthracnose": 87.5,
    "Dieback": 5.2,
    "Healthy": 2.1,
    "Leaf Spot": 3.8,
    "Powdery Mildew": 1.4
  },
  "infection_area": "35.2%",
  "severity": "High (गंभीर)",
  "risk_level": "Moderate",
  "image_path": "static/uploads/1774695355_leaf.jpg",
  "engine": "PyTorch (V2 PRO + XAI)",
  "metrics": {
    "latency": "2.04s"
  }
}
```

---

## 📊 STATISTICS APIs

### 2. Dashboard Stats
**Endpoint**: `GET /api/stats`

**Description**: Get all-time statistics

**Response**:
```json
{
  "total": 150,
  "diseased": 98,
  "healthy": 52,
  "distribution": {
    "Anthracnose": 45,
    "Dieback": 23,
    "Healthy": 52,
    "Leaf Spot": 18,
    "Powdery Mildew": 12
  },
  "trend": {
    "labels": ["Mar 22", "Mar 23", "Mar 24", "Mar 25", "Mar 26", "Mar 27", "Mar 28"],
    "data": [65.5, 72.3, 68.9, 75.2, 71.8, 69.4, 73.6]
  }
}
```

### 3. AI Insights
**Endpoint**: `GET /api/stats/ai-insights`

**Description**: Get AI-generated plantation insights (async)

**Response**:
```json
{
  "ai_insights": "Plantation health shows 34.7% healthy rate with Anthracnose as dominant pathogen (30%). Recommend increased fungicide application during monsoon season. Early detection improving with 73.6% recent health index."
}
```

### 4. Live Stats
**Endpoint**: `GET /api/stats/live`

**Description**: Real-time analytics

**Response**:
```json
{
  "total": 150,
  "healthy": 52,
  "pathogens": 98,
  "distribution": {...},
  "recent_confidence": [87.5, 92.3, 78.9, ...]
}
```

---

## 📜 HISTORY APIs

### 5. Get History
**Endpoint**: `GET /api/history`

**Description**: Get scan history (last 50)

**Response**:
```json
[
  {
    "id": 123,
    "prediction": "Anthracnose",
    "confidence": 87.5,
    "image": "static/uploads/1774695355_leaf.jpg",
    "date": "2026-03-28 16:45:30"
  },
  ...
]
```

### 6. Clear History
**Endpoint**: `POST /api/history/clear`

**Description**: Delete all scan history

**Response**:
```json
{
  "success": true,
  "message": "History cleared"
}
```

---

## 🧬 FORENSIC APIs

### 7. Forensic Report
**Endpoint**: `GET /api/report/forensic/<report_id>`

**Description**: Get AI-generated forensic analysis

**Response**:
```json
{
  "summary": "Anthracnose infection detected with moderate severity",
  "micro_observations": "Fungal spores visible on leaf surface with characteristic brown lesions",
  "steps": [
    "Apply Carbendazim 0.1% spray",
    "Remove infected leaves",
    "Monitor for 14 days"
  ],
  "quarantine": "Isolate affected plants within 5m radius",
  "recommendation": "Increase spray frequency during monsoon"
}
```

---

## 🎓 DATA COLLECTION APIs

### 8. Dataset Stats
**Endpoint**: `GET /api/data_collection/stats`

**Description**: Get dataset statistics

**Response**:
```json
{
  "success": true,
  "stats": {
    "total_images": 1200,
    "total_labels": 450,
    "total_classes": 5
  }
}
```

### 9. Save Label
**Endpoint**: `POST /api/save-label`

**Description**: Save YOLO format bounding box labels

**Request**:
```json
{
  "image": "leaf_001.jpg",
  "boxes": [
    {
      "cls": 0,
      "x": 0.5,
      "y": 0.5,
      "w": 0.3,
      "h": 0.3
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "message": "Label saved: leaf_001.txt"
}
```

### 10. Prepare Dataset
**Endpoint**: `POST /api/prepare-dataset`

**Description**: Create train/val split

**Response**:
```json
{
  "success": true,
  "message": "Dataset optimized: 5 classes, 1200 images ready",
  "classes": ["Anthracnose", "Dieback", "Healthy", "Leaf Spot", "Powdery Mildew"]
}
```

---

## 🔥 TRAINING APIs

### 11. Start Training
**Endpoint**: `POST /api/train`

**Description**: Trigger model training in background

**Response**:
```json
{
  "success": true,
  "status": "training_started",
  "message": "Neural engine training initiated. Check console for progress."
}
```

### 12. Training Status
**Endpoint**: `GET /api/train/status`

**Description**: Get current training status

**Response**:
```json
{
  "status": "running",
  "log": "Epoch [5/10] - Loss: 0.3245 | Acc: 89.2% | Val Acc: 87.5%"
}
```

### 13. Reload Model
**Endpoint**: `POST /api/reload-model`

**Description**: Reload neural engine after training

**Response**:
```json
{
  "success": true,
  "message": "Neural engine reloaded successfully"
}
```

---

## 🔧 SYSTEM APIs

### 14. Engine Status
**Endpoint**: `GET /api/engine/status`

**Description**: Get neural engine status

**Response**:
```json
{
  "active_engine": "PyTorch",
  "available": ["TensorFlow", "PyTorch"],
  "labels": ["Anthracnose", "Dieback", "Healthy", "Leaf Spot", "Powdery Mildew"],
  "health": "STABLE"
}
```

### 15. Health Check
**Endpoint**: `GET /health`

**Description**: System health status

**Response**:
```json
{
  "status": "healthy",
  "active_engine": "PyTorch",
  "components": {
    "model": "ONLINE",
    "ollama": "ONLINE"
  }
}
```

---

## 🎯 ERROR CODES

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 404 | Not Found (report/resource missing) |
| 500 | Server Error |
| 503 | Service Unavailable (AI offline) |

---

## 🔐 AUTHENTICATION

Currently no authentication required. For production:
- Add JWT tokens
- Implement API keys
- Rate limiting

---

## 📝 NOTES

- All image uploads limited to 50MB
- Supported formats: JPG, JPEG, PNG, GIF
- Model inference: ~2s per image
- Training: 30-60 minutes (depends on dataset size)
- Cache TTL: 60 seconds for dashboard stats

---

## 🚀 RATE LIMITS

No rate limits currently. Recommended for production:
- 100 requests/minute per IP
- 1000 requests/hour per IP

---

## 📞 SUPPORT

For API issues or questions:
- GitHub Issues: [Project Issues](https://github.com/yourusername/cashew-disease-detection/issues)
- Email: support@cashewai.com

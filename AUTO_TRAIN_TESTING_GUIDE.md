# 🧪 AUTO TRAIN SYSTEM - TESTING GUIDE

## ✅ SERVER STATUS
Flask running on: **http://127.0.0.1:5000**
- Neural Engine: **ONLINE** ✅
- Ollama AI: **ENABLED** ✅

## 🎯 TESTING STEPS

### 1. Test Data Collection Page
```
URL: http://127.0.0.1:5000/data-collection
```

**Expected**:
- Page loads fast (< 1 second)
- Stats show: Total Images, YOLO Annotations, Active Classes
- All buttons visible and working

### 2. Test Label Saving
**Steps**:
1. Click "Drop specimens here" or click to upload images
2. Draw bounding boxes on the image (click and drag)
3. Select disease class from sidebar
4. Click "SAVE DIAGNOSTIC"

**Expected**:
- Status shows: "✓ Data successfully committed to training buffer"
- File created: `dataset/labels/[image_name].txt`
- YOLO format: `class x_center y_center width height`

### 3. Test Dataset Optimization
**Steps**:
1. Click "OPTIMIZE DATASET" button

**Expected**:
- Status shows: "✓ Dataset optimized: X classes, Y images ready"
- Folders created: `dataset/train/` and `dataset/val/`
- Images organized by class

### 4. Test Training Trigger
**Steps**:
1. Click "TRAIN AI NEURAL ENGINE" button
2. Confirm dialog

**Expected**:
- Status shows: "🚀 Initiating training pipeline..."
- Then: "✓ Training started! Monitor console for progress"
- Training runs in background
- Status updates every 5 seconds: "🔥 Training in progress..."

### 5. Test Training Status
**Automatic** (polls every 5 seconds):
- While training: "🔥 Training in progress..."
- When complete: "✓ Training complete! Reloading model..."
- Then: "✓ Neural engine updated successfully!"

### 6. Verify Model Reload
**After training completes**:
- Go to Detection page
- Upload test image
- Should use NEW trained model
- Check confidence scores

## 🔧 API ENDPOINTS TO TEST

### Test Stats API
```bash
curl http://127.0.0.1:5000/api/data_collection/stats
```

**Expected Response**:
```json
{
  "success": true,
  "stats": {
    "total_images": 1200,
    "total_labels": 0,
    "total_classes": 5
  }
}
```

### Test Save Label API
```bash
curl -X POST http://127.0.0.1:5000/api/save-label \
  -H "Content-Type: application/json" \
  -d '{"image":"test.jpg","boxes":[{"cls":0,"x":0.5,"y":0.5,"w":0.2,"h":0.2}]}'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Label saved: test.txt"
}
```

### Test Training Trigger
```bash
curl -X POST http://127.0.0.1:5000/api/train
```

**Expected Response**:
```json
{
  "success": true,
  "status": "training_started",
  "message": "Neural engine training initiated..."
}
```

### Test Training Status
```bash
curl http://127.0.0.1:5000/api/train/status
```

**Expected Response**:
```json
{
  "status": "idle",
  "message": "No active training session"
}
```

## 📁 FILES TO CHECK

After labeling and saving:
- `dataset/labels/[image_name].txt` - YOLO format labels

After dataset optimization:
- `dataset/train/Anthracnose/` - Training images
- `dataset/train/Dieback/`
- `dataset/train/Healthy/`
- `dataset/train/Leaf Spot/`
- `dataset/train/Powdery Mildew/`
- `dataset/val/[same structure]` - Validation images

After training:
- `models/cashew_micro_pt.pth` - Updated model weights

## 🚨 TROUBLESHOOTING

### Labels not saving?
- Check browser console for errors
- Verify `dataset/labels/` folder exists
- Check Flask console for "[LABEL SAVE ERROR]"

### Training not starting?
- Verify `train_pytorch.py` exists
- Check Flask console for "[TRAINING START ERROR]"
- Ensure dataset has train/val folders

### Model not reloading?
- Check Flask console for sync messages
- Verify new model file exists
- Try manual reload: `curl -X POST http://127.0.0.1:5000/api/reload-model`

## ✅ SUCCESS INDICATORS

- ✅ Page loads in < 1 second
- ✅ Labels save to `dataset/labels/`
- ✅ Dataset optimizer creates train/val folders
- ✅ Training starts in background
- ✅ Status updates every 5 seconds
- ✅ Model auto-reloads when training completes

## 🎉 READY TO USE!

Your auto-train system is fully operational. Go to the Data Collection page and start labeling!

# 🌿 Cashew Disease Detection - AI Platform

**Ultra Pro Max AI-powered disease detection system for cashew plants using deep learning.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

- 🧠 **AI-Powered Detection** - EfficientNetV2-B3 deep learning model
- 🎯 **5 Disease Classes** - Anthracnose, Dieback, Healthy, Leaf Spot, Powdery Mildew
- 📊 **Real-time Analytics** - Live dashboard with statistics
- 🔥 **Ultra Pro UI** - Gaming-style interface with neon effects
- 🔔 **Live Notifications** - Real-time detection alerts
- 🔊 **Sound Feedback** - Professional audio notifications
- 📱 **Responsive Design** - Works on all devices
- 🤖 **AI Assistant** - Ollama integration for insights

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### Detection Interface
![Detection](https://via.placeholder.com/800x400?text=Detection+Screenshot)

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.11
- **ML Framework**: TensorFlow 2.15
- **Model**: EfficientNetV2-B3 (Transfer Learning)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Custom glassmorphism design
- **AI Integration**: Ollama (optional)

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cashew-disease-detection.git
cd cashew-disease-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
```bash
python init_db.py
```

5. **Run the application**
```bash
python app.py
```

6. **Open browser**
```
http://127.0.0.1:5000
```

## 🎯 Model Training

### Quick Training
```bash
python train_model_pro.py
```

### Google Colab Training (Recommended)
1. Upload `training_notebook.ipynb` to Google Colab
2. Upload dataset to Google Drive
3. Run all cells
4. Download trained model

### Training Features
- ✅ 2-Phase training (frozen → fine-tuning)
- ✅ Class weight balancing
- ✅ Advanced data augmentation
- ✅ Learning rate scheduling
- ✅ Early stopping
- ✅ TensorBoard logging

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Architecture | EfficientNetV2-B3 |
| Input Size | 224x224 |
| Classes | 5 |
| Accuracy | 90%+ |
| Parameters | ~14M |

## 🌍 Deployment

### Option 1: Render (Recommended)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Deploy automatically

### Option 2: Railway
1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Deploy from GitHub
4. Auto-configured

### Option 3: Local Production
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📁 Project Structure

```
cashew-disease-detection/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── predict.py             # Prediction logic
├── train_model_pro.py     # Training script
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment config
├── models/               # Trained models
│   ├── cashew_model.keras
│   └── config.json
├── static/               # Static files
│   ├── css/
│   ├── uploads/
│   └── favicon.svg
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── detection.html
│   ├── history.html
│   └── report.html
└── dataset/              # Training data
    ├── Anthracnose/
    ├── Dieback/
    ├── Healthy/
    ├── Leaf Spot/
    └── Powdery Mildew/
```

## 🎮 Usage

1. **Upload Image** - Drag & drop or browse
2. **Analyze** - AI processes the image
3. **View Results** - Get disease prediction with confidence
4. **See Report** - Detailed analysis with recommendations
5. **Track History** - View all past detections

## 🔧 Configuration

Edit `.env` file:
```env
SECRET_KEY=your-secret-key
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Shreyas**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- TensorFlow team for the amazing framework
- EfficientNet authors for the model architecture
- Flask community for the web framework
- All contributors and supporters

## 📞 Support

For support, email your@email.com or open an issue on GitHub.

---

**Made with ❤️ and 🔥 by Shreyas**

⭐ Star this repo if you find it helpful!

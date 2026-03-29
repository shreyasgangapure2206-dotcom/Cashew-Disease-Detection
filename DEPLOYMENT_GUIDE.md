# 🚀 DEPLOYMENT GUIDE - Step by Step

## 📋 Prerequisites

1. **Install Git**
   - Download: https://git-scm.com/download/win
   - Install with default settings
   - Restart terminal after installation

2. **Create GitHub Account**
   - Go to: https://github.com
   - Sign up if you don't have an account

3. **Create Render Account**
   - Go to: https://render.com
   - Sign up with GitHub (recommended)

---

## 🔥 STEP 1: PREPARE PROJECT

### 1.1 Clean Up Large Files

Run these commands in PowerShell:

```powershell
# Remove dataset (too large for GitHub)
Remove-Item -Recurse -Force dataset -ErrorAction SilentlyContinue

# Remove virtual environment
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# Remove pycache
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue

# Remove instance database
Remove-Item -Recurse -Force instance -ErrorAction SilentlyContinue
```

### 1.2 Verify Files

Make sure these files exist:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `models/cashew_model.keras` (your trained model)

---

## 🔥 STEP 2: GITHUB SETUP

### 2.1 Initialize Git

Open PowerShell in your project folder:

```powershell
# Initialize git
git init

# Check status
git status
```

### 2.2 Add Files

```powershell
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status
```

### 2.3 Commit

```powershell
# First commit
git commit -m "Initial commit - Cashew Disease Detection AI Platform"
```

### 2.4 Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `cashew-disease-detection`
3. Description: `AI-powered cashew disease detection using deep learning`
4. Make it **Public** (for free deployment)
5. **DON'T** initialize with README (we already have one)
6. Click **Create repository**

### 2.5 Push to GitHub

Copy the commands from GitHub (they'll look like this):

```powershell
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/cashew-disease-detection.git

# Rename branch to main
git branch -M main

# Push
git push -u origin main
```

**⚠️ IMPORTANT:** Replace `YOUR_USERNAME` with your actual GitHub username!

---

## 🔥 STEP 3: RENDER DEPLOYMENT

### 3.1 Create Web Service

1. Go to: https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Click **Connect GitHub** (if not connected)
4. Find your repository: `cashew-disease-detection`
5. Click **Connect**

### 3.2 Configure Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `cashew-disease-detection` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` |

### 3.3 Environment Variables (Optional)

Click **Advanced** → **Add Environment Variable**:

```
SECRET_KEY = your-secret-key-here
```

### 3.4 Deploy

1. Click **Create Web Service**
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors

### 3.5 Access Your App

Once deployed, you'll get a URL like:
```
https://cashew-disease-detection.onrender.com
```

---

## 🎯 TROUBLESHOOTING

### Issue: Model file too large

**Solution:** Use Git LFS (Large File Storage)

```powershell
# Install Git LFS
git lfs install

# Track model files
git lfs track "*.keras"
git lfs track "*.h5"

# Add .gitattributes
git add .gitattributes

# Commit and push
git commit -m "Add Git LFS for model files"
git push
```

### Issue: Deployment fails

**Check:**
1. All files in `requirements.txt` are correct
2. `Procfile` exists and is correct
3. Model file is included in repo
4. No syntax errors in `app.py`

### Issue: App crashes on Render

**Solutions:**
1. Check Render logs for errors
2. Increase timeout in `Procfile`:
   ```
   web: gunicorn app:app --timeout 120 --workers 2
   ```
3. Add more memory (upgrade plan if needed)

---

## 🔥 PYTORCH MODERNIZATION
If you are moving from TensorFlow to the **PyTorch Neural Engine** (`ai_pytorch.py`):

1.  **Requirements**: Add `torch` and `torchvision` to your `requirements.txt`.
2.  **Deployment**: In `app.py`, change your model loader to use `CashewClassifier` from `ai_pytorch.py`.
3.  **Stability**: PyTorch is generally more stable on Render/Railway due to lower initial memory overhead compared to TensorFlow.

---

## 🚀 ADVANCED DEPLOYMENT - PRODUCTION CHECKLIST
For large-scale or robust commercial deployments:

### 1. PostgreSQL Integration
SQLite is great for development, but for production, use a managed database like **Railway PostgreSQL** or **AWS RDS**.
- Update `DATABASE_URL` in your environment variables.

### 2. High-Performance Static Serving
Use **WhiteNoise** to serve your CSS/JS files at lightning speed without Nginx:
```python
# app.py
from whitenoise import WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')
```

### 3. Monitoring & Analytics
- **Health Checks**: Access `/health` to verify system status.
- **Charts**: Dashboard now supports live `Chart.js` analytics based on your real history data.

---

## 🔥 ALTERNATIVE: RAILWAY DEPLOYMENT

Railway is easier but has limited free tier.

### Railway Steps:

1. Go to: https://railway.app
2. Click **Start a New Project**
3. Choose **Deploy from GitHub repo**
4. Select your repository
5. Railway auto-detects everything
6. Click **Deploy**
7. Done! 🎉

---

## 📊 POST-DEPLOYMENT

### Update Model

To update your model after training:

```powershell
# Replace model file
# Copy new cashew_model.keras to models/

# Commit and push
git add models/cashew_model.keras
git commit -m "Update model with better accuracy"
git push

# Render will auto-deploy
```

### Monitor Performance

1. Check Render dashboard for:
   - CPU usage
   - Memory usage
   - Response times
   - Error logs

2. Set up monitoring:
   - Add health check endpoint
   - Enable email alerts

---

## 🎉 SUCCESS CHECKLIST

- ✅ Git installed
- ✅ GitHub repository created
- ✅ Code pushed to GitHub
- ✅ Render account created
- ✅ Web service deployed
- ✅ App accessible via URL
- ✅ Model predictions working
- ✅ UI loading correctly

---

## 🚀 NEXT STEPS

1. **Share Your App**
   - Add URL to README
   - Share on LinkedIn
   - Add to portfolio

2. **Improve Model**
   - Run `train_model_pro.py`
   - Get 90%+ accuracy
   - Update deployment

3. **Add Features**
   - User authentication
   - API endpoints
   - Mobile app
   - Analytics dashboard

---

## 📞 NEED HELP?

If you get stuck:

1. Check Render logs
2. Check GitHub Actions (if enabled)
3. Google the error message
4. Ask on Stack Overflow
5. Check Render documentation

---

**Made with 🔥 by Shreyas**

Good luck with deployment! 🚀

"""
Cashew Micro-AI Training Engine
Handles the training of PyTorch-based models for cashew disease identification.
"""
import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# ============================================================================
# MICRO-AI TRAINING ENGINE (PYTORCH)
# Developed for Cashew Disease Prediction - V2.0
# ============================================================================

# 1. Configuration
DATASET_PATH = "dataset"
BATCH_SIZE = 16
IMG_SIZE = 224
EPOCHS = 10
LEARNING_RATE = 0.001
SAVE_PATH = "models/cashew_micro_pt.pth"

# 2. Data Preparation (Micro Transformations)
data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

def train_model():
    """
    Main training loop for the Cashew Micro-AI model.
    """
    print("🚀 INITIALIZING PYTORCH MICRO-TRAINING ENGINE...")

    # Create models directory if not exists
    if not os.path.exists("models"):
        os.makedirs("models")

    # Load dataset
    if not os.path.exists(DATASET_PATH):
        print(f"❌ ERROR: Dataset path '{DATASET_PATH}' not found.")
        return

    full_dataset = datasets.ImageFolder(DATASET_PATH, transform=data_transforms['train'])
    class_names = full_dataset.classes
    num_classes = len(class_names)

    print(f"📊 Dataset Stats: {len(full_dataset)} images found in {num_classes} classes.")
    print(f"🏷️ Classes: {class_names}")

    # Split (Simple 80/20 split)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_data, val_data = torch.utils.data.random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)

    # 3. Model Architecture (Micro: MobileNetV3-Small)
    print("🧠 Building Micro-AI Model (MobileNetV3 Small)...")
    model = models.mobilenet_v3_small(weights='IMAGENET1K_V1')

    # Replace final classifier for our classes
    last_layer_in = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(last_layer_in, num_classes)

    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    print(f"⚡ Device detected: {device}")

    # 4. Optimization
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 5. Training Loop
    print("\n" + "="*40)
    print("🎬 STARTING TRAINING (Micro-Optimization)")
    print("="*40)

    for epoch in range(EPOCHS):
        start_time = time.time()
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        epoch_loss = running_loss / train_size
        epoch_acc = 100. * correct / total

        # Validation pass
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        val_acc = 100. * val_correct / val_total
        duration = time.time() - start_time

        print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {epoch_loss:.4f} | "
              f"Acc: {epoch_acc:.2f}% | Val Acc: {val_acc:.2f}% | Time: {duration:.1f}s")

    # 6. Finalize & Save
    print("\n" + "="*40)
    print("🏆 TRAINING COMPLETE!")
    print(f"💾 Saving model to {SAVE_PATH}...")

    # Save model and metadata (Labels)
    state = {
        'state_dict': model.state_dict(),
        'classes': class_names
    }
    torch.save(state, SAVE_PATH)
    print("🏁 [SUCCESS] Micro-Model saved.")

if __name__ == "__main__":
    train_model()

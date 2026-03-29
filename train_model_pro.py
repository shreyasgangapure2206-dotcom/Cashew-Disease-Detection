"""
🔥 ULTRA PRO MAX Training Script
Production-grade model training with all optimizations
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from datetime import datetime
import json

# Disable oneDNN warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

print("=" * 80)
print("🔥 ULTRA PRO MAX TRAINING PIPELINE")
print("=" * 80)

# ==================== CONFIGURATION ====================
IMG_SIZE = 224
BATCH_SIZE = 16  # 🔥 Smaller batch = better generalization
EPOCHS = 50
INITIAL_LR = 0.001
FINE_TUNE_LR = 0.0001  # 🔥 Lower LR for fine-tuning

LABELS = ['Anthracnose', 'Dieback', 'Healthy', 'Leaf Spot', 'Powdery Mildew']
NUM_CLASSES = len(LABELS)

DATASET_PATH = 'dataset'
MODEL_SAVE_PATH = 'models/cashew_model_pro.h5'
CONFIG_SAVE_PATH = 'models/config.json'

print(f"📐 Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"📦 Batch size: {BATCH_SIZE}")
print(f"🔢 Classes: {NUM_CLASSES}")
print(f"📊 Epochs: {EPOCHS}")

# ==================== DATA AUGMENTATION (UPGRADED) ====================
print("\n🎨 Creating ULTRA data augmentation pipeline...")

data_augmentation = keras.Sequential([
    layers.RandomRotation(0.2),
    layers.RandomFlip("horizontal"),
    layers.RandomZoom(0.2),
    layers.RandomTranslation(0.2, 0.2),
    layers.RandomBrightness(0.2),  # 🔥 NEW
    layers.RandomContrast(0.2),    # 🔥 NEW
], name='data_augmentation')

print("✅ Augmentation pipeline created with 6 layers")

# ==================== LOAD DATASET ====================
print("\n📂 Loading dataset...")

# Load full dataset
train_ds = keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.3,
    subset="training",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    label_mode='categorical',
    class_names=LABELS
)

val_ds = keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.3,
    subset="validation",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    label_mode='categorical',
    class_names=LABELS
)

# Performance optimization
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Apply augmentation to training set
train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y),
    num_parallel_calls=AUTOTUNE
)

print("✅ Dataset loaded and augmented")

# ==================== CALCULATE CLASS WEIGHTS ====================
print("\n⚖️ Calculating class weights for imbalanced data...")

# Count samples per class
class_counts = {}
for class_name in LABELS:
    class_path = os.path.join(DATASET_PATH, class_name)
    if os.path.exists(class_path):
        count = len([f for f in os.listdir(class_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        class_counts[class_name] = count

total_samples = sum(class_counts.values())

# Calculate weights (inverse frequency)
class_weights = {}
for i, class_name in enumerate(LABELS):
    weight = total_samples / (NUM_CLASSES * class_counts[class_name])
    class_weights[i] = weight
    print(f"  {class_name}: {class_counts[class_name]} samples → weight: {weight:.2f}")

print("✅ Class weights calculated")

# ==================== BUILD MODEL ====================
print("\n🏗️ Building EfficientNetV2-B3 model...")

# Input layer
inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

# Normalization (divide by 255)
x = layers.Rescaling(1./255)(inputs)

# Base model
base_model = keras.applications.EfficientNetV2B3(
    include_top=False,
    weights='imagenet',
    input_tensor=x,
    pooling=None
)

# 🔥 PHASE 1: Freeze base model
base_model.trainable = False

# Add custom head
x = layers.GlobalAveragePooling2D(name='global_avg_pool')(base_model.output)
x = layers.BatchNormalization()(x)
x = layers.Dense(256, activation='relu', name='dense_256')(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(128, activation='relu', name='dense_128')(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax', name='predictions')(x)

model = keras.Model(inputs=inputs, outputs=outputs, name='cashew_disease_classifier')

print(f"✅ Model built: {model.name}")
print(f"📊 Total params: {model.count_params():,}")
print(f"🔒 Base model frozen: {not base_model.trainable}")

# ==================== COMPILE MODEL (PHASE 1) ====================
print("\n⚙️ Compiling model for Phase 1 (frozen base)...")

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=INITIAL_LR),
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=2, name='top_2_accuracy')]
)

print("✅ Model compiled")

# ==================== CALLBACKS ====================
print("\n📋 Setting up callbacks...")

callbacks = [
    # Early stopping
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ),
    
    # Model checkpoint
    keras.callbacks.ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    
    # 🔥 Learning rate reduction
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.3,
        patience=3,
        min_lr=1e-6,
        verbose=1
    ),
    
    # TensorBoard
    keras.callbacks.TensorBoard(
        log_dir=f'models/logs/efficientnetv2_b3_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        histogram_freq=1
    )
]

print("✅ Callbacks configured")

# ==================== PHASE 1: TRAIN WITH FROZEN BASE ====================
print("\n" + "=" * 80)
print("🚀 PHASE 1: Training with frozen base model")
print("=" * 80)

history_phase1 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20,  # First 20 epochs
    callbacks=callbacks,
    class_weight=class_weights,  # 🔥 Use class weights
    verbose=1
)

print("\n✅ Phase 1 training complete!")

# ==================== PHASE 2: FINE-TUNING ====================
print("\n" + "=" * 80)
print("🔥 PHASE 2: Fine-tuning (unfreezing last 30 layers)")
print("=" * 80)

# Unfreeze last 30 layers
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

print(f"🔓 Unfrozen last 30 layers")
print(f"📊 Trainable params: {sum([tf.size(w).numpy() for w in model.trainable_weights]):,}")

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=FINE_TUNE_LR),  # 🔥 Lower LR
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=2, name='top_2_accuracy')]
)

print("✅ Model recompiled with lower learning rate")

# Continue training
history_phase2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    initial_epoch=len(history_phase1.history['loss']),
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
)

print("\n✅ Phase 2 fine-tuning complete!")

# ==================== SAVE MODEL ====================
print("\n💾 Saving final model...")

model.save(MODEL_SAVE_PATH)
print(f"✅ Model saved: {MODEL_SAVE_PATH}")

# Save configuration
config = {
    "model_name": "EfficientNetV2-B3 Pro",
    "version": "2.0",
    "img_size": IMG_SIZE,
    "num_classes": NUM_CLASSES,
    "labels": LABELS,
    "accuracy": f"{max(history_phase2.history['val_accuracy']) * 100:.2f}",
    "dataset_size": f"~{total_samples} images",
    "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "batch_size": BATCH_SIZE,
    "epochs_phase1": 20,
    "epochs_phase2": EPOCHS,
    "augmentation": "6-layer pipeline",
    "class_weights": "enabled"
}

with open(CONFIG_SAVE_PATH, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ Config saved: {CONFIG_SAVE_PATH}")

# ==================== FINAL RESULTS ====================
print("\n" + "=" * 80)
print("🎉 TRAINING COMPLETE!")
print("=" * 80)

final_val_acc = max(history_phase2.history['val_accuracy']) * 100
final_val_loss = min(history_phase2.history['val_loss'])

print(f"\n📊 Final Results:")
print(f"  - Validation Accuracy: {final_val_acc:.2f}%")
print(f"  - Validation Loss: {final_val_loss:.4f}")
print(f"  - Model: {MODEL_SAVE_PATH}")
print(f"  - Config: {CONFIG_SAVE_PATH}")

print("\n🚀 Model ready for deployment!")
print("=" * 80)

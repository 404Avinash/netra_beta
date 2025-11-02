"""
N.E.T.R.A. Machine Learning Model Training
==========================================
Trains XGBoost model for threat detection using historical sensor data.

Model Features:
- XGBoost Classifier (accurate, ~5MB)
- Trained on 1200 historical records
- Multi-class classification (CRITICAL/HIGH/MODERATE/LOW)
- Feature importance analysis
- Cross-validation for robustness

Author: Avinash Jha
Date: November 2, 2025
"""

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import json
from datetime import datetime

# Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Check for command-line argument to use large dataset
import sys
USE_LARGE_DATASET = '--large' in sys.argv or '-l' in sys.argv

# Create models directory if not exists
os.makedirs('../models', exist_ok=True)

print("="*70)
print("🤖 N.E.T.R.A. ML MODEL TRAINING")
print("="*70)
print(f"📅 Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🎯 Model Type: XGBoost Classifier")
if USE_LARGE_DATASET:
    print(f"📊 Data Source: netra_threat_log_large.csv (10K+ records)")
else:
    print(f"📊 Data Source: netra_threat_log.csv (1.2K records)")
print("="*70 + "\n")

# ============================================================================
# STEP 1: Load and Prepare Data
# ============================================================================

print("📂 STEP 1: Loading Data...")
try:
    # Select dataset based on command-line argument
    if USE_LARGE_DATASET:
        data_file = '../netra_threat_log_large.csv'
    else:
        data_file = '../netra_threat_log.csv'
    
    df = pd.read_csv(data_file)
    print(f"✅ Loaded {len(df)} records from {data_file}")
    print(f"📅 Date Range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    print(f"📍 Locations: {df['Location'].nunique()} unique locations")
    print(f"🗺️ States: {df['State'].nunique()} states")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# ============================================================================
# STEP 2: Feature Engineering
# ============================================================================

print("\n🔧 STEP 2: Feature Engineering...")

# Base sensor features
sensor_features = [
    'Fume_Detection',
    'Metal_Detection', 
    'GPR_Reading',
    'Ground_CV',
    'Drone_CV',
    'Disturbance',
    'Thermal'
]

# Create derived features for better ML performance
print("   Creating derived features...")

# Feature 1: Sensor correlations (multi-sensor fusion indicators)
df['Fume_Metal_Product'] = df['Fume_Detection'] * df['Metal_Detection'] / 100
df['CV_Average'] = (df['Ground_CV'] + df['Drone_CV']) / 2
df['Surface_Anomaly'] = (df['Disturbance'] + df['Thermal']) / 2

# Feature 2: High-risk combinations
df['High_Fume_Metal'] = ((df['Fume_Detection'] > 70) & (df['Metal_Detection'] > 70)).astype(int)
df['High_CV_Detection'] = ((df['Ground_CV'] > 70) | (df['Drone_CV'] > 70)).astype(int)
df['Multiple_Indicators'] = (
    (df['Fume_Detection'] > 60).astype(int) +
    (df['Metal_Detection'] > 60).astype(int) +
    (df['GPR_Reading'] > 60).astype(int) +
    (df['Disturbance'] > 60).astype(int)
)

# Feature 3: Explosive characteristics
# Encode explosive danger level
danger_encoder = LabelEncoder()
df['Danger_Level_Encoded'] = danger_encoder.fit_transform(df['Danger_Level'])

# Encode explosive class
class_encoder = LabelEncoder()
df['Explosive_Class_Encoded'] = class_encoder.fit_transform(df['Explosive_Class'])

# All features for training
all_features = sensor_features + [
    'Fume_Metal_Product',
    'CV_Average',
    'Surface_Anomaly',
    'High_Fume_Metal',
    'High_CV_Detection',
    'Multiple_Indicators',
    'Danger_Level_Encoded',
    'Explosive_Class_Encoded'
]

print(f"✅ Created {len(all_features)} features total")
print(f"   - Base sensors: {len(sensor_features)}")
print(f"   - Derived features: {len(all_features) - len(sensor_features)}")

# ============================================================================
# STEP 3: Prepare Training Data
# ============================================================================

print("\n📊 STEP 3: Preparing Training Data...")

# Features (X)
X = df[all_features].copy()

# Target (y) - Threat Level classification
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(df['Threat_Level'])

# Map threat levels
threat_level_mapping = {i: label for i, label in enumerate(target_encoder.classes_)}
print(f"   Threat Level Mapping: {threat_level_mapping}")

# Check for any missing values
if X.isnull().any().any():
    print("⚠️  Warning: Found missing values, filling with median...")
    X = X.fillna(X.median())

print(f"✅ Data prepared: {X.shape[0]} samples, {X.shape[1]} features")

# Class distribution
print("\n📈 Target Distribution:")
for level, count in zip(*np.unique(y, return_counts=True)):
    label = threat_level_mapping[level]
    percentage = (count / len(y)) * 100
    print(f"   {label:12s}: {count:4d} ({percentage:5.1f}%)")

# ============================================================================
# STEP 4: Split Data
# ============================================================================

print(f"\n✂️  STEP 4: Splitting Data (Test Size: {TEST_SIZE*100:.0f}%)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")

# ============================================================================
# STEP 5: Train XGBoost Model
# ============================================================================

print("\n🚀 STEP 5: Training XGBoost Model...")
print("   This may take 1-2 minutes...")

# XGBoost parameters optimized for threat detection
model = XGBClassifier(
    n_estimators=200,           # More trees for better accuracy
    max_depth=6,                # Deep enough to capture complex patterns
    learning_rate=0.1,          # Standard learning rate
    subsample=0.8,              # Use 80% of data per tree
    colsample_bytree=0.8,       # Use 80% of features per tree
    random_state=RANDOM_STATE,
    eval_metric='mlogloss',     # Multi-class log loss
    use_label_encoder=False,
    verbosity=0                 # Quiet mode
)

# Train the model
model.fit(X_train, y_train)
print("✅ Model training complete!")

# ============================================================================
# STEP 6: Model Evaluation
# ============================================================================

print("\n📊 STEP 6: Evaluating Model...")

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Accuracy scores
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\n🎯 Accuracy Scores:")
print(f"   Training Accuracy: {train_accuracy*100:.2f}%")
print(f"   Test Accuracy:     {test_accuracy*100:.2f}%")

# Cross-validation
print(f"\n🔄 {CV_FOLDS}-Fold Cross-Validation...")
cv_scores = cross_val_score(model, X, y, cv=CV_FOLDS, scoring='accuracy')
print(f"   CV Accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

# Classification report
print("\n📋 Classification Report (Test Set):")
report = classification_report(
    y_test, y_pred_test, 
    target_names=threat_level_mapping.values(),
    digits=3
)
print(report)

# Confusion matrix
print("\n🔢 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred_test)
print("    Predicted →")
print("Actual ↓")
for i, label in threat_level_mapping.items():
    print(f"{label:12s}: {cm[i]}")

# ============================================================================
# STEP 7: Feature Importance Analysis
# ============================================================================

print("\n📊 STEP 7: Feature Importance...")

# Get feature importance
feature_importance = pd.DataFrame({
    'Feature': all_features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 10 Most Important Features:")
for idx, row in feature_importance.head(10).iterrows():
    print(f"   {row['Feature']:30s}: {row['Importance']:.4f}")

# ============================================================================
# STEP 8: Save Model and Metadata
# ============================================================================

print("\n💾 STEP 8: Saving Model...")

# Save the XGBoost model
model_path = '../models/netra_xgboost_model.pkl'
joblib.dump(model, model_path)
print(f"✅ Model saved: {model_path}")

# Save encoders
encoders = {
    'target_encoder': target_encoder,
    'danger_encoder': danger_encoder,
    'class_encoder': class_encoder,
    'threat_level_mapping': threat_level_mapping
}
encoders_path = '../models/netra_encoders.pkl'
joblib.dump(encoders, encoders_path)
print(f"✅ Encoders saved: {encoders_path}")

# Save feature names (important for prediction)
features_path = '../models/netra_features.json'
with open(features_path, 'w') as f:
    json.dump({
        'sensor_features': sensor_features,
        'all_features': all_features,
        'feature_importance': feature_importance.to_dict('records')
    }, f, indent=2)
print(f"✅ Features saved: {features_path}")

# Save model metadata
metadata = {
    'model_type': 'XGBoost',
    'version': '1.0.0',
    'training_date': datetime.now().isoformat(),
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'train_accuracy': float(train_accuracy),
    'test_accuracy': float(test_accuracy),
    'cv_accuracy_mean': float(cv_scores.mean()),
    'cv_accuracy_std': float(cv_scores.std()),
    'num_features': len(all_features),
    'threat_levels': list(threat_level_mapping.values()),
    'feature_names': all_features,
    'class_distribution': {
        label: int(count) for label, count in 
        zip(threat_level_mapping.values(), np.bincount(y))
    }
}

metadata_path = '../models/netra_model_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✅ Metadata saved: {metadata_path}")

# Get model file size
model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f"\n📦 Model Size: {model_size_mb:.2f} MB")

# ============================================================================
# STEP 9: Test Prediction Function
# ============================================================================

print("\n🧪 STEP 9: Testing Prediction Function...")

def predict_threat(sensors, explosive_info):
    """
    Test prediction function (will be integrated into Streamlit)
    
    Args:
        sensors: dict with keys [fume, metal, gpr, ground_cv, drone_cv, disturbance, thermal]
        explosive_info: dict with keys [danger_level, explosive_class]
    
    Returns:
        dict with threat_level and probability
    """
    # Load model and encoders
    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    
    # Prepare features
    features = {
        'Fume_Detection': sensors['fume'],
        'Metal_Detection': sensors['metal'],
        'GPR_Reading': sensors['gpr'],
        'Ground_CV': sensors['ground_cv'],
        'Drone_CV': sensors['drone_cv'],
        'Disturbance': sensors['disturbance'],
        'Thermal': sensors['thermal']
    }
    
    # Derived features
    features['Fume_Metal_Product'] = sensors['fume'] * sensors['metal'] / 100
    features['CV_Average'] = (sensors['ground_cv'] + sensors['drone_cv']) / 2
    features['Surface_Anomaly'] = (sensors['disturbance'] + sensors['thermal']) / 2
    features['High_Fume_Metal'] = int(sensors['fume'] > 70 and sensors['metal'] > 70)
    features['High_CV_Detection'] = int(sensors['ground_cv'] > 70 or sensors['drone_cv'] > 70)
    features['Multiple_Indicators'] = sum([
        int(sensors['fume'] > 60),
        int(sensors['metal'] > 60),
        int(sensors['gpr'] > 60),
        int(sensors['disturbance'] > 60)
    ])
    
    # Encode explosive info
    features['Danger_Level_Encoded'] = encoders['danger_encoder'].transform([explosive_info['danger_level']])[0]
    features['Explosive_Class_Encoded'] = encoders['class_encoder'].transform([explosive_info['explosive_class']])[0]
    
    # Create feature array in correct order
    X_new = np.array([[features[f] for f in all_features]])
    
    # Predict
    prediction = model.predict(X_new)[0]
    probabilities = model.predict_proba(X_new)[0]
    
    threat_level = encoders['target_encoder'].inverse_transform([prediction])[0]
    confidence = float(probabilities[prediction] * 100)
    
    return {
        'threat_level': threat_level,
        'probability': confidence,
        'all_probabilities': {
            encoders['target_encoder'].inverse_transform([i])[0]: float(prob * 100)
            for i, prob in enumerate(probabilities)
        }
    }

# Test with sample data (use actual classes from dataset)
print("\n📝 Test Case 1: High Threat Scenario")
test_sensors_1 = {
    'fume': 85,
    'metal': 90,
    'gpr': 75,
    'ground_cv': 80,
    'drone_cv': 70,
    'disturbance': 65,
    'thermal': 60
}
test_explosive_1 = {
    'danger_level': 'Very High',
    'explosive_class': 'Primary Explosive'  # Use actual class from data
}

try:
    result_1 = predict_threat(test_sensors_1, test_explosive_1)
    print(f"   Predicted: {result_1['threat_level']} ({result_1['probability']:.1f}% confidence)")
except Exception as e:
    print(f"   ⚠️ Test failed: {e}")

print("\n📝 Test Case 2: Low Threat Scenario")
test_sensors_2 = {
    'fume': 15,
    'metal': 20,
    'gpr': 25,
    'ground_cv': 18,
    'drone_cv': 22,
    'disturbance': 10,
    'thermal': 12
}
test_explosive_2 = {
    'danger_level': 'Low',
    'explosive_class': 'Low Explosive'
}

try:
    result_2 = predict_threat(test_sensors_2, test_explosive_2)
    print(f"   Predicted: {result_2['threat_level']} ({result_2['probability']:.1f}% confidence)")
except Exception as e:
    print(f"   ⚠️ Test failed: {e}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*70)
print("✅ MODEL TRAINING COMPLETE!")
print("="*70)
print(f"\n📊 Summary:")
print(f"   • Model Type: XGBoost Classifier")
print(f"   • Test Accuracy: {test_accuracy*100:.2f}%")
print(f"   • CV Accuracy: {cv_scores.mean()*100:.2f}%")
print(f"   • Model Size: {model_size_mb:.2f} MB")
print(f"   • Features: {len(all_features)}")
print(f"   • Classes: {len(threat_level_mapping)}")
print(f"\n📁 Files Created:")
print(f"   • {model_path}")
print(f"   • {encoders_path}")
print(f"   • {features_path}")
print(f"   • {metadata_path}")
print(f"\n🚀 Next Steps:")
print(f"   1. Run 'pip install xgboost' if not installed")
print(f"   2. Integrate model into netra_unified_app.py")
print(f"   3. Test locally before deploying to Streamlit Cloud")
print("="*70)

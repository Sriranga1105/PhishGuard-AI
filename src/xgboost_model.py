import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# 1. Load dataset
df = pd.read_csv(r"D:\Intern_project\PhishGuard AI\data\processed\urldata.csv")

# 2. Split features & labels
X = df.drop(["Label", "Domain"], axis=1)
y = df["Label"]

# 3. Apply SMOTE to balance dataset
smote = SMOTE(random_state=42)
X_balanced, y_balanced = smote.fit_resample(X, y)

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# 5. Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Train XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train_scaled, y_train)

# 7. Predict probabilities and tune threshold
y_probs = model.predict_proba(X_test_scaled)[:, 1]

# Choose threshold (0.5 is default)
threshold = 0.5
y_pred = (y_probs >= threshold).astype(int)

# 8. Evaluation
print("\n🔍 Classification Report:")
print(classification_report(y_test, y_pred))
print(f"✅ Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"📈 AUC Score: {roc_auc_score(y_test, y_probs):.4f}")

# 9. Feature Importance Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=model.feature_importances_, y=X.columns)
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig(r"D:\Intern_project\PhishGuard AI\feature_importance1.png")
plt.show()

# 10. Save model and scaler
joblib.dump(model, r"D:\Intern_project\PhishGuard AI\models\xgb_model.pkl")
joblib.dump(scaler, r"D:\Intern_project\PhishGuard AI\models\scaler.pkl")
print("✅ Model and scaler saved.")
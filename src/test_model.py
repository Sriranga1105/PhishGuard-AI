import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, accuracy_score, 
                             roc_auc_score, confusion_matrix, ConfusionMatrixDisplay)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# 1. Load and inspect data
df = pd.read_csv(r"D:\Intern_project\PhishGuard AI\data\processed\urldata.csv")

# Check data quality
print("Data Overview:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\nMissing Values:")
print(df.isnull().sum())
print("\nClass Distribution:")
print(df['Label'].value_counts(normalize=True))

# 2. Preprocessing
# Drop non-feature columns
df = df.drop(['Domain'], axis=1)

# Convert all columns to numeric (safe guard)
df = df.apply(pd.to_numeric, errors='coerce')

# Handle missing values if any
df = df.dropna()

# 3. Split data
X = df.drop('Label', axis=1)
y = df['Label']

# Split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

# 4. Create preprocessing and modeling pipeline
pipeline = ImbPipeline([
    ('smote', SMOTE(random_state=42)),
    ('scaler', StandardScaler()),
    ('xgb', XGBClassifier(
        use_label_encoder=False, 
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1
    ))
])

# 5. Hyperparameter tuning
param_grid = {
    'xgb__learning_rate': [0.01, 0.1, 0.2],
    'xgb__max_depth': [3, 5, 7],
    'xgb__subsample': [0.8, 1.0],
    'xgb__colsample_bytree': [0.8, 1.0],
    'xgb__gamma': [0, 0.1, 0.2]
}

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring='roc_auc',
    cv=5,
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train)

# 6. Best model evaluation
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
y_probs = best_model.predict_proba(X_test)[:, 1]

print("\n🔥 Best Parameters:")
print(grid_search.best_params_)

print("\n📊 Performance Evaluation:")
print(classification_report(y_test, y_pred))
print(f"ROC AUC Score: {roc_auc_score(y_test, y_probs):.4f}")

# 7. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig(r'D:\Intern_project\PhishGuard AI\confusion_matrix.png')
plt.show()

# 8. Feature Importance
xgb_model = best_model.named_steps['xgb']
feature_importance = pd.Series(xgb_model.feature_importances_, index=X.columns)
feature_importance = feature_importance.sort_values(ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x=feature_importance.values, y=feature_importance.index)
plt.title('Feature Importance (Sorted)')
plt.tight_layout()
plt.savefig(r'D:\Intern_project\PhishGuard AI\feature_importance2.png')
plt.show()

# 9. Save artifacts
joblib.dump(best_model, r'D:\Intern_project\PhishGuard AI\models_deep\best_xgb_model.pkl')
joblib.dump(grid_search.best_params_, r'D:\Intern_project\PhishGuard AI\models_deep\best_params.pkl')
print("\n✅ Model and parameters saved successfully!")

# 10. Final Validation
print("\nFinal Model Validation:")
print("Training Score:", best_model.score(X_train, y_train))
print("Test Score:", best_model.score(X_test, y_test))
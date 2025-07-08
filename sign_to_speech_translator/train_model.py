import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# Load data
data_path = "data/sign_data.csv"
model_path = "models/trained_model.pkl"

print("[📦] Loading dataset...")
df = pd.read_csv(data_path)

# Features and labels
X = df.drop("label", axis=1)
y = df["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("[🤖] Training Random Forest classifier...")
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"[✅] Accuracy: {acc:.2f}")
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
with open(model_path, "wb") as f:
    pickle.dump(clf, f)
print(f"[💾] Model saved to: {model_path}")

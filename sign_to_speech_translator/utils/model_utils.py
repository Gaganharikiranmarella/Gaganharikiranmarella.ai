# utils/model_utils.py

import pickle
import os

def save_model(model, path="models/trained_model.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)

def load_model(path="models/trained_model.pkl"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import numpy as np

# Wczytanie danych
df = pd.read_csv("train_data.csv")

X = df[[
    'Air temperature [K]',
    'Process temperature [K]',
    'Rotational speed [rpm]',
    'Torque [Nm]',
    'Tool wear [min]'
]]
y = df['Machine failure']

# Podział na trening i test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Trening modelu z wagami klas
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Predykcje probabilistyczne
y_prob = model.predict_proba(X_test)[:, 1]

# Próg decyzyjny na 0.3
threshold = 0.3
y_pred = (y_prob >= threshold).astype(int)

# Ewaluacja
print(f"Raport klasyfikacji (threshold = {threshold}):")
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_prob))

print("Macierz pomyłek:")
print(confusion_matrix(y_test, y_pred))

# Zapis modelu
joblib.dump(model, "model.pkl")
print("Zapisano model jako model.pkl")

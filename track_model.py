"""import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data=pd.read_csv("data.csv",header=None)
X=data.iloc[:,:-1]
y=data.iloc[:,-1]
model=RandomForestClassifier()
model.fit(X,y)
joblib.dump(model,"model.pkl")
print("Model trained and saved as model.pkl")


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# Step 1: Load dataset
# -----------------------------
data = pd.read_csv("data.csv", header=None)

# Last column is label, others are features
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

print("Dataset loaded")
print("X shape:", X.shape)
print("y shape:", y.shape)

# -----------------------------
# Step 2: Train the model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# -----------------------------
# Step 3: Save the model
# -----------------------------
joblib.dump(model, "model.pkl")

# -----------------------------
# Step 4: Verify model features
# -----------------------------
print("Model trained successfully")
print("Model saved as model.pkl")
print("Number of features learned by model:", model.n_features_in_)"""

"""import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load CSV
data = pd.read_csv("data.csv")

# Remove non-numeric rows (header safety)
data = data.apply(pd.to_numeric, errors="coerce")
data = data.dropna()

# Split features and labels
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

print("Dataset loaded")
print("X shape:", X.shape)
print("y shape:", y.shape)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained successfully")
print("Model saved as model.pkl")
print("Number of features:", model.n_features_in_)"""
#new code
"""import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

labels = os.listdir("data")
label_map = {l:i for i,l in enumerate(labels)}

X, y = [], []

for label in labels:
    for file in os.listdir(f"data/{label}"):
        X.append(np.load(f"data/{label}/{file}"))
        y.append(label_map[label])

X = np.array(X)
y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(30,126)),
    Dropout(0.3),
    LSTM(256),
    Dense(128, activation='relu'),
    Dense(len(labels), activation='softmax')
])

model.compile('adam','categorical_crossentropy',metrics=['accuracy'])
model.fit(X_train, y_train, epochs=40)

model.save("model.h5")
np.save("labels.npy", labels)

print("Accuracy:", model.evaluate(X_test, y_test))"""

#both hands
import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Load labels
labels = sorted(os.listdir("data"))
label_map = {label: i for i, label in enumerate(labels)}

X, y = [], []

for label in labels:
    for file in os.listdir(f"data/{label}"):
        X.append(np.load(f"data/{label}/{file}"))
        y.append(label_map[label])

X = np.array(X)
y = to_categorical(y, num_classes=len(labels))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(30, 126)),
    Dropout(0.3),
    LSTM(256),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(len(labels), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
model.fit(X_train, y_train, epochs=40, batch_size=32)

# Save
model.save("model.h5")
np.save("labels.npy", labels)

# Evaluate
loss, acc = model.evaluate(X_test, y_test)
print("Model Accuracy:", acc * 100)

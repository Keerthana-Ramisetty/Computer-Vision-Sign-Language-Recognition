"""import cv2
import mediapipe as mp
import numpy as np
#import pickle
import pyttsx3
import joblib

model = joblib.load("model.pkl")

# Load trained model

# Text to speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_pred = ""
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    prediction = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])

            if len(landmarks) == 42:
                data = np.array(landmarks).reshape(1, -1)
                prediction = model.predict(data)[0]

                if prediction != last_pred:
                    engine.say(prediction)
                    engine.runAndWait()
                    last_pred = prediction

    # Show prediction text
    cv2.putText(
        frame,
        f"Prediction: {prediction}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Sign Language Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""

import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import joblib
import time

# -----------------------------
# Load trained model
# -----------------------------
try:
    model = joblib.load("model.pkl")
except Exception as e:
    print(f"❌ Failed to load model.pkl: {e}")
    exit()

# -----------------------------
# Text to speech setup
# -----------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# -----------------------------
# MediaPipe Hands setup
# -----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# -----------------------------
# Camera setup with auto-select
# -----------------------------
cap = None
for i in range(5):  # try first 5 camera indexes
    temp_cap = cv2.VideoCapture(i)
    if temp_cap.isOpened():
        cap = temp_cap
        print(f"✅ Using camera index {i}")
        break

if cap is None:
    print("❌ No camera found! Exiting...")
    exit()

# -----------------------------
# Main loop
# -----------------------------
last_pred = ""
pred_cooldown = 1.0  # seconds to avoid repeated speech
last_time = 0

print("Press 'Q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠ Failed to read frame from camera")
        break

    frame = cv2.flip(frame, 1)  # mirror image
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    prediction = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y])

            # Predict only if we have all 21 landmarks
            if len(landmarks) == 42:
                data = np.array(landmarks).reshape(1, -1)
                try:
                    prediction = model.predict(data)[0]
                except Exception as e:
                    print(f"⚠ Prediction error: {e}")
                    prediction = ""

                # Speak prediction if changed and cooldown passed
                current_time = time.time()
                if prediction != last_pred and (current_time - last_time) > pred_cooldown:
                    engine.say(prediction)
                    engine.runAndWait()
                    last_pred = prediction
                    last_time = current_time

    # Display prediction text on frame
    cv2.putText(
        frame,
        f"Prediction: {prediction}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show the frame
    cv2.imshow("Sign Language Recognition", frame)

    # Quit on 'Q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

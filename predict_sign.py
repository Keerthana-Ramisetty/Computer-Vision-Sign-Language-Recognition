"""import cv2
import mediapipe as mp
import joblib
import numpy as np

model =joblib.load("model.pkl")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

labels = {"a": 0, "b": 1, "c": 2}

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            data = []
            for lm in hand.landmark:
                data.extend([lm.x, lm.y])
            prediction=model.predict([np.array(data)])
            sign=labels[prediction[0]]

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame,f"Sign: {sign}",(50,100),
                        cv2.FONT_HERSHEY_SIMPLEX,1.5(0,255,0),3)
            cv2.imshow("Sign Language Recognition",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()"""

import cv2
import mediapipe as mp
import joblib
import numpy as np

# Load trained model
model = joblib.load("model.pkl")

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Label mapping (same as training)
labels = {0: "A", 1: "B", 2: "C"}

# Open webcam
cap = cv2.VideoCapture(0)

print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # ------------------ PREDICTION PART (THIS IS WHERE IT GOES) ------------------
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            data = []

            # Extract 21 landmarks (x, y)
            for lm in hand.landmark:
                data.extend([lm.x, lm.y])

            # Ensure correct feature count
            if len(data) == 42:
                data_np = np.array(data).reshape(1, -1)
                prediction = model.predict(data_np)
                sign = labels[prediction[0]]

                # Draw landmarks and label
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                cv2.putText(
                    frame,
                    f"Sign: {sign}",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (0, 255, 0),
                    3
                )
    # ---------------------------------------------------------------------------

    cv2.imshow("Sign Language Prediction", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
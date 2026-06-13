"""import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3

model = load_model("model.h5")
labels = np.load("labels.npy")

engine = pyttsx3.init()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

cap = cv2.VideoCapture(0)
sequence = []
sentence = []

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    keypoints = np.zeros(126)
    if res.multi_hand_landmarks:
        idx = 0
        for hand in res.multi_hand_landmarks:
            for lm in hand.landmark:
                keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                idx += 3

    sequence.append(keypoints)
    sequence = sequence[-30:]

    if len(sequence) == 30:
        pred = model.predict(np.expand_dims(sequence, axis=0))[0]
        action = labels[np.argmax(pred)]

        if len(sentence)==0 or action != sentence[-1]:
            sentence.append(action)
            engine.say(action)
            engine.runAndWait()

    cv2.putText(frame," ".join(sentence[-5:]),(10,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Sign Language AI", frame)
    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()"""
#both hands
"""import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3

# Load LSTM model
model = load_model("model.h5")  
labels = np.load("labels.npy")  # Make sure labels.npy exists

engine = pyttsx3.init()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
cap = cv2.VideoCapture(0)  # external camera

sequence = []
sentence = []

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    keypoints = np.zeros(126)
    if res.multi_hand_landmarks:
        idx = 0
        for hand in res.multi_hand_landmarks:
            for lm in hand.landmark:
                keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                idx += 3

    sequence.append(keypoints)
    sequence = sequence[-30:]  # maintain last 30 frames

    if len(sequence) == 30:
        pred = model.predict(np.expand_dims(sequence, axis=0))[0]
        action = labels[np.argmax(pred)]

        # Only append if changed
        if len(sentence) == 0 or action != sentence[-1]:
            sentence.append(action)
            engine.say(action)
            engine.runAndWait()

    # Display sentence on top-left corner
    cv2.putText(frame, " ".join(sentence[-5:]), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Sign Language AI", frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()"""

"""import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3

# ----------------------------
# Load LSTM model and labels
# ----------------------------
model = load_model("model.h5")  
labels = np.load("labels.npy")  # Make sure labels.npy exists

# ----------------------------
# Text-to-Speech
# ----------------------------
engine = pyttsx3.init()

# ----------------------------
# MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

# ----------------------------
# Video capture
# ----------------------------
cap = cv2.VideoCapture(0)  # Change 0 if using external camera

sequence = []
prev_action = None  # Store last prediction to avoid repeating

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        continue

    frame = cv2.flip(frame, 1)  # Mirror for natural view
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    # ----------------------------
    # Extract keypoints for both hands
    # ----------------------------
    keypoints = np.zeros(126)  # 21 landmarks * 3 coords * 2 hands
    if res.multi_hand_landmarks:
        idx = 0
        for hand in res.multi_hand_landmarks:
            for lm in hand.landmark:
                keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                idx += 3

    # ----------------------------
    # Append to sequence and keep last 30 frames
    # ----------------------------
    sequence.append(keypoints)
    sequence = sequence[-30:]

    # ----------------------------
    # Predict action when sequence has 30 frames
    # ----------------------------
    current_action = ""
    if len(sequence) == 30:
        pred = model.predict(np.expand_dims(sequence, axis=0))[0]
        action = labels[np.argmax(pred)]

        # Only trigger if prediction changed
        if action != prev_action:
            prev_action = action
            current_action = action
            engine.say(action)
            engine.runAndWait()
        else:
            # No new prediction, don't display anything
            current_action = ""

    # ----------------------------
    # Display current prediction only
    # ----------------------------
    if prev_action:
        display_text = prev_action if current_action != "" else ""
        cv2.putText(frame, display_text, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # ----------------------------
    # Show video
    # ----------------------------
    cv2.imshow("Sign Language AI", frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()"""
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyttsx3
import threading
import time

# ----------------------------
# Load model and labels
# ----------------------------
model = load_model("model.h5")
labels = np.load("labels.npy")

# ----------------------------
# Text-to-Speech (threaded)
# ----------------------------
engine = pyttsx3.init()
def speak(text):
    threading.Thread(target=lambda: engine.say(text) or engine.runAndWait(), daemon=True).start()

# ----------------------------
# MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# ----------------------------
# Camera setup
# ----------------------------
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

sequence = []
prev_action = ""
frame_count = 0
SEQ_LEN = 30
PRED_EVERY = 3  # Predict every 3 frames

# ----------------------------
# Main loop
# ----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    #frame = cv2.flip(frame, 1)
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
            if cap.isOpened():
                print(f"✅ Camera working at index {i}")
                cap.release()
            else:
                print(f"❌ Camera NOT working at index {i}")
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)

    # ----------------------------
    # Extract keypoints
    # ----------------------------
    keypoints = np.zeros(126)  # 2 hands * 21 landmarks * 3 coords
    if res.multi_hand_landmarks:
        for h_idx, hand in enumerate(res.multi_hand_landmarks):
            for l_idx, lm in enumerate(hand.landmark):
                idx = h_idx*63 + l_idx*3
                keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]

    # Normalize keypoints (optional, improves accuracy)
    keypoints = keypoints - np.mean(keypoints)

    # ----------------------------
    # Update sequence
    # ----------------------------
    sequence.append(keypoints)
    if len(sequence) > SEQ_LEN:
        sequence.pop(0)

    # ----------------------------
    # Predict action every PRED_EVERY frames
    # ----------------------------
    frame_count += 1
    if len(sequence) == SEQ_LEN and frame_count % PRED_EVERY == 0:
        seq_input = np.expand_dims(sequence, axis=0)
        pred = model.predict(seq_input, verbose=0)[0]
        action = labels[np.argmax(pred)]

        # Trigger only if changed
        if action != prev_action:
            prev_action = action
            speak(action)

    # ----------------------------
    # Display last action
    # ----------------------------
    if prev_action:
        cv2.putText(frame, prev_action, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

    # ----------------------------
    # Show video
    # ----------------------------
    cv2.imshow("Sign Language AI", frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
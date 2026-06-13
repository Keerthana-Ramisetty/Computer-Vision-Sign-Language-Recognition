"""import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
cap.set(cv2.CAP_PROP_FPS,30)
#  IMPORTANT CHECK
if not cap.isOpened():
    print(" ERROR: Camera not accessible")
    exit()

file = open("data.csv", "a", newline="")
writer = csv.writer(file)

labels = {"a": 0, "b": 1, "c": 2}

print("Press A, B, C to collect data | Q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print(" Failed to read frame from camera")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    
    key = cv2.waitKey(1) & 0xFF   

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            data = []
            for lm in hand.landmark:
                data.extend([lm.x, lm.y])

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            #key = cv2.waitKey(1) & 0xFF
            if chr(key).lower() in labels and len(data) == 42:
                writer.writerow(data + [labels[chr(key).lower()]])
                print("Saved:", chr(key).upper())

    cv2.imshow("Collect Data", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

file.close()
cap.release()
cv2.destroyAllWindows()"""
# new code 
"""import cv2
import mediapipe as mp
import numpy as np
import os

label = input("Enter gesture name: ")
os.makedirs(f"data/{label}", exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

cap = cv2.VideoCapture(0)

for seq in range(30):
    frames = []
    print(f"Sequence {seq}")
    for frame in range(30):
        ret, img = cap.read()
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        landmarks = np.zeros(126)

        if res.multi_hand_landmarks:
            idx = 0
            for hand in res.multi_hand_landmarks:
                for lm in hand.landmark:
                    landmarks[idx:idx+3] = [lm.x, lm.y, lm.z]
                    idx += 3

        frames.append(landmarks)
        cv2.imshow("Collecting", img)
        cv2.waitKey(30)

    np.save(f"data/{label}/{seq}.npy", frames)

cap.release()
cv2.destroyAllWindows()"""

#  both hands
"""import cv2
import mediapipe as mp
import numpy as np
import os

ACTION = input("Enter word/sentence: ")
SEQUENCES = 30
FRAMES = 30

os.makedirs(f"data/{ACTION}", exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
cap = cv2.VideoCapture(3, cv2.CAP_V4L2)

if not cap.isOpened():
    print("❌ Camera not opened")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
for seq in range(SEQUENCES):
    sequence = []
    print(f"Recording sequence {seq}")
    for frame in range(FRAMES):
        ret, img = cap.read()
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        keypoints = np.zeros(126)

        if result.multi_hand_landmarks:
            idx = 0
            for hand in result.multi_hand_landmarks:
                for lm in hand.landmark:
                    keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                    idx += 3

        sequence.append(keypoints)
        cv2.imshow("Collecting Data", img)
        cv2.waitKey(30)

    np.save(f"data/{ACTION}/{seq}.npy", sequence)

cap.release()
cv2.destroyAllWindows()"""

"""import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ----------------------------
# User input for gesture
# ----------------------------
ACTION = input("Enter word/sentence for data collection: ")
SEQUENCES = 30
FRAMES = 30

# ----------------------------
# Create folder for gesture
# ----------------------------
os.makedirs(f"data/{ACTION}", exist_ok=True)

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# ----------------------------
# Open internal camera (index 0)
# ----------------------------
cap = cv2.VideoCapture(0)  # Internal camera

if not cap.isOpened():
    print("❌ Could not open internal camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ----------------------------
# Data collection loop
# ----------------------------
for seq in range(SEQUENCES):
    sequence = []
    print(f"\nRecording sequence {seq+1}/{SEQUENCES} for '{ACTION}'")
    
    # Countdown before recording
    for i in range(3, 0, -1):
        ret, img = cap.read()
        if not ret:
            continue
        cv2.putText(img, f"Get ready in {i}", (400, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.imshow("Collecting Data", img)
        cv2.waitKey(1000)  # Wait 1 second per countdown number

    # Capture frames
    for frame_num in range(FRAMES):
        ret, img = cap.read()
        if not ret:
            continue
        img = cv2.flip(img, 1)  # Mirror image for natural view
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        keypoints = np.zeros(126)  # 2 hands × 21 landmarks × 3 coords
        if result.multi_hand_landmarks:
            idx = 0
            for hand_landmarks in result.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                    idx += 3
                # Optional: draw landmarks on the frame
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        sequence.append(keypoints)

        # Display recording progress
        cv2.putText(img, f"Frame {frame_num+1}/{FRAMES}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Collecting Data", img)
        cv2.waitKey(30)

    # Save sequence
    np.save(f"data/{ACTION}/{seq}.npy", sequence)
    print(f"Saved sequence {seq+1} to data/{ACTION}/{seq}.npy")

# ----------------------------
# Release resources
# ----------------------------
cap.release()
cv2.destroyAllWindows()
print("✅ Data collection complete!")"""

"""import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ----------------------------
# Function to list available cameras
# ----------------------------
def list_cameras(max_test=5):
    available = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

# ----------------------------
# Ask user for gesture
# ----------------------------
ACTION = input("Enter word/sentence for data collection: ")
SEQUENCES = 30
FRAMES = 30

# ----------------------------
# Create folder for gesture
# ----------------------------
os.makedirs(f"data/{ACTION}", exist_ok=True)

# ----------------------------
# List available cameras
# ----------------------------
cameras = list_cameras()
if not cameras:
    print("❌ No cameras detected!")
    exit()
print(f"Available cameras: {cameras}")
camera_index = int(input(f"Select camera index from above list: "))

# ----------------------------
# Open selected camera
# ----------------------------
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print(f"❌ Could not open camera {camera_index}")
    exit()

# Optional: set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# ----------------------------
# Data collection loop
# ----------------------------
for seq in range(SEQUENCES):
    sequence = []
    print(f"\nRecording sequence {seq+1}/{SEQUENCES} for '{ACTION}'")
    
    # Countdown before recording
    for i in range(3, 0, -1):
        ret, img = cap.read()
        if not ret:
            continue
        cv2.putText(img, f"Get ready in {i}", (400, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.imshow("Collecting Data", img)
        cv2.waitKey(500)

    # Capture frames
    for frame_num in range(FRAMES):
        ret, img = cap.read()
        if not ret:
            continue
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        keypoints = np.zeros(126)  # 2 hands × 21 landmarks × 3 coords
        if result.multi_hand_landmarks:
            idx = 0
            for hand_landmarks in result.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                    idx += 3
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        sequence.append(keypoints)

        # Display progress
        cv2.putText(img, f"Frame {frame_num+1}/{FRAMES}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Collecting Data", img)
        cv2.waitKey(1)

    # Save sequence
    np.save(f"data/{ACTION}/{seq}.npy", sequence)
    print(f"Saved sequence {seq+1} to data/{ACTION}/{seq}.npy")

# ----------------------------
# Release resources
# ----------------------------
cap.release()
cv2.destroyAllWindows()
print("✅ Data collection complete!")"""

"""import cv2
import mediapipe as mp
import numpy as np
import os

# ----------------------------
# Function to list available cameras
# ----------------------------
def list_cameras(max_test=5):
    available = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

# ----------------------------
# User input for gesture
# ----------------------------
ACTION = input("Enter word/sentence for data collection: ")
SEQUENCES = 30   # Total sequences
FRAMES = 30      # Frames per sequence

# ----------------------------
# Create folder for gesture
# ----------------------------
os.makedirs(f"data/{ACTION}", exist_ok=True)

# ----------------------------
# Detect available cameras and select
# ----------------------------
cameras = list_cameras()
if not cameras:
    print("❌ No cameras detected!")
    exit()
print(f"Available cameras: {cameras}")
camera_index = int(input("Select camera index from above list: "))

# ----------------------------
# Open selected camera
# ----------------------------
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print(f"❌ Could not open camera {camera_index}")
    exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# ----------------------------
# Ultra-fast data collection loop
# ----------------------------
print(f"\nStarting ultra-fast data collection for '{ACTION}'...")

for seq in range(SEQUENCES):
    sequence = []

    for frame_num in range(FRAMES):
        ret, img = cap.read()
        if not ret:
            continue

        img = cv2.flip(img, 1)  # Mirror image
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        keypoints = np.zeros(126)  # 2 hands × 21 landmarks × 3 coords
        if result.multi_hand_landmarks:
            idx = 0
            for hand_landmarks in result.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                    idx += 3
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        sequence.append(keypoints)

        # Display frame counter
        cv2.putText(img, f"Seq {seq+1}/{SEQUENCES}  Frame {frame_num+1}/{FRAMES}",
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Collecting Data", img)
        cv2.waitKey(1)  # Minimal delay for display

    # Save sequence
    np.save(f"data/{ACTION}/{seq}.npy", sequence)
    print(f"Saved sequence {seq+1}/{SEQUENCES}")

# ----------------------------
# Release resources
# ----------------------------
cap.release()
cv2.destroyAllWindows()
print("✅ Ultra-fast data collection complete!")"""

import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ----------------------------
# Function to list available cameras
# ----------------------------
def list_cameras(max_test=5):
    available = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

# ----------------------------
# User input for gesture
# ----------------------------
ACTION = input("Enter word/sentence for data collection: ")
SEQUENCES = 30   # Total sequences
FRAMES = 30      # Frames per sequence
TOTAL_TIME = 60  # seconds to complete all sequences

# ----------------------------
# Create folder for gesture
# ----------------------------
os.makedirs(f"data/{ACTION}", exist_ok=True)

# ----------------------------
# Detect available cameras and select
# ----------------------------
cameras = list_cameras()
if not cameras:
    print("❌ No cameras detected!")
    exit()
print(f"Available cameras: {cameras}")
camera_index = int(input("Select camera index from above list: "))

# ----------------------------
# Open selected camera
# ----------------------------
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print(f"❌ Could not open camera {camera_index}")
    exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# ----------------------------
# Calculate timing per frame
# ----------------------------
total_frames = SEQUENCES * FRAMES
frame_duration = TOTAL_TIME / total_frames  # seconds per frame

# ----------------------------
# Ultra-fast timed data collection
# ----------------------------
print(f"\nStarting timed data collection for '{ACTION}' (~{TOTAL_TIME} seconds)...")

for seq in range(SEQUENCES):
    sequence = []

    for frame_num in range(FRAMES):
        start_time = time.time()

        ret, img = cap.read()
        if not ret:
            continue

        img = cv2.flip(img, 1)  # Mirror image
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        keypoints = np.zeros(126)  # 2 hands × 21 landmarks × 3 coords
        if result.multi_hand_landmarks:
            idx = 0
            for hand_landmarks in result.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    keypoints[idx:idx+3] = [lm.x, lm.y, lm.z]
                    idx += 3
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        sequence.append(keypoints)

        # Display frame progress
        cv2.putText(img, f"Seq {seq+1}/{SEQUENCES} Frame {frame_num+1}/{FRAMES}",
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Collecting Data", img)

        # Wait to maintain frame duration
        elapsed = time.time() - start_time
        wait_time = max(int((frame_duration - elapsed) * 1000), 1)  # in ms
        cv2.waitKey(wait_time)

    # Save sequence
    np.save(f"data/{ACTION}/{seq}.npy", sequence)
    print(f"Saved sequence {seq+1}/{SEQUENCES}")

# ----------------------------
# Release resources
# ----------------------------
cap.release()
cv2.destroyAllWindows()
print("✅ Timed ultra-fast data collection complete!")
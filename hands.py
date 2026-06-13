

import random

# Landmark class
class Landmark:
    def __init__(self, x, y, z):
        self.x = x  # normalized (0.0 – 1.0)
        self.y = y
        self.z = z

# HandLandmarks class

class HandLandmarks:
    def __init__(self, landmarks):
        # List of 21 Landmark objects
        self.landmark = landmarks

# Results class
class Results:
    def __init__(self):
        # Will store detected hands
        self.multi_hand_landmarks = None

# Hands main class
class Hands:
    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Internally MediaPipe loads ML models
        self.palm_detection_model = "palm_detection.tflite"
        self.hand_landmark_model = "hand_landmark.tflite"

    def process(self, image_rgb):

        results = Results()

        # detect hand
        detected = self._detect_hand(image_rgb)
        if not detected:
            return results

        #  predict landmarks
        landmarks = self._predict_landmarks(image_rgb)

        results.multi_hand_landmarks = [
            HandLandmarks(landmarks)
        ]

        return results

    def _detect_hand(self, image):
        
       # Simulates palm detection using confidence threshold
        
        confidence = random.uniform(0.6, 1.0)
        return confidence >= self.min_detection_confidence

    def _predict_landmarks(self, image):
    
        #Simulates 21 hand landmarks
        
        landmarks = []

        for _ in range(21):
            x = random.random()
            y = random.random()
            z = random.uniform(-0.1, 0.1)
            landmarks.append(Landmark(x, y, z))

        return landmarks

# Hand connections (skeleton)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        
    (0, 5), (5, 6), (6, 7), (7, 8),       
    (0, 9), (9, 10), (10, 11), (11, 12),   
    (0, 13), (13, 14), (14, 15), (15, 16), 
    (0, 17), (17, 18), (18, 19), (19, 20) 
]
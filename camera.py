import cv2

for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
    if cap.isOpened():
        print(f"✅ Camera working at index {i}")
        cap.release()
    else:
        print(f"❌ Camera NOT working at index {i}")
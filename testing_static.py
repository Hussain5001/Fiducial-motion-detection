'''
import cv2
import apriltag

# Initialize AprilTag detector
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

print(f"Initialized detector with families: {options.families}")
# Load an image with the tag
image_path = "videos/static36.jpg"  # Replace with your image path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Detect AprilTags
detections = detector.detect(image)

if detections:
    print(f"Detected {len(detections)} tags!")
    for detection in detections:
        print(f"Tag ID: {detection.tag_id}, Center: {detection.center}")
else:
    print("No tags detected.")
'''
import cv2
import apriltag
import numpy as np
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# Initialize AprilTag detector
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
print(f"Supported tag families: {options.families}")

# Open the video file
video_path = "videos/phone_vid2.mp4"  
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit()

# preprocessing as 60fps on higher resolution giving issues
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Video FPS: {fps}")
use_preprocessing = fps >= 55

all_detections = []



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if use_preprocessing:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    detections = detector.detect(gray)
    if detections:
        print(f"Detected {len(detections)} AprilTag(s):")
        for detection in detections:
            print(f"Tag ID: {detection.tag_id}, Center: {detection.center}")
            all_detections.append({
                "Tag ID": detection.tag_id,
                "Center X": detection.center[0],
                "Center Y": detection.center[1]
            })
    else:
        print("No tags detected in this frame.")

    for detection in detections:
        (cx, cy) = detection.center
        corners = detection.corners
        cv2.circle(frame, (int(cx), int(cy)), 5, (0, 255, 0), -1)  
        for corner in corners:
            cv2.circle(frame, tuple(int(x) for x in corner), 5, (255, 0, 0), -1)  

    cv2.imshow('AprilTag Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#saving data
output_file = "tracking_data.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Tag ID", "Center X", "Center Y"])
    writer.writeheader()
    writer.writerows(all_detections)

#reading
x_data = []
y_data = []
with open(output_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        x_data.append(float(row["Center X"]))
        y_data.append(float(row["Center Y"]))

#plotting
plt.plot(x_data, y_data, label="Tag Motion")
plt.xlabel("Center X")
plt.ylabel("Center Y")
plt.title("AprilTag Motion Path")
plt.legend()
plt.savefig("tag_motion_plot.png")
print("Plot saved as tag_motion_plot.png")

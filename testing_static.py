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

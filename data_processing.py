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
video_path = "sample_data/30fps/sample_30_300.mp4" 
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


'''

import cv2
import apriltag
import csv
import os
import matplotlib
matplotlib.use('TkAgg')

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
print(f"Supported tag families: {options.families}")


input_dir = "sample_data"  
output_dir = "processed_data/individual_vids"
os.makedirs(output_dir, exist_ok=True)

#preprocessing function if needed
def preprocess_frame(frame):
    """Preprocess frame to reduce noise for AprilTag detection."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return gray

def process_video(video_path, output_csv_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    #information for preprocessing
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Processing {video_path} | FPS: {fps} | Resolution: {width}x{height}")

    #preprocess for high resolution and and higher fps
    use_preprocessing = (fps >= 55) or (width * height > 1920 * 1080)
    print(f"Preprocessing Enabled: {use_preprocessing}")

    #create csv
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Frame", "Tag ID", "Center X", "Center Y"])
        writer.writeheader()

        
        frame_number = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_number += 1
            try:
                #preprocess
                if use_preprocessing:
                    gray = preprocess_frame(frame)
                else:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #detect
                detections = detector.detect(gray)
                if detections:
                    for detection in detections:
                        writer.writerow({
                            "Frame": frame_number,
                            "Tag ID": detection.tag_id,
                            "Center X": detection.center[0],
                            "Center Y": detection.center[1]
                        })
                else:
                    #frames with no detection
                    writer.writerow({
                        "Frame": frame_number,
                        "Tag ID": "None",
                        "Center X": "None",
                        "Center Y": "None"
                    })
            except Exception as e:
                print(f"Error on frame {frame_number} of {video_path}: {e}")
                continue

    cap.release()
    print(f"Finished processing {video_path} | Saved to {output_csv_path}")

#process all videos
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".mp4"):
            video_path = os.path.join(root, file)

            #generate output csv path
            relative_path = os.path.relpath(video_path, input_dir)
            csv_filename = os.path.splitext(relative_path)[0] + ".csv"
            output_csv_path = os.path.join(output_dir, csv_filename)


            process_video(video_path, output_csv_path)

print("All videos have been processed and data has been saved.")

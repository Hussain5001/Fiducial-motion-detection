import cv2
import apriltag
import csv
import os
import numpy as np

#initialize AprilTag detector
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
print(f"Supported tag families: {options.families}")

#paths
input_dir = "sample_data_retro"  
output_dir = "processed_data_retro" 
os.makedirs(output_dir, exist_ok=True)

#function to process a single video
def process_video(video_path, output_csv_path, num_tags=4):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    #create CSV file and write headers
    fieldnames = ["Frame"] + [f"X_{i},Y_{i}" for i in range(num_tags)] + ["Action"]
    fieldnames = [item for sublist in [field.split(",") for field in fieldnames] for item in sublist] 
    with open(output_csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        frame_number = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_number += 1

            #convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #detect AprilTags
            detections = detector.detect(gray)

            row = {"Frame": frame_number, "Action": ""}
            for tag_id in range(num_tags):
                row[f"X_{tag_id}"] = None
                row[f"Y_{tag_id}"] = None

            #populate detected tag coordinates
            for detection in detections:
                tag_id = detection.tag_id
                if 0 <= tag_id < num_tags:  
                    row[f"X_{tag_id}"] = detection.center[0]
                    row[f"Y_{tag_id}"] = detection.center[1]

            #write the row to the CSV
            writer.writerow(row)

            #display the frame with detections
            for detection in detections:
                (cx, cy) = detection.center
                corners = detection.corners
                cv2.circle(frame, (int(cx), int(cy)), 5, (0, 255, 0), -1)  
                for corner in corners:
                    cv2.circle(frame, tuple(int(x) for x in corner), 5, (255, 0, 0), -1) 
            cv2.imshow("AprilTag Detection", frame)

            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Finished processing {video_path} | Saved to {output_csv_path}")

#process all videos in the input directory
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".mp4"):
            video_path = os.path.join(root, file)

            #generate output CSV path
            relative_path = os.path.relpath(video_path, input_dir)
            csv_filename = os.path.splitext(relative_path)[0] + ".csv"
            output_csv_path = os.path.join(output_dir, csv_filename)


            os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

            process_video(video_path, output_csv_path)

print("All videos have been processed and data has been saved.")

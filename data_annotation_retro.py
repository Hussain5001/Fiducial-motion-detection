import cv2
import pandas as pd
import os

#Paths
input_dir = "processed_data_retro" 
video_dir = "sample_data_retro"  
output_dir = "annotated_data"  
os.makedirs(output_dir, exist_ok=True)

#action enumeration
actions = {
    1: "Picking up book",
    2: "Moving book",
    3: "Placing book on Stack 1",
    4: "Placing book on Stack 2",
    5: "Placing book on Stack 3"
}

#function to annotate actions for a single video
def annotate_video(video_path, csv_path, output_csv_path):

    window_name = "Video Annotation"
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return
    
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #load CSV data
    df = pd.read_csv(csv_path)
    df["Action"] = None 

    
    frame_number = 0
    frame_points = []  #store the frames where action changes

    print("Instructions:")
    print("1. Watch the video and press 's' to mark a frame.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1

        #display frame number
        cv2.putText(frame, f"Frame: {frame_number}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        #display
        cv2.imshow("Video Annotation", frame)

        key = cv2.waitKey(150) & 0xFF  #playback speed adjustment 
        if key == ord("s"): 
            print(f"Marked frame: {frame_number}")
            frame_points.append(frame_number)
        elif key == ord("q"): 
            print("Finished marking frame points.")
            break

    cap.release()
    cv2.destroyAllWindows()

    #annotate actions
    action_labels = [1, 2, 3, 4, 5]
    for i in range(len(frame_points) + 1):
        start = frame_points[i - 1] if i > 0 else 1
        end = frame_points[i] if i < len(frame_points) else len(df)

        #extract the target stack from video name
        parts = video_path.split("_")
        number_part = parts[-1].split(".")[0]  
        action_digit=int(str(number_part)[0])

        #assign either pickig up, moving or stacking
        action = action_labels[i] if i < len(frame_points) else action_labels[action_digit+1]
        df.loc[start - 1 : end - 1, "Action"] = action

    #save the annotated CSV
    df.to_csv(output_csv_path, index=False)
    print(f"Annotated CSV saved to {output_csv_path}")

#process all videos and corresponding CSVs
for root, dirs, files in os.walk(video_dir):
    for file in files:
        if file.endswith(".mp4"):
            video_path = os.path.join(root, file)
            csv_filename = os.path.splitext(file)[0] + ".csv"
            csv_path = os.path.join(input_dir, csv_filename)
            output_csv_path = os.path.join(output_dir, csv_filename)

            if os.path.exists(csv_path):
                print(f"Processing {video_path} with {csv_path}")
                print(video_path)
                annotate_video(video_path, csv_path, output_csv_path)
            else:
                print(f"Warning: No CSV file found for {video_path}")

print("All videos have been annotated.")

import cv2
import os

def extract_every_10th_frame(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get video properties
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}")
    print(f"Total frames: {total_frames}")

    frame_number = 0
    saved_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Save every 10th frame
        if frame_number % 7 == 0:
            frame_filename = os.path.join(output_folder, f"frame_{frame_number:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            print(f"Saved frame {frame_number}")

        frame_number += 1

    # Release the video capture object
    video.release()

    print(f"Extracted {saved_count} frames to {output_folder}")
    print(f"Total frames processed: {frame_number}")

# Example usage
project_name = "white"
video_path = os.path.join("./videos/", project_name) + ".mp4"
output_folder = os.path.join("./videos/output", project_name)

extract_every_10th_frame(video_path, output_folder)

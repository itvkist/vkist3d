import cv2
import os

def slice_video_to_images(video_path, output_folder, frame_interval=10):
    """
    Slices a video into frames and saves them as images.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Directory where the images will be saved.
        frame_interval (int): Save one frame every 'frame_interval' frames.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {frame_count}")

    count = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            filename = os.path.join(output_folder, f"frame_{saved:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
        count += 1

    cap.release()
    print(f"Saved {saved} images to '{output_folder}'")

if __name__ == "__main__":
    project_name = "temple_chen_kieu_indoor"
    video_path = os.path.join("./videos/", project_name) + ".mp4"
    output_folder = os.path.join("./videos/output", project_name)
    frame_rate_interval = 60                 # Save every 10th frame
    # ==============

    slice_video_to_images(video_path, output_folder, frame_rate_interval)

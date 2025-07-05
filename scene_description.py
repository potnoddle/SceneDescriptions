import argparse
from transformers import pipeline
import cv2
import time
from PIL import Image
import torch
import os
import sys

def describe_scene(source):
    """
    Generates a text description of a scene from an image or video source.
    """
    try:
        print(f"[DEBUG] describe_scene called with source: {source}")
        cuda_available = torch.cuda.is_available()
        print(f"[DEBUG] CUDA available: {cuda_available}")

        if isinstance(source, str):
            print(f"[DEBUG] Source is a string: {source}")
            if not source.lower().startswith(('http://', 'https://')) and os.path.exists(source):
                print(f"[DEBUG] Detected local file: {source}")
                if source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    image_processor = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", device=0 if cuda_available else -1)
                    description = image_processor(source)[0]["generated_text"]
                    print(f"[DEBUG] Image description generated: {description}")
                    return description
                else:
                    print(f"[DEBUG] Detected local video file: {source}")
                    video_capture = cv2.VideoCapture(source)
                    if not video_capture.isOpened():
                        print(f"Error: Could not open video file: {source}")
                        return None
                    return _describe_video_feed(video_capture, is_live_feed=False, cuda_available=cuda_available)
            elif source.lower().startswith(('http://', 'https://')):
                print(f"[DEBUG] Detected remote file: {source}")
                if source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    image_processor = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", device=0 if cuda_available else -1)
                    description = image_processor(source)[0]["generated_text"]
                    print(f"[DEBUG] Image description generated: {description}")
                    return description
                else:
                    print(f"[DEBUG] Detected remote video file: {source}")
                    video_capture = cv2.VideoCapture(source)
                    if not video_capture.isOpened():
                        print(f"Error: Could not open video file: {source}")
                        return None
                    return _describe_video_feed(video_capture, is_live_feed=False, cuda_available=cuda_available)
            else:
                print("Error: File does not exist or unsupported source.")
                return None

        elif isinstance(source, cv2.VideoCapture):
            print(f"[DEBUG] Source is a cv2.VideoCapture object")
            if not source.isOpened():
                print("Error: Could not open video feed.")
                return None
            return _describe_video_feed(source, is_live_feed=True, cuda_available=cuda_available)

        else:
            print("Error: Invalid source type. Please provide a file path or a cv2.VideoCapture object.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def _describe_video_feed(video_capture, is_live_feed, cuda_available):
    """
    Generates a text description of a video feed, optionally including timestamps for live feeds.
    Allows breaking the loop with 'q' key.
    """
    try:
        print(f"[DEBUG] _describe_video_feed called. is_live_feed={is_live_feed}")
        image_processor = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", device=0 if cuda_available else -1)
        descriptions = []
        frame_count = 0
        max_live_frames = 1000  # Large number, but user can break with 'q'
        while True:
            ret, frame = video_capture.read()
            frame_count += 1
            print(f"[DEBUG] Reading frame {frame_count}: ret={ret}")
            if not ret:
                if is_live_feed:
                    print("End of live feed.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            print(f"[DEBUG] Frame {frame_count} converted to RGB.")
            pil_image = Image.fromarray(frame_rgb)
            print(f"[DEBUG] Frame {frame_count} converted to PIL Image.")
            description = image_processor(pil_image)[0]["generated_text"]
            print(f"[DEBUG] Frame {frame_count} description: {description}")

            if is_live_feed:
                timestamp = time.strftime("%H:%M:%S")
                descriptions.append(f"[{timestamp}] {description}")
                cv2.imshow("Live Feed (press 'q' to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("[DEBUG] 'q' pressed, breaking live feed loop.")
                    break
                if frame_count >= max_live_frames:
                    print(f"[DEBUG] Reached max_live_frames ({max_live_frames}), breaking loop.")
                    break
            else:
                descriptions.append(description)
                print(f"[DEBUG] Not live feed, breaking after first frame.")
                break

        video_capture.release()
        cv2.destroyAllWindows()
        print(f"[DEBUG] Video capture released. Total frames processed: {frame_count}")

        return "\n".join(descriptions) if descriptions else None
    except Exception as e:
        print(f"An error occurred during video processing: {e}")
        if video_capture.isOpened():
            video_capture.release()
        cv2.destroyAllWindows()
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Describe a scene from an image, video, or camera.")
    parser.add_argument('--source', type=str, help="Path/URL to image or video file. If not provided and --camera is not set, will prompt for input.")
    parser.add_argument('--camera', type=int, nargs='?', const=0, help="Camera index to use (default 0).")
    args = parser.parse_args()

    if args.camera is not None:
        print(f"[DEBUG] Starting live feed description example with camera {args.camera}...")
        video_capture = cv2.VideoCapture(args.camera)
        live_feed_description = describe_scene(video_capture)
        if live_feed_description:
            print(f"Live Feed Description:\n{live_feed_description}\n")
    elif args.source:
        print(f"[DEBUG] Starting description for source: {args.source}")
        description = describe_scene(args.source)
        if description:
            print(f"Description:\n{description}\n")
    else:
        print("Please provide --source <file_or_url> or --camera [camera_index].")
        source = input("Enter the path/URL to the image or video file, or camera index: ").strip()
        if source.isdigit():
            camera_index = int(source)
            video_capture = cv2.VideoCapture(camera_index)
            describe_scene(video_capture)
        else:
            describe_scene(source)
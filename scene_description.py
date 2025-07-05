import argparse
from transformers import pipeline
import cv2
import time
from PIL import Image
import torch
import os
import sys

def describe_scene(source, model="Salesforce/blip-image-captioning-base", device=None, use_fast=None,
                   frame_interval=1, max_frames=1000, no_display=False, output=None):
    """
    Generates a text description of a scene from an image or video source.
    """
    try:
        print(f"[DEBUG] describe_scene called with source: {source}")
        # Device logic
        cuda_available = torch.cuda.is_available()
        print(f"[DEBUG] CUDA available: {cuda_available}")
        if device is None:
            device = "cuda" if cuda_available else "cpu"
        print(f"[DEBUG] Using device: {device}")

        # use_fast logic
        if use_fast is None:
            use_fast = not cuda_available  # Use fast if CUDA is not available
        print(f"[DEBUG] use_fast: {use_fast}")

        pipeline_kwargs = {"model": model, "use_fast": use_fast}
        pipeline_kwargs["device"] = 0 if device == "cuda" else -1

        if isinstance(source, str):
            print(f"[DEBUG] Source is a string: {source}")
            if not source.lower().startswith(('http://', 'https://')) and os.path.exists(source):
                print(f"[DEBUG] Detected local file: {source}")
                if source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    image_processor = pipeline("image-to-text", **pipeline_kwargs)
                    description = image_processor(source)[0]["generated_text"]
                    print(f"[DEBUG] Image description generated: {description}")
                    if output:
                        with open(output, "w", encoding="utf-8") as f:
                            f.write(description)
                    return description
                else:
                    print(f"[DEBUG] Detected local video file: {source}")
                    video_capture = cv2.VideoCapture(source)
                    if not video_capture.isOpened():
                        print(f"Error: Could not open video file: {source}")
                        return None
                    return _describe_video_feed(
                        video_capture, is_live_feed=False, pipeline_kwargs=pipeline_kwargs,
                        frame_interval=frame_interval, max_frames=max_frames, no_display=no_display, output=output
                    )
            elif source.lower().startswith(('http://', 'https://')):
                print(f"[DEBUG] Detected remote file: {source}")
                if source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    image_processor = pipeline("image-to-text", **pipeline_kwargs)
                    description = image_processor(source)[0]["generated_text"]
                    print(f"[DEBUG] Image description generated: {description}")
                    if output:
                        with open(output, "w", encoding="utf-8") as f:
                            f.write(description)
                    return description
                else:
                    print(f"[DEBUG] Detected remote video file: {source}")
                    video_capture = cv2.VideoCapture(source)
                    if not video_capture.isOpened():
                        print(f"Error: Could not open video file: {source}")
                        return None
                    return _describe_video_feed(
                        video_capture, is_live_feed=False, pipeline_kwargs=pipeline_kwargs,
                        frame_interval=frame_interval, max_frames=max_frames, no_display=no_display, output=output
                    )
            else:
                print("Error: File does not exist or unsupported source.")
                return None

        elif isinstance(source, cv2.VideoCapture):
            print(f"[DEBUG] Source is a cv2.VideoCapture object")
            if not source.isOpened():
                print("Error: Could not open video feed.")
                return None
            return _describe_video_feed(
                source, is_live_feed=True, pipeline_kwargs=pipeline_kwargs,
                frame_interval=frame_interval, max_frames=max_frames, no_display=no_display, output=output
            )

        else:
            print("Error: Invalid source type. Please provide a file path or a cv2.VideoCapture object.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def _describe_video_feed(video_capture, is_live_feed, pipeline_kwargs,
                         frame_interval=1, max_frames=1000, no_display=False, output=None):
    """
    Generates a text description of a video feed, optionally including timestamps for live feeds.
    Allows breaking the loop with 'q' key.
    """
    try:
        print(f"[DEBUG] _describe_video_feed called. is_live_feed={is_live_feed}")
        print(f"[DEBUG] frame_interval={frame_interval}, max_frames={max_frames}, no_display={no_display}")
        image_processor = pipeline("image-to-text", **pipeline_kwargs)
        descriptions = []
        frame_count = 0
        processed_frames = 0
        while processed_frames < max_frames:
            ret, frame = video_capture.read()
            if not ret:
                if is_live_feed:
                    print("End of live feed.")
                break
            frame_count += 1
            if frame_count % frame_interval != 0:
                continue
            processed_frames += 1
            print(f"[DEBUG] Processing frame {frame_count} (processed {processed_frames})")
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            description = image_processor(pil_image)[0]["generated_text"]
            print(f"[DEBUG] Frame {frame_count} description: {description}")

            if is_live_feed:
                timestamp = time.strftime("%H:%M:%S")
                descriptions.append(f"[{timestamp}] {description}")
                if not no_display:
                    cv2.imshow("Live Feed (press 'q' to quit)", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("[DEBUG] 'q' pressed, breaking live feed loop.")
                        break
            else:
                descriptions.append(description)
                print(f"[DEBUG] Not live feed, breaking after first frame.")
                break  # Only process first frame for video files by default

        video_capture.release()
        if not no_display:
            cv2.destroyAllWindows()
        print(f"[DEBUG] Video capture released. Total frames processed: {processed_frames}")

        result = "\n".join(descriptions) if descriptions else None
        if output and result:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
        return result
    except Exception as e:
        print(f"An error occurred during video processing: {e}")
        if video_capture.isOpened():
            video_capture.release()
        if not no_display:
            cv2.destroyAllWindows()
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Describe a scene from an image, video, or camera.")
    parser.add_argument('--source', type=str, help="Path/URL to image or video file.")
    parser.add_argument('--camera', type=int, nargs='?', const=0, help="Camera index to use (default 0).")
    parser.add_argument('--frame-interval', type=int, default=1, help="Process every Nth frame (default: 1).")
    parser.add_argument('--max-frames', type=int, default=1000, help="Maximum number of frames to process (default: 1000).")
    parser.add_argument('--model', type=str, default="Salesforce/blip-image-captioning-base", help="Hugging Face model to use.")
    parser.add_argument('--output', type=str, help="Write output to this file.")
    parser.add_argument('--no-display', action='store_true', help="Do not display video/camera frames.")
    parser.add_argument('--device', choices=['cpu', 'cuda'], help="Force device (cpu or cuda).")
    parser.add_argument('--use-fast', action='store_true', help="Force use_fast=True for the processor.")
    parser.add_argument('--no-fast', action='store_true', help="Force use_fast=False for the processor.")
    args = parser.parse_args()

    # Determine use_fast logic
    use_fast = None
    if args.use_fast:
        use_fast = True
    elif args.no_fast:
        use_fast = False

    if args.camera is not None:
        print(f"[DEBUG] Starting live feed description example with camera {args.camera}...")
        video_capture = cv2.VideoCapture(args.camera)
        live_feed_description = describe_scene(
            video_capture,
            model=args.model,
            device=args.device,
            use_fast=use_fast,
            frame_interval=args.frame_interval,
            max_frames=args.max_frames,
            no_display=args.no_display,
            output=args.output
        )
        if live_feed_description:
            print(f"Live Feed Description:\n{live_feed_description}\n")
    elif args.source:
        print(f"[DEBUG] Starting description for source: {args.source}")
        description = describe_scene(
            args.source,
            model=args.model,
            device=args.device,
            use_fast=use_fast,
            frame_interval=args.frame_interval,
            max_frames=args.max_frames,
            no_display=args.no_display,
            output=args.output
        )
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
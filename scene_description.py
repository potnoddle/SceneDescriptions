from transformers import pipeline
import cv2
import time

def describe_scene(source):
    """
    Generates a text description of a scene from an image or video source.

    Args:
        source: Either a path to an image/video file (string) or a video capture object (cv2.VideoCapture).

    Returns:
        A string containing the scene description, or None if an error occurs.
    """

    try:
        if isinstance(source, str):  # Image or video file
            if source.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # Image
                image_processor = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
                description = image_processor(source)[0]["generated_text"]
                return description
            else:  # Video file
                video_capture = cv2.VideoCapture(source)
                if not video_capture.isOpened():
                    print(f"Error: Could not open video file: {source}")
                    return None
                return _describe_video_feed(video_capture, is_live_feed=False)

        elif isinstance(source, cv2.VideoCapture):  # Live video feed
            if not source.isOpened():
                print("Error: Could not open video feed.")
                return None
            return _describe_video_feed(source, is_live_feed=True)

        else:
            print("Error: Invalid source type. Please provide a file path or a cv2.VideoCapture object.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def _describe_video_feed(video_capture, is_live_feed):
    """
    Generates a text description of a video feed, optionally including timestamps for live feeds.

    Args:
        video_capture: A cv2.VideoCapture object representing the video feed.
        is_live_feed: A boolean indicating whether the feed is live (True) or from a file (False).

    Returns:
        A string containing the scene description with optional timestamps, or None if the video capture fails.
    """
    try:
        image_processor = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        descriptions = []
        while True:
            ret, frame = video_capture.read()
            if not ret:
                if is_live_feed:
                    print("End of live feed.")
                break  # End of video or live feed

            # Convert frame to RGB (required by the model)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get description
            description = image_processor(frame_rgb)[0]["generated_text"]

            if is_live_feed:
                timestamp = time.strftime("%H:%M:%S")
                descriptions.append(f"[{timestamp}] {description}")
            else:
                descriptions.append(description)
            if not is_live_feed:
                break # Process only the first frame for video files

        video_capture.release()  # Release the video capture object

        return "\n".join(descriptions) if descriptions else None
    except Exception as e:
        print(f"An error occurred during video processing: {e}")
        if video_capture.isOpened():
            video_capture.release()
        return None

if __name__ == "__main__":
    # Example usage with an image file:
    image_path = "your_image.jpg"  # Replace with your image file
    image_description = describe_scene(image_path)
    if image_description:
        print(f"Image Description:\n{image_description}\n")

    # Example usage with a video file:
    video_path = "your_video.mp4"  # Replace with your video file
    video_description = describe_scene(video_path)
    if video_description:
        print(f"Video Description:\n{video_description}\n")

    # Example usage with a live video feed (camera):
    #video_capture = cv2.VideoCapture(0)  # 0 usually represents the default camera
    #live_feed_description = describe_scene(video_capture)
    #if live_feed_description:
    #    print(f"Live Feed Description:\n{live_feed_description}")

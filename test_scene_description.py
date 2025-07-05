from scene_description import describe_scene
import cv2


def test_image():
    image_path = "test-data/new-york.jpg"  # Replace with your image file
    print("[TEST] Testing image description...")
    description = describe_scene(image_path)
    print(f"Image Description:\n{description}\n")


def test_video():
    video_path = "test-data/sample.mp4"  # Replace with your video file
    print("[TEST] Testing video description...")
    description = describe_scene(video_path)
    print(f"Video Description:\n{description}\n")


def test_camera(camera_index=0):
    print(f"[TEST] Testing live camera feed (camera {camera_index})...")
    video_capture = cv2.VideoCapture(camera_index)
    description = describe_scene(video_capture)
    print(f"Live Feed Description:\n{description}\n")


if __name__ == "__main__":
    test_image()
    test_video()
    # test_camera()  # Uncomment to test live camera
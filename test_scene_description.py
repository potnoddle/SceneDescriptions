import pytest
from scene_description import describe_scene  # Assuming scene_description.py is in the same directory


def test_describe_scene_with_image():
    """Tests describe_scene with a local image file."""

    # Replace 'path/to/your/test_image.jpg' with an actual image file in your project
    image_path = "test_image.jpg"  # Update with your test image file name

    # Create a dummy image file if it doesn't exist
    try:
        with open(image_path, "rb") as f:
            pass
    except FileNotFoundError:
        with open(image_path, "wb") as f:
            f.write(b"This is a dummy image file.")

    description = describe_scene(image_path)
    assert isinstance(description, str), f"Expected a string description, got: {type(description)}"
    assert len(description) > 0, "Description should not be empty."


def test_describe_scene_with_video():
    """Tests describe_scene with a local video file."""

    # Replace 'path/to/your/test_video.mp4' with an actual video file in your project
    video_path = "test_video.mp4"  # Update with your test video file name

    # Create a dummy video file if it doesn't exist
    try:
        with open(video_path, "rb") as f:
            pass
    except FileNotFoundError:
        with open(video_path, "wb") as f:
            f.write(b"This is a dummy video file.")

    description = describe_scene(video_path)
    assert isinstance(description, str), f"Expected a string description, got: {type(description)}"
    assert len(description) > 0, "Description should not be empty."

# To run the tests:
# 1. Save this file as test_scene_description.py in the same directory as scene_description.py
# 2. Run pytest from your terminal:  pytest
# You can also specify the file: pytest test_scene_description.py
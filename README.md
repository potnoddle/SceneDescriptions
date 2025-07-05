# Scene Description Project

This project uses a pre-trained image captioning model to generate text descriptions of scenes from images or videos. It can process both static images, video files, and live video feeds (e.g., from a webcam).

## Requirements

- Python 3.7+
- `transformers` library
- `opencv-python` library

## Installation

1.  **Install the required libraries:**

    ```bash
    pip install transformers opencv-python
    ```

    This will install the necessary packages, including `transformers` for the image captioning model and `opencv-python` for video handling.

2.  **Download the model (automatic):**

    The first time you run the script, it will automatically download the `Salesforce/blip-image-captioning-base` model from the Hugging Face Model Hub. This may take a few minutes depending on your internet connection.

## Usage

1.  **Clone the repository (if applicable) or download the `scene_description.py` script.**

2.  **Run the script from the command line:**

    ```bash
    python scene_description.py
    ```

3.  **Modify the example usage in the `if __name__ == "__main__":` block of `scene_description.py` to suit your needs.**  You can provide:

    -   A path to an image file (e.g., `"your_image.jpg"`).  Supported image formats include PNG, JPG, JPEG, BMP, and TIFF.
    -   A path to a video file (e.g., `"your_video.mp4"`).  The script currently processes only the first frame of video files for a general scene description.
    -   (Optional)  Uncomment the live video feed section and adjust `cv2.VideoCapture(0)` if necessary to use your default camera (usually `0`). Camera access may require permissions depending on your operating system.

4.  **The script will print the generated descriptions to the console.**

## Example

Here's an example of the output you might see:


4.  **(Optional) Test the live feed:** Uncomment the live feed section and run the script. Verify that it captures frames from your camera and generates descriptions with timestamps.

For more rigorous testing, we have included a test suite using the `pytest` framework. This suite includes test functions that assert the expected behavior of the `describe_scene` function with different file inputs.

## Running Tests

1.  Ensure you have `pytest` installed. If not, install it using pip:

    ```bash
    pip install pytest
    ```

2.  Run the tests from the project's root directory:

    ```bash
    pytest
    ```

    Or, to run a specific test file:

    ```bash
    pytest test_scene_description.py
    ```

## Test Script (`test_scene_description.py`)

```python
import pytest
from scene_description import describe_scene  # Assuming scene_description.py is in the same directory

def test_describe_scene_with_image():
    description = describe_scene("test_image.jpg")  # Update with your test image file name
    assert isinstance(description, str), f"Expected a string description, got: {type(description)}"
    assert len(description) > 0, "Description should not be empty."

def test_describe_scene_with_video():
    description = describe_scene("test_video.mp4")  # Update with your test video file name
    assert isinstance(description, str), f"Expected a string description, got: {type(description)}"
    assert len(description) > 0, "Description should not be empty."
```

**Note:** You should replace `"test_image.jpg"` and `"test_video.mp4"` in the test script with the actual paths to your test image and video files. If the files do not exist, the test script will create dummy files for testing purposes. For more accurate testing, it is recommended to use real sample files that represent the inputs your application will handle.

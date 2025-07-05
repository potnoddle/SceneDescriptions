## Code Structure

-   `describe_scene(source, model, device, use_fast, frame_interval, max_frames, no_display, output)`:  
    The main function that handles scene description. It takes a `source` argument (file path, URL, or `cv2.VideoCapture` object) and several options for model selection, device, processor speed, frame sampling, output, and display. It returns a string containing the scene description or `None` if an error occurs. It calls the `_describe_video_feed` helper function to handle video inputs.

-   `_describe_video_feed(video_capture, is_live_feed, pipeline_kwargs, frame_interval, max_frames, no_display, output)`:  
    This helper function processes video feeds. It extracts frames from the `video_capture`, converts them to RGB, uses the image captioning pipeline to get a description, and optionally adds a timestamp for live feeds. It returns a string containing the descriptions (with timestamps if applicable) or `None` on failure.

## Testing

To test the script:

1.  **Prepare test files:**  
    Have a sample image file and a short video file available.

2.  **Run the script with arguments:**  
    Use the command line to specify your test files and options.  
    Example for image:
    ```sh
    python scene_description.py --source path/to/test-image.jpg
    ```
    Example for video:
    ```sh
    python scene_description.py --source path/to/test-video.mp4 --frame-interval 10 --max-frames 5
    ```
    Example for live camera (default camera 0):
    ```sh
    python scene_description.py --camera
    ```
    Example for live camera (camera 1, no display, save output):
    ```sh
    python scene_description.py --camera 1 --no-display --output camera_output.txt
    ```

3.  **Observe the output:**  
    Ensure that the descriptions generated are reasonable for the content of your test files. If you specified `--output`, check the output file.

4.  **Test different options:**  
    - Try `--device cpu` or `--device cuda` to force device selection.
    - Use `--use-fast` or `--no-fast` to control processor speed.
    - Try a different model with `--model`.

5.  **(Optional) Automated testing:**  
    For more rigorous testing, create a dedicated test suite using a framework like `pytest`.  
    Example test file (`test_scene_description.py`):
    ```python
    from scene_description import describe_scene

    def test_image_description():
        result = describe_scene("tests/test-image.jpg")
        assert isinstance(result, str) and len(result) > 0

    def test_video_description():
        result = describe_scene("tests/test-video.mp4", max_frames=2)
        assert isinstance(result, str) and len(result) > 0
    ```

6.  **Error handling:**  
    Test with invalid files or sources to ensure errors are handled gracefully.

---

**Tip:**  
Press `q` to quit the live camera feed if display is enabled.

For more details on options, see the [README.md](README.md).

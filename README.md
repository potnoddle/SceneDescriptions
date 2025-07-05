# SceneDescriptions

A Python tool to generate text descriptions of scenes from images, video files, or live camera feeds using Hugging Face Transformers.

## Requirements

- Python 3.8+
- `transformers`
- `torch`
- `opencv-python`
- `Pillow`

Install dependencies:
```sh
pip install transformers torch opencv-python Pillow
```

## Usage

Run the script from the command line:

### Describe an image (local or remote)
```sh
python scene_description.py --source path/to/image.jpg
python scene_description.py --source https://example.com/image.jpg
```

### Describe a video file (local or remote)
```sh
python scene_description.py --source path/to/video.mp4
python scene_description.py --source https://example.com/video.mp4
```

### Describe a live camera feed (default camera 0)
```sh
python scene_description.py --camera
```

### Describe a live camera feed (specific camera index)
```sh
python scene_description.py --camera 1
```

### Additional Options

- `--frame-interval N` : Process every Nth frame (default: 1)
- `--max-frames N` : Maximum number of frames to process (default: 1000)
- `--model MODEL_NAME` : Hugging Face model to use (default: Salesforce/blip-image-captioning-base)
- `--output FILE` : Write output to this file
- `--no-display` : Do not display video/camera frames
- `--device cpu|cuda` : Force device (cpu or cuda)
- `--use-fast` : Force use_fast=True for the processor
- `--no-fast` : Force use_fast=False for the processor

### Example: Process every 10th frame from a video and save output
```sh
python scene_description.py --source path/to/video.mp4 --frame-interval 10 --output results.txt
```

### Example: Use a different model and force CPU
```sh
python scene_description.py --source path/to/image.jpg --model Salesforce/blip-image-captioning-large --device cpu
```

## Notes

- Press `q` to quit the live camera feed.
- CUDA will be used if available for faster inference, unless overridden.
- If neither `--source` nor `--camera` is provided, you will be prompted for input.

## Testing

Move your tests to a separate file, e.g. `test_scene_description.py`, and import `describe_scene` for unit or integration testing.

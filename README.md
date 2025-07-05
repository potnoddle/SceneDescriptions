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

If neither `--source` nor `--camera` is provided, you will be prompted for input.

## Notes

- Press `q` to quit the live camera feed.
- CUDA will be used if available for faster inference.

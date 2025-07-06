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

### Available Models

You can use different pre-trained models with the `--model` argument. Here are some popular options:

#### BLIP Models (Recommended)
- `Salesforce/blip-image-captioning-base` (default) - Good balance of speed and quality
- `Salesforce/blip-image-captioning-large` - Higher quality but slower inference
- `Salesforce/blip2-opt-2.7b` - BLIP-2 model with better performance
- `Salesforce/blip2-flan-t5-xl` - BLIP-2 with T5 language model

#### Vision Encoder-Decoder Models
- `nlpconnect/vit-gpt2-image-captioning` - ViT + GPT-2 combination, good for general captioning
- `microsoft/trocr-base-printed` - Optimized for text recognition in images
- `microsoft/trocr-large-printed` - Larger version for better text recognition

#### Other Popular Models
- `microsoft/git-base` - Generative Image-to-text Transformer
- `microsoft/git-large` - Larger version of GIT model
- `google/vit-base-patch16-224` - Vision Transformer base model

#### Usage Examples with Different Models
```sh
# Use the large BLIP model for better quality
python scene_description.py --source image.jpg --model Salesforce/blip-image-captioning-large

# Use ViT-GPT2 model
python scene_description.py --source image.jpg --model nlpconnect/vit-gpt2-image-captioning

# Use BLIP-2 for state-of-the-art performance
python scene_description.py --source image.jpg --model Salesforce/blip2-opt-2.7b
```

**Note**: Larger models provide better quality descriptions but require more computational resources and memory. Choose based on your hardware capabilities and quality requirements.

## Examples

### Basic Image Captioning with Different Models

#### Using the default BLIP base model
```sh
python scene_description.py --source path/to/image.jpg
```

#### Using BLIP large model for higher quality
```sh
python scene_description.py --source path/to/image.jpg --model Salesforce/blip-image-captioning-large
```

#### Using ViT-GPT2 model (faster alternative)
```sh
python scene_description.py --source path/to/image.jpg --model nlpconnect/vit-gpt2-image-captioning
```

#### Using BLIP-2 for state-of-the-art performance
```sh
python scene_description.py --source path/to/image.jpg --model Salesforce/blip2-opt-2.7b
```

### Advanced Examples

#### Process video with different model and save output
```sh
python scene_description.py --source path/to/video.mp4 --model Salesforce/blip-image-captioning-large --frame-interval 10 --output results.txt
```

#### Force CPU usage with a specific model
```sh
python scene_description.py --source path/to/image.jpg --model nlpconnect/vit-gpt2-image-captioning --device cpu
```

#### Live camera feed with custom model
```sh
python scene_description.py --camera 0 --model Salesforce/blip-image-captioning-large --max-frames 100
```

#### Remote image with different model
```sh
python scene_description.py --source https://example.com/image.jpg --model microsoft/git-base --output description.txt
```

#### Batch processing with optimized settings
```sh
# Fast processing with ViT-GPT2
python scene_description.py --source path/to/video.mp4 --model nlpconnect/vit-gpt2-image-captioning --frame-interval 30 --no-display --output batch_results.txt
```

### Internet Webcam Examples

#### Connect to public webcam streams
```sh
# Abbey Road Studios, London (famous crosswalk)
python scene_description.py --source "https://video-downloads.earthcam.com/fecnetwork/9974.flv/chunklist_w827842225.m3u8" --model Salesforce/blip-image-captioning-base --frame-interval 60 --max-frames 10

# Times Square, New York City
python scene_description.py --source "https://videos3.earthcam.com/fecnetwork/4029.flv/chunklist_w1313086007.m3u8" --model nlpconnect/vit-gpt2-image-captioning --frame-interval 120 --output nyc_times_square.txt

# Generic IP camera examples (replace with actual camera IPs)
python scene_description.py --source "rtsp://username:password@192.168.1.100:554/stream1" --model Salesforce/blip-image-captioning-base --no-display --output security_log.txt

# HTTP MJPEG stream example
python scene_description.py --source "http://192.168.1.100:8080/video" --frame-interval 30 --max-frames 50
```

#### Popular Public Webcam URLs (Working Examples)
```sh
# Trevi Fountain, Rome (via SkylineWebcams)
python scene_description.py --source "https://hd-auth.skylinewebcams.com/live.m3u8?a=8l9dv3r6r0sht4go" --model Salesforce/blip-image-captioning-large --frame-interval 180

# Venice - St. Mark's Square
python scene_description.py --source "https://hd-auth.skylinewebcams.com/live.m3u8?a=piazza-san-marco" --model microsoft/git-base --max-frames 20 --output venice_observations.txt

# EarthCam Network examples (check earthcam.com for current URLs)
# Seaside Heights, New Jersey
python scene_description.py --source "https://videos3.earthcam.com/fecnetwork/15559.flv/chunklist_w1110524063.m3u8" --frame-interval 300 --output beach_activity.txt

# Nature/Wildlife cams (National Parks, Zoos)
# San Diego Zoo Panda Cam (check zoo websites for current streams)
python scene_description.py --source "https://zoo-cam-url/live.m3u8" --model Salesforce/blip2-opt-2.7b --frame-interval 600 --output wildlife_behavior.txt
```

#### Finding More Webcam URLs
```sh
# Check these websites for current working URLs:
# - https://www.earthcam.com/ (various categories)
# - https://www.skylinewebcams.com/ (European locations)
# - https://www.insecam.org/ (worldwide collection)
# - Local traffic departments for traffic cams
# - National parks and zoos for nature cams

# Example workflow to test a new URL:
python scene_description.py --source "NEW_WEBCAM_URL_HERE" --model nlpconnect/vit-gpt2-image-captioning --frame-interval 60 --max-frames 5 --output test_stream.txt
```

#### Using the Webcam Links Database
A comprehensive CSV file (`webcam_links.csv`) is included with this project containing accessible webcam URLs, descriptions, and technical details. You can use this database to:

```sh
# Test multiple webcams from the CSV
# Example using some entries from the database:

# Abbey Road Studios (Cultural)
python scene_description.py --source "https://video-downloads.earthcam.com/fecnetwork/9974.flv/chunklist_w827842225.m3u8" --model Salesforce/blip-image-captioning-base --output abbey_road.txt

# Times Square (Urban)
python scene_description.py --source "https://videos3.earthcam.com/fecnetwork/4029.flv/chunklist_w1313086007.m3u8" --model nlpconnect/vit-gpt2-image-captioning --output times_square.txt

# Trevi Fountain (Tourist)
python scene_description.py --source "https://hd-auth.skylinewebcams.com/live.m3u8?a=fontana-di-trevi" --model microsoft/git-base --output trevi_fountain.txt
```

**CSV Database Structure:**
- **Name**: Webcam location name
- **Description**: Brief description of what the camera shows
- **Location**: Geographic location
- **Stream Type**: Technical format (HLS, RTSP, MJPEG, HTTP)
- **URL**: Direct stream URL
- **Provider**: Service provider (EarthCam, SkylineWebcams, etc.)
- **Category**: Type of location (Urban, Beach, Tourist, etc.)
- **Status**: Current availability status

### Specialized Use Cases

#### Security monitoring with text logs
```sh
# Monitor security camera and log descriptions with timestamps
python scene_description.py --source "rtsp://192.168.1.100:554/stream" --model Salesforce/blip-image-captioning-base --frame-interval 300 --output security_log.txt --no-display
```

#### Wildlife observation
```sh
# Analyze wildlife camera with detailed descriptions
python scene_description.py --source path/to/wildlife_video.mp4 --model Salesforce/blip2-opt-2.7b --frame-interval 60 --output wildlife_behavior.txt
```

#### Traffic analysis
```sh
# Analyze traffic patterns from traffic cam
python scene_description.py --source "http://traffic-cam-url/stream" --model nlpconnect/vit-gpt2-image-captioning --frame-interval 180 --max-frames 100 --output traffic_analysis.txt
```

#### Multiple camera comparison
```sh
# Compare descriptions from different models on same source
python scene_description.py --source camera_feed.mp4 --model Salesforce/blip-image-captioning-base --output blip_base_results.txt
python scene_description.py --source camera_feed.mp4 --model Salesforce/blip-image-captioning-large --output blip_large_results.txt
python scene_description.py --source camera_feed.mp4 --model nlpconnect/vit-gpt2-image-captioning --output vit_gpt2_results.txt
```

### Performance Optimization Examples

#### Low-resource environments
```sh
# Optimized for CPU-only environments
python scene_description.py --source path/to/video.mp4 --model nlpconnect/vit-gpt2-image-captioning --device cpu --use-fast --frame-interval 60 --no-display
```

#### High-quality analysis
```sh
# Maximum quality for important content
python scene_description.py --source path/to/important_video.mp4 --model Salesforce/blip2-flan-t5-xl --device cuda --no-fast --frame-interval 1 --max-frames 500
```

#### Real-time monitoring
```sh
# Live feed with frequent updates
python scene_description.py --camera 0 --model Salesforce/blip-image-captioning-base --frame-interval 5 --max-frames 1000 --output live_monitoring.txt
```

**Note on Internet Webcams**: Many public webcam streams require specific formats (RTSP, HLS, MJPEG). Always respect the terms of service of webcam providers and avoid overloading their servers with too frequent requests.

## Notes

- Press `q` to quit the live camera feed.
- CUDA will be used if available for faster inference, unless overridden.
- If neither `--source` nor `--camera` is provided, you will be prompted for input.

## Testing

Move your tests to a separate file, e.g. `test_scene_description.py`, and import `describe_scene` for unit or integration testing.

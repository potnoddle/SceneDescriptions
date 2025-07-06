import pandas as pd
import argparse
import cv2
import requests
from multiprocessing import Process, Queue
from tqdm import tqdm
import sys

def check_http_url(url, timeout=5):
    """Checks if an HTTP(S) or JPEG URL is accessible using a HEAD request."""
    try:
        # Use a session object for potential connection pooling
        with requests.Session() as s:
            s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            response = s.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code == 200
    except requests.RequestException:
        return False

def check_video_stream(url, queue):
    """
    Worker function to check a video stream URL with OpenCV.
    This function is designed to run in a separate process.
    """
    cap = cv2.VideoCapture(url)
    is_open = cap.isOpened()
    if is_open:
        # A more robust check is to try and read a frame.
        ret, _ = cap.read()
        is_open = ret
    queue.put(is_open)
    cap.release()

def is_url_active(url, stream_type, timeout=10):
    """
    Checks if a URL is active using the appropriate method based on stream type.
    Uses a subprocess with a timeout for video streams to prevent hangs.
    """
    stream_type = str(stream_type).upper()

    if stream_type in ['JPEG', 'JPG']:
        return check_http_url(url, timeout=timeout)

    # For video streams (HLS, RTSP, MJPEG, etc.), use OpenCV in a subprocess
    # to prevent the main script from hanging on a bad network link.
    q = Queue()
    p = Process(target=check_video_stream, args=(url, q))
    p.start()
    p.join(timeout=timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return False  # Timed out

    if q.empty():
        return False  # Process likely crashed or finished without returning a value

    return q.get()

def main(input_file, output_file, timeout):
    """
    Reads a CSV of webcam links, removes duplicates, checks for active links,
    and saves the result to a new CSV file.
    """
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file}'")
        sys.exit(1)

    print(f"Loaded {len(df)} records from '{input_file}'.")

    # Remove template/placeholder URLs first
    df = df[~df['Category'].isin(['Template', 'Security'])].copy()

    # Remove duplicates based on URL, keeping the first entry
    original_count = len(df)
    df.drop_duplicates(subset=['URL'], keep='first', inplace=True)
    print(f"Removed {original_count - len(df)} duplicate records. {len(df)} unique URLs to check.")

    active_rows = []

    # Use tqdm for a nice progress bar
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Checking URLs"):
        if is_url_active(row['URL'], row.get('Stream Type', 'HLS'), timeout):
            active_rows.append(row)

    if not active_rows:
        print("\nNo active links found. Output file will not be created.")
        return

    # Create a new DataFrame from the list of active link rows
    active_df = pd.DataFrame(active_rows)

    # Update the status column for clarity
    active_df['Status'] = 'Verified Active'

    print(f"\nFound {len(active_df)} active and unique links.")

    # Save to output file
    active_df.to_csv(output_file, index=False, quoting=1) # quoting=1 is csv.QUOTE_ALL
    print(f"Saved verified links to '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check webcam links from a CSV file, remove duplicates, and save active links.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i', '--input', default='webcam_links.csv', help="Path to the input CSV file."
    )
    parser.add_argument(
        '-o', '--output', default='verified_webcam_links.csv', help="Path to save the output CSV file with verified links."
    )
    parser.add_argument(
        '-t', '--timeout', type=int, default=10, help="Timeout in seconds for checking each URL."
    )
    args = parser.parse_args()

    main(args.input, args.output, args.timeout)
import cv2  # pip install opencv-python
import numpy as np  # pip install numpy
import pytesseract as pt  # pip install pytesseract
import datetime as dt
import json
import os
import sys

def mse(frame_a, frame_b):
    return np.sum((frame_a.astype('float') - frame_b.astype('float')) ** 2) / frame_a.size

def detect_capture(frame_a, frame_b, frame_count, mse_threshold):
    if frame_a is None or frame_b is None or frame_a.size != frame_b.size:
        return True
    else:
        error = mse(frame_a, frame_b)
        if error > 0: print(f"Frame #{frame_count} has error {error:,f} detect capture {error > mse_threshold}")
        return error > mse_threshold

def capture_slides(video_path, output_path, mse_threshold, sec_skip):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_skips = frame_rate * sec_skip
    print(frame_skips)
    prev_frame = None
    frame_count = 0
    while cap.isOpened():
        (grabSuccessful, frame) = cap.read()
        if not grabSuccessful: break
        if frame_count % frame_skips == 0 and detect_capture(prev_frame, frame, frame_count, mse_threshold):
            timestamp = str(dt.timedelta(seconds=frame_count/frame_rate))
            save_path = os.path.join(output_path, f"time_{timestamp}.jpg".replace(':', ';'))
            cv2.imwrite(save_path, frame)
            print(f"Saved screenshot: {save_path}")
            prev_frame = frame
        frame_count = frame_count + 1
    cap.release()

def read_slides(output_path):
    summary_path = os.path.join(output_path, "summary.txt")
    border_length = 15
    with open(summary_path, 'w') as summary_file:
        slides = filter(lambda s: s.endswith(".jpg"), os.listdir(output_path))
        slides = map(lambda s: os.path.join(output_path, s), slides)
        for slide in slides:
            text = pt.image_to_string(slide)
            summary_file.write(f"{'>' * border_length} {slide} {'>' * border_length}" + os.linesep)
            summary_file.write(text + os.linesep)
            summary_file.write(f"{'<' * border_length} {slide} {'<' * border_length}" + os.linesep)
            print(f"Processed text in: {slide}")
        print(f"Summary file written: {summary_path}")

if __name__ == '__main__':
    src_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    config_path = os.path.join(src_path, "config.json")
    with open(config_path) as json_file:
        config = json.load(json_file)
    mse_threshold = config['mse_threshold']
    sec_skip = config['sec_skip']
    pt.pytesseract.tesseract_cmd = config['tesseract_path']
    video_path = config['video_path']
    (path, file_name) = os.path.split(video_path)
    output_path = os.path.join(path, f"processed_{file_name}")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        capture_slides(video_path, output_path, mse_threshold, sec_skip)
    read_slides(output_path)

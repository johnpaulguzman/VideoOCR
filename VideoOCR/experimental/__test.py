import cv2  # pip install opencv-python
import numpy as np  # pip install numpy
import pytesseract as pt  # pip install pytesseract
import datetime as dt
import os
import sys

def mse(frame_a, frame_b):
    if frame_a is None or frame_b is None: return 0
    import code; code.interact(local={**locals(), **globals()})
    return np.sum((frame_a.astype('float') - frame_b.astype('float')) ** 2)

def detect_capture(frame_a, frame_b, frame_count, error_threshold):
    if frame_a is None or frame_b is None:
        return True
    else:
        error = mse(frame_a, frame_b)
        if error > 0: print(f"Frame #{frame_count} has error {error:,f} detect capture {error > error_threshold}")
        return error > error_threshold

def cv2_generator(cap):
    frame_count = 0
    while cap.isOpened():
        (grab_successful, frame) = cap.read()
        if not grab_successful: break
        frame_count += 1
        yield (frame_count, frame)
    cap.release()

def capture_slides(video_path, output_directory, error_threshold):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_skips = frame_rate * sec_skip
    prev_frame = None
    errors = []
    for (frame_count, frame) in cv2_generator(cap):
        errors += [mse(prev_frame, frame)]
        prev_frame = frame
    import code; code.interact(local={**locals(), **globals()})

def read_slides(output_directory):
    summary_path = f"{output_directory}/summary.txt"
    border_length = 15
    with open(summary_path, 'w') as summary_file:
        slides = filter(lambda s: s.endswith(".jpg"), os.listdir(output_directory))
        slides = map(lambda s: os.path.join(output_directory, s), slides)
        for slide in slides:
            text = pt.image_to_string(slide)
            summary_file.write(f"{'>' * border_length} {slide} {'>' * border_length}" + os.linesep)
            summary_file.write(text + os.linesep)
            summary_file.write(f"{'<' * border_length} {slide} {'<' * border_length}" + os.linesep)
            print(f"Processed text in: {slide}")
        print(f"Summary file written: {summary_path}")

if __name__ == '__main__':
    video_path = sys.argv[1]
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    output_directory = f"test_processed_{video_path}"
    error_threshold = 10 ** 7
    sec_skip = 2
    capture_slides(video_path, output_directory, error_threshold)

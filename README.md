# VideoOCR


---
## Installation
  - Install [Python 3](https://www.python.org/downloads/)
  - Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
  - Run: `pip install -r requirements.txt`

---
## Usage
  - Update the contents of `config.json`
    - Use absolute paths
    - `mse_threshold`: used for detecting change between 2 frames (default=10) 
    - `sec_skip`: used to skip some frames immediately after a new frame capture (default=2)
  - Run: `python video_ocr.py`

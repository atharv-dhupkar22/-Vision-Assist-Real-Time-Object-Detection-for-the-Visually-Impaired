# -Vision-Assist-Real-Time-Object-Detection-for-the-Visually-Impaired
# 👁️‍🗨️ Vision Assist — Real-Time Object Detection for the Visually Impaired

Empowering visually impaired individuals with AI-powered real-time object detection and multilingual audio feedback.  
Built with **YOLOv8 + OpenCV + pyttsx3 + Google TTS**, this Python-based solution captures live video, identifies surrounding objects, and narrates them — all in your preferred language. 🌍🔊

---

## 🎯 Features

✅ Real-time object detection using YOLOv8  
✅ Audio feedback via offline or online TTS  
✅ Multilingual speech support (English, Hindi, Marathi, etc.)  
✅ Smart speech throttling (no repetition)  
✅ Detection logs stored with timestamps  
✅ Clean modular codebase & easy customization

---

## 🧠 How It Works


- Captures live webcam frames
- Detects common objects using YOLOv8
- Avoids repeating the same object every second
- Converts labels into natural speech using `pyttsx3` or `gTTS`
- Saves logs to `logs/detections.csv`

---


## 🛠️ Installation

### 📌 Prerequisites

- Python 3.8+
- pip
- Webcam & audio output (speaker/headphones)

### ⚙️ Setup

```bash
# 1. Clone or download this repo
git clone 
cd vision-assist

# 2. (Optional) Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install required packages
pip install -r requirements.txt

# 4. Run the app
python main.py

# 🔥 Industrial AI Safety Monitoring System

An AI-powered Industrial Safety Monitoring System that performs **real-time Fire, Smoke, Object Detection, Threat Analysis, Event Recording, and Alert Generation** using YOLOv8 and Computer Vision.

---

## 🚀 Features

- 🔥 Fire Detection
- 💨 Smoke Detection
- 👷 Person Detection
- 🚜 Industrial Object Detection
- 📷 Live Camera Monitoring
- 📊 Threat Level Analysis
- 🔔 Telegram Alerts
- 📧 Email Alerts
- 🚨 Siren Alert
- 🎥 Automatic Event Recording
- 📸 Snapshot Capture
- 📈 FPS Counter
- 🖥️ Heads-Up Display (HUD)
- 🧠 Object Tracking
- 📋 Event Logging

---

# Project Structure

```
Industrial-AI-Safety-Monitor/
│
├── main.py
├── train_model.py
├── data.yaml
├── fire_smoke.pt
│
├── config/
│     └── settings.py
│
├── detectors/
│     ├── fire_detector.py
│     ├── object_detector.py
│     ├── scene_detector.py
│     └── threat_analyzer.py
│
├── tracking/
│     └── tracker.py
│
├── alerts/
│     ├── telegram_alert.py
│     ├── email_alert.py
│     └── siren.py
│
├── recording/
│     └── event_recorder.py
│
├── ui/
│     └── hud.py
│
├── utils/
│     ├── fps.py
│     └── logger.py
│
├── dataset/
│     ├── train/
│     ├── valid/
│     └── data.yaml
│
└── requirements.txt
```

---

# Tech Stack

- Python 3.10+
- OpenCV
- YOLOv8 (Ultralytics)
- NumPy
- PyTorch
- Threading
- SMTP (Email)
- Telegram Bot API

---

# Libraries Used

Install all required packages:

```bash
pip install ultralytics
pip install opencv-python
pip install numpy
pip install torch torchvision
pip install pyyaml
pip install requests
pip install pillow
pip install tqdm
```

Or

```bash
pip install -r requirements.txt
```

---

# Dataset

Dataset follows YOLO format.

```
dataset/

    train/
        images/
        labels/

    valid/
        images/
        labels/

    data.yaml
```

---

# Model Training

Train the custom Fire & Smoke model.

```bash
python train_model.py
```

Training Parameters

| Parameter | Value |
|-----------|-------|
| Model | YOLOv8 Nano |
| Epochs | 100 |
| Image Size | 640 |
| Batch Size | 8 |

---

# Running the System

```bash
python main.py
```

The system will

- Start Camera
- Detect Fire
- Detect Smoke
- Detect Objects
- Track Objects
- Analyze Threat Level
- Record Events
- Send Alerts
- Display Live Monitoring Window

Press **Q** to Exit.

---

# Workflow

```
Camera Input
      │
      ▼
Frame Capture
      │
      ▼
Fire & Smoke Detection (YOLOv8)
      │
      ▼
Object Detection
      │
      ▼
Scene Analysis
      │
      ▼
Object Tracking
      │
      ▼
Threat Analyzer
      │
      ▼
HIGH / CRITICAL ?
      │
      ├────────── No
      │             │
      │             ▼
      │        Continue Monitoring
      │
      ▼
Save Snapshot
      │
      ▼
Record Event
      │
      ▼
Send Alerts
(Telegram / Email / Siren)
      │
      ▼
Display HUD
      │
      ▼
Next Frame
```

---

# Threat Levels

- 🟢 LOW
- 🟡 MEDIUM
- 🟠 HIGH
- 🔴 CRITICAL

---

# Future Improvements

- PPE Detection (Helmet, Vest, Gloves)
- Fall Detection
- Gas Leak Detection
- Thermal Camera Support
- Multi-Camera Monitoring
- Web Dashboard
- Mobile Application
- Cloud Deployment
- AI-Based Accident Prediction

---

# Results

- Real-time Fire Detection
- Smoke Detection
- Threat Classification
- Automatic Alert Generation
- Event Recording
- Live Monitoring Dashboard

---

# Author

**P.Santhosh**

MCA Student

---

# License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, don't forget to **Star** this repository.

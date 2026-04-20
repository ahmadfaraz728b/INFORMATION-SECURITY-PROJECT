# 🛡️ HID Biometric Shield (BadUSB Detection System)

## 📌 Project Overview
HID Biometric Shield is a real-time security system designed to detect **BadUSB / HID injection attacks** by analyzing keystroke behavior patterns. It uses behavioral biometrics such as typing rhythm, speed, and variance to distinguish between humans and automated input devices.

The system provides a live GUI dashboard for monitoring, threat scoring, and audit logging.

---

## 🚨 Problem Statement
Physical HID devices (BadUSBs) can inject scripted keystrokes that mimic human input. Traditional security tools struggle to detect such attacks because they appear as normal keyboard activity.

---

## 🎯 Solution
This system detects HID injection by:
- Monitoring inter-keystroke timing
- Calculating variance and average speed
- Identifying robotic typing patterns
- Generating a real-time threat score
- Triggering mitigation on attack detection

---

## ⚙️ Features

### 🔍 Behavioral Analysis
- Captures inter-keystroke intervals
- Uses sliding window (max 25 samples)
- Requires minimum 12 samples before analysis

### 📊 Threat Detection
- Variance-based anomaly detection
- Speed threshold analysis
- Combined scoring system (0–100%)

### 🧠 Threat Scoring Logic
- +50 if variance < robotic precision limit
- +50 if average speed < human threshold
- Score ≥100 triggers mitigation

### 🖥️ Live Dashboard
- Typing Velocity (average interval)
- Rhythm Variance
- Threat Probability (%)
- Real-time color-coded threat gauge

### 📜 Audit Logging
- Logs all events with timestamps
- Stores:
  - Arm/disarm actions
  - Simulated attacks
  - CRITICAL detections
- Saves to `security_audit.txt`

### ⚔️ Mitigation Actions
- Immediate CRITICAL alert popup
- Clears keystroke history
- Stops monitoring system
- Logs incident for forensic analysis

### 🧪 Attack Simulation
- Simulates HID injection behavior
- Uses fast fixed intervals (~10–50ms)
- Used for testing detection accuracy

---

## 🧮 Key Thresholds

```python
ROBOTIC_PRECISION_LIMIT = 0.0004
HUMAN_SPEED_THRESHOLD = 0.07

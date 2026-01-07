# Biometric Identity Verification System (PoC)

**Status:** Proof of Concept  
**Security Domain:** Physical Access Control / Anti-Spoofing

## Overview
A Python-based facial recognition system designed to simulate secure access control. It utilizes `dlib` for 128-point facial landmark estimation and includes a modular framework for **Liveness Detection** to mitigate Presentation Attacks (2D photo spoofing).

## Key Features
* **Real-Time Recognition:** Processes video feeds using the HOG (Histogram of Oriented Gradients) algorithm.
* **Access Logging:** Automatically logs timestamps and authorization states for audit trails.
* **Anti-Spoofing Architecture:** Contains placeholder logic for depth-map analysis and blink detection (Liveness Check).

## Tech Stack
* **Core:** Python 3.10, OpenCV (cv2)
* **ML Engine:** `face_recognition` (dlib wrapper)
* **Data Handling:** JSON / Local File Storage

## Installation
```bash
# Install dependencies (CMake required for dlib)
pip install -r requirements.txt

# Add authorized images to /database folder
mkdir database
cp my_photo.jpg database/admin.jpg

# Run the surveillance engine
python main.py

Disclaimer
Proprietary Logic Notice: This repository contains the core recognition framework. The advanced "Liveness Detection" algorithm (used to differentiate between a real face and a screen/photo) has been replaced with a placeholder function for public release.

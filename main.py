import face_recognition
import cv2
import json
import requests
import asyncio
import os
import sys
import time

# --- CONFIGURATION ---
# In a real deployment, these would be loaded from a secure .env file
CONFIG = {
    "THRESHOLD": 0.6,
    "LOG_FILE": "access_logs.txt",
    "CAMERA_INDEX": 0
}

# --- SETUP ---
print("[*] Initializing Biometric Engine...")
known_face_encodings = []
known_face_names = []

# Load authorized personnel
if os.path.exists("database"):
    print("[*] Loading Identity Database...")
    for filename in os.listdir("database"):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            name = filename.split('.')[0]
            try:
                image = face_recognition.load_image_file(f"database/{filename}")
                encs = face_recognition.face_encodings(image)
                if encs:
                    known_face_encodings.append(encs[0])
                    known_face_names.append(name)
                    print(f"    [+] Loaded ID: {name}")
            except Exception as e:
                print(f"    [!] Error loading {filename}: {e}")

# --- CORE LOGIC ---
def log_access(name, status):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] USER: {name} | STATUS: {status}\n"
    with open(CONFIG["LOG_FILE"], "a") as f:
        f.write(entry)
    print(entry.strip())

def liveness_check(frame):
    """
    Simulated Liveness Detection.
    In a production environment, this would analyze depth maps, 
    eye-blinking, or texture analysis to prevent 2D spoofing.
    """
    # Placeholder: Assuming True for this PoC
    return True

def draw_hud(frame, status, name="Unknown"):
    h, w, _ = frame.shape
    color = (0, 255, 0) if status == "GRANTED" else (0, 0, 255)
    
    # Target Box
    cv2.rectangle(frame, (int(w/2)-100, int(h/2)-100), (int(w/2)+100, int(h/2)+100), color, 2)
    
    # Status Text
    cv2.putText(frame, f"ID: {name.upper()}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, f"ACCESS: {status}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return frame

def start_surveillance():
    print("[*] SECURITY FEED ACTIVE. PRESS 'q' TO STOP.")
    cam = cv2.VideoCapture(CONFIG["CAMERA_INDEX"])
    
    process_this_frame = True
    
    while True:
        ret, frame = cam.read()
        if not ret: break

        # Optimization: Process every other frame
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            name = "Unknown"
            status = "DENIED"

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=CONFIG["THRESHOLD"])
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    
                    if liveness_check(frame):
                        status = "GRANTED"
                        log_access(name, "AUTHORIZED")
                    else:
                        status = "SPOOF DETECTED"
                        log_access(name, "SPOOF_ATTEMPT")
                else:
                    log_access("Unknown", "DENIED")

        process_this_frame = not process_this_frame

        # Display Result
        cv2.imshow('Biometric Identity Verification System', draw_hud(frame, status, name))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_surveillance()

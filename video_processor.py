import cv2
import numpy as np
import time

class VideoProcessor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        self.blink_count = 0
        self.last_state_change = time.time()
        self.prev_gray = None

    def process_frame(self, frame):
        """Traitement dynamique de la webcam (mouvement + visage + yeux)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Calcul du mouvement global (différence entre images consécutives)
        motion_score = 0.0
        if self.prev_gray is not None:
            diff = cv2.absdiff(self.prev_gray, gray)
            motion_score = np.mean(diff)
        self.prev_gray = gray.copy()

        # 2. Détection du visage
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        
        status = "Actif / Normal"
        ear_avg = 0.35

        if len(faces) == 0:
            status = "Visage absent"
            ear_avg = 0.15
        else:
            for (x, y, w, h) in faces:
                # Dessiner le rectangle du visage
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Analyser la zone des yeux (partie supérieure du visage)
                roi_gray = gray[y:y+int(h*0.6), x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3)
                
                # Si le mouvement est très faible et peu d'yeux détectés -> simuler de la fatigue
                if motion_score < 1.5 and len(eyes) < 2:
                    ear_avg = 0.18
                    status = "Fatigue / Inattention"
                else:
                    ear_avg = 0.32
                    status = "Vigilant"

        return frame, ear_avg, status, motion_score
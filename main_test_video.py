from scr.video_processor import VideoProcessor
import cv2
from src.video_processor import VideoProcessor

cap = cv2.VideoCapture(0)
processor = VideoProcessor()

print("Démarrage du test vidéo... Appuie sur 'q' pour quitter.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Traitement
    frame, ear, status, blinks = processor.process_frame(frame)

    # Affichage des métriques à l'écran
    color = (0, 255, 0) if status == "Vigilant" else (0, 0, 255)
    cv2.putText(frame, f"EAR: {ear:.2f}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f"Statut: {status}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(frame, f"Clignements: {blinks}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("Test Module Video - Stress/Fatigue", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
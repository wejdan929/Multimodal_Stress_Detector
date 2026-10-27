import cv2
import time
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from fusion_engine import FusionEngine
def main():
    print("Initialisation du système multimodal (Caméra + Micro)...")
    
    # Initialisation des modules
    cap = cv2.VideoCapture(0)
    video_proc = VideoProcessor()
    audio_proc = AudioProcessor(duration=0.5)
    fusion_engine = FusionEngine()

    # Démarrage de l'audio
    audio_proc.start_listening()
    
    print("Application lancée ! Regarde la caméra. Appuie sur 'q' pour quitter.")

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Erreur de lecture de la webcam.")
                break

            # 1. Traitement Vidéo
            frame, ear, video_status, blinks = video_proc.process_frame(frame)

            # 2. Récupération Audio
            rms, zcr, voice_status = audio_proc.get_metrics()

            # 3. Fusion Multimodale
            global_status, status_color, score = fusion_engine.evaluate_state(
                video_status, voice_status, rms
            )

            # 4. Affichage graphique sur la fenêtre vidéo
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (620, 180), (50, 50, 50), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

            cv2.putText(frame, f"--- SYSTEME MULTIMODAL STRESS/FATIGUE ---", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"EAR (Yeux): {ear:.2f} | Clignements: {blinks}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Audio RMS (Vol): {rms:.4f} | Statut: {voice_status}", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
            cv2.putText(frame, f"Statut Global: {global_status}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

            cv2.imshow("Multimodal Stress & Fatigue Detector", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        audio_proc.stop_listening()
        cap.release()
        cv2.destroyAllWindows()
        print("Arrêt propre de l'application.")

if __name__ == "__main__":
    main()
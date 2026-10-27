import time
from scr.audio_processor import AudioProcessor

print("Initialisation du processeur audio...")
audio_proc = AudioProcessor(duration=1.0)

print("Démarrage de l'écoute du micro... Parle ou fais du bruit (Appuie sur Ctrl+C pour arrêter).")
audio_proc.start_listening()

try:
    while True:
        rms, zcr, status = audio_proc.get_metrics()
        print(f"RMS (Volume): {rms:.4f} | ZCR (Variation): {zcr:.4f} | Statut: {status}", end="\r")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nArrêt de l'écoute...")
    audio_proc.stop_listening()
    print("Test audio terminé avec succès !")
import time
from audio_processor import AudioProcessor

def main():
    print("=== TEST DU MODULE AUDIO ===")
    print("Parlez dans le micro pour voir si les valeurs changent (Appuyez sur Ctrl+C pour quitter).\n")
    
    # Initialisation et démarrage de l'écoute audio
    audio_proc = AudioProcessor()
    audio_proc.start_listening()
    
    try:
        while True:
            rms, zcr, status = audio_proc.get_metrics()
            # Affiche les valeurs en direct dans la console
            print(f"Volume RMS (Volume): {rms:.4f} | Statut: {status}", end="\r")
            time.sleep(0.3)
            
    except KeyboardInterrupt:
        print("\n\nArrêt du test audio.")
        audio_proc.stop_listening()

if __name__ == "__main__":
    main()
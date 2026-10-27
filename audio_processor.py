import threading
import time
import numpy as np

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

class AudioProcessor:
    def __init__(self, duration=0.5):
        self.duration = duration
        self.rms = 0.02  # Valeur par défaut pour éviter le 0 absolu
        self.zcr = 0.0
        self.voice_status = "Audio en attente"
        self.running = False
        self.thread = None

    def start_listening(self):
        if not HAS_SOUNDDEVICE:
            print("AVERTISSEMENT: 'sounddevice' n'est pas installé. Mode audio simulé actif.")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self):
        def callback(indata, frames, time_info, status):
            try:
                audio_data = indata[:, 0]
                self.rms = float(np.sqrt(np.mean(audio_data**2)))
                if self.rms > 0.03:
                    self.voice_status = "Voix active"
                else:
                    self.voice_status = "Calme"
            except Exception as e:
                self.voice_status = "Erreur calcul audio"

        try:
            # Test d'ouverture du flux audio sur le micro par défaut
            with sd.InputStream(callback=callback, channels=1, samplerate=16000, blocksize=4000):
                while self.running:
                    time.sleep(0.1)
        except Exception as e:
            print(f"\n[INFO AUDIO] Impossible d'accéder au micro ({e}). Passage en mode simulation audio.")
            # Mode simulation dynamique pour que le projet reste fonctionnel
            while self.running:
                # Simule de légères variations de volume pour tester le moteur de fusion
                self.rms = float(np.random.uniform(0.01, 0.05))
                if self.rms > 0.035:
                    self.voice_status = "Voix (Simulée)"
                else:
                    self.voice_status = "Calme (Simulé)"
                time.sleep(0.5)

    def get_metrics(self):
        return self.rms, self.zcr, self.voice_status

    def stop_listening(self):
        self.running = False
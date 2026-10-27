class FusionEngine:
    def __init__(self):
        pass

    def evaluate_state(self, video_status, voice_status, rms):
        """Combine les signaux vidéo et audio pour évaluer l'état global."""
        score = 0.0

        # Poids de la vidéo (fatigue / absence)
        if "Fatigue" in video_status or "absent" in video_status:
            score += 0.6

        # Poids de l'audio (niveau sonore / voix)
        if rms > 0.06:
            score += 0.4
        elif rms < 0.01:
            score += 0.1

        # Décision finale du score combiné
        if score >= 0.7:
            return "Stress / Fatigue Élevé", (0, 0, 255), score       # Rouge
        elif score >= 0.4:
            return "Attention / Légère Fatigue", (0, 165, 255), score  # Orange
        else:
            return "Normal / Détendu", (0, 255, 0), score             # Vert
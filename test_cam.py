import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERREUR : Impossible d'ouvrir la webcam 0 !")
else:
    ret, frame = cap.read()
    if ret:
        print("SUCCÈS : La caméra fonctionne et a capturé une image !")
    else:
        print("ERREUR : La caméra est ouverte mais ne renvoie aucune image (flux vide).")

cap.release()
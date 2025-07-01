import cv2
import mediapipe
import time
import os

from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager

# RUTA ABSOLUTA al archivo compartido con el juego
LETRA_DETECTADA_PATH = "C:/Users/pro20/Documents/proyectos_CGVCM/Proyecto_Final/cg-project/letra_detectada.txt"
ultima_letra = None

if __name__ == "__main__":
    videos = load_dataset()
    reference_signs = load_reference_signs(videos)
    sign_recorder = SignRecorder(reference_signs)
    webcam_manager = WebcamManager()

    print("Attempting to open webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Still could not open webcam")
            exit(1)

    print("Webcam opened successfully!")
    print("Press 'r' to record a sign, 'q' to quit")

    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from webcam")
                break

            image, results = mediapipe_detection(frame, holistic)
            sign_detected, is_recording = sign_recorder.process_results(results)
            webcam_manager.update(frame, results, sign_detected, is_recording)

            if sign_detected and isinstance(sign_detected, str) and len(sign_detected) == 1:
                letra = sign_detected.upper()
                if letra != ultima_letra:  # Solo guardar si es diferente a la última letra guardada
                    print(f"[INFO] Letra detectada: {letra}")
                    try:
                        with open(LETRA_DETECTADA_PATH, "w") as f:
                            f.write(letra)
                            ultima_letra = letra  # Actualiza
                    except Exception as e:
                        print(f"[ERROR] No se pudo escribir la letra detectada: {e}")


            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("r"):
                print("Recording toggled!")
                sign_recorder.record()

            elif pressedKey == ord("q"):
                print("Quitting...")
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Program ended successfully")


def iniciar_detector_letras():
    videos = load_dataset()
    reference_signs = load_reference_signs(videos)

    sign_recorder = SignRecorder(reference_signs)
    webcam_manager = WebcamManager()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open webcam with CAP_DSHOW, trying default...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Still could not open webcam")
            return

    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            image, results = mediapipe_detection(frame, holistic)
            sign_detected, is_recording = sign_recorder.process_results(results)

            # Mostrar cámara opcionalmente
            webcam_manager.update(frame, results, sign_detected, is_recording)

            # Guardar la letra si fue detectada correctamente
            if sign_detected and len(sign_detected) == 1:
                letra = sign_detected.upper()
                with open("letra_detectada.txt", "w") as f:
                    f.write(letra)

            # Opcional: espera corta para no sobreescribir archivo cada frame
            time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()

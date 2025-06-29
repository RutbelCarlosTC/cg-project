# sign_recognizer.py
import cv2
import mediapipe

from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager


class SignRecognizer:
    def __init__(self):
        # Cargar dataset y señas de referencia
        self.videos = load_dataset()
        self.reference_signs = load_reference_signs(self.videos)
        self.sign_recorder = SignRecorder(self.reference_signs)
        self.webcam_manager = WebcamManager()
        self.last_sign = None
        self.running = False

    def run_once(self):
        """
        Corre la detección por un solo frame y retorna la seña detectada.
        """
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("No se pudo abrir la cámara")

        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise RuntimeError("No se pudo leer el frame de la cámara")

        with mediapipe.solutions.holistic.Holistic(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as holistic:
            image, results = mediapipe_detection(frame, holistic)
            sign_detected, _ = self.sign_recorder.process_results(results)
            self.webcam_manager.update(frame, results, sign_detected, False)

            if sign_detected and sign_detected != "Seña desconocida":
                self.last_sign = sign_detected

        cap.release()
        cv2.destroyAllWindows()
        return self.last_sign

    def run_loop(self):
        """
        Corre la detección en un bucle continuo, mostrando resultados y permitiendo grabar.
        """
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("No se pudo abrir la cámara")

        with mediapipe.solutions.holistic.Holistic(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as holistic:
            self.running = True
            print("Presiona 'r' para grabar, 'q' para salir")

            while cap.isOpened() and self.running:
                ret, frame = cap.read()
                if not ret:
                    break

                image, results = mediapipe_detection(frame, holistic)
                sign_detected, is_recording = self.sign_recorder.process_results(results)

                if sign_detected and sign_detected != "Seña desconocida" and sign_detected != self.last_sign:
                    print(f"\nSeña detectada: {sign_detected}")
                    self.last_sign = sign_detected

                self.webcam_manager.update(frame, results, sign_detected, is_recording)

                pressedKey = cv2.waitKey(1) & 0xFF
                if pressedKey == ord("r"):
                    self.sign_recorder.record()
                elif pressedKey == ord("q"):
                    self.running = False

        cap.release()
        cv2.destroyAllWindows()
        print("Finalizado")

    def get_last_sign(self):
        return self.last_sign

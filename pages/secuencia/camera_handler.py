import cv2
import mediapipe
import threading
import time
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.mediapipe_utils import mediapipe_detection

class CameraHandler:
    def __init__(self, parent):
        self.parent = parent
        
        # Variables de la cámara
        self.cap = None
        self.camera_thread = None
        self.camera_running = False
        self.current_frame = None
        
        # Estado de grabación para el indicador visual
        self.is_recording_visual = False
    
    def iniciar_camara(self):
        """Inicializar la cámara"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("No se pudo abrir la cámara")
            
            self.camera_running = True
            self.camera_thread = threading.Thread(target=self.proceso_camara, daemon=True)
            self.camera_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo inicializar la cámara: {e}")
    
    def proceso_camara(self):
        """Proceso principal de la cámara con reconocimiento"""
        with mediapipe.solutions.holistic.Holistic(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as holistic:
            
            while self.camera_running and self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                try:
                    # Procesar frame con MediaPipe
                    image, results = mediapipe_detection(frame, holistic)
                    
                    # Procesar resultados del reconocimiento
                    if (self.parent.game_logic.sign_recorder and 
                        self.parent.game_logic.game_active):
                        
                        sign_detected, is_recording = self.parent.game_logic.sign_recorder.process_results(results)
                        
                        # Actualizar estado de grabación visual
                        self.is_recording_visual = is_recording
                        
                        # Procesar detección de seña
                        if sign_detected:
                            self.parent.game_logic.procesar_deteccion_sena(sign_detected)
                    
                    # Dibujar landmarks
                    self.dibujar_landmarks(image, results)
                    
                    # Dibujar indicador de grabación
                    self.dibujar_indicador_grabacion(image)
                    
                    # Convertir y mostrar frame
                    self.mostrar_frame(image)
                    
                except Exception as e:
                    print(f"Error en proceso de cámara: {e}")
                
                time.sleep(0.03)  # ~30 FPS
    
    def dibujar_landmarks(self, image, results):
        """Dibujar landmarks de MediaPipe"""
        mp_drawing = mediapipe.solutions.drawing_utils
        mp_holistic = mediapipe.solutions.holistic
        
        # Dibujar manos
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
    def dibujar_indicador_grabacion(self, image):
        """Dibujar círculo indicador de grabación en la esquina"""
        # Obtener dimensiones de la imagen
        height, width = image.shape[:2]
        
        # Posición del círculo (esquina superior derecha)
        center_x = width - 30
        center_y = 30
        radius = 15
        
        # Color del círculo basado en el estado de grabación
        if self.is_recording_visual:
            # Rojo cuando está grabando
            color = (0, 0, 255)  # BGR format
            thickness = -1  # Círculo relleno
        else:
            # Azul cuando no está grabando
            color = (255, 0, 0)  # BGR format
            thickness = -1  # Círculo relleno
        
        # Dibujar el círculo
        cv2.circle(image, (center_x, center_y), radius, color, thickness)
        
        # Opcional: Agregar un borde blanco para mejor visibilidad
        cv2.circle(image, (center_x, center_y), radius + 2, (255, 255, 255), 2)
    
    def set_recording_state(self, is_recording):
        """Establecer el estado de grabación para el indicador visual"""
        self.is_recording_visual = is_recording
    
    def mostrar_frame(self, frame):
        """Mostrar frame en la interfaz"""
        try:
            # Redimensionar frame
            frame = cv2.resize(frame, (600, 500))
            frame = cv2.flip(frame, 1)  # Efecto espejo
            
            # Convertir a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convertir a ImageTk
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image)
            
            # Actualizar label (debe ejecutarse en el hilo principal)
            if self.parent.ui.video_label.winfo_exists():
                self.parent.ui.video_label.configure(image=photo, text="")
                self.parent.ui.video_label.image = photo  # Mantener referencia
                
        except Exception as e:
            print(f"Error al mostrar frame: {e}")
    
    def detener_camara(self):
        """Detener la cámara"""
        self.camera_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Solo hacer join si no estamos en el mismo hilo
        if self.camera_thread and self.camera_thread != threading.current_thread():
            self.camera_thread.join(timeout=1.0)
        
        self.camera_thread = None
"""
Manejador de cámara para detección de señas
"""

import cv2
import threading
import time
import numpy as np
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk
import mediapipe as mp
from utils.mediapipe_utils import mediapipe_detection

class CameraHandler:
    """Maneja la captura de video y detección de señas en tiempo real"""

    def __init__(self, app):
        self.app = app

        # Configuración de MediaPipe
        self.mp_holistic = mp.solutions.holistic
        self.holistic = None
        self.mp_drawing = mp.solutions.drawing_utils

        # Estado de la cámara
        self.cap = None
        self.thread = None
        self.running = False
        self.frame_actual = None

        # Control de detección
        self.ultima_letra_detectada = None
        self.tiempo_ultima_deteccion = 0
        self.intervalo_deteccion = 1.5  # Segundos entre detecciones válidas

        # Configuración de visualización
        self.WIDTH = 400
        self.HEIGHT = 300

    def iniciar_camara(self):
        """Inicia la captura de cámara"""
        try:
            self.app.ui.mostrar_camara_iniciando()

            # Inicializar MediaPipe
            self.holistic = self.mp_holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )

            # Probar diferentes backends para la cámara
            backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, None]

            for backend in backends:
                try:
                    if backend is None:
                        self.cap = cv2.VideoCapture(0)
                        print("Intentando con backend por defecto...")
                    else:
                        self.cap = cv2.VideoCapture(0, backend)
                        print(f"Intentando con backend: {backend}")

                    if self.cap.isOpened():
                        # Configurar propiedades
                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        self.cap.set(cv2.CAP_PROP_FPS, 30)

                        # Probar leer un frame
                        ret, test_frame = self.cap.read()
                        if ret and test_frame is not None:
                            print("✅ Cámara iniciada exitosamente")
                            break
                        else:
                            self.cap.release()
                            self.cap = None

                except Exception as e:
                    print(f"Error con backend {backend}: {e}")
                    if self.cap:
                        self.cap.release()
                        self.cap = None
                    continue

            if not self.cap or not self.cap.isOpened():
                raise RuntimeError("No se pudo abrir la cámara")

            # Iniciar hilo de captura
            self.running = True
            self.thread = threading.Thread(target=self._bucle_captura, daemon=True)
            self.thread.start()

        except Exception as e:
            print(f"❌ Error al iniciar cámara: {e}")
            self.app.ui.mostrar_error_camara(f"Error: {str(e)}")
            messagebox.showerror("Error Cámara", str(e))

    def _bucle_captura(self):
        """Bucle principal de captura y procesamiento"""
        frame_count = 0
        errores_consecutivos = 0
        max_errores = 10

        print("🎥 Iniciando bucle de captura...")

        while self.running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()

                if not ret or frame is None:
                    errores_consecutivos += 1
                    print(f"⚠️ Error leyendo frame {frame_count}, error #{errores_consecutivos}")

                    if errores_consecutivos >= max_errores:
                        print("❌ Demasiados errores, deteniendo captura")
                        break

                    time.sleep(0.1)
                    continue

                # Reset contador de errores
                errores_consecutivos = 0
                frame_count += 1

                # Procesar frame
                self.frame_actual = frame
                frame_procesado = self._procesar_frame(frame)
                self._mostrar_en_ui(frame_procesado)

                # Control de FPS
                time.sleep(0.033)  # ~30 FPS

            except Exception as e:
                print(f"❌ Error en bucle de captura: {e}")
                errores_consecutivos += 1
                if errores_consecutivos >= max_errores:
                    break
                time.sleep(0.1)

        print("🛑 Bucle de captura terminado")
        if self.cap:
            self.cap.release()

    def _procesar_frame(self, frame):
        """Procesa un frame para detección de señas"""
        try:
            # Detección con MediaPipe
            image, results = mediapipe_detection(frame, self.holistic)

            # Procesar con detector de señas
            sign_detected = None
            is_recording = False

            if self.app.sign_detector and self.app.logic.juego_activo:
                sign_detected, is_recording = self.app.sign_detector.procesar_resultados_mediapipe(results)

                # Procesar letra detectada válida
                if (sign_detected and isinstance(sign_detected, str) and
                    len(sign_detected) == 1 and self._es_deteccion_valida(sign_detected)):

                    letra = sign_detected.upper()
                    print(f"🔤 Letra detectada: {letra}")

                    # Actualizar UI y procesar en lógica
                    self.app.ui.actualizar_resultado(letra)
                    self.app.logic.procesar_letra_detectada(letra)

                    # Actualizar control de detección
                    self.ultima_letra_detectada = letra
                    self.tiempo_ultima_deteccion = time.time()

            # Preparar frame para visualización
            frame_visual = self._preparar_frame_visual(image, results, sign_detected, is_recording)

            return frame_visual

        except Exception as e:
            print(f"❌ Error procesando frame: {e}")
            return frame

    def _es_deteccion_valida(self, letra):
        """Verifica si una detección es válida (no duplicada)"""
        tiempo_actual = time.time()

        # Evitar detecciones duplicadas
        if (letra == self.ultima_letra_detectada and
            tiempo_actual - self.tiempo_ultima_deteccion < self.intervalo_deteccion):
            return False

        return True

    def _preparar_frame_visual(self, image, results, sign_detected, is_recording):
        """Prepara el frame para visualización con landmarks y texto"""
        frame = image.copy()

        # 1. Dibujar landmarks de las manos
        self._dibujar_landmarks(frame, results)

        # 2. Dibujar texto de seña detectada
        if sign_detected:
            self._dibujar_texto_seña(frame, sign_detected.upper())

        # 3. Indicador de grabación
        color_indicador = (25, 35, 240) if is_recording else (245, 242, 226)
        cv2.circle(frame, (30, 30), 20, color_indicador, -1)

        # 4. Estado del juego
        if self.app.logic.juego_activo:
            cv2.putText(frame, "JUEGO ACTIVO", (10, frame.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return frame

    def _dibujar_landmarks(self, image, results):
        """Dibuja los landmarks de las manos"""
        # Mano izquierda
        self.mp_drawing.draw_landmarks(
            image,
            landmark_list=results.left_hand_landmarks,
            connections=self.mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(232, 254, 255), thickness=1, circle_radius=1
            ),
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(255, 249, 161), thickness=2, circle_radius=2
            ),
        )

        # Mano derecha
        self.mp_drawing.draw_landmarks(
            image,
            landmark_list=results.right_hand_landmarks,
            connections=self.mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(232, 254, 255), thickness=1, circle_radius=2
            ),
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(255, 249, 161), thickness=2, circle_radius=2
            ),
        )

    def _dibujar_texto_seña(self, frame, texto):
        """Dibuja el texto de la seña detectada"""
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 1
        thickness = 2

        # Calcular posición centrada
        (text_w, text_h), _ = cv2.getTextSize(texto, font, font_scale, thickness)
        x = (frame.shape[1] - text_w) // 2
        y = frame.shape[0] - text_h - 20

        # Fondo semitransparente
        cv2.rectangle(frame, (0, y - 10), (frame.shape[1], frame.shape[0]), (255, 255, 255), -1)

        # Texto
        cv2.putText(frame, texto, (x, y + text_h), font, font_scale, (118, 62, 37), thickness)

    def _mostrar_en_ui(self, frame):
        """Muestra el frame en la interfaz de usuario"""
        try:
            # Redimensionar manteniendo proporción
            height, width = frame.shape[:2]
            aspect_ratio = width / height

            if aspect_ratio > self.WIDTH / self.HEIGHT:
                new_width = self.WIDTH
                new_height = int(self.WIDTH / aspect_ratio)
            else:
                new_height = self.HEIGHT
                new_width = int(self.HEIGHT * aspect_ratio)

            # Redimensionar y aplicar espejo
            frame_resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            frame_flipped = cv2.flip(frame_resized, 1)

            # Convertir a formato compatible con CustomTkinter
            rgb_frame = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            # Crear CTkImage
            ctk_image = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(new_width, new_height)
            )

            # Actualizar UI en el hilo principal
            if hasattr(self.app.ui, 'video_label') and self.app.ui.video_label.winfo_exists():
                self.app.ui.video_label.configure(image=ctk_image, text="")
                self.app.ui.video_label.image = ctk_image  # Mantener referencia

        except Exception as e:
            print(f"❌ Error mostrando frame en UI: {e}")
            # Fallback: mostrar mensaje de error
            if hasattr(self.app.ui, 'video_label') and self.app.ui.video_label.winfo_exists():
                self.app.ui.video_label.configure(image=None, text="Error de video")

    def capturar_frame_actual(self):
        """Retorna el frame actual para procesamiento externo"""
        return self.frame_actual.copy() if self.frame_actual is not None else None

    def esta_ejecutando(self):
        """Verifica si la cámara está ejecutándose"""
        return self.running and self.cap is not None and self.cap.isOpened()

    def pausar_deteccion(self):
        """Pausa temporalmente la detección (mantiene video)"""
        # Implementar si se necesita pausar solo la detección
        pass

    def reanudar_deteccion(self):
        """Reanuda la detección"""
        # Implementar si se necesita reanudar detección
        pass

    def detener_camara(self):
        """Detiene la cámara y libera recursos"""
        print("🛑 Deteniendo cámara...")

        # Detener el hilo de captura
        self.running = False

        # Esperar a que termine el hilo
        if self.thread and self.thread.is_alive():
            try:
                self.thread.join(timeout=2.0)
                if self.thread.is_alive():
                    print("⚠️ El hilo de cámara no terminó en el tiempo esperado")
                else:
                    print("✅ Hilo de cámara terminado correctamente")
            except Exception as e:
                print(f"❌ Error al terminar hilo: {e}")

        # Liberar cámara
        if self.cap:
            try:
                self.cap.release()
                print("✅ Cámara liberada")
            except Exception as e:
                print(f"❌ Error al liberar cámara: {e}")

        # Cerrar MediaPipe
        if self.holistic:
            try:
                self.holistic.close()
                print("✅ MediaPipe cerrado")
            except Exception as e:
                print(f"❌ Error al cerrar MediaPipe: {e}")

        # Limpiar referencias
        self.cap = None
        self.holistic = None
        self.frame_actual = None

        print("🏁 Cámara detenida completamente")

    def reiniciar_camara(self):
        """Reinicia la cámara completamente"""
        print("🔄 Reiniciando cámara...")
        self.detener_camara()
        time.sleep(1)  # Esperar un poco antes de reiniciar
        self.iniciar_camara()

    def obtener_estadisticas(self):
        """Retorna estadísticas de la cámara"""
        return {
            'ejecutando': self.esta_ejecutando(),
            'camara_disponible': self.cap is not None,
            'thread_activo': self.thread is not None and self.thread.is_alive(),
            'mediapipe_activo': self.holistic is not None,
            'ultima_deteccion': self.ultima_letra_detectada,
            'tiempo_ultima_deteccion': self.tiempo_ultima_deteccion
        }

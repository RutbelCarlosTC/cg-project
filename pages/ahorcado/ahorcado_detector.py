import time
import threading

try:
    from utils.dataset_utils import load_dataset, load_reference_signs
    from sign_recorder import SignRecorder
except ImportError:
    # Fallback si no están disponibles
    print("⚠️ Módulos de detección no encontrados. Funcionando en modo simulación.")

    class SignRecorder:
        def __init__(self, reference_signs=None):
            self.recording = False

        def process_results(self, results):
            return None, self.recording

        def record(self):
            self.recording = True
            threading.Timer(3.0, self._stop_recording).start()

        def _stop_recording(self):
            self.recording = False

    def load_dataset():
        return {}

    def load_reference_signs(videos):
        return {}

class SignDetector:
    """Maneja la detección y grabación de señas LSP"""

    def __init__(self):
        self.sign_recorder = None
        self.esta_grabando = False
        self.letra_detectada = None
        self.callback_deteccion = None
        self.timer_grabacion = None

        # Cargar el modelo de detección
        self.inicializar_detector()

    def inicializar_detector(self):
        """Inicializa el detector de señas con el modelo entrenado"""
        try:
            print("[INFO] Cargando modelo de detección de señas...")
            videos = load_dataset()
            reference_signs = load_reference_signs(videos)
            self.sign_recorder = SignRecorder(reference_signs)
            print("[INFO] Modelo de detección cargado exitosamente")
        except Exception as e:
            print(f"[ERROR] Error al cargar modelo de detección: {e}")
            self.sign_recorder = None

    def esta_disponible(self):
        """Verifica si el detector está disponible"""
        return self.sign_recorder is not None

    def procesar_resultados_mediapipe(self, results):
        """Procesa los resultados de MediaPipe y detecta señas"""
        if not self.sign_recorder:
            return None, False

        try:
            # Usar el SignRecorder para procesar los resultados
            sign_detected, is_recording = self.sign_recorder.process_results(results)

            # Actualizar estado de grabación
            if is_recording != self.esta_grabando:
                self.esta_grabando = is_recording

            return sign_detected, is_recording

        except Exception as e:
            print(f"[ERROR] Error al procesar resultados: {e}")
            return None, False

    def iniciar_grabacion(self):
        """Inicia la grabación manual de una seña"""
        if not self.sign_recorder:
            print("[ERROR] SignRecorder no disponible")
            return

        try:
            self.esta_grabando = True
            self.letra_detectada = None

            # Iniciar grabación en el SignRecorder
            self.sign_recorder.record()

            # Programar el fin de la grabación después de 3 segundos
            if self.timer_grabacion:
                self.timer_grabacion.cancel()

            self.timer_grabacion = threading.Timer(3.0, self._finalizar_grabacion)
            self.timer_grabacion.start()

            print("[INFO] Grabación iniciada - 3 segundos")

        except Exception as e:
            print(f"[ERROR] Error al iniciar grabación: {e}")
            self.esta_grabando = False

    def _finalizar_grabacion(self):
        """Finaliza la grabación automáticamente"""
        try:
            self.esta_grabando = False
            print("[INFO] Grabación finalizada automáticamente")

        except Exception as e:
            print(f"[ERROR] Error al finalizar grabación: {e}")

    def detener_grabacion(self):
        """Detiene la grabación manualmente y retorna la letra detectada"""
        try:
            if self.timer_grabacion:
                self.timer_grabacion.cancel()
                self.timer_grabacion = None

            self.esta_grabando = False
            letra = self.letra_detectada
            self.letra_detectada = None

            print(f"[INFO] Grabación detenida. Letra detectada: {letra}")
            return letra

        except Exception as e:
            print(f"[ERROR] Error al detener grabación: {e}")
            return None

    def get_sign_recorder(self):
        """Retorna la instancia del SignRecorder para uso directo"""
        return self.sign_recorder

    def reset(self):
        """Resetea el estado del detector"""
        try:
            if self.timer_grabacion:
                self.timer_grabacion.cancel()
                self.timer_grabacion = None

            self.esta_grabando = False
            self.letra_detectada = None

            print("[INFO] Detector de señas reseteado")

        except Exception as e:
            print(f"[ERROR] Error al resetear detector: {e}")

    def get_estado(self):
        """Retorna el estado actual del detector"""
        return {
            'disponible': self.esta_disponible(),
            'grabando': self.esta_grabando,
            'letra_detectada': self.letra_detectada,
            'sign_recorder_activo': self.sign_recorder is not None
        }

class SignDetectorCallback:
    """Clase auxiliar para manejar callbacks de detección"""

    def __init__(self, callback_function):
        self.callback = callback_function
        self.ultima_letra = None
        self.tiempo_ultima_deteccion = 0
        self.intervalo_minimo = 1.0  # Segundos entre detecciones

    def procesar_deteccion(self, letra):
        """Procesa una nueva detección evitando duplicados"""
        if not letra:
            return

        tiempo_actual = time.time()

        # Evitar detecciones duplicadas muy seguidas
        if (letra == self.ultima_letra and
            tiempo_actual - self.tiempo_ultima_deteccion < self.intervalo_minimo):
            return

        # Procesar la nueva detección
        self.ultima_letra = letra
        self.tiempo_ultima_deteccion = tiempo_actual

        if self.callback:
            self.callback(letra)

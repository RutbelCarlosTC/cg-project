import random
from typing import Set, List

class AhorcadoLogic:
    """Maneja toda la lógica del juego de ahorcado"""

    def __init__(self, app):
        self.app = app
        self.sign_detector = None
        self.camera_handler = None

        # Estado del juego
        self.palabra_actual = ""
        self.letras_correctas: Set[str] = set()
        self.letras_incorrectas: List[str] = []
        self.intentos_restantes = 6
        self.juego_activo = False
        self.esta_grabando = False

        # Lista de palabras para el juego
        self.palabras = [
            "PROGRAMACION", "COMPUTADORA", "PYTHON", "ALGORITMO",
            "DESARROLLO", "SOFTWARE", "HARDWARE", "INTERNET",
            "TECNOLOGIA", "INTELIGENCIA", "ARTIFICIAL", "LENGUAJE"
        ]

    def set_sign_detector(self, sign_detector):
        """Establece el detector de señas"""
        self.sign_detector = sign_detector

    def set_camera_handler(self, camera_handler):
        """Establece el manejador de cámara"""
        self.camera_handler = camera_handler

    def iniciar_nuevo_juego(self, palabra=None):
        """Inicia un nuevo juego con una palabra aleatoria o específica"""
        if palabra is None:
            self.palabra_actual = random.choice(self.palabras)
        else:
            self.palabra_actual = palabra.upper()

        # Resetear estado
        self.letras_correctas = set()
        self.letras_incorrectas = []
        self.intentos_restantes = 6
        self.juego_activo = True
        self.esta_grabando = False

        # Actualizar UI
        self.app.ui.iniciar_juego(self.palabra_actual)
        self.app.ui.actualizar_mensaje("¡Nuevo juego iniciado! Presiona 'R' o el botón para hacer una seña.")

        print(f"[DEBUG] Nueva palabra: {self.palabra_actual}")

    def toggle_recording(self):
        """Alterna el estado de grabación de señas"""
        if not self.juego_activo:
            return

        if not self.esta_grabando:
            self.iniciar_grabacion()
        else:
            self.detener_grabacion()

    def iniciar_grabacion(self):
        """Inicia la grabación de una seña"""
        if not self.sign_detector:
            self.app.ui.actualizar_mensaje("Error: Detector de señas no disponible")
            return

        self.esta_grabando = True
        self.sign_detector.iniciar_grabacion()

        # Actualizar UI
        self.app.ui.actualizar_estado_grabacion(True)
        self.app.ui.actualizar_mensaje("🔴 Grabando seña... Mantén la posición durante 3 segundos")

        print("[DEBUG] Iniciando grabación de seña")

    def detener_grabacion(self):
        """Detiene la grabación de una seña"""
        if not self.esta_grabando:
            return

        self.esta_grabando = False
        if self.sign_detector:
            letra_detectada = self.sign_detector.detener_grabacion()
            self.procesar_letra_detectada(letra_detectada)

        # Actualizar UI
        self.app.ui.actualizar_estado_grabacion(False)

    def procesar_letra_detectada(self, letra):
        """Procesa una letra detectada por el sistema de señas"""
        if not letra or not self.juego_activo:
            self.app.ui.actualizar_mensaje("No se detectó ninguna letra válida")
            return

        letra = letra.upper()

        # Verificar si la letra ya fue usada
        if letra in self.letras_correctas or letra in self.letras_incorrectas:
            self.app.ui.actualizar_mensaje(f"La letra '{letra}' ya fue usada")
            return

        # Actualizar resultado en UI
        self.app.ui.actualizar_resultado(letra)

        # Procesar la letra
        self.procesar_letra(letra)

    def procesar_letra(self, letra):
        """Procesa una letra (desde detección o teclado virtual)"""
        if not self.juego_activo:
            return

        letra = letra.upper()

        # Verificar si la letra ya fue usada
        if letra in self.letras_correctas or letra in self.letras_incorrectas:
            self.app.ui.actualizar_mensaje(f"La letra '{letra}' ya fue usada")
            return

        # Verificar si la letra está en la palabra
        if letra in self.palabra_actual:
            # Letra correcta
            self.letras_correctas.add(letra)
            self.app.ui.marcar_letra_usada(letra, True)
            self.app.ui.mostrar_palabra(self.palabra_actual, self.letras_correctas)
            self.app.ui.actualizar_mensaje(f"¡Correcto! La letra '{letra}' está en la palabra")

            # Verificar si ganó
            if self.verificar_victoria():
                self.terminar_juego(True)
        else:
            # Letra incorrecta
            self.letras_incorrectas.append(letra)
            self.intentos_restantes -= 1
            self.app.ui.marcar_letra_usada(letra, False)
            self.app.ui.dibujar_ahorcado_parte(len(self.letras_incorrectas))

            if self.intentos_restantes > 0:
                self.app.ui.actualizar_mensaje(
                    f"La letra '{letra}' no está en la palabra. "
                    f"Te quedan {self.intentos_restantes} intentos"
                )

            # Verificar si perdió
            if self.intentos_restantes <= 0:
                self.terminar_juego(False)

        print(f"[DEBUG] Letra procesada: {letra}, Correctas: {self.letras_correctas}, "
              f"Incorrectas: {self.letras_incorrectas}")

    def verificar_victoria(self):
        """Verifica si el jugador ha ganado"""
        for letra in self.palabra_actual:
            if letra not in self.letras_correctas:
                return False
        return True

    def terminar_juego(self, victoria):
        """Termina el juego actual"""
        self.juego_activo = False
        self.esta_grabando = False

        if victoria:
            mensaje = f"🎉 ¡Felicidades! Has adivinado la palabra: {self.palabra_actual}"
        else:
            mensaje = f"😞 Game Over. La palabra era: {self.palabra_actual}"

        self.app.ui.actualizar_mensaje(mensaje)

        # Mostrar todas las letras de la palabra
        all_letters = set(self.palabra_actual)
        self.app.ui.mostrar_palabra(self.palabra_actual, all_letters)

        print(f"[DEBUG] Juego terminado. Victoria: {victoria}")

    def obtener_estado_juego(self):
        """Retorna el estado actual del juego"""
        return {
            'palabra': self.palabra_actual,
            'letras_correctas': self.letras_correctas,
            'letras_incorrectas': self.letras_incorrectas,
            'intentos_restantes': self.intentos_restantes,
            'juego_activo': self.juego_activo,
            'esta_grabando': self.esta_grabando
        }

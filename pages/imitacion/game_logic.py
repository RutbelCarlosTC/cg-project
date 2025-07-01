import random
from tkinter import messagebox
from utils.dataset_utils import load_dataset, load_reference_signs
from sign_recorder import SignRecorder

class GameLogic:
    def __init__(self, parent):
        self.parent = parent
        
        # Juego actual
        self.sign_to_immitate = None
        self.sign_category = None
        self.tiempo_restante = 0
        self.game_active = False
        self.esperando_resultado = False

        # Palabras por categoría
        self.palabras_disponibles = {
            "despedidas": ["Adios", "Hasta luego", "Hasta manana"],
            "cortesia": ["Gracias"],
            "lugares": ["Casa"],
            "personas": ["Vecino", "Companero"],
            "colores": ["Celeste", "Verde"],
            "posesivos": ["Mi"],
            "acciones": ["Jugar", "Aplaudir", "Botar"],
            "objetos": ["Basura"],
            "preposiciones": ["De"]
        }

        # Reconocimiento
        self.sign_recorder = None
        self.reference_signs = None
    
    def init_sign_recognition(self):
        """Inicializar el sistema de reconocimiento de señas"""
        try:
            videos = load_dataset()
            self.reference_signs = load_reference_signs(videos)
            self.sign_recorder = SignRecorder(self.reference_signs)
            print("Sistema de reconocimiento inicializado correctamente")
        except Exception as e:
            print(f"Error al inicializar reconocimiento: {e}")
            messagebox.showerror("Error", "No se pudo inicializar el sistema de reconocimiento de señas")
    
    def iniciar_juego(self):
        """Inicia nuevo juego"""
        if self.game_active:
            self.reiniciar_juego()
            return

        self.game_active = True
        self.generar_nueva_sena()
        self.parent.camera_handler.iniciar_camara()
        self.iniciar_temporizador()
        self.parent.ui.actualizar_botones_juego_activo()
    
    def reiniciar_juego(self):
        """Reiniciar el juego"""
        self.game_active = False
        self.tiempo_restante = 0
        self.sign_to_immitate = None
        self.parent.camera_handler.detener_camara()
        self.parent.ui.actualizar_botones_juego_inactivo()
        self.parent.ui.resetear_video()
        self.parent.ui.actualizar_instruccion("💡 Presiona 'Iniciar Juego' para comenzar")
        self.parent.ui.actualizar_temporizador("Tiempo restante: 0:00", 0)
        
    def generar_nueva_sena(self):
        categoria = random.choice(list(self.palabras_disponibles.keys()))
        palabra = random.choice(self.palabras_disponibles[categoria])
        self.sign_to_immitate = palabra
        self.sign_category = categoria

        self.parent.ui.mostrar_sena(palabra, categoria)
        self.parent.ui.actualizar_instruccion(f"💡 Haz la seña: \"{palabra}\" ({categoria.title()})")
    
    def iniciar_temporizador(self):
        self.tiempo_restante = 30
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        if self.game_active and self.tiempo_restante > 0:
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            texto = f"Tiempo restante: {minutos}:{segundos:02d}"
            progreso = self.tiempo_restante / 30
            self.parent.ui.actualizar_temporizador(texto, progreso)
            self.tiempo_restante -= 1
            self.parent.after(1000, self.actualizar_temporizador)
        elif self.game_active:
            self.tiempo_agotado()

    def toggle_recording(self):
        if not self.sign_recorder or not self.game_active:
            return

        self.parent.ui.actualizar_estado_grabacion(True)
        self.parent.camera_handler.set_recording_state(True)
        self.sign_recorder.record()
        self.parent.after(1000, self._restaurar_estado_grabacion)

    def _restaurar_estado_grabacion(self):
        self.parent.ui.actualizar_estado_grabacion(False)
        self.parent.camera_handler.set_recording_state(False)

    def procesar_deteccion_sena(self, sign_detected):
        if not self.game_active or self.esperando_resultado:
            return

        self.esperando_resultado = True

        if sign_detected.upper() == self.sign_to_immitate.upper():
            self.game_active = False  # 🔑 DETIENE el temporizador
            self.parent.ui.mostrar_mensaje_resultado("✅ Seña correcta", correcto=True)
            self.parent.after(2000, self._nivel_completado)
        else:
            self.parent.ui.mostrar_mensaje_resultado("❌ Seña incorrecta", correcto=False)
            self.parent.after(2000, self._permitir_reintento)

    def _nivel_completado(self):
        self.esperando_resultado = False
        messagebox.showinfo("¡Correcto!", f"¡Muy bien! Has imitado la seña: \"{self.sign_to_immitate}\"")
        self.reiniciar_juego()
        self.parent.ui.ocultar_mensaje_resultado()

    def _permitir_reintento(self):
        self.esperando_resultado = False
        self.parent.ui.ocultar_mensaje_resultado()

    def tiempo_agotado(self):
        self.game_active = False
        messagebox.showwarning("Tiempo Agotado", f"No lograste imitar la seña \"{self.sign_to_immitate}\" a tiempo.")
        self.reiniciar_juego()
            
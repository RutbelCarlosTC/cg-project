import random
from tkinter import messagebox
from utils.dataset_utils import load_dataset, load_reference_signs
from sign_recorder import SignRecorder

class GameLogic:
    def __init__(self, parent):
        self.parent = parent
        
        # Variables del juego
        self.secuencia_actual = []
        self.nivel_actual = 1
        self.paso_actual = 0
        self.tiempo_restante = 0
        self.precision = 0
        self.game_active = False
        self.esperando_resultado = False  # <- Agrega esto

        
        # Palabras disponibles ampliadas
        self.palabras_disponibles = {
            "vocales": ["A", "E", "I", "O", "U"],
            "consonantes": ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", 
                           "N", "Ñ", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
        }
        
         # Plantillas de oraciones ampliadas
        self.plantillas_oraciones = [
            # Niveles 1-2 (2-3 letras)
            ["S", "I"], ["N", "O"], ["V", "I"], ["C", "A"],
            ["V", "E", "R"], ["S", "O", "L"], ["D", "O", "S"],
            
            # Niveles 3-5 (3-5 letras)
            ["C", "A", "S", "A"], ["V", "A", "S", "O"],
            ["C", "A", "M", "A"], ["M", "A", "M", "A"],
            ["P", "A", "D", "R", "E"], ["M", "A", "D", "R", "E"],
            
            # Niveles 6+ (palabras reales)
            ["H", "O", "L", "A"], ["A", "M", "O", "R"], ["L", "U", "Z"],
            ["M", "I", "O"], ["D", "O", "S"], ["M", "I", "L"],
            ["M", "A", "R"], ["A", "M", "E"], ["R", "I", "O"]
        ]
        
        # Sistema de reconocimiento
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
    
    def generar_secuencia(self):
        """Generar nueva secuencia basada en el nivel"""
        if self.nivel_actual <= 2:
            # Niveles 1-2: Oraciones cortas (2-3 palabras)
            oraciones_cortas = [seq for seq in self.plantillas_oraciones if len(seq) <= 3]
            nueva_secuencia = random.choice(oraciones_cortas)
        elif self.nivel_actual <= 4:
            # Niveles 3-4: Oraciones medianas (3-4 palabras)
            oraciones_medianas = [seq for seq in self.plantillas_oraciones if len(seq) <= 4]
            nueva_secuencia = random.choice(oraciones_medianas)
        else:
            # Nivel 5+: Cualquier oración
            nueva_secuencia = random.choice(self.plantillas_oraciones)
        
        # Asegurar que no repetimos la secuencia anterior
        intentos = 0
        while intentos < 10 and nueva_secuencia == self.secuencia_actual:
            if self.nivel_actual <= 2:
                oraciones_cortas = [seq for seq in self.plantillas_oraciones if len(seq) <= 3]
                nueva_secuencia = random.choice(oraciones_cortas)
            elif self.nivel_actual <= 4:
                oraciones_medianas = [seq for seq in self.plantillas_oraciones if len(seq) <= 4]
                nueva_secuencia = random.choice(oraciones_medianas)
            else:
                nueva_secuencia = random.choice(self.plantillas_oraciones)
            intentos += 1
        
        self.secuencia_actual = nueva_secuencia
        self.parent.ui.mostrar_secuencia(self.secuencia_actual)
    
    def iniciar_juego(self):
        """Iniciar nueva partida"""
        if not self.game_active:
            self.game_active = True
            self.paso_actual = 0
            self.generar_secuencia()
            self.parent.camera_handler.iniciar_camara()
            self.actualizar_instruccion()
            
            # Actualizar botones
            self.parent.ui.actualizar_botones_juego_activo()
        else:
            self.reiniciar_juego()
    
    def reiniciar_juego(self):
        """Reiniciar el juego"""
        self.game_active = False
        self.paso_actual = 0
        self.tiempo_restante = 0
        self.precision = 0
        
        # Detener cámara
        self.parent.camera_handler.detener_camara()
        
        # Reset UI
        self.parent.ui.actualizar_botones_juego_inactivo()
        self.parent.ui.actualizar_instruccion("💡 Presiona 'Iniciar Juego' para comenzar")
        self.parent.ui.resetear_video()
    
    def actualizar_instruccion(self):
        """Actualizar la instrucción actual"""
        if self.game_active and self.paso_actual < len(self.secuencia_actual):
            palabra_actual = self.secuencia_actual[self.paso_actual]
            tipo_seña = self.obtener_tipo_seña(palabra_actual)
            
            # Mostrar la oración completa como contexto
            oracion_completa = " ".join(self.secuencia_actual)
            texto = f"💡 Haz la seña: \"{palabra_actual}\" ({tipo_seña})\n🔗 Oración: \"{oracion_completa}\" - ({self.paso_actual + 1} de {len(self.secuencia_actual)})"
            self.parent.ui.actualizar_instruccion(texto)
        elif self.paso_actual >= len(self.secuencia_actual):
            oracion_completa = " ".join(self.secuencia_actual)
            self.parent.ui.actualizar_instruccion(f"🎉 ¡Oración completada: \"{oracion_completa}\"!")
            # Programar la finalización del nivel en el hilo principal
            self.parent.after(100, self.completar_nivel)
    
    def obtener_tipo_seña(self, palabra):
        """Obtener el tipo de seña para mostrar contexto al usuario"""
        for categoria, palabras in self.palabras_disponibles.items():
            if palabra in palabras:
                categorias_nombres = {
                    "vocales": "Vocal",
                    "consonantes": "Consonante"
                }
                return categorias_nombres.get(categoria, "Seña")
        return "Seña"
    
    def toggle_recording(self):
        """Alternar grabación de seña"""
        if not self.sign_recorder or not self.game_active:
            return

        # Actualizar UI y indicador visual en la cámara
        self.parent.ui.actualizar_estado_grabacion(True)
        self.parent.camera_handler.set_recording_state(True)
        self.sign_recorder.record()

        # Restaurar estado después de 1 segundo
        self.parent.after(1500, lambda: self._restaurar_estado_grabacion())
    
    def _restaurar_estado_grabacion(self):
        """Restaurar estado de grabación en UI y cámara"""
        self.parent.ui.actualizar_estado_grabacion(False)
        self.parent.camera_handler.set_recording_state(False)
    
    
    def avanzar_paso(self):
        """Avanzar al siguiente paso de la secuencia"""
        self.paso_actual += 1
        self.precision = 0
        
        if self.paso_actual < len(self.secuencia_actual):
           self.actualizar_instruccion()
        else:
            self.actualizar_instruccion()  # Esto ahora programa completar_nivel
    
    def completar_nivel(self):
        """Completar nivel actual"""
        if not self.game_active:  # Evitar múltiples llamadas
            return
            
        self.game_active = False
        nivel_completado = self.nivel_actual
        oracion_completada = " ".join(self.secuencia_actual)
        self.nivel_actual += 1
        
        # Programar el diálogo y la preparación del siguiente nivel
        self.parent.after(100, lambda: self._mostrar_dialogo_nivel_completado(nivel_completado, oracion_completada))
    
    def _mostrar_dialogo_nivel_completado(self, nivel_completado, oracion_completada):
        """Mostrar diálogo de nivel completado y preparar siguiente nivel"""
        messagebox.showinfo(
            "¡Nivel Completado!",
            f"¡Felicidades! Has completado el nivel {nivel_completado}\n"
            f"Oración: \"{oracion_completada}\"\n"
            f"Próximo nivel: {self.nivel_actual}"
        )
        
        # Preparar siguiente nivel sin reiniciar completamente
        self.preparar_siguiente_nivel()
    
    def preparar_siguiente_nivel(self):
        """Preparar el siguiente nivel sin reiniciar la cámara"""
        self.paso_actual = 0
        self.precision = 0
        self.game_active = True
        
        # Generar nueva secuencia
        self.generar_secuencia()
        
        # Actualizar UI
        self.actualizar_instruccion()
        
        # Los botones ya están en estado activo, no necesitan cambio
    
    
    def procesar_deteccion_sena(self, sign_detected):
        """Procesar la detección de una seña después de grabación"""
        if not self.game_active or self.esperando_resultado:
            return  # No hacer nada si no estamos listos

        if self.paso_actual < len(self.secuencia_actual):
            palabra_esperada = self.secuencia_actual[self.paso_actual]
            
            if sign_detected.upper() == palabra_esperada.upper():
                self.esperando_resultado = True
                self.parent.ui.mostrar_mensaje_resultado("✅ Seña correcta", correcto=True)
                self.parent.after(2000, lambda: self._continuar_despues_resultado(True))
            else:
                self.esperando_resultado = True
                self.parent.ui.mostrar_mensaje_resultado("❌ Seña incorrecta", correcto=False)
                self.parent.after(2000, lambda: self._continuar_despues_resultado(False))
    
    def _continuar_despues_resultado(self, acierto):
        """Acciones después de mostrar el resultado del gesto"""
        self.esperando_resultado = False
        self.parent.ui.ocultar_mensaje_resultado()
        if acierto:
            self.avanzar_paso()
            

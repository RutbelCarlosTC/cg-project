import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas

class AhorcadoUI(ctk.CTkFrame):
    """Interfaz de usuario principal del juego de ahorcado"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="#B39DDB")
        self.parent = parent

        # Configuración del grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Variables de estado
        self.labels_palabra = []
        self.botones_letras = {}

        # Crear la interfaz
        self.crear_titulo()
        self.crear_seccion_camara()
        self.crear_seccion_ahorcado()
        self.crear_seccion_teclado()

    def crear_titulo(self):
        """Crea el título principal"""
        self.titulo = ctk.CTkLabel(
            self,
            text="🎯 Ahorcado - Lenguaje de Señas",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        self.titulo.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="ew", padx=20)

    def crear_seccion_camara(self):
        """Crea la sección de cámara y detección"""
        self.frame_camara = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.frame_camara.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Título de cámara
        self.titulo_camara = ctk.CTkLabel(
            self.frame_camara,
            text="📷 Tu Cámara",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="gray"
        )
        self.titulo_camara.pack(pady=(10, 5))

        # Video display
        self.video_label = ctk.CTkLabel(
            self.frame_camara,
            text="Iniciando cámara...",
            font=ctk.CTkFont(size=14),
            fg_color="#1a1a1a",
            text_color="white",
            corner_radius=10,
            width=400,
            height=300
        )
        self.video_label.pack(pady=10, padx=10, fill="both", expand=True)

        # Estado de detección
        self.frame_estado = ctk.CTkFrame(self.frame_camara, fg_color="transparent")
        self.frame_estado.pack(pady=5)

        self.estado_detection = ctk.CTkLabel(
            self.frame_estado,
            text="🟢 Detectando letra",
            font=ctk.CTkFont(size=12),
            text_color="#4CAF50"
        )
        self.estado_detection.pack(side="left", padx=5)

        self.estado_analysis = ctk.CTkLabel(
            self.frame_estado,
            text="🟡 Analizando",
            font=ctk.CTkFont(size=12),
            text_color="#FF9800"
        )
        self.estado_analysis.pack(side="left", padx=5)

        # Resultado de detección
        self.result_label = ctk.CTkLabel(
            self.frame_camara,
            text="Resultado: -",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1976D2"
        )
        self.result_label.pack(pady=(5, 10))

        # Mensajes al usuario
        self.message_label = ctk.CTkLabel(
            self.frame_camara,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#333333",
            wraplength=380,
            justify="center"
        )
        self.message_label.pack(pady=(0, 10))

        # Botón para hacer seña
        self.btn_hacer_sena = ctk.CTkButton(
            self.frame_camara,
            text='🔴 Hacer seña (R)',
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FF5722",
            hover_color="#E64A19",
            height=40,
            command=self._on_hacer_sena_click
        )
        self.btn_hacer_sena.pack(pady=(5, 15), padx=10, fill="x")

        # Controles adicionales
        self.frame_controles = ctk.CTkFrame(self.frame_camara, fg_color="transparent")
        self.frame_controles.pack(pady=(0, 10), fill="x", padx=10)

        self.btn_nuevo_juego = ctk.CTkButton(
            self.frame_controles,
            text="🎮 Nuevo Juego",
            font=ctk.CTkFont(size=12),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=120,
            height=35,
            command=self._on_nuevo_juego_click
        )
        self.btn_nuevo_juego.pack(side="left", padx=(0, 5))

        self.btn_reiniciar_camara = ctk.CTkButton(
            self.frame_controles,
            text="📹 Reiniciar",
            font=ctk.CTkFont(size=12),
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=120,
            height=35,
            command=self._on_reiniciar_camara_click
        )
        self.btn_reiniciar_camara.pack(side="right", padx=(5, 0))

    def crear_seccion_ahorcado(self):
        """Crea la sección del dibujo del ahorcado"""
        self.frame_ahorcado = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.frame_ahorcado.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Título
        titulo_ahorcado = ctk.CTkLabel(
            self.frame_ahorcado,
            text="🎪 El Ahorcado",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="gray"
        )
        titulo_ahorcado.pack(pady=(10, 5))

        # Canvas para el dibujo
        self.canvas_ahorcado = tk.Canvas(
            self.frame_ahorcado,
            bg="white",
            width=280,
            height=350,
            highlightthickness=0
        )
        self.canvas_ahorcado.pack(pady=20, padx=20, fill="both", expand=True)

        # Información del juego
        self.info_label = ctk.CTkLabel(
            self.frame_ahorcado,
            text="Intentos restantes: 6",
            font=ctk.CTkFont(size=12),
            text_color="#333333"
        )
        self.info_label.pack(pady=(0, 10))

        # Dibujar horca inicial
        self.dibujar_horca()

    def crear_seccion_teclado(self):
        """Crea la sección del teclado virtual"""
        self.frame_teclado = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.frame_teclado.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Título
        titulo_teclado = ctk.CTkLabel(
            self.frame_teclado,
            text="⌨️ Palabra",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="gray"
        )
        titulo_teclado.pack(pady=(10, 10))

        # Configurar grid
        for i in range(8):
            self.frame_teclado.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.frame_teclado.grid_columnconfigure(i, weight=1)

        # Frame para la palabra
        self.frame_palabra = ctk.CTkFrame(self.frame_teclado, fg_color="transparent")
        self.frame_palabra.pack(pady=(0, 15), fill="x", padx=10)

        # Teclado alfabético
        self.crear_teclado_alfabetico()

    def crear_teclado_alfabetico(self):
        """Crea el teclado alfabético virtual"""
        letras = [
            ['A', 'B', 'C', 'D', 'E', 'F'],
            ['G', 'H', 'I', 'J', 'K', 'L'],
            ['M', 'N', 'O', 'P', 'Q', 'R'],
            ['S', 'T', 'U', 'V', 'W', 'X'],
            ['Y', 'Z', '', '', '', '']
        ]

        # Frame para el teclado
        self.frame_teclado_botones = ctk.CTkFrame(self.frame_teclado, fg_color="transparent")
        self.frame_teclado_botones.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for fila, row in enumerate(letras):
            for col, letra in enumerate(row):
                if letra:
                    btn = ctk.CTkButton(
                        self.frame_teclado_botones,
                        text=letra,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        width=45,
                        height=45,
                        fg_color="#E3F2FD",
                        text_color="#1976D2",
                        hover_color="#BBDEFB",
                        border_width=1,
                        border_color="#1976D2",
                        command=lambda l=letra: self._on_letra_click(l)
                    )
                    btn.grid(row=fila, column=col, padx=2, pady=2, sticky="nsew")
                    self.botones_letras[letra] = btn

        # Configurar grid del frame de botones
        for i in range(5):
            self.frame_teclado_botones.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.frame_teclado_botones.grid_columnconfigure(i, weight=1)

    # Métodos de manejo de eventos
    def _on_hacer_sena_click(self):
        """Maneja el click del botón hacer seña"""
        if hasattr(self.parent, 'logic'):
            self.parent.logic.toggle_recording()

    def _on_nuevo_juego_click(self):
        """Maneja el click del botón nuevo juego"""
        if hasattr(self.parent, 'logic'):
            self.parent.logic.iniciar_nuevo_juego()

    def _on_reiniciar_camara_click(self):
        """Maneja el click del botón reiniciar cámara"""
        if hasattr(self.parent, 'camera_handler'):
            self.parent.camera_handler.reiniciar_camara()

    def _on_letra_click(self, letra):
        """Maneja el click de una letra del teclado virtual"""
        if hasattr(self.parent, 'logic'):
            self.parent.logic.procesar_letra(letra)

    # Métodos de actualización de UI
    def mostrar_palabra(self, palabra, letras_correctas):
        """Muestra la palabra con las letras adivinadas"""
        # Limpiar labels anteriores
        for label in self.labels_palabra:
            label.destroy()
        self.labels_palabra.clear()

        # Crear frame para centrar las letras
        self.frame_palabra.pack_forget()
        self.frame_palabra = ctk.CTkFrame(self.frame_teclado, fg_color="transparent")
        self.frame_palabra.pack(pady=(0, 15), fill="x", padx=10)

        # Crear labels para cada letra
        for i, letra in enumerate(palabra):
            if letra in letras_correctas:
                texto = letra
                color_bg = "#4CAF50"
                color_texto = "white"
            else:
                texto = "_"
                color_bg = "#E3F2FD"
                color_texto = "#1976D2"

            label = ctk.CTkLabel(
                self.frame_palabra,
                text=texto,
                font=ctk.CTkFont(size=20, weight="bold"),
                fg_color=color_bg,
                text_color=color_texto,
                width=35,
                height=35,
                corner_radius=8
            )
            label.grid(row=0, column=i, padx=2, pady=5)
            self.labels_palabra.append(label)

    def marcar_letra_usada(self, letra, es_correcta):
        """Marca una letra como usada en el teclado"""
        if letra in self.botones_letras:
            if es_correcta:
                color = "#4CAF50"
                text_color = "white"
            else:
                color = "#F44336"
                text_color = "white"

            self.botones_letras[letra].configure(
                fg_color=color,
                text_color=text_color,
                state="disabled"
            )

    def actualizar_resultado(self, letra):
        """Actualiza el resultado de la detección"""
        self.result_label.configure(text=f"Resultado: {letra.upper()}")

    def actualizar_mensaje(self, mensaje):
        """Actualiza el mensaje informativo"""
        self.message_label.configure(text=mensaje)

    def actualizar_estado_grabacion(self, grabando):
        """Actualiza el estado visual de grabación"""
        if grabando:
            self.estado_detection.configure(
                text="🔴 Grabando seña",
                text_color="#F44336"
            )
            self.btn_hacer_sena.configure(
                text="🔴 Grabando...",
                state="disabled"
            )
        else:
            self.estado_detection.configure(
                text="🟢 Detectando letra",
                text_color="#4CAF50"
            )
            self.btn_hacer_sena.configure(
                text="🔴 Hacer seña (R)",
                state="normal"
            )

    def actualizar_info_juego(self, intentos_restantes):
        """Actualiza la información del juego"""
        self.info_label.configure(text=f"Intentos restantes: {intentos_restantes}")

    # Métodos de dibujo del ahorcado
    def dibujar_horca(self):
        """Dibuja la estructura básica de la horca"""
        self.canvas_ahorcado.delete("all")

        # Base
        self.canvas_ahorcado.create_line(50, 320, 150, 320, width=4, fill="black")
        # Poste vertical
        self.canvas_ahorcado.create_line(100, 320, 100, 50, width=4, fill="black")
        # Travesaño superior
        self.canvas_ahorcado.create_line(100, 50, 180, 50, width=4, fill="black")
        # Cuerda
        self.canvas_ahorcado.create_line(180, 50, 180, 80, width=3, fill="black")

    def dibujar_ahorcado_parte(self, numero_parte):
        """Dibuja una parte del ahorcado"""
        canvas = self.canvas_ahorcado

        if numero_parte == 1:  # Cabeza
            canvas.create_oval(165, 80, 195, 110, outline="red", width=3)
        elif numero_parte == 2:  # Cuerpo
            canvas.create_line(180, 110, 180, 200, width=3, fill="red")
        elif numero_parte == 3:  # Brazo izquierdo
            canvas.create_line(180, 140, 150, 170, width=3, fill="red")
        elif numero_parte == 4:  # Brazo derecho
            canvas.create_line(180, 140, 210, 170, width=3, fill="red")
        elif numero_parte == 5:  # Pierna izquierda
            canvas.create_line(180, 200, 150, 240, width=3, fill="red")
        elif numero_parte == 6:  # Pierna derecha
            canvas.create_line(180, 200, 210, 240, width=3, fill="red")

    # Métodos de estado de cámara
    def mostrar_camara_iniciando(self):
        """Muestra mensaje de cámara iniciando"""
        self.video_label.configure(
            image=None,
            text="🔄 Iniciando cámara...",
            text_color="white"
        )

    def mostrar_error_camara(self, mensaje):
        """Muestra mensaje de error de cámara"""
        self.video_label.configure(
            image=None,
            text=f"❌ {mensaje}",
            text_color="red"
        )

    # Método de inicialización de juego
    def iniciar_juego(self, palabra):
        """Inicializa la UI para un nuevo juego"""
        # Mostrar palabra inicial
        self.mostrar_palabra(palabra, set())

        # Resetear teclado
        for btn in self.botones_letras.values():
            btn.configure(
                fg_color="#E3F2FD",
                text_color="#1976D2",
                state="normal"
            )

        # Resetear canvas
        self.dibujar_horca()

        # Actualizar información
        self.actualizar_info_juego(6)
        self.actualizar_resultado("-")

        # Habilitar botón de hacer seña
        self.btn_hacer_sena.configure(state="normal")

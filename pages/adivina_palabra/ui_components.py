import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class SecuenciaUI:
    def __init__(self, parent):
        self.parent = parent
        
        # Referencias a widgets importantes
        self.sequence_container = None
        self.instruction_label = None
        self.timer_label = None
        self.time_progress = None
        self.start_btn = None
        self.record_btn = None
        self.video_label = None
        self.video_frame = None
        self.back_btn = None
        self.help_btn = None
        self.alphabet_btn = None
        self.recording_indicator = None
        self.help_window = None  # Ventana de ayuda
        self.alphabet_window = None  # Ventana del abecedario
    
    def setup_ui(self):
        """Configurar toda la interfaz de usuario"""
        self._setup_header()
        self._setup_main_container()
    
    def _setup_header(self):
        """Configurar el header con botón regresar, título y botones de ayuda"""
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 0))
        
        # Botón regresar (izquierda)
        self.back_btn = ctk.CTkButton(
            header,
            text="← Regresar",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            width=120,
            fg_color="#CCCCCC",
            hover_color="#AAAAAA",
            text_color="#003366"
        )
        self.back_btn.pack(side="left")
        
        # Frame para botones de la derecha
        right_buttons_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_buttons_frame.pack(side="right")
        
        # Botón del abecedario
        self.alphabet_btn = ctk.CTkButton(
            right_buttons_frame,
            text="ABC",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            width=50,
            height=40,
            fg_color="#FF9800",
            hover_color="#F57C00",
            text_color="white",
            corner_radius=20,
            command=self.mostrar_abecedario
        )
        self.alphabet_btn.pack(side="left", padx=(0, 10))
        
        # Botón de ayuda
        self.help_btn = ctk.CTkButton(
            right_buttons_frame,
            text="?",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold"),
            width=40,
            height=40,
            fg_color="#2196F3",
            hover_color="#1976D2",
            text_color="white",
            corner_radius=20,
            command=self.mostrar_ayuda
        )
        self.help_btn.pack(side="left")
        
        # Título (centro)
        title = ctk.CTkLabel(
            header,
            text="Completa la Palabra",
            font=ctk.CTkFont("Helvetica", size=28, weight="bold"),
            text_color="#6B4EBA"
        )
        title.pack(side="top")
    
    def mostrar_abecedario(self):
        """Muestra una ventana con la imagen del abecedario"""
        ventana_abc = tk.Toplevel(self.parent)
        ventana_abc.title("Abecedario")
        ventana_abc.geometry("520x450")
        ventana_abc.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        ventana_abc.transient(self.parent)
        ventana_abc.grab_set()
        
        # Cargar y redimensionar la imagen
        imagen = Image.open(f"assets/games/alfabeto2.png")
        imagen = imagen.resize((500, 350), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(imagen)
        
        # Crear un label para mostrar la imagen
        label_imagen = tk.Label(ventana_abc, image=img_tk)
        label_imagen.image = img_tk  # Mantener una referencia para evitar que se elimine
        label_imagen.pack(pady=10)
        
        # Botón para cerrar la ventana
        btn_cerrar = tk.Button(
            ventana_abc, 
            text="Cerrar", 
            command=ventana_abc.destroy,
            font=("Arial", 12),
            bg="#f0f0f0",
            relief="raised",
            padx=20,
            pady=5
        )
        btn_cerrar.pack(pady=10)
        
        # Hacer que la ventana sea modal (opcional)
        ventana_abc.focus_set()
        


    def mostrar_ayuda(self):
        """Mostrar ventana de ayuda"""
        if self.help_window is not None:
            self.help_window.lift()  # Traer al frente si ya existe
            return
            
        # Crear ventana de ayuda
        self.help_window = ctk.CTkToplevel(self.parent)
        self.help_window.title("Ayuda - Completa la Palabra")
        self.help_window.geometry("500x600")
        self.help_window.resizable(False, False)
        
        # Centrar la ventana
        self.help_window.transient(self.parent)
        self.help_window.grab_set()  # Modal
        
        # Configurar cierre de ventana
        self.help_window.protocol("WM_DELETE_WINDOW", self.cerrar_ayuda)
        
        # Contenido de la ayuda
        self._setup_help_content()
    
    def _setup_help_content(self):
        """Configurar el contenido de la ventana de ayuda"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.help_window, fg_color="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="🎮 ¿Cómo jugar Completa la Palabra?",
            font=ctk.CTkFont("Helvetica", size=20, weight="bold"),
            text_color="#6B4EBA"
        )
        title.pack(pady=(20, 15))
        
        # Contenido scrollable
        scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Secciones de ayuda
        self._add_help_section(
            scroll_frame,
            "🎯 Objetivo del Juego",
            "Completa las secuencias de palabras mostradas realizando las señas correspondientes con tus manos."
        )
        
        self._add_help_section(
            scroll_frame,
            "▶️ Cómo Empezar",
            "1. Presiona el botón '🎮 Iniciar Juego'\n" +
            "2. Se mostrará una secuencia de letras \n" +
            "3. Sigue las instrucciones que aparecen en pantalla"
        )
        
        self._add_help_section(
            scroll_frame,
            "🤲 Realizar Señas",
            "1. Posiciónate frente a la cámara\n" +
            "2. Presiona '🔴 Grabar Seña' cuando esté habilitado\n" +
            "3. Realiza la seña de la letra indicada\n" +
            "4. El sistema detectará y evaluará tu seña automáticamente"
        )
        
        self._add_help_section(
            scroll_frame,
            "💡 Consejos",
            "• Asegúrate de tener buena iluminación\n" +
            "• Mantén las manos visibles en la cámara\n" +
            "• Realiza las señas de forma clara y pausada\n" +
            "• Si no reconoce tu seña, inténtalo nuevamente"
        )
        
        self._add_help_section(
            scroll_frame,
            "🔄 Controles",
            "• 'Iniciar Juego': Comienza una nueva partida\n" +
            "• 'Reiniciar': Vuelve a empezar el juego actual\n" +
            "• 'Grabar Seña': Captura y evalúa tu seña\n" +
            "• '← Regresar': Vuelve al menú principal"
        )
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            main_frame,
            text="Entendido",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049",
            command=self.cerrar_ayuda,
            width=120,
            height=35
        )
        close_btn.pack(pady=(10, 20))
    
    def _add_help_section(self, parent, titulo, contenido):
        """Agregar una sección a la ayuda"""
        # Frame de la sección
        section_frame = ctk.CTkFrame(parent, fg_color="#F8F9FA", corner_radius=8)
        section_frame.pack(fill="x", pady=8)
        
        # Título de la sección
        title_label = ctk.CTkLabel(
            section_frame,
            text=titulo,
            font=ctk.CTkFont("Helvetica", size=16, weight="bold"),
            text_color="#2E7D32",
            anchor="w"
        )
        title_label.pack(fill="x", padx=15, pady=(15, 5))
        
        # Contenido de la sección
        content_label = ctk.CTkLabel(
            section_frame,
            text=contenido,
            font=ctk.CTkFont("Helvetica", size=13),
            text_color="#424242",
            anchor="w",
            justify="left"
        )
        content_label.pack(fill="x", padx=15, pady=(5, 15))
    
    def cerrar_ayuda(self):
        """Cerrar ventana de ayuda"""
        if self.help_window:
            self.help_window.destroy()
            self.help_window = None
    
    def _setup_main_container(self):
        """Configurar el contenedor principal"""
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._setup_left_panel(main_container)
        self._setup_right_panel(main_container)
    
    def _setup_left_panel(self, parent):
        """Configurar panel izquierdo con secuencia y controles"""
        left_panel = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self._setup_sequence_section(left_panel)
        self._setup_instruction_section(left_panel)
        self._setup_controls_section(left_panel)
    
    def _setup_sequence_section(self, parent):
        """Configurar sección de secuencia"""
        sequence_frame = ctk.CTkFrame(parent, fg_color="#E8F5E8", corner_radius=10)
        sequence_frame.pack(fill="x", padx=20, pady=20)
        
        sequence_title = ctk.CTkLabel(
            sequence_frame,
            text="Completa la palabra",
            font=ctk.CTkFont("Helvetica", size=16, weight="bold"),
            text_color="#2E7D32"
        )
        sequence_title.pack(pady=10)
        
        # Contenedor para las palabras de la secuencia
        self.sequence_container = ctk.CTkFrame(sequence_frame, fg_color="transparent")
        self.sequence_container.pack(pady=10)
    
    def _setup_instruction_section(self, parent):
        """Configurar sección de instrucciones"""
        self.instruction_frame = ctk.CTkFrame(parent, fg_color="#FFF3E0", corner_radius=10)
        self.instruction_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.instruction_label = ctk.CTkLabel(
            self.instruction_frame,
            text="💡 Presiona 'Iniciar Juego' para comenzar",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            text_color="#E65100"
        )
        self.instruction_label.pack(pady=15)
    
    def _setup_timer_section(self, parent):
        """Configurar sección del temporizador"""
        timer_frame = ctk.CTkFrame(parent, fg_color="#E3F2FD", corner_radius=10)
        timer_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        timer_icon = ctk.CTkLabel(
            timer_frame,
            text="⏱️",
            font=ctk.CTkFont(size=20)
        )
        timer_icon.pack(side="left", padx=(15, 5), pady=10)
        
        self.timer_label = ctk.CTkLabel(
            timer_frame,
            text="Tiempo restante: 0:00",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            text_color="#1565C0"
        )
        self.timer_label.pack(side="left", pady=10)
        
    
    def _setup_controls_section(self, parent):
        """Configurar sección de controles (solo botón iniciar)"""
        controls_frame = ctk.CTkFrame(parent, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.start_btn = ctk.CTkButton(
            controls_frame,
            text="🎮 Iniciar Juego",
            font=ctk.CTkFont("Helvetica", size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049",
            height=45
        )
        self.start_btn.pack(fill="x", pady=5)

        # Botón de grabación debajo de la cámara
        self.record_btn = ctk.CTkButton(
            controls_frame,
            text="🔴 Grabar Seña",
            font=ctk.CTkFont("Helvetica", size=16, weight="bold"),
            fg_color="#FF5722",
            hover_color="#E64A19",
            height=45,
            state="disabled"
        )
        self.record_btn.pack(fill="x", pady=5)
    
    def _setup_right_panel(self, parent):
        """Configurar panel derecho con cámara y botón de grabación"""
        right_panel = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Título de la cámara
        camera_title = ctk.CTkLabel(
            right_panel,
            text="📹 Tu Intento",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold"),
            text_color="#1976D2"
        )
        camera_title.pack(pady= 10)
        
        # Frame para el video
        self.video_frame = ctk.CTkFrame(right_panel, fg_color="#2C3E50", corner_radius=10)
        self.video_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Label para mostrar el video
        self.video_label = ctk.CTkLabel(
            self.video_frame,
            text="Imita la seña aquí",
            font=ctk.CTkFont("Helvetica", size=16),
            text_color="#ECF0F1"
        )
        self.video_label.pack(expand=True)
        
        self.detection_result_label = ctk.CTkLabel(
        right_panel,
        text="",
        font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
        text_color="#000000",
        fg_color="#FFFFFF",
        corner_radius=8)
        
        self.detection_result_label.pack(pady=(0, 10), padx=10)

    def mostrar_secuencia(self, secuencia_actual):
        """Mostrar la secuencia en la interfaz"""
        # Limpiar contenedor anterior
        for widget in self.sequence_container.winfo_children():
            widget.destroy()
        
        # Crear contenedor horizontal para las palabras
        words_frame = ctk.CTkFrame(self.sequence_container, fg_color="transparent")
        words_frame.pack()
        
        for i, palabra in enumerate(secuencia_actual):
            # Crear frame para cada palabra
            word_frame = ctk.CTkFrame(words_frame, fg_color="#FFFFFF", corner_radius=8)
            word_frame.pack(side="left", padx=5, pady=5)
        
            
            word_label = ctk.CTkLabel(
                word_frame,
                text=palabra,
                font=ctk.CTkFont("Helvetica", size=12, weight="bold"),
                text_color="#2E7D32"
            )
            word_label.pack(padx=10, pady=(0, 10))
            
            # Flecha entre palabras (excepto la última)
            if i < len(secuencia_actual) - 1:
                arrow_label = ctk.CTkLabel(
                    words_frame,
                    text="→",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#666666"
                )
                arrow_label.pack(side="left", padx=5)
    
    def actualizar_instruccion(self, texto):
        """Actualizar texto de instrucciones"""
        self.instruction_label.configure(text=texto)
    
    def actualizar_botones_juego_activo(self):
        """Actualizar botones cuando el juego está activo"""
        self.start_btn.configure(text="🔄 Reiniciar", fg_color="#FF9800", hover_color="#F57C00")
        self.record_btn.configure(state="normal")
    
    def actualizar_botones_juego_inactivo(self):
        """Actualizar botones cuando el juego está inactivo"""
        self.start_btn.configure(text="🎮 Iniciar Juego", fg_color="#4CAF50", hover_color="#45A049")
        self.record_btn.configure(state="disabled")
        
    
    def actualizar_estado_grabacion(self, grabando):
        """Actualizar estado del botón de grabación"""
        if grabando:
            self.record_btn.configure(state="disabled", text="🎙️ Grabando...", fg_color="#FFC107")
            
        else:
            self.record_btn.configure(state="normal", text="🔴 Grabar Seña", fg_color="#FF5722")
            
    
    def resetear_video(self):
        """Resetear el video a su estado inicial"""
        self.video_label.configure(image=None, text="Imita la seña aquí")
    
    def mostrar_mensaje_resultado(self, texto, correcto=True):
        """Mostrar el mensaje de resultado bajo la cámara"""
        color = "#4CAF50" if correcto else "#F44336"
        self.detection_result_label.configure(text=texto, text_color=color)
        self.detection_result_label.update()

    def ocultar_mensaje_resultado(self):
        """Ocultar el mensaje de resultado"""
        self.detection_result_label.configure(text="")

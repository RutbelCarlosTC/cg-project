import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import os

class ImitacionUI:
    def __init__(self, parent):
        self.parent = parent
        self.video_label = None
        self.gif_label = None
        self.instruction_label = None
        self.timer_label = None
        self.time_progress = None
        self.start_btn = None
        self.record_btn = None
        self.detection_result_label = None
        self.frames = []  # Para GIF animado
        self.help_window = None  # Ventana de ayuda
        self.current_frame = 0
        self.animation_id = None

    def setup_ui(self):
        self._setup_header()
        self._setup_main()

    def _setup_header(self):
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 0))

        self.back_btn = ctk.CTkButton(  # <- REINSTANCIAR para evitar error
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

        title = ctk.CTkLabel(
            header,
            text="Imita la Seña",
            font=ctk.CTkFont("Helvetica", size=28, weight="bold"),
            text_color="#6B4EBA"
        )
        title.pack(side="top")


    def _setup_main(self):
        container = ctk.CTkFrame(self.parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        left = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=15)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._setup_instruction(left)
        self._setup_timer(left)
        self._setup_controls(left)

        right = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=15)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        camera_title = ctk.CTkLabel(
            right,
            text="📹 Tu intento",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold"),
            text_color="#1976D2"
        )
        camera_title.pack(pady=10)

        self.video_label = ctk.CTkLabel(
            right,
            text="Aquí se mostrará la seña",
            font=ctk.CTkFont("Helvetica", size=14),
            text_color="#2C3E50",
            width=300,
            height=300
        )
        self.video_label.pack(pady=10)

        self.detection_result_label = ctk.CTkLabel(
            right,
            text="",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            text_color="#000000",
            fg_color="#FFFFFF",
            corner_radius=8)
        self.detection_result_label.pack(pady=(0, 10), padx=10)

    def _setup_instruction(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="#FFF3E0", corner_radius=10)
        self.gif_label = ctk.CTkLabel(
            frame,
            text="Aquí se mostrará la seña",
            font=ctk.CTkFont("Helvetica", size=14),
            text_color="#2C3E50",
            width=300,
            height=300
        )
        self.gif_label.pack(pady=(10, 5))
        frame.pack(fill="x", padx=20, pady=(20, 10))

        self.instruction_label = ctk.CTkLabel(
            frame,
            text="💡 Presiona 'Iniciar Juego' para comenzar",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            text_color="#E65100"
        )
        self.instruction_label.pack(pady=15)

    def _setup_timer(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="#E3F2FD", corner_radius=10)
        frame.pack(fill="x", padx=20, pady=(0, 20))

        icon = ctk.CTkLabel(frame, text="⏱️", font=ctk.CTkFont(size=20))
        icon.pack(side="left", padx=(15, 5), pady=10)

        self.timer_label = ctk.CTkLabel(
            frame,
            text="Tiempo restante: 0:00",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold"),
            text_color="#1565C0"
        )
        self.timer_label.pack(side="left", pady=10)

        self.time_progress = ctk.CTkProgressBar(frame, width=200)
        self.time_progress.pack(side="right", padx=15, pady=10)
        self.time_progress.set(0)

    def _setup_controls(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 20))

        self.start_btn = ctk.CTkButton(
            frame,
            text="🎮 Iniciar Juego",
            font=ctk.CTkFont("Helvetica", size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049",
            height=45
        )
        self.start_btn.pack(fill="x", pady=5)

        self.record_btn = ctk.CTkButton(
            frame,
            text="🔴 Grabar Seña",
            font=ctk.CTkFont("Helvetica", size=16, weight="bold"),
            fg_color="#FF5722",
            hover_color="#E64A19",
            height=45,
            state="disabled"
        )
        self.record_btn.pack(fill="x", pady=5)
    
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
            text="🎮 ¿Cómo jugar Imita la Seña?",
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
            "Completa las señas de palabras mostradas en gifs realizando las señas correspondientes con tus manos."
        )
        
        self._add_help_section(
            scroll_frame,
            "▶️ Cómo Empezar",
            "1. Presiona el botón '🎮 Iniciar Juego'\n" +
            "2. Se mostrará una gif de una palabra\n" +
            "3. Sigue el movimiento de la seña que aparece en pantalla"
        )
        
        self._add_help_section(
            scroll_frame,
            "🤲 Realiza la Seña",
            "1. Posiciónate frente a la cámara\n" +
            "2. Presiona '🔴 Grabar Seña' cuando esté habilitado\n" +
            "3. Realiza la seña de la palabra indicada\n" +
            "4. El sistema detectará y evaluará tu seña automáticamente"
        )
        
        self._add_help_section(
            scroll_frame,
            "📊 Palabras Disponibles",
            "• Adiós 👋\n" +
            "• Compañero 👋\n" +
            "• De nada 😊\n" +
            "• Casa 🏠\n" +
            "• Celeste 🟦\n" +
            "• etc."
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

    def mostrar_sena(self, nombre, categoria):
        """Cargar y mostrar GIF o imagen de la seña"""
        self._detener_animacion()
        ruta = f"assets/senas/{nombre.lower().replace(' ', '_')}.gif"
        try:
            img = Image.open(ruta)
            img.thumbnail((300, 300))  # <- Limita el tamaño visible

            if getattr(img, "is_animated", False):
                self.frames = [ImageTk.PhotoImage(frame.copy().resize((300, 300))) for frame in ImageSequence.Iterator(img)]
                self.current_frame = 0
                self._animar_gif()
            else:
                self.frames = []
                photo = ImageTk.PhotoImage(img)
                self.gif_label.configure(image=photo, text="No hay foto")
                self.gif_label.image = photo
        except Exception as e:
            self.gif_label.configure(text=f"❌ No se pudo cargar la seña {nombre}")
            print(f"Error al cargar imagen: {e}")

    def _animar_gif(self):
        if not self.frames:
            return
        frame = self.frames[self.current_frame]
        self.gif_label.configure(image=frame, text="")
        self.gif_label.image = frame
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.animation_id = self.gif_label.after(100, self._animar_gif)

    def _detener_animacion(self):
        if self.animation_id:
            self.video_label.after_cancel(self.animation_id)
            self.animation_id = None

    def actualizar_instruccion(self, texto):
        self.instruction_label.configure(text=texto)

    def actualizar_temporizador(self, texto, progreso):
        self.timer_label.configure(text=texto)
        self.time_progress.set(progreso)

    def actualizar_botones_juego_activo(self):
        self.start_btn.configure(text="🔄 Reiniciar", fg_color="#FF9800", hover_color="#F57C00")
        self.record_btn.configure(state="normal")

    def actualizar_botones_juego_inactivo(self):
        self.start_btn.configure(text="🎮 Iniciar Juego", fg_color="#4CAF50", hover_color="#45A049")
        self.record_btn.configure(state="disabled")

    def actualizar_estado_grabacion(self, grabando):
        if grabando:
            self.record_btn.configure(state="disabled", text="🎙️ Grabando...", fg_color="#FFC107")
        else:
            self.record_btn.configure(state="normal", text="🔴 Grabar Seña", fg_color="#FF5722")

    def resetear_video(self):
        self._detener_animacion()
        self.video_label.configure(image=None, text="Aquí se mostrará la seña")

    def mostrar_mensaje_resultado(self, texto, correcto=True):
        color = "#4CAF50" if correcto else "#F44336"
        self.detection_result_label.configure(text=texto, text_color=color)
        self.detection_result_label.update()

    def ocultar_mensaje_resultado(self):
        self.detection_result_label.configure(text="")
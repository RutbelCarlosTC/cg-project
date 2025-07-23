import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from .ahorcado_logic import AhorcadoLogic
from .ui_component import AhorcadoUI
from .camera_handler import CameraHandler
from .ahorcado_detector import SignDetector

class AhorcadoSeñasGame(ctk.CTkFrame):
    """Juego de Ahorcado integrado con el sistema de navegación principal"""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller  # Referencia a MainApp
        self.help_window = None  # Ventana de ayuda

        # Estado de inicialización
        self.juego_inicializado = False

        # Inicializar componentes del juego
        self.setup_components()

        # Protocolo de limpieza
        self.bind('<Destroy>', self.on_destroy)

    def setup_components(self):
        """Inicializa todos los componentes del juego"""
        # Configuración del grid
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Contenido principal
        self.grid_columnconfigure(0, weight=1)

        # Crear header con botón de regreso
        self.crear_header()

        # Crear frame principal para el juego
        self.game_frame = ctk.CTkFrame(self, fg_color="#ECF0F1")
        self.game_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # 1. Detector de señas
        self.sign_detector = SignDetector()

        # 2. Lógica del juego
        self.logic = AhorcadoLogic(self)

        # 3. Interfaz de usuario (dentro del game_frame)
        self.ui = AhorcadoUI(self.game_frame)
        self.ui.pack(fill="both", expand=True)

        # 4. Manejador de cámara
        self.camera_handler = CameraHandler(self)

        # Conectar componentes
        self.logic.set_sign_detector(self.sign_detector)
        self.logic.set_camera_handler(self.camera_handler)

        # Configurar eventos de teclado
        self.setup_bindings()

    def crear_header(self):
        """Crea el header con título y botón de regreso"""
        header_frame = ctk.CTkFrame(self, fg_color="#EAF6FF", height=60)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)

        # Configurar grid del header
        header_frame.grid_columnconfigure(1, weight=1)

        # Botón de regreso
        btn_back = ctk.CTkButton(
            header_frame,
            text="← Regresar",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#CCCCCC",
            hover_color="#AAAAAA",
            text_color="#003366",
            width=100,
            height=40,
            command=self.volver_al_menu
        )
        btn_back.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Título del juego
        titulo = ctk.CTkLabel(
            header_frame,
            text="Ahorcado - Lenguaje de Señas",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#6B4EBA"
        )
        titulo.grid(row=0, column=1, pady=10, sticky="")

        # Frame para botones de la derecha
        right_buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
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

    def setup_bindings(self):
        """Configura los eventos de teclado"""
        # Hacer que el frame pueda recibir focus
        self.focus_set()
        self.bind('<KeyPress-r>', self.on_record_key)
        self.bind('<KeyPress-R>', self.on_record_key)

        # También vincular al controller principal
        self.controller.bind('<KeyPress-r>', self.on_record_key)
        self.controller.bind('<KeyPress-R>', self.on_record_key)

    def on_record_key(self, event):
        """Maneja la tecla 'r' para iniciar grabación"""
        if self.logic.juego_activo and self.winfo_viewable():
            self.logic.toggle_recording()

    def volver_al_menu(self):
        """Regresa al menú de selección de juegos"""
        try:
            # Detener la cámara antes de cambiar de página
            self.detener_juego()

            # Cambiar a la página de selección de juegos
            self.controller.show_frame("GameSelectionPage")

        except Exception as e:
            print(f"Error al volver al menú: {e}")
            # Como fallback, ir al menú principal
            self.controller.show_frame("Menu")

    def mostrar_abecedario(self):
        """Muestra una ventana con la imagen del abecedario"""
        ventana_abc = tk.Toplevel(self)
        ventana_abc.title("Abecedario")
        ventana_abc.geometry("520x450")
        ventana_abc.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        ventana_abc.transient(self)
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
        self.help_window = ctk.CTkToplevel(self)
        self.help_window.title("Ayuda - Completa la Palabra")
        self.help_window.geometry("500x600")
        self.help_window.resizable(False, False)
        
        # Centrar la ventana
        self.help_window.transient(self)
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
            text="🎮 ¿Cómo jugar Ahorcado",
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
            "Adivina la palabra secreta haciendo señas de letras del alfabeto LSP."
        )
        
        self._add_help_section(
            scroll_frame,
            "🎮 CONTROLES",
            "• Presiona 'R' o el botón rojo para hacer una seña'\n" +
            "• También puedes usar el teclado virtual\n" +
            "• Mantén la seña por 3 segundos para que se detecte"
        )
        
        self._add_help_section(
            scroll_frame,
            "🤲 REGLAS",
            "• Tienes 6 intentos fallidos máximo\n" +
            "• Cada letra incorrecta dibuja una parte del ahorcado\n" +
            "• Gana adivinando toda la palabra\n" +
            "• Pierde si se completa el dibujo del ahorcado"
        )
        
        self._add_help_section(
            scroll_frame,
            "📊 Palabras Disponibles",
            "• PROGRAMACION \n" +
            "• COMPUTADORA \n" +
            "• PYTHON \n" +
            "• INTERNET \n" +
            "• LENGUAJE \n" +
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

    """
    def mostrar_ayuda(self):
        Muestra ventana de ayuda
        help_window = ctk.CTkToplevel(self)
        help_window.title("Ayuda - Ahorcado con Señas")
        help_window.geometry("500x400")
        help_window.transient(self.controller)
        help_window.grab_set()

        # Contenido de ayuda
        help_text = 
🎯 CÓMO JUGAR AHORCADO CON SEÑAS

📋 OBJETIVO:
Adivina la palabra secreta haciendo señas de letras del alfabeto LSP.

🎮 CONTROLES:
• Presiona 'R' o el botón rojo para hacer una seña
• También puedes usar el teclado virtual
• Mantén la seña por 3 segundos para que se detecte

🏆 REGLAS:
• Tienes 6 intentos fallidos máximo
• Cada letra incorrecta dibuja una parte del ahorcado
• Gana adivinando toda la palabra
• Pierde si se completa el dibujo del ahorcado

💡 CONSEJOS:
• Asegúrate de tener buena iluminación
• Mantén la mano visible para la cámara
• Haz las señas de forma clara y estable
• Puedes usar ambas manos si es necesario

🔤 SEÑAS:
Consulta la "Lista de Señas" desde el menú principal
para ver todas las letras del alfabeto LSP.
        

        help_label = ctk.CTkLabel(
            help_window,
            text=help_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            wraplength=450
        )
        help_label.pack(pady=20, padx=20, fill="both", expand=True)

        # Botón cerrar
        btn_close = ctk.CTkButton(
            help_window,
            text="Cerrar",
            command=help_window.destroy
        )
        btn_close.pack(pady=10)
    """

    def iniciar_juego(self):
        """Inicia el juego (llamado cuando se muestra la página)"""
        if not self.juego_inicializado:
            try:
                print("🎮 Iniciando Ahorcado con Señas...")

                # Mostrar mensaje de carga
                if hasattr(self, 'ui'):
                    self.ui.mostrar_camara_iniciando()
                    self.ui.actualizar_mensaje("🔄 Iniciando juego...")

                # Inicializar juego en un hilo separado para no bloquear UI
                self.after(500, self._inicializar_delayed)

            except Exception as e:
                print(f"❌ Error al iniciar juego: {e}")
                if hasattr(self, 'ui'):
                    self.ui.mostrar_error_camara(f"Error: {str(e)}")

    def _inicializar_delayed(self):
        """Inicialización retardada para mejor UX"""
        try:
            # Iniciar lógica del juego
            self.logic.iniciar_nuevo_juego()

            # Iniciar cámara
            self.camera_handler.iniciar_camara()

            self.juego_inicializado = True
            print("✅ Juego inicializado correctamente")

        except Exception as e:
            print(f"❌ Error en inicialización: {e}")
            if hasattr(self, 'ui'):
                self.ui.mostrar_error_camara("Error al inicializar")

    def detener_juego(self):
        """Detiene el juego y libera recursos"""
        try:
            print("🛑 Deteniendo Ahorcado con Señas...")

            # Detener cámara
            if hasattr(self, 'camera_handler'):
                self.camera_handler.detener_camara()

            # Resetear estado
            if hasattr(self, 'logic'):
                self.logic.juego_activo = False

            self.juego_inicializado = False
            print("✅ Juego detenido correctamente")

        except Exception as e:
            print(f"❌ Error al detener juego: {e}")

    def reiniciar_juego(self):
        """Reinicia completamente el juego"""
        self.detener_juego()
        self.after(1000, self.iniciar_juego)  # Reiniciar después de 1 segundo

    def on_destroy(self, event=None):
        """Cleanup cuando se destruye el widget"""
        if event and event.widget == self:
            self.detener_juego()

    def tkraise(self, aboveThis=None):
        """Override para iniciar juego cuando se muestra la página"""
        super().tkraise(aboveThis)

        # Iniciar juego solo si no está ya inicializado
        if not self.juego_inicializado:
            self.after(100, self.iniciar_juego)  # Pequeño delay para que se renderice la UI

    def destroy(self):
        """Override para limpiar recursos al usar con MainApp"""
        self.detener_juego()
        super().destroy()

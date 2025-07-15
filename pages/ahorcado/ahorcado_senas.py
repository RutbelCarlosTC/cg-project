
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

        # Botón de ayuda (opcional)
        btn_help = ctk.CTkButton(
            header_frame,
            text="❓",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#CCCCCC",
            hover_color="#AAAAAA",
            text_color="#003366",
            width=40,
            height=40,
            command=self.mostrar_ayuda
        )
        btn_help.grid(row=0, column=2, padx=20, pady=10, sticky="e")

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

    def mostrar_ayuda(self):
        """Muestra ventana de ayuda"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("Ayuda - Ahorcado con Señas")
        help_window.geometry("500x400")
        help_window.transient(self.controller)
        help_window.grab_set()

        # Contenido de ayuda
        help_text = """
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
        """

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

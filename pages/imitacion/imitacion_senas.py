import customtkinter as ctk
from pages.imitacion.ui_components import ImitacionUI
from pages.imitacion.game_logic import GameLogic
from pages.imitacion.camera_handler import CameraHandler

class ImitacionSeñasGame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#E6F3FF")
        
        # Inicializar componentes
        self.ui = ImitacionUI(self)
        self.game_logic = GameLogic(self)
        self.camera_handler = CameraHandler(self)
        
        # Configurar UI
        self.ui.setup_ui()
        
        # Conectar callbacks
        self._connect_callbacks()
        
        # Inicializar reconocimiento de señas
        self.game_logic.init_sign_recognition()
    
    def _connect_callbacks(self):
        """Conectar callbacks entre componentes"""
        # Callbacks de UI a GameLogic
        self.ui.start_btn.configure(command=self.game_logic.iniciar_juego)
        self.ui.record_btn.configure(command=self.game_logic.toggle_recording)
        
        # Callback de regreso al menú
        self.ui.back_btn.configure(command=self.regresar_menu)
    
    def regresar_menu(self):
        """Regresar al menú principal"""
        self.camera_handler.detener_camara()
        self.controller.show_frame("GameSelectionPage")
    
    def destroy(self):
        """Cleanup al destruir el widget"""
        self.camera_handler.detener_camara()
        super().destroy()
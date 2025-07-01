import customtkinter as ctk
from pages.games_selector import GameSelectionPage
from pages.abecedario import SenhaWindow
from pages.lista_senas import ListaSenasWindow
from pages.secuencia.secuencia_senas import SecuenciaSeñasGame
from pages.imitacion.imitacion_senas import ImitacionSeñasGame

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EnSEÑA PLAY")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Modo visual (opcional)
        ctk.set_appearance_mode("light")  # o "dark"
        ctk.set_default_color_theme("blue")  # azul, dark-blue, green, etc.
        
        # === Contenedor principal ===
        container = ctk.CTkFrame(self, corner_radius=0)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # === Páginas ===
        # Menú principal
        self.menu_page = self.create_menu(container)
        self.frames["Menu"] = self.menu_page
        
        # Página de selección de juegos
        game_page = GameSelectionPage(parent=container, controller=self)
        self.frames["GameSelectionPage"] = game_page
        game_page.grid(row=0, column=0, sticky="nsew")
        
        # Página de lista de señas
        lista_page = ListaSenasWindow(parent=container, controller=self)
        self.frames["ListaSenasWindow"] = lista_page
        lista_page.grid(row=0, column=0, sticky="nsew")
        
        #Juegos Imitacion de Señas
        imitacion_game = ImitacionSeñasGame(parent=container, controller=self)
        self.frames["ImitacionSeñasGame"] = imitacion_game
        imitacion_game.grid(row=0, column=0, sticky="nsew")

        # Juego Secuencia de Señas
        secuencia_game = SecuenciaSeñasGame(parent=container, controller=self)
        self.frames["SecuenciaSeñasGame"] = secuencia_game
        secuencia_game.grid(row=0, column=0, sticky="nsew")
        
        # Mostrar menú principal al inicio
        self.show_frame("Menu")
    
    def create_menu(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="#AEEEEE")  # Fondo celeste
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Título principal
        title_label = ctk.CTkLabel(
            frame,
            text="EnSEÑA PLAY",
            font=ctk.CTkFont("Helvetica", 48, weight="bold"),
            text_color="#003366"
        )
        title_label.pack(pady=40)
        
        # Contenedor de botones
        buttons_frame = ctk.CTkFrame(frame, fg_color="#AEEEEE")
        buttons_frame.pack(pady=30)
        
        # Opciones del menú
        options = ["Jugar", "Como Jugar", "Lista de Señas", "Opciones", "Salir"]
        
        for option in options:
            btn = ctk.CTkButton(
                buttons_frame,
                text=option,
                font=ctk.CTkFont("Helvetica", size=35, weight="bold"),
                width=350,
                fg_color="#008B8B",
                hover_color="#20B2AA",
                text_color="white",
                command=lambda opt=option: self.handle_option(opt)
            )
            btn.pack(pady=10, fill="x", expand=True)
        
        return frame
    
    def handle_option(self, option):
        if option == "Salir":
            self.destroy()
        elif option == "Jugar":
            self.show_frame("GameSelectionPage")
        elif option == "Lista de Señas":
            self.show_frame("ListaSenasWindow")
        else:
            print(f"Seleccionaste: {option}")
    
    def show_frame(self, page_name):
        """Cambiar a la página especificada"""
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
        else:
            print(f"Error: Página '{page_name}' no encontrada")
    
    def destroy(self):
        """Cleanup al cerrar la aplicación"""
        # Limpiar recursos de las páginas que lo requieran
        if "SecuenciaSeñasGame" in self.frames:
            try:
                self.frames["SecuenciaSeñasGame"].destroy()
            except:
                pass
            
        elif "ImitacionSeñasGame" in self.frames:
            try:
                self.frames["ImitacionSeñasGame"].destroy()
            except:
                pass

        super().destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
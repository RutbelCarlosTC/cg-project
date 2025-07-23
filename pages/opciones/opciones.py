import customtkinter as ctk
import pygame

class OpcionesWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Opciones")
        self.configure(fg_color="#D1F2EB")
        self.resizable(False, False)

        # Dimensiones y centrado en pantalla
        ancho = 360
        alto = 200
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Hacer ventana modal y encima de la principal
        self.transient(master)     # La vincula a la ventana principal
        self.grab_set()            # Hace que la ventana bloquee la principal
        self.focus_force()         # Fuerza el foco en esta ventana

        # Encabezado
        ctk.CTkLabel(self, text="🎵 Configuración de Música", font=("Arial", 18, "bold"), text_color="#154360").pack(pady=(20, 10))

        # Slider para volumen
        self.slider_volumen = ctk.CTkSlider(
            self, from_=0, to=1, number_of_steps=100,
            command=self.cambiar_volumen, width=220
        )
        self.slider_volumen.set(pygame.mixer.music.get_volume())
        self.slider_volumen.pack(pady=10)

        # Etiqueta de porcentaje
        self.label_porcentaje = ctk.CTkLabel(self, text=f"{int(self.slider_volumen.get()*100)}%", font=("Arial", 12))
        self.label_porcentaje.pack()

        # Botón cerrar
        ctk.CTkButton(self, text="Cerrar", command=self.destroy, fg_color="#117A65", hover_color="#0E6655").pack(pady=(20, 10))

    def cambiar_volumen(self, valor):
        volumen = float(valor)
        pygame.mixer.music.set_volume(volumen)
        self.label_porcentaje.configure(text=f"{int(volumen*100)}%")

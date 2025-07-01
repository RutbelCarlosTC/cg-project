import customtkinter as ctk
from PIL import Image, ImageTk
import os

class GameSelectionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # === Encabezado: Regresar + Título ===
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 0))

        back_btn = ctk.CTkButton(
            header,
            text="Regresar",
            font=ctk.CTkFont("Helvetica",size=14, weight="bold"),
            width=100,
            fg_color="#CCCCCC",
            hover_color="#AAAAAA",
            text_color="#003366",
            command=lambda: self.controller.show_frame("Menu")
        )
        back_btn.pack(side="left", padx=(0, 20))

        title = ctk.CTkLabel(
            header,
            text="Elige un juego",
            font=ctk.CTkFont("Helvetica",size=32, weight="bold"),
            text_color="#003366"
        )
        title.pack(side="top")

        # === Scrollable Frame que ocupa todo ===
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color="#EAF6FF")
        self.scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # === Cargar juegos ===
        self.juegos = [
            {"nombre": "Ahorcado", "imagen": "assets/games/ahorcado.png"}, 
            {"nombre": "Adivina la Palabra", "imagen": "assets/games/adivina_la_palabra.jpeg"},
            {"nombre": "Imita la Seña", "imagen": "assets/games/Reconoce_la_sena.png"},
            {"nombre": "Secuencia de Señas", "imagen": "assets/games/Secuencia_de_senas.png"},
            {"nombre": "Proximamente", "imagen": "assets/games/proximamente.png"},
            {"nombre": "Proximamente", "imagen": "assets/games/proximamente.png"},
        ]

        self.imagenes = []
        self.mostrar_juegos()

        # Configura grilla (3 columnas × 2 filas)
        for r in range(2):
            self.scrollable.grid_rowconfigure(r, weight=1)
        for c in range(3):
            self.scrollable.grid_columnconfigure(c, weight=1)

    def mostrar_juegos(self):
        for i, juego in enumerate(self.juegos):
            fila = i // 3
            col = i % 3

            # === Celda individual ===
            item = ctk.CTkFrame(self.scrollable, fg_color="#FFFFFF", corner_radius=10)
            item.grid(row=fila, column=col, padx=10, pady=10, sticky="nsew")

            # === Imagen ===
            if os.path.exists(juego["imagen"]):
                img = Image.open(juego["imagen"]).resize((180, 180), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                self.imagenes.append(tk_img)

                img_label = ctk.CTkLabel(item, image=tk_img, text="")
                img_label.pack(padx=10, pady=(10, 5), expand=True)

            # === Botón ===
            btn = ctk.CTkButton(item,
                                text=f"{juego['nombre']}",
                                font=ctk.CTkFont("Helvetica",size=24, weight="bold"),
                                fg_color="#008B8B",
                                hover_color="#20B2AA",
                                command=lambda j=juego["nombre"]: self.jugar(j))
            btn.pack(pady=(0, 10), fill="x", padx=10)

    def jugar(self, nombre_juego):
        print(f"Iniciar {nombre_juego}")
        
        # Navegar según el juego seleccionado
        if nombre_juego == "Secuencia de Señas":
            self.controller.show_frame("SecuenciaSeñasGame")
        elif nombre_juego == "Imita la Seña":
            self.controller.show_frame("ImitacionSeñasGame")
        elif nombre_juego == "Proximamente":
            # Mostrar mensaje de próximamente
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Próximamente", "Este juego estará disponible próximamente.")
        else:
            # Para otros juegos, mostrar mensaje por ahora
            import tkinter.messagebox as messagebox
            messagebox.showinfo("En desarrollo", f"El juego '{nombre_juego}' está en desarrollo.")
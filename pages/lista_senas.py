import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

class ListaSenasWindow(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_color = "#AEEEEE"

        self.configure(fg_color=self.bg_color)
        
        self.bg_color = "#AEEEEE"
        self.button_style = {
            'font': ('Helvetica', 12),
            'bg': '#008B8B',
            'fg': 'white',
            'activebackground': '#20B2AA',
            'bd': 0,
            'relief': 'flat',
            'padx': 10,
            'pady': 5
        }
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="Lista de Señas",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=(0, 20))
        
        # Frame para el contenido (abecedario y palabras)
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True)
        
        # Sección del abecedario
        abecedario_frame = tk.LabelFrame(
            content_frame,
            text="Abecedario",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10,
        )
        abecedario_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Hacer el frame clickeable
        abecedario_frame.bind("<Button-1>", lambda e: self.mostrar_abecedario())
        
        # Mostrar el abecedario en 3 filas como en tu imagen
        letras = [
            "a b c d e f",
            "g h i j k l",
            "m n ñ o p q",
            "r s t u v w",
            "x y z"
        ]
        
        for fila in letras:
            tk.Label(
                abecedario_frame,
                text=fila,
                font=("Courier", 18),
                bg=self.bg_color
            ).pack(pady=5)
        
        # Boton 
        
        
        
        # Sección de palabras
        palabras_frame = tk.LabelFrame(
            content_frame,
            text="Palabras",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        palabras_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Aquí iría la lista de palabras (puedes implementar un sistema de búsqueda)
        tk.Label(
            palabras_frame,
            text="Selecciona una categoría:",
            font=("Helvetica", 12),
            bg=self.bg_color
        ).pack(pady=10)
        
        # Ejemplo de categorías (puedes expandir esto)
        categorias = ["Familia", "Colores", "Números", "Comida", "Saludos"]
        
        for categoria in categorias:
            btn = tk.Button(
                palabras_frame,
                text=categoria,
                command=lambda c=categoria: self.mostrar_palabras(c),
                **self.button_style
            )
            btn.pack(pady=5, fill="x")
        
        # Botón para volver
        tk.Button(
            main_frame,
            text="Volver al Menú Principal",
            font=("Helvetica", 12, "bold"),
            command=self.cerrar_ventana,
            bg="#008B8B",
            fg="white",
            activebackground="#20B2AA",
            padx=20,
            pady=5
        ).pack(pady=20)
    
    def mostrar_palabras(self, categoria):
        # Aquí implementarías la lógica para mostrar palabras de la categoría seleccionada
        print(f"Mostrando palabras de: {categoria}")
        # Puedes usar otro Toplevel o actualizar la sección de palabras
        
    def mostrar_abecedario(self):
        # Aquí implementarías la lógica para cambiar a vista de abecedario
        print(f"Mostrando palabras de: abecedario")
        from pages.abecedario import SenhaWindow
        SenhaWindow(self)
        
    
    def cerrar_ventana(self):
        self.controller.show_frame("Menu")
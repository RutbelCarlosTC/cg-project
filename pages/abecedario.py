import tkinter as tk
from PIL import Image, ImageTk

class SenhaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Abecedario")
        self.geometry("800x700")
        
        # Configuración de estilo
        self.bg_color = "#AEEEEE"
        self.configure(bg=self.bg_color)
        
        # Contenedor principal
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        # Frame para la imagen (primero en el orden)
        img_frame = tk.Frame(main_frame, bg=self.bg_color)
        img_frame.pack(fill="both", expand=True, pady=20)
        
        # Cargar imagen
        try:
            imagen = Image.open(f"assets/games/alfabeto.jpg")
            #imagen = Image.new('RGB', (400, 400), color='#008B8B')
            img_tk = ImageTk.PhotoImage(imagen)
            
            img_label = tk.Label(
                img_frame,
                image=img_tk,
                bg=self.bg_color
            )
            img_label.image = img_tk
            img_label.pack(expand=True)
            
        except Exception as e:
            tk.Label(
                img_frame,
                text="No se pudo cargar la imagen",
                font=("Helvetica", 14),
                bg=self.bg_color,
                fg="red"
            ).pack(expand=True)
        
        # Frame para el botón (abajo)
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=(0, 20))
        
        # Botón Volver (ahora en la parte inferior)
        btn_volver = tk.Button(
            btn_frame,
            text="Volver",
            command=self.cerrar_ventana,
            font=("Helvetica", 12, "bold"),
            bg="#008B8B",
            fg="white",
            activebackground="#20B2AA",
            padx=20,
            pady=5
        )
        btn_volver.pack(pady=10)
    
    def cerrar_ventana(self):
        self.destroy()
        self.master.deiconify()
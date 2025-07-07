import tkinter as tk
from PIL import Image, ImageTk

class SenhaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Abecedario")
        self.geometry("650x550")  # Ventana más pequeña
        
        # Configuración de estilo
        self.bg_color = "#AEEEEE"
        self.configure(bg=self.bg_color)
        
        # Configurar la ventana para que sea modal (opcional)
        self.transient(master)
        self.grab_set()  # Hace que la ventana sea modal
        
        # Centrar la ventana
        self.center_window()
        
        # Contenedor principal
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)  # Menos padding
        
        # Frame para la imagen (primero en el orden)
        img_frame = tk.Frame(main_frame, bg=self.bg_color)
        img_frame.pack(fill="both", expand=True)  # Sin pady para que esté más pegado
        
        # Cargar imagen
        try:
            imagen = Image.open(f"assets/games/alfabeto.jpg")
            # Redimensionar la imagen a un tamaño más compacto
            imagen = imagen.resize((500, 350), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(imagen)
            
            img_label = tk.Label(
                img_frame,
                image=img_tk,
                bg=self.bg_color
            )
            img_label.image = img_tk  # Mantener referencia
            img_label.pack(expand=True)
            
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            # Crear un placeholder en caso de error
            placeholder = tk.Label(
                img_frame,
                text="📖 ABECEDARIO EN SEÑAS 📖",
                font=("Helvetica", 18, "bold"),
                bg="#008B8B",
                fg="white",
                padx=40,
                pady=30
            )
            placeholder.pack(expand=True)
        
        # Frame para el botón (abajo) - más pegado
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=(10, 0))  # Menos espacio arriba
        
        # Botón Cerrar (cambié el texto)
        btn_cerrar = tk.Button(
            btn_frame,
            text="Cerrar",
            command=self.cerrar_ventana,
            font=("Helvetica", 12, "bold"),
            bg="#008B8B",
            fg="white",
            activebackground="#20B2AA",
            padx=20,
            pady=5
        )
        btn_cerrar.pack(pady=5)  # Menos padding
        
        # Manejar el evento de cerrar la ventana con la X
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def cerrar_ventana(self):
        """Cierra la ventana correctamente"""
        self.grab_release()  # Libera el grab modal
        self.destroy()  # Destruye la ventana
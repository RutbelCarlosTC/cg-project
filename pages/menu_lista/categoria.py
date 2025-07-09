import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
import requests
from io import BytesIO

class CategoriaVideosWindow(tk.Toplevel):
    def __init__(self, master, categoria):
        super().__init__(master)
        self.master = master
        self.categoria = categoria
        self.title(f"Videos - {categoria}")
        self.geometry("650x600")  # Tamaño similar al de abecedario pero más alto
        
        # Configuración de estilo
        self.bg_color = "#AEEEEE"
        self.configure(bg=self.bg_color)
        
        # Configurar la ventana para que sea modal
        self.transient(master)
        self.grab_set()
        
        # Centrar la ventana
        self.center_window()
        
        # Frame principal (sin scroll)
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título de la categoría (fuera del scroll)
        tk.Label(
            main_frame,
            text=categoria.upper(),
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg="#003366"
        ).pack(pady=(0, 15))
        
        # Frame contenedor para el canvas y scrollbar
        container = tk.Frame(main_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True)
        
        # Canvas con scroll vertical
        self.canvas = tk.Canvas(
            container,
            bg=self.bg_color,
            highlightthickness=0,
            width=600,  # Ancho fijo para controlar el área de contenido
            height=450  # Altura fija para el área desplazable
        )
        self.scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Frame desplazable dentro del canvas
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=self.bg_color,
            padx=10
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Cargar videos de la categoría
        self.cargar_videos()
        
        # Botón Cerrar (fuera del área de scroll)
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=(15, 5))
        
        btn_cerrar = tk.Button(
            btn_frame,
            text="Cerrar",
            command=self.cerrar_ventana,
            font=("Helvetica", 12, "bold"),
            bg="#008B8B",
            fg="white",
            activebackground="#20B2AA",
            padx=30,
            pady=5,
            bd=0,
            relief="flat"
        )
        btn_cerrar.pack()
        
        # Manejar el evento de cerrar la ventana con la X
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    
    def cargar_videos(self):
        """Carga los videos de la categoría seleccionada"""
        videos = self.obtener_videos_por_categoria(self.categoria)
        
        for video in videos:
            self.crear_video_card(video)
    
    def obtener_videos_por_categoria(self, categoria):
        """Devuelve los videos para la categoría dada"""
        videos_por_categoria = {
            "Familia": [
                {"titulo": "LSP - Vocabulario de Familia", "id": "ISeg2AZo8Mk"},
                #{"titulo": "LSP- Familia - Parte 1", "id": "dernDK9ipBs"},
                #{"titulo": "LSP- Familia - Parte 2", "id": "UInOtvdlhYY"},
            ],
            "Colores": [
                {"titulo": "LSP - Colores - Parte 1", "id": "KbhTMsqN_t4"},
                {"titulo": "LSP - Colores - Parte 2", "id": "l2vSBp31suY"},
            ],
            "Números": [
                {"titulo": "LSP - Números - Parte 1", "id": "OGwAaaGwFzw"},
                {"titulo": "LSP - Números - Parte 2", "id": "84GKec_Ws5U"},
            ],
            "Alimentos": [
                {"titulo": "LSP - Alimentos", "id": "__chbqUUrtk"},
                {"titulo": "LSP - Frutas", "id": "lAwRj1JDaR4"},
                {"titulo": "LSP - Verduras", "id": "9pAgFmR4H-I"},
            ],
            "Saludos": [
                {"titulo": "LSP - El estado de ánimo y saludos", "id": "ffP-Uvw5Gr4"},
            ],
        }
        
        return videos_por_categoria.get(categoria, [])
    
    def crear_video_card(self, video):
        """Crea un frame con la miniatura y título del video"""
        video_frame = tk.Frame(
            self.scrollable_frame,
            bg="white",
            bd=2,
            relief="groove",
            padx=5,
            pady=10
        )
        video_frame.pack(fill="x", pady=10, ipady=5)
        
        # Título del video
        tk.Label(
            video_frame,
            text=video["titulo"],
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#003366",
            wraplength=550,  # Ajustado al ancho del canvas
            justify="center"
        ).pack(pady=(0, 10))
        
        # Miniatura del video (ancho completo)
        try:
            # Obtener miniatura de YouTube
            thumbnail_url = f"https://img.youtube.com/vi/{video['id']}/mqdefault.jpg"
            response = requests.get(thumbnail_url, stream=True)
            
            if response.status_code == 200:
                img_data = response.content
                thumbnail = Image.open(BytesIO(img_data))
                
                # Redimensionar manteniendo relación de aspecto (16:9)
                original_width, original_height = thumbnail.size
                new_width = 550  # Ancho casi completo
                new_height = int(new_width * original_height / original_width)
                
                thumbnail = thumbnail.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(thumbnail)
                
                img_label = tk.Label(
                    video_frame,
                    image=img_tk,
                    bg="white",
                    cursor="hand2"
                )
                img_label.image = img_tk
                img_label.pack()
                
                # Hacer clickable la miniatura
                img_label.bind("<Button-1>", lambda e, vid=video: self.abrir_video(vid))
            else:
                raise Exception("No se pudo cargar miniatura")
                
        except Exception as e:
            print(f"Error cargando miniatura: {e}")
            # Placeholder si falla
            placeholder = tk.Label(
                video_frame,
                text="Miniatura no disponible",
                bg="white",
                fg="gray",
                font=("Helvetica", 12),
                padx=150,
                pady=50
            )
            placeholder.pack()
        
        # Botón para abrir el video
        tk.Button(
            video_frame,
            text="VER VIDEO",
            command=lambda v=video: self.abrir_video(v),
            font=("Helvetica", 11, "bold"),
            bg="#008B8B",
            fg="white",
            activebackground="#20B2AA",
            padx=15,
            pady=3,
            bd=0,
            relief="flat"
        ).pack(pady=(10, 0))
    
    def abrir_video(self, video):
        """Abre el video en YouTube"""
        webbrowser.open(f"https://www.youtube.com/watch?v={video['id']}")
    
    def _on_mousewheel(self, event):
        """Maneja el scroll con la rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
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
        self.grab_release()
        self.destroy()
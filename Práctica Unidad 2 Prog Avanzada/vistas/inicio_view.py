import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class InicioView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        self.pack(padx=20, pady=20, fill="both", expand=True)

        # Descargar la imagen desde la URL
        url = "https://blog.pearsonlatam.com/hs-fs/hubfs/Blog%20HED/Multimedia/Imágenes%20de%20Blog/contenidos-de-biblioteca-virtual-para-elearning.jpg?width=800&name=contenidos-de-biblioteca-virtual-para-elearning.jpg"
        response = requests.get(url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        
        # Redimensionar imagen
        image = image.resize((400, 250))  # Ajusta el tamaño según lo necesites
        self.photo = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 250))

        # Mostrar la imagen
        imagen_label = ctk.CTkLabel(self, image=self.photo, text="")  # text="" para que no muestre texto al lado
        imagen_label.pack(pady=10)

        # Título
        titulo = ctk.CTkLabel(self, text="Biblioteca Digital", font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(10, 30))

        # Botón de búsqueda
        btn_busqueda = ctk.CTkButton(self, text="Buscar libros", command=self.controlador.mostrar_busqueda)
        btn_busqueda.pack(pady=10)

        # Botón de préstamo
        btn_prestamo = ctk.CTkButton(self, text="Realizar préstamo", command=self.controlador.mostrar_prestamo)
        btn_prestamo.pack(pady=10)

        # Botón de administración
        btn_admin = ctk.CTkButton(self, text="Administrar catálogo", command=self.controlador.mostrar_admin)
        btn_admin.pack(pady=10)

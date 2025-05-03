import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta
from PIL import Image
import requests
from io import BytesIO

class AdministracionView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        self.pack(fill="both", expand=True)

        # Descargar y mostrar la imagen
        url = "https://img.innovaciondigital360.com/wp-content/uploads/2023/02/13163115/Bibliotecas-digitales.jpg"
        response = requests.get(url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image = image.resize((400, 300))
        self.img = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 300))
        imagen_label = ctk.CTkLabel(self, image=self.img, text="")
        imagen_label.pack(pady=10)

        ctk.CTkLabel(self, text="Administración del Catálogo", font=("Arial", 20)).pack(pady=10)

        # Sección: Agregar libro
        ctk.CTkLabel(self, text="Agregar Nuevo Libro", font=("Arial", 16)).pack(pady=5)
        self.entry_titulo = ctk.CTkEntry(self, placeholder_text="Título", width=300)
        self.entry_autor = ctk.CTkEntry(self, placeholder_text="Autor", width=300)
        self.entry_genero = ctk.CTkEntry(self, placeholder_text="Género", width=300)

        self.entry_titulo.pack(pady=2)
        self.entry_autor.pack(pady=2)
        self.entry_genero.pack(pady=2)

        ctk.CTkButton(self, text="Agregar Libro", command=self.agregar_libro).pack(pady=8)

        # Sección: Registrar Devolución
        ctk.CTkLabel(self, text="Registrar Devolución", font=("Arial", 16)).pack(pady=10)
        self.libros = self.cargar_libros()
        prestados = [libro["titulo"] for libro in self.libros if not libro.get("disponible", True)]

        self.combo_devolucion = ctk.CTkComboBox(self, values=prestados, width=300)
        self.combo_devolucion.pack(pady=5)

        self.entry_fecha_prestamo = ctk.CTkEntry(self, placeholder_text="Fecha de préstamo (dd/mm/aaaa)", width=300)
        self.entry_fecha_prestamo.pack(pady=2)

        ctk.CTkButton(self, text="Registrar Devolución", command=self.registrar_devolucion).pack(pady=8)

        # Nota de penalización
        self.label_penalizacion = ctk.CTkLabel(self, text="Nota: La penalización por retraso se aplica cuando el libro se devuelve después de 7 días.", font=("Arial", 12), text_color="red")
        self.label_penalizacion.pack(pady=10)

        # Botón de regresar
        btn_regresar = ctk.CTkButton(self, text="Regresar", command=self.controlador.mostrar_inicio)
        btn_regresar.pack(pady=10)

    def cargar_libros(self):
        ruta = "data/libros.json"
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar_libros(self):
        ruta = "data/libros.json"
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.libros, f, indent=4, ensure_ascii=False)

    def agregar_libro(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        genero = self.entry_genero.get().strip()

        if not titulo or not autor or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        nuevo_libro = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "disponible": True
        }
        self.libros.append(nuevo_libro)
        self.guardar_libros()
        messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente.")
        self.entry_titulo.delete(0, "end")
        self.entry_autor.delete(0, "end")
        self.entry_genero.delete(0, "end")

    def registrar_devolucion(self):
        titulo = self.combo_devolucion.get()
        fecha_texto = self.entry_fecha_prestamo.get().strip()

        if not titulo or not fecha_texto:
            messagebox.showerror("Error", "Debes seleccionar un libro y escribir la fecha.")
            return

        try:
            fecha_prestamo = datetime.strptime(fecha_texto, "%d/%m/%Y")
            dias_transcurridos = (datetime.now() - fecha_prestamo).days
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Usa dd/mm/aaaa.")
            return

        for libro in self.libros:
            if libro["titulo"] == titulo:
                libro["disponible"] = True
                self.guardar_libros()

                if dias_transcurridos > 7:
                    dias_retraso = dias_transcurridos - 7
                    messagebox.showwarning("Penalización", f"El libro fue devuelto con {dias_retraso} días de retraso. ¡Se aplicará una penalización!")
                else:
                    messagebox.showinfo("Éxito", "Devolución registrada correctamente.")
                return

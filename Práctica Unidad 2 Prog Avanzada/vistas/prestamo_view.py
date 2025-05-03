import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os

class PrestamoView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        self.pack(fill="both", expand=True)

        # Título
        ctk.CTkLabel(self, text="Realizar Préstamo", font=("Arial", 20)).pack(pady=10)

        # Cargar libros
        self.libros = self.cargar_libros()
        self.libros_disponibles = [libro for libro in self.libros if libro.get("disponible", True)]

        # Selección de libro
        ctk.CTkLabel(self, text="Seleccione un libro:").pack(pady=5)
        opciones = [libro["titulo"] for libro in self.libros_disponibles]
        self.opcion_libro = ctk.CTkComboBox(self, values=opciones, width=300)
        self.opcion_libro.pack(pady=5)

        # Nombre del lector
        ctk.CTkLabel(self, text="Nombre del lector:").pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(self, width=300)
        self.entry_nombre.pack(pady=5)

        # Botón realizar préstamo
        ctk.CTkButton(self, text="Confirmar Préstamo", command=self.realizar_prestamo).pack(pady=10)

        # Fecha de devolución
        self.label_fecha = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_fecha.pack(pady=10)

        # Botón regresar
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

    def realizar_prestamo(self):
        nombre = self.entry_nombre.get().strip()
        titulo = self.opcion_libro.get()

        if not nombre or not titulo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        for libro in self.libros:
            if libro["titulo"] == titulo and libro.get("disponible", True):
                libro["disponible"] = False
                fecha_prestamo = datetime.now()
                fecha_devolucion = fecha_prestamo + timedelta(days=7)
                self.guardar_libros()

                self.label_fecha.configure(
                    text=f"Fecha de devolución: {fecha_devolucion.strftime('%d/%m/%Y')}"
                )
                messagebox.showinfo("Éxito", f"Préstamo registrado para {nombre}")
                return

        messagebox.showwarning("No disponible", "El libro ya ha sido prestado.")
import customtkinter as ctk
from tkinter import ttk
import json
import os

class BusquedaView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        self.pack(fill="both", expand=True)
        self.libros = self.cargar_libros()

        # Título de la vista
        ctk.CTkLabel(self, text="Buscar Libros", font=("Arial", 20)).pack(pady=10)

        # Filtros
        filtro_frame = ctk.CTkFrame(self)
        filtro_frame.pack(pady=10)

        ctk.CTkLabel(filtro_frame, text="Título:").grid(row=0, column=0, padx=5)
        self.entry_titulo = ctk.CTkEntry(filtro_frame, width=150)
        self.entry_titulo.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(filtro_frame, text="Autor:").grid(row=0, column=2, padx=5)
        self.entry_autor = ctk.CTkEntry(filtro_frame, width=150)
        self.entry_autor.grid(row=0, column=3, padx=5)

        ctk.CTkLabel(filtro_frame, text="Género:").grid(row=0, column=4, padx=5)
        self.entry_genero = ctk.CTkEntry(filtro_frame, width=150)
        self.entry_genero.grid(row=0, column=5, padx=5)

        ctk.CTkButton(self, text="Buscar", command=self.buscar_libros).pack(pady=10)

        # Tabla de resultados
        self.tabla = ttk.Treeview(self, columns=("Título", "Autor", "Género", "Disponible"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)
        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Botón de regresar
        btn_regresar = ctk.CTkButton(self, text="Regresar", command=self.controlador.mostrar_inicio)
        btn_regresar.pack(pady=10)

    def cargar_libros(self):
        ruta = "data/libros.json"
        if not os.path.exists(ruta):
            return []

        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def buscar_libros(self):
        titulo = self.entry_titulo.get().lower()
        autor = self.entry_autor.get().lower()
        genero = self.entry_genero.get().lower()

        resultados = []
        for libro in self.libros:
            if (
                titulo in libro["titulo"].lower()
                and autor in libro["autor"].lower()
                and genero in libro["genero"].lower()
            ):
                resultados.append(libro)

        self.actualizar_tabla(resultados)

    def actualizar_tabla(self, libros):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for libro in libros:
            disponible = "Sí" if libro.get("disponible", True) else "No"
            self.tabla.insert("", "end", values=(libro["titulo"], libro["autor"], libro["genero"], disponible))

import json
import os

class Libro:
    def __init__(self, titulo, autor, genero, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.disponible = disponible

    def __repr__(self):
        return f"Libro(titulo={self.titulo}, autor={self.autor}, genero={self.genero}, disponible={self.disponible})"

    @classmethod
    def cargar_libros(cls):
        ruta = "data/libros.json"
        if not os.path.exists(ruta):
            return []

        with open(ruta, "r", encoding="utf-8") as f:
            libros_data = json.load(f)
            return [cls(**libro) for libro in libros_data]

    @classmethod
    def guardar_libros(cls, libros):
        ruta = "data/libros.json"
        with open(ruta, "w", encoding="utf-8") as f:
            libros_data = [libro.__dict__ for libro in libros]
            json.dump(libros_data, f, indent=4, ensure_ascii=False)

    def guardar(self):
        libros = self.cargar_libros()
        libros.append(self)
        self.guardar_libros(libros)

    @classmethod
    def actualizar_disponibilidad(cls, titulo, disponible):
        libros = cls.cargar_libros()
        for libro in libros:
            if libro.titulo == titulo:
                libro.disponible = disponible
        cls.guardar_libros(libros)

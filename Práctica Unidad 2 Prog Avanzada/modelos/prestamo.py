from datetime import datetime, timedelta
import json
import os

class Prestamo:
    def __init__(self, libro, usuario, fecha_prestamo=None, fecha_devolucion=None):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo or datetime.now().strftime("%Y-%m-%d")
        self.fecha_devolucion = fecha_devolucion or (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")

    def __repr__(self):
        return f"Prestamo(libro={self.libro}, usuario={self.usuario}, fecha_prestamo={self.fecha_prestamo}, fecha_devolucion={self.fecha_devolucion})"

    @classmethod
    def cargar_prestamos(cls):
        ruta = "data/prestamos.json"
        if not os.path.exists(ruta):
            return []

        with open(ruta, "r", encoding="utf-8") as f:
            prestamos_data = json.load(f)
            return [cls(**prestamo) for prestamo in prestamos_data]

    @classmethod
    def guardar_prestamos(cls, prestamos):
        ruta = "data/prestamos.json"
        with open(ruta, "w", encoding="utf-8") as f:
            prestamos_data = [prestamo.__dict__ for prestamo in prestamos]
            json.dump(prestamos_data, f, indent=4, ensure_ascii=False)

    def guardar(self):
        prestamos = self.cargar_prestamos()
        prestamos.append(self)
        self.guardar_prestamos(prestamos)

    @classmethod
    def calcular_penalizacion(cls, fecha_devolucion_real):
        fecha_devolucion_real = datetime.strptime(fecha_devolucion_real, "%Y-%m-%d")
        fecha_devolucion = datetime.strptime(cls.fecha_devolucion, "%Y-%m-%d")

        if fecha_devolucion_real > fecha_devolucion:
            # Penalización de 1 día por cada día de retraso
            retraso = (fecha_devolucion_real - fecha_devolucion).days
            return retraso * 2  # Penalización de $2 por día de retraso
        return 0
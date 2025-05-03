from vistas.inicio_view import InicioView
from vistas.busqueda_view import BusquedaView
from vistas.prestamo_view import PrestamoView
from vistas.administracion_view import AdministracionView

class Controlador:
    def __init__(self, app):
        self.app = app

    def limpiar_vista(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_vista()
        InicioView(self.app, self)

    def mostrar_busqueda(self):
        self.limpiar_vista()
        BusquedaView(self.app, self)

    def mostrar_prestamo(self):
        self.limpiar_vista()
        PrestamoView(self.app, self)

    def mostrar_admin(self):
        self.limpiar_vista()
        AdministracionView(self.app, self)

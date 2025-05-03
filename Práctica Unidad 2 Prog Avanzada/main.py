import customtkinter as ctk
from controladores.controlador import Controlador

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca Digital")
        self.geometry("700x500")

        self.controlador = Controlador(self)
        self.controlador.mostrar_inicio()

if __name__ == "__main__":
    app = App()
    app.mainloop()

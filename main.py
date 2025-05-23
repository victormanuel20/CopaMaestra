from controller import CoctelController
from CopaMaestra import CopaMaestra

if __name__ == "__main__":
    vista = CopaMaestra(None)
    controlador = CoctelController(vista)
    vista.controller = controlador
    vista.iniciar()

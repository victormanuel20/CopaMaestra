from controller import CoctelController
from vista import VistaPrincipal

if __name__ == "__main__":
    vista = VistaPrincipal(None)
    controlador = CoctelController(vista)
    vista.controller = controlador
    vista.iniciar()

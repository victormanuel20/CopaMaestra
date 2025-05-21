import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

class VentanaDetalle:
    def __init__(self, datos_coctel):
        self.ventana = ttk.Toplevel()
        self.ventana.title(f"🍸 {datos_coctel['nombre']} - Detalles")
        self.ventana.geometry("650x600")
        self.ventana.resizable(False, False)

        # Estilo visual
        estilo = ttk.Style("journal")  # Prueba otros: 'superhero', 'flatly', 'cosmo', 'morph', 'vapor', etc.

        # Título
        ttk.Label(self.ventana, text=datos_coctel['nombre'], font=("Helvetica", 20, "bold"), bootstyle="danger").pack(pady=10)

        # Imagen
        if datos_coctel['imagen']:
            try:
                response = requests.get(datos_coctel['imagen'])
                imagen = Image.open(BytesIO(response.content))
                imagen = imagen.resize((200, 200))
                img_tk = ImageTk.PhotoImage(imagen)
                panel = ttk.Label(self.ventana, image=img_tk)
                panel.image = img_tk
                panel.pack(pady=5)
                print(f"🖼️ Imagen cargada desde: {datos_coctel['imagen']}")
            except:
                ttk.Label(self.ventana, text="(Imagen no disponible)", bootstyle="secondary").pack()

        # Instrucciones
        ttk.Label(self.ventana, text="📋 Instrucciones:", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))
        ttk.Label(self.ventana, text=datos_coctel['instrucciones'], wraplength=500, justify="center").pack()

        # Ingredientes y medidas
        ttk.Label(self.ventana, text="🍸 Ingredientes:", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))
        for ing, med in zip(datos_coctel['ingredientes'], datos_coctel['medidas']):
            linea = f"• {ing} ({med})"
            ttk.Label(self.ventana, text=linea).pack()

        # Sabor
        if datos_coctel['sabor']:
            ttk.Label(self.ventana, text="🍬 Sabor:", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))
            ttk.Label(self.ventana, text=datos_coctel['sabor']).pack()

        # Botón cerrar
        ttk.Button(self.ventana, text="❌ Cerrar", bootstyle="danger-outline", width=20,
                   command=self.ventana.destroy).pack(pady=30)

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

class VentanaDetalle:
    def __init__(self, datos_coctel):
        self.ventana = ttk.Toplevel()
        self.ventana.title(f"🍸 {datos_coctel['nombre']} - Detalles")
        self.ventana.geometry("700x600")  # Ventana un poco más grande
        self.ventana.resizable(False, False)
        self.ventana.lift()
        self.ventana.focus_force()

        estilo = ttk.Style("journal")

        # Botón cerrar arriba a la derecha
        frame_top = ttk.Frame(self.ventana)
        frame_top.pack(fill="x", pady=(5, 0))
        ttk.Button(
            frame_top,
            text="❌ Cerrar",
            bootstyle="danger-outline",
            width=12,
            command=self.ventana.destroy
        ).pack(side="right", padx=10)

        # Título
        ttk.Label(self.ventana, text=datos_coctel['nombre'], font=("Helvetica", 20, "bold"), bootstyle="danger").pack(pady=5)

        # Imagen
        if datos_coctel['imagen']:
            try:
                response = requests.get(datos_coctel['imagen'])
                imagen = Image.open(BytesIO(response.content))
                imagen = imagen.resize((180, 180))
                img_tk = ImageTk.PhotoImage(imagen)
                panel = ttk.Label(self.ventana, image=img_tk)
                panel.image = img_tk
                panel.pack(pady=5)
            except:
                ttk.Label(self.ventana, text="(Imagen no disponible)", bootstyle="secondary").pack()

        # Instrucciones
        ttk.Label(self.ventana, text="📋 Instrucciones:", font=("Helvetica", 12, "bold")).pack(pady=(10, 2))
        ttk.Label(self.ventana, text=datos_coctel['instrucciones'], wraplength=650, justify="center").pack()

        # Ingredientes y medidas
        ttk.Label(self.ventana, text="🍸 Ingredientes:", font=("Helvetica", 12, "bold")).pack(pady=(10, 2))
        for ing, med in zip(datos_coctel['ingredientes'], datos_coctel['medidas']):
            linea = f"• {ing} ({med})"
            ttk.Label(self.ventana, text=linea, font=("Helvetica", 10)).pack()

        # Sabor
        if datos_coctel['sabor']:
            ttk.Label(self.ventana, text="🍬 Sabor:", font=("Helvetica", 12, "bold")).pack(pady=(10, 2))
            ttk.Label(self.ventana, text=datos_coctel['sabor'], font=("Helvetica", 11)).pack()

import tkinter as tk
from tkinter import font
from ventana_detalle import VentanaDetalle



"""
class VentanaResultado:
    def __init__(self, cocteles_simulados=None):
        self.ventana = tk.Toplevel()
        self.ventana.title("🎯 Recomendaciones para ti")
        self.ventana.geometry("400x400")
        self.ventana.configure(bg="#fff7f0")

        titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        button_font = font.Font(size=12, weight="bold")

        tk.Label(self.ventana, text="🍸 ¡Estos cócteles son para ti!", font=titulo_font,
                 bg="#fff7f0", fg="#8B0000").pack(pady=20)

        self.cocteles = cocteles_simulados or ["Cóctel A", "Cóctel B", "Cóctel C"]

        for nombre in self.cocteles:
            tk.Button(self.ventana, text=f"{nombre}", font=button_font,
                      width=25, bg="#ffcc80", fg="black",
                      command=lambda n=nombre: self.mostrar_detalle(n)).pack(pady=8)

        tk.Label(self.ventana, text="Haz clic para conocer más 🍹", bg="#fff7f0", fg="#333333",
                 font=("Helvetica", 10)).pack(pady=10)

        # Botón para cerrar la ventana
        tk.Button(self.ventana, text="❌ Cerrar ventana", font=button_font, bg="#d32f2f", fg="white",
                  width=20, command=self.ventana.destroy).pack(pady=10)

    def mostrar_detalle(self, nombre):
        print(f"🔍 Mostrando detalles para: {nombre}")

"""


class VentanaResultado:

    def __init__(self, controller, lista_ids):
        self.controller = controller
        self.ventana = tk.Toplevel()
        self.ventana.title("🎯 Recomendaciones para ti")
        self.ventana.geometry("400x450")
        self.ventana.configure(bg="#fff7f0")

        titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        button_font = font.Font(size=12, weight="bold")

        tk.Label(self.ventana, text="🍸 ¡Estos cócteles son para ti!", font=titulo_font,
                bg="#fff7f0", fg="#8B0000").pack(pady=20)

        self.ids = lista_ids

        for id_coctel in self.ids:
            print(f"🧾 Procesando cóctel ID {id_coctel}...")  # para depurar

            try:
                datos = self.controller.obtener_datos_coctel(id_coctel)
                nombre = datos["nombre"]
            except Exception as e:
                print(f"❌ Error al buscar ID {id_coctel}: {e}")
                continue

            tk.Button(self.ventana, text=nombre, font=button_font,
                    width=30, bg="#ffcc80", fg="black",
                    command=lambda i=id_coctel: self.mostrar_detalle(i)).pack(pady=8)


        tk.Label(self.ventana, text="Haz clic para conocer más 🍹", bg="#fff7f0", fg="#333333",
                font=("Helvetica", 10)).pack(pady=10)

        tk.Button(self.ventana, text="❌ Cerrar ventana", font=button_font, bg="#d32f2f", fg="white",
                width=20, command=self.ventana.destroy).pack(pady=10)
  
        
    def mostrar_detalle(self, id_coctel):
        datos = self.controller.obtener_datos_coctel(id_coctel)
        print(f"🔍 Detalles de '{datos['nombre']}' (ID: {id_coctel})")
        VentanaDetalle(datos)  # ← Aquí abrimos la nueva ventana



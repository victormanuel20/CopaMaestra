import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk
from ventana_resultado import VentanaResultado

usuario_data = {
    'edad': None,
    'estrato': None,
    'carrera': None,
    'genero': None
}

class CopaMaestra:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("🏆 COPA MAESTRA - Sistema Experto de Cócteles")
        self.root.geometry("520x500")
        self.root.configure(bg="#f0f0f0")

        self.carreras = ['administracion', 'arquitectura', 'derecho', 'diseño', 'ingenieria', 'medicina', 'sistemas']
        self.estratos = [1, 2, 3, 4, 5, 6]
        self.generos = ['femenino', 'masculino']

        titulo_font = font.Font(family="Helvetica", size=18, weight="bold")
        label_font = font.Font(size=12)
        entry_font = font.Font(size=12)
        button_font = font.Font(size=12, weight="bold")

        tk.Label(self.root, text="🏆 COPA MAESTRA", font=titulo_font, bg="#f0f0f0", fg="#003366").pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)

        # Edad
        self.agregar_campo(frame, "Edad:", 0, entry_font, label_font)
        self.entry_edad = self.crear_entry(frame, 0, entry_font)

        # Estrato - Combobox
        tk.Label(frame, text="Estrato:", font=label_font, bg="#f0f0f0").grid(row=1, column=0, sticky='e', pady=5)
        self.estrato_var = tk.StringVar()
        self.combo_estrato = ttk.Combobox(frame, textvariable=self.estrato_var, values=self.estratos,
                                          state="readonly", font=entry_font)
        self.combo_estrato.current(0)
        self.combo_estrato.grid(row=1, column=1, pady=5)

        # Carrera - Combobox
        tk.Label(frame, text="Carrera:", font=label_font, bg="#f0f0f0").grid(row=2, column=0, sticky='e', pady=5)
        self.carrera_var = tk.StringVar()
        self.combo_carrera = ttk.Combobox(frame, textvariable=self.carrera_var, values=self.carreras,
                                          state="readonly", font=entry_font)
        self.combo_carrera.current(0)
        self.combo_carrera.grid(row=2, column=1, pady=5)

        # Género - Combobox
        tk.Label(frame, text="Género:", font=label_font, bg="#f0f0f0").grid(row=3, column=0, sticky='e', pady=5)
        self.genero_var = tk.StringVar()
        self.combo_genero = ttk.Combobox(frame, textvariable=self.genero_var, values=self.generos,
                                         state="readonly", font=entry_font)
        self.combo_genero.current(0)
        self.combo_genero.grid(row=3, column=1, pady=5)

        # Botones
        boton_frame = tk.Frame(self.root, bg="#f0f0f0")
        boton_frame.pack(pady=30)

        tk.Button(boton_frame, text="📂 Cargar Datos", font=button_font, bg="#4CAF50", fg="white",
                  width=25, command=self.cargar_datos).grid(row=0, column=0, pady=5, padx=10)

        tk.Button(boton_frame, text="🔮 Recomendar Cóctel", font=button_font, bg="#2196F3", fg="white",
                  width=25, command=self.recomendar_coctel).grid(row=1, column=0, pady=5, padx=10)

        tk.Button(boton_frame, text="🧹 Borrar Campos", font=button_font, bg="#FFC107", fg="black",
                  width=25, command=self.borrar_campos).grid(row=2, column=0, pady=5, padx=10)

        tk.Button(boton_frame, text="❌ Cerrar", font=button_font, bg="#e53935", fg="white",
                  width=25, command=self.root.destroy).grid(row=3, column=0, pady=5, padx=10)

    def agregar_campo(self, frame, texto, fila, entry_font, label_font):
        tk.Label(frame, text=texto, font=label_font, bg="#f0f0f0").grid(row=fila, column=0, sticky='e', pady=5)

    def crear_entry(self, frame, fila, font):
        entry = tk.Entry(frame, font=font, width=25)
        entry.grid(row=fila, column=1, pady=5)
        return entry

    def cargar_datos(self):
        self.controller.cargar_datos()
        messagebox.showinfo("Carga de datos", "✅ Bases de datos cargadas correctamente.")

    def borrar_campos(self):
        self.entry_edad.delete(0, tk.END)
        self.combo_estrato.current(0)
        self.combo_carrera.current(0)
        self.combo_genero.current(0)
        print("🧹 Campos borrados.")

    def recomendar_coctel(self):
        edad = self.entry_edad.get()
        estrato = self.estrato_var.get()
        carrera = self.carrera_var.get()
        genero = self.genero_var.get()

        if not (edad and estrato and carrera and genero):
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        usuario_data['edad'] = int(edad)
        usuario_data['estrato'] = int(estrato)
        usuario_data['carrera'] = carrera
        usuario_data['genero'] = genero

        print("✅ Datos ingresados por el usuario:")
        for key, value in usuario_data.items():
            print(f"- {key.capitalize()}: {value}")

        #cocteles = self.controller.recomendar_cocteles(usuario_data)
        ids = self.controller.recomendar_cocteles(usuario_data)
        # 👉 Imprimir nombres de los cócteles en consola
        
        self.controller.mostrar_todos_los_nombres()
        VentanaResultado(self.controller, ids)



    def iniciar(self):
        self.root.mainloop()

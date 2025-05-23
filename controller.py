import pandas as pd
from PrologEngine import PrologEngine

class CoctelController:
    def __init__(self):
        self.engine = PrologEngine("motor.pl")  # ← Especificamos el archivo del motor Prolog
        self.data_calificaciones = None
        self.data_cocktails = None
        self.ids_recomendados = []  # ← aquí guardamos la inferencia

    def cargar_datos(self):
        print("📦 Cargando bases de datos...")

        try:
            self.data_calificaciones = pd.read_csv("data/base_calificaciones_cocteles_6000.csv")
            self.data_cocktails = pd.read_excel("data/cocktails_con_sabores.xlsx")

            print(f"✅ Calificaciones cargadas: {len(self.data_calificaciones)} registros")
            print(self.data_calificaciones.head(100))
            print("...")

            print(f"✅ Cócteles cargados: {len(self.data_cocktails)} registros")
            print(self.data_cocktails.head(100))
            print("...")

        except FileNotFoundError:
            print("❌ Error: uno de los archivos no fue encontrado.")
        except Exception as e:
            print(f"❌ Error al cargar los datos: {e}")
        else:
            print("✔️ Datos cargados correctamente.")
            # 🔁 Cargar hechos en el motor Prolog
            self.engine.cargar_datos(self.data_calificaciones.to_dict(orient="records"))
            self.engine.mostrar_todos_los_hechos(n=10)  # <-- Aquí llamas para ver los hechos cargados
          
    """
    def recomendar_cocteles(self, datos_usuario):
        print("📊 Ejecutando inferencia (simulada)...")
        print(f"Datos recibidos: {datos_usuario}")
        # Simulación fija, luego se conecta con Prolog o cálculo real
        return ["Margarita", "Mojito", "Negroni"]
        
    """
    
    """
    def recomendar_cocteles(self, datos_usuario):
        print("🧠 Ejecutando consulta en Prolog (simulada por ahora)...")
        print(f"📥 Entrada del usuario: {datos_usuario}")
        
        # ✅ Devuelve IDs reales de cocktails.xlsx
        return [17222, 13501, 17225]  # A1, ABC, Ace
    
    """
    
    def recomendar_cocteles(self, datos_usuario):
        print("📊 Ejecutando inferencia desde el motor...")
        ids = self.engine.recomendar_cocteles(datos_usuario)
        self.ids_recomendados = ids  # 💾 guardamos los IDs para luego usarlos en otros métodos
        return ids

        
                
    def obtener_datos_coctel(self, id_coctel):
        try:
            row = self.data_cocktails[self.data_cocktails['id'] == id_coctel].iloc[0]
            nombre = row['Drink']
            instrucciones = row['Inuctions'] if pd.notna(row['Inuctions']) else "Sin instrucciones"
            imagen = row['DrinkThumb'] if pd.notna(row['DrinkThumb']) else ""

            ingredientes = []
            medidas = []

            for i in range(1, 7):
                ingrediente = row.get(f'Ingredient{i}')
                medida = row.get(f'Measure{i}')

                if pd.notna(ingrediente):
                    ingredientes.append(ingrediente)
                    if pd.notna(medida):
                        medidas.append(medida)
                    else:
                        medidas.append("Cantidad no especificada")

            sabor = row['Flavor'] if pd.notna(row['Flavor']) else "Desconocido"

            # Quita los prints aquí, solo retorna el diccionario
            return {
                'nombre': nombre,
                'instrucciones': instrucciones,
                'imagen': imagen,
                'ingredientes': ingredientes,
                'medidas': medidas,
                'sabor': sabor
            }

        except Exception as e:
            print(f"❌ Error al obtener datos del cóctel ID {id_coctel}: {e}")
            return {
                'nombre': 'Desconocido',
                'instrucciones': 'No disponible',
                'imagen': '',
                'ingredientes': [],
                'medidas': [],
                'sabor': "Desconocido"
            }

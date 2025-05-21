from pyswip import Prolog

class PrologEngine:
    def __init__(self, path="motor.pl"):
        self.prolog = Prolog()
        try:
            self.prolog.consult(path)
            print(f"✅ Motor Prolog cargado desde: {path}")
        except Exception as e:
            print(f"⚠️ No se pudo cargar el motor Prolog: {e}")

    def cargar_resultados(self, data):
        print("⚙️ Cargando calificaciones al motor Prolog...")
        for row in data:
            try:
                cmd = (
                    f"calificacion({row['Edad']}, {row['Estrato']}, "
                    f"'{row['Carrera'].lower()}', '{row['Genero'].lower()}', "
                    f"{row['Coctel_ID']}, {row['Calificacion']})"
                )
                list(self.prolog.query(cmd))
            except Exception as e:
                print("❌ Error al agregar un hecho")
                print("➡️", e)
                print("➡️ Row fallida:", row)


    def recomendar_cocteles(self, datos_usuario):
        print("🧠 Ejecutando consulta en Prolog (simulada por ahora)...")
        print(f"📥 Entrada del usuario: {datos_usuario}")
        return [17222, 13501, 17225]  # ✅ Estos sí son IDs reales de cócteles




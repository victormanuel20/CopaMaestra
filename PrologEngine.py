from pyswip import Prolog

class PrologEngine:
    def __init__(self, path="motor.pl"):
        self.prolog = Prolog()
        try:
            self.prolog.consult(path)

        except Exception as e:
            print(f"⚠️ No se pudo cargar el motor Prolog: {e}")

    def cargar_datos(self, data):
        print("⚙️ Cargando calificaciones al motor Prolog...")
        total = 0
        for i, row in enumerate(data):
            try:
                cmd = (
                    f"agregar_calificacion({row['Edad']}, {row['Estrato']}, "
                    f"'{row['Carrera'].lower()}', '{row['Genero'].lower()}', "
                    f"{row['Coctel_ID']}, {row['Calificacion']})"
                )
                list(self.prolog.query(cmd))
                
                total += 1
            except Exception as e:
                print("❌ Error al agregar un hecho:", e)
                print("➡️ Row fallida:", row)
        print(f"📌 Hechos cargados en Prolog: {total}")

    
    def recomendar_cocteles(self, datos_usuario):
        try:
            consulta = (
                f"recomendar_cocteles({datos_usuario['edad']}, {datos_usuario['estrato']}, "
                f"'{datos_usuario['carrera'].lower()}', '{datos_usuario['genero'].lower()}', Lista)"
            )
            resultado = list(self.prolog.query(consulta))
            if resultado:
                lista_ids = resultado[0]['Lista']
                print("🔎 IDs recomendados:", lista_ids)
                return [id_ for id_ in lista_ids if isinstance(id_, int)]
            else:
                print("⚠️ Prolog no devolvió resultados.")
                return []
        except Exception as e:
            print(f"❌ Error al consultar Prolog: {e}")
            return []

    def mostrar_total_hechos(self):
        try:
            resultado = list(self.prolog.query("findall(_, calificacion(_,_,_,_,_,_), L), length(L, Total)."))
            print("📌 Hechos cargados en Prolog:", resultado[0]['Total'] if resultado else "Error")
        except Exception as e:
            print(f"❌ Error al contar hechos: {e}")

    def mostrar_todos_los_hechos(self, n=10):
        try:
            resultados = list(self.prolog.query("calificacion(E, Es, C, G, Id, Cal)"))
            for hecho in resultados[:n]:
                print(hecho)
            print(f"Total de hechos mostrados: {min(n, len(resultados))} de {len(resultados)}")
        except Exception as e:
            print(f"❌ Error al consultar hechos: {e}")






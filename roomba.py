import tkinter as tk

class Room:
    def __init__(self):
        self.zones = {}

    def agregar_zona(self, nombre, largo, ancho, color):
        self.zones[nombre] = {"largo": largo, "ancho": ancho, "color": color}

    def calcular_superficie_total(self):
        superficie_total = 0
        for zona, dimensiones in self.zones.items():
            superficie_total += dimensiones["largo"] * dimensiones["ancho"]
        return superficie_total


class VacuumRobot:
    def __init__(self, room):
        self.room = room

    def estimar_tiempo_limpieza(self, velocidad_m2_por_minuto):
        tiempos_por_zona = {}
        for zona, dimensiones in self.room.zones.items():
            area = dimensiones["largo"] * dimensiones["ancho"]
            tiempo = area / velocidad_m2_por_minuto
            tiempos_por_zona[zona] = tiempo
        return tiempos_por_zona


class VacuumRobotGUI:
    def __init__(self, master):
        self.master = master
        master.title("ASPIRACION ROOMBA")  # Título de la ventana
        self.room = Room()
        self.lienzo_frame = tk.Frame(master)
        self.lienzo_frame.pack(expand=True, fill=tk.BOTH)

        self.label_title = tk.Label(self.lienzo_frame, text="ASPIRACION ROOMBA", font=("Arial", 20, "bold"))
        self.label_title.pack()

        self.label_zona = tk.Label(self.lienzo_frame, text="Nombre de la zona:")
        self.label_zona.pack()
        self.entry_zona = tk.Entry(self.lienzo_frame)
        self.entry_zona.pack()

        self.label_largo = tk.Label(self.lienzo_frame, text="Largo (cm):")
        self.label_largo.pack()
        self.entry_largo = tk.Entry(self.lienzo_frame)
        self.entry_largo.pack()

        self.label_ancho = tk.Label(self.lienzo_frame, text="Ancho (cm):")
        self.label_ancho.pack()
        self.entry_ancho = tk.Entry(self.lienzo_frame)
        self.entry_ancho.pack()

        self.button_agregar = tk.Button(self.lienzo_frame, text="Agregar Zona", command=self.agregar_zona)
        self.button_agregar.pack()

        self.lienzo = tk.Canvas(self.lienzo_frame, bg="white")
        self.lienzo.pack(expand=True, fill=tk.BOTH)

        self.factor_escala_inicial = 0.7  # Factor de escala inicial para la primera zona
        self.escala = self.factor_escala_inicial
        self.pos_x = 20  # Ajustamos la posición inicial x para que comience más cerca del borde
        self.pos_y = 20  # Ajustamos la posición inicial y para que comience más cerca del borde

    def agregar_zona(self):
        nombre = self.entry_zona.get()
        largo = float(self.entry_largo.get().replace(",", ".")) / 100  # Convertir de cm a metros
        ancho = float(self.entry_ancho.get().replace(",", ".")) / 100  # Convertir de cm a metros
        color = self.obtener_color_zona()
        self.room.agregar_zona(nombre, largo, ancho, color)
        self.mostrar_zonas()

    def obtener_color_zona(self):
        # Colores suaves en tonalidad suave
        colores = ["#ADD8E6", "#FFA07A", "#FFC0CB", "#FFFF99", "#B0E0E6"]
        indice_color = len(self.room.zones) % len(colores)
        return colores[indice_color]

    def mostrar_zonas(self):
        self.lienzo.delete("all")

        lienzo_width = self.lienzo.winfo_width()
        lienzo_height = self.lienzo.winfo_height()

        max_ancho = max(self.room.zones.values(), key=lambda x: x["ancho"])["ancho"]
        max_largo = max(self.room.zones.values(), key=lambda x: x["largo"])["largo"]

        x_offset = 20
        y_offset = 20
        row_height = 0

        for nombre, dimensiones in self.room.zones.items():
            factor_escala_x = lienzo_width / max_largo
            factor_escala_y = lienzo_height / max_ancho
            factor_escala = min(factor_escala_x, factor_escala_y) * self.escala

            x1 = x_offset
            y1 = y_offset
            x2 = x1 + dimensiones["largo"] * factor_escala
            y2 = y1 + dimensiones["ancho"] * factor_escala

            if x2 > lienzo_width:  # Si la zona no cabe en la fila actual, empezamos una nueva fila
                x_offset = 20
                y_offset += row_height + 20  # 20 píxeles de espacio entre filas
                row_height = 0

                x1 = x_offset
                y1 = y_offset
                x2 = x1 + dimensiones["largo"] * factor_escala
                y2 = y1 + dimensiones["ancho"] * factor_escala

            color = dimensiones["color"]

            area = dimensiones["largo"] * dimensiones["ancho"]
            tiempo = VacuumRobot(self.room).estimar_tiempo_limpieza(1)  # Suponiendo velocidad de 1 m²/min

            self.lienzo.create_rectangle(x1, y1, x2, y2, fill=color)
            area_text = f"{nombre}\nÁrea: {area:.2f} m²\nTiempo: {tiempo[nombre]:.2f} minutos"  # Mostrar tiempo por zona
            self.lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=area_text, font=("Arial", 8, "bold"), justify="center")

            x_offset = x2 + 20  # 20 píxeles de espacio entre zonas
            row_height = max(row_height, y2 - y1)  # Actualizamos la altura de la fila

def main():
    root = tk.Tk()
    app = VacuumRobotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
















































































































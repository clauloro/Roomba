import tkinter as tk

class Room:
    def __init__(self):
        self.zones = {}

    def agregar_zona(self, nombre, largo, ancho, color):
        self.zones[nombre] = {"largo": largo, "ancho": ancho, "color": color}

    def calcular_superficie_total(self):
        superficie_total = 31.5  # Área total de la habitación en metros cuadrados
        for zona, dimensiones in self.zones.items():
            superficie_total -= dimensiones["largo"] * dimensiones["ancho"]
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

    def tiempo_total_limpieza(self, velocidad_m2_por_minuto):
        tiempo_total = sum(self.estimar_tiempo_limpieza(velocidad_m2_por_minuto).values())
        return tiempo_total

class VacuumRobotGUI:
    def __init__(self, master):
        self.master = master
        master.title("ASPIRACION ROOMBA")  
        self.room = Room()

        self.label_bg = "#F0F0F0" 
        self.entry_bg = "#FFFFFF"  
        self.button_bg = "#4CAF50"  
        self.button_fg = "#FFFFFF"  

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.label_title = tk.Label(self.main_frame, text="ASPIRACION ROOMBA", font=("Arial", 20, "bold"), bg=self.label_bg)
        self.label_title.pack(pady=(0, 20))

        self.label_zona = tk.Label(self.main_frame, text="Nombre de la zona:", bg=self.label_bg)
        self.label_zona.pack(anchor="w", padx=10, pady=5)
        self.entry_zona = tk.Entry(self.main_frame, bg=self.entry_bg, bd=2)  
        self.entry_zona.pack(fill=tk.X, padx=10, pady=5)

        self.label_largo = tk.Label(self.main_frame, text="Largo (cm):", bg=self.label_bg)
        self.label_largo.pack(anchor="w", padx=10, pady=5)
        self.entry_largo = tk.Entry(self.main_frame, bg=self.entry_bg, bd=2)  
        self.entry_largo.pack(fill=tk.X, padx=10, pady=5)

        self.label_ancho = tk.Label(self.main_frame, text="Ancho (cm):", bg=self.label_bg)
        self.label_ancho.pack(anchor="w", padx=10, pady=5)
        self.entry_ancho = tk.Entry(self.main_frame, bg=self.entry_bg, bd=2)  
        self.entry_ancho.pack(fill=tk.X, padx=10, pady=5)

        self.button_agregar = tk.Button(self.main_frame, text="Agregar Zona", bg=self.button_bg, fg=self.button_fg, command=self.agregar_zona, bd=2)  
        self.button_agregar.pack(pady=10)

        self.lienzo_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="groove")  
        self.lienzo_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.lienzo = tk.Canvas(self.lienzo_frame, bg="white")
        self.lienzo.pack(expand=True, fill=tk.BOTH)

        self.factor_escala_inicial = 0.5  
        self.escala = self.factor_escala_inicial

        self.button_listo = tk.Button(self.main_frame, text="Listo", bg=self.button_bg, fg=self.button_fg, command=self.calcular_mueble, bd=2)
        self.button_listo.pack(pady=10)

    def agregar_zona(self):
        nombre = self.entry_zona.get()
        largo = float(self.entry_largo.get().replace(",", ".")) / 100  
        ancho = float(self.entry_ancho.get().replace(",", ".")) / 100  
        color = self.obtener_color_zona()
        self.room.agregar_zona(nombre, largo, ancho, color)
        self.mostrar_zonas()

    def obtener_color_zona(self):
        colores = ["#ADD8E6", "#FFA07A", "#FFC0CB", "#FFFF99", "#B0E0E6"]
        indice_color = len(self.room.zones) % len(colores)
        return colores[indice_color]

    def mostrar_zonas(self):
        self.lienzo.delete("all")

        lienzo_width = self.lienzo_frame.winfo_width()  
        lienzo_height = self.lienzo_frame.winfo_height() 

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

            if x2 > lienzo_width:  
                x_offset = 20
                y_offset += row_height + 20 
                row_height = 0

                x1 = x_offset
                y1 = y_offset
                x2 = x1 + dimensiones["largo"] * factor_escala
                y2 = y1 + dimensiones["ancho"] * factor_escala

            color = dimensiones["color"]

            area = dimensiones["largo"] * dimensiones["ancho"]
            tiempo = VacuumRobot(self.room).estimar_tiempo_limpieza(1)  

            self.lienzo.create_rectangle(x1, y1, x2, y2, fill=color)
            area_text = f"{nombre}\nÁrea: {area:.2f} m²\nTiempo: {tiempo[nombre]:.2f} minutos"  
            self.lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=area_text, font=("Arial", 8, "bold"), justify="center")

            x_offset = x2 + 20  
            row_height = max(row_height, y2 - y1)  

    def calcular_mueble(self):
        # Calcular y mostrar el área restante (mueble)
        area_restante = self.room.calcular_superficie_total()
        if area_restante > 0:
            lienzo_width = self.lienzo_frame.winfo_width()
            lienzo_height = self.lienzo_frame.winfo_height()

            x1 = lienzo_width * 0.7
            y1 = lienzo_height * 0.7
            x2 = lienzo_width * 0.9
            y2 = lienzo_height * 0.9

            self.lienzo.create_rectangle(x1, y1, x2, y2, fill="gray")
            mueble_text = f"Mueble\nÁrea: {area_restante:.2f} m²"
            self.lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=mueble_text, font=("Arial", 8, "bold"), justify="center")

            self.lienzo.config(scrollregion=self.lienzo.bbox("all"))

            # Calcular el área total de limpieza sin contar el área del mueble
            area_limpieza_total = sum(dimensiones["largo"] * dimensiones["ancho"] for dimensiones in self.room.zones.values())
            area_limpieza_sin_mueble = area_limpieza_total - area_restante

            # Mostrar el área total de limpieza
            total_text = f"Área Total de Limpieza: {area_limpieza_sin_mueble:.2f} m²"
            self.lienzo.create_text(lienzo_width / 2, lienzo_height * 0.95, text=total_text, font=("Arial", 10, "bold"), justify="center")

            # Calcular el tiempo total de limpieza sin contar el área del mueble
            velocidad_m2_por_minuto = 1  # Velocidad de limpieza en metros cuadrados por minuto
            tiempo_total_sin_mueble = VacuumRobot(self.room).tiempo_total_limpieza(velocidad_m2_por_minuto)

            # Mostrar el tiempo total de limpieza sin el área del mueble
            tiempo_text = f"Tiempo Total de Limpieza: {tiempo_total_sin_mueble:.2f} minutos"
            self.lienzo.create_text(lienzo_width / 2, lienzo_height * 0.97, text=tiempo_text, font=("Arial", 10, "bold"), justify="center")


def main():
    root = tk.Tk()
    app = VacuumRobotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()





























































































































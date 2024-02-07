import tkinter as tk
import random

class Room:
    def __init__(self):
        self.zones = {}

    def agregar_zona(self, nombre, largo, ancho):
        self.zones[nombre] = {"largo": largo, "ancho": ancho, "obstaculos": []}

    def agregar_obstaculo(self, zona, x, y):
        self.zones[zona]["obstaculos"].append((x, y))

    def calcular_superficie_total(self):
        superficie_total = 0
        for zona, dimensiones in self.zones.items():
            superficie_total += dimensiones["largo"] * dimensiones["ancho"]
        return superficie_total


class VacuumRobot:
    def __init__(self, room):
        self.room = room

    def estimar_tiempo_limpieza(self, velocidad_m2_por_minuto):
        superficie_total = self.room.calcular_superficie_total()
        tiempo_limpieza_minutos = superficie_total / velocidad_m2_por_minuto
        return tiempo_limpieza_minutos


class VacuumRobotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Robot Aspirador")

        self.room = Room()

        self.label_zona = tk.Label(master, text="Nombre de la zona:")
        self.label_zona.grid(row=0, column=0)
        self.entry_zona = tk.Entry(master)
        self.entry_zona.grid(row=0, column=1)

        self.label_largo = tk.Label(master, text="Largo (metros):")
        self.label_largo.grid(row=1, column=0)
        self.entry_largo = tk.Entry(master)
        self.entry_largo.grid(row=1, column=1)

        self.label_ancho = tk.Label(master, text="Ancho (metros):")
        self.label_ancho.grid(row=2, column=0)
        self.entry_ancho = tk.Entry(master)
        self.entry_ancho.grid(row=2, column=1)

        self.button_agregar = tk.Button(master, text="Agregar Zona", command=self.agregar_zona)
        self.button_agregar.grid(row=3, columnspan=2)

        self.lienzo = tk.Canvas(master, width=400, height=400)
        self.lienzo.grid(row=4, columnspan=2)

    def agregar_zona(self):
        nombre = self.entry_zona.get()
        largo = float(self.entry_largo.get().replace(",", "."))
        ancho = float(self.entry_ancho.get().replace(",", "."))
        self.room.agregar_zona(nombre, largo, ancho)
        self.agregar_obstaculos_aleatorios(nombre)
        self.mostrar_zonas()

    def agregar_obstaculos_aleatorios(self, zona):
        largo = int(self.room.zones[zona]["largo"] * 20)
        ancho = int(self.room.zones[zona]["ancho"] * 20)
        for _ in range(random.randint(0, 5)):
            x = random.randint(0, largo)
            y = random.randint(0, ancho)
            self.room.agregar_obstaculo(zona, x, y)

    def mostrar_zonas(self):
        self.lienzo.delete("all")

        max_largo = max(self.room.zones.values(), key=lambda x: x["largo"])["largo"]
        max_ancho = max(self.room.zones.values(), key=lambda x: x["ancho"])["ancho"]
        escala_largo = 400 / max_largo
        escala_ancho = 400 / max_ancho

        for nombre, dimensiones in self.room.zones.items():
            x1 = 10
            y1 = 10
            x2 = 10 + dimensiones["largo"] * escala_largo
            y2 = 10 + dimensiones["ancho"] * escala_ancho
            area = dimensiones["largo"] * dimensiones["ancho"]
            tiempo = VacuumRobot(self.room).estimar_tiempo_limpieza(1)  # Suponiendo velocidad de 1 m²/min
            self.lienzo.create_rectangle(x1, y1, x2, y2, fill="lightblue")
            self.lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{nombre}\nÁrea: {area:.2f} m²\nTiempo: {tiempo:.2f} minutos", font=("Arial", 8, "bold"), justify="center")

            # Mostrar obstáculos
            for obstaculo in dimensiones["obstaculos"]:
                self.lienzo.create_rectangle(x1 + obstaculo[0] * escala_largo, y1 + obstaculo[1] * escala_ancho,
                                             x1 + obstaculo[0] * escala_largo + 5, y1 + obstaculo[1] * escala_ancho + 5, fill="red")


def main():
    root = tk.Tk()
    app = VacuumRobotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()



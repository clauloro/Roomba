import tkinter as tk


class Room:
    def __init__(self):
        self.zones = {}

    def agregar_zona(self, nombre, largo, ancho):
        self.zones[nombre] = {"largo": largo, "ancho": ancho}

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

        self.room = Room()

    def agregar_zona(self):
        nombre = self.entry_zona.get()
        largo = float(self.entry_largo.get())
        ancho = float(self.entry_ancho.get())
        self.room.agregar_zona(nombre, largo, ancho)
        self.entry_zona.delete(0, tk.END)
        self.entry_largo.delete(0, tk.END)
        self.entry_ancho.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = VacuumRobotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


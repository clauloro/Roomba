import tkinter as tk

class Room:
    def __init__(self):
        self.zones = {
            "Zona 1": {"largo": 5.00, "ancho": 1.50},
            "Zona 2": {"largo": 4.80, "ancho": 1.01},
            "Zona 3": {"largo": 3.09, "ancho": 4.80},
            "Zona 4": {"largo": 0.90, "ancho": 2.20}
        }

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


# Interfaz gráfica de usuario 
class VacuumRobotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Robot Aspirador")

        self.label_superficie = tk.Label(master, text="Superficie total a limpiar:")
        self.label_superficie.pack()

        self.label_tiempo = tk.Label(master, text="Tiempo estimado de limpieza:")
        self.label_tiempo.pack()

        self.calcular_resultados()

    def calcular_resultados(self):
        room = Room()
        robot = VacuumRobot(room)
        velocidad_m2_por_minuto = 2
        tiempo_limpieza_minutos = robot.estimar_tiempo_limpieza(velocidad_m2_por_minuto)

        self.label_superficie.config(text=f"Superficie total a limpiar: {room.calcular_superficie_total()} m^2")
        self.label_tiempo.config(text=f"Tiempo estimado de limpieza: {tiempo_limpieza_minutos} minutos")


def main():
    root = tk.Tk()
    app = VacuumRobotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


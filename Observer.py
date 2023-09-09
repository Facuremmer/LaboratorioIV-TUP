import sys

#Clase que creo para que represente un objeto observable
class WeatherAlert:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

class WeatherObserver:
    def update(self, message):
        pass

#Clase que represneta una aplicacion. Hereda de WeatherObserver
class MobileApp(WeatherObserver):
    def __init__(self, name):
        self._name = name

    def update(self, message):
        print(f"{self._name} Nueva notificación de clima 2.0: {message}")

#Clase que representa la estacion meteorologica.
class WeatherStation:
    def __init__(self):
        self._weather_alert = WeatherAlert()
        self._current_weather = "Hoy estará soleado"

    def simulate_weather_change(self):
        if self._current_weather == "Hoy estará soleado":
            self._current_weather = "Hoy estará nublado"
        else:
            self._current_weather = "Hoy estará soleado"
        self._weather_alert.notify_observers(f"{self._current_weather}")


if __name__ == "__main__":
    weather_station = WeatherStation()

    mobile_app_1 = MobileApp("Usuario 1 -")
    mobile_app_2 = MobileApp("Usuario 2 -")

    weather_station._weather_alert.add_observer(mobile_app_1)
    weather_station._weather_alert.add_observer(mobile_app_2)

    print("\nSeleccione una opción:")
    print("1. Simular notificación")
    print("2. Salir")

    while True:
        option = input()

        if option == "1":
            weather_station.simulate_weather_change()
        elif option == "2":
            sys.exit(0)
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")




































import time
import threading
from abc import ABC, abstractmethod
import pyodbc
import keyboard 

# Clase Singleton para la conexión a la base de datos
class SingletonMeta(type):
    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            instancia = super().__call__(*args, **kwargs)
            cls._instancias[cls] = instancia
        return cls._instancias[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    _connection = None

    def __init__(self):
        self.connect()

    def connect(self):
        if self._connection is None:
            try:
                connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-OMAF4KB\\SQLEXPRESS;DATABASE=Tienda;UID=DESKTOP-OMAF4KB\\facun;Trusted_Connection=yes"
                self._connection = pyodbc.connect(connection_string)
                print("Conexión exitosa a la base de datos.")
            except Exception as e:
                print("Error de conexión a la base de datos:", str(e))

    def execute_query(self, query):
        if self._connection is not None:
            cursor = self._connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        else:
            print("No se puede ejecutar la consulta. La conexión a la base de datos no está establecida.")

# Clase Observador que responde a los cambios en la tabla "Persona"
class Observador(ABC):
    @abstractmethod
    def actualizar(self) -> None:
        pass

# Clase Sujeto que representa la tabla "Persona" en la base de datos
class PersonaDatabase(ABC):
    @abstractmethod
    def adjuntar(self, observador: Observador) -> None:
        pass

    @abstractmethod
    def desvincular(self, observador: Observador) -> None:
        pass

    @abstractmethod
    def notificar(self) -> None:
        pass

    @abstractmethod
    def obtener_personas(self) -> list:
        pass

class PersonaDatabaseConcreta(PersonaDatabase):
    def __init__(self, connection):
        self._observadores = []
        self._connection = connection

    def adjuntar(self, observador: Observador) -> None:
        # Agrega un observador a la lista de observadores
        self._observadores.append(observador)

    def desvincular(self, observador: Observador) -> None:
        # Elimina un observador de la lista de observadores
        self._observadores.remove(observador)

    def notificar(self) -> None:
        # Notifica a todos los observadores cuando hay cambios en los datos
        for observador in self._observadores:
            observador.actualizar()

    def obtener_personas(self) -> list:
        # Obtiene datos de la tabla "Persona" desde la base de datos
        query = "SELECT * FROM Persona"
        cursor = self._connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

# Implementación del Observador
class CambioPersonaObserver(Observador):
    def __init__(self, persona_db):
        self._persona_db = persona_db

    def actualizar(self) -> None:
        # Actualiza y mostra los datos cuando se notifican cambios
        personas = self._persona_db.obtener_personas()
        print("Notificación: Cambios en la tabla Persona")
        for persona in personas:
            print(persona)

def monitorear_cambios(persona_db):
    ultima_actualizacion = None

    while True:
        personas = persona_db.obtener_personas()
        actualizacion_actual = hash(str(personas))

        if ultima_actualizacion is None:
            ultima_actualizacion = actualizacion_actual
        elif actualizacion_actual != ultima_actualizacion:
            # Comprobar si ha habido cambios en los datos y notifica si es así
            print("Notificación: Cambios en la tabla Persona")
            for persona in personas:
                print(persona)
            ultima_actualizacion = actualizacion_actual

        time.sleep(5)  # Espera 5 segundos antes de volver a verificar

if __name__ == "__main__":
    db_connection = DatabaseConnection()

    if db_connection._connection:
        persona_db = PersonaDatabaseConcreta(db_connection._connection)
        cambio_persona_observer = CambioPersonaObserver(persona_db)

        persona_db.adjuntar(cambio_persona_observer)

        # Inicia el monitoreo de cambios en segundo plano
        monitor_thread = threading.Thread(target=monitorear_cambios, args=(persona_db,))
        monitor_thread.daemon = True
        monitor_thread.start()

        # "Esc" para finalizar
        try:
            keyboard.wait("esc") 
            print("Programa finalizado.")
        except KeyboardInterrupt:
            pass
    else:
        print("La conexión a la base de datos falló.")


#Meta clas epara garantizar que solo haya una conoxion a la base de datos.
class SingletonMeta(type):
    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            instancia = super().__call__(*args, **kwargs)
            cls._instancias[cls] = instancia
        return cls._instancias[cls]

#Conexion a la base
class DatabaseConnection(metaclass=SingletonMeta):
    _connection = None

    def __init__(self):
        self.connect()

    def connect(self):
        if self._connection is None:
            try:
                import pyodbc
                connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-OMAF4KB\\SQLEXPRESS;DATABASE=Tienda;UID=DESKTOP-OMAF4KB\facun;Trusted_Connection=yes"
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

if __name__ == "__main__":

    db_connection = DatabaseConnection()

    if db_connection._connection:  
        query = "SELECT * FROM Persona"

        # Ejecuta consulta y mostra los resultados si la conexión es exitosa
        result = db_connection.execute_query(query)

        if result:
            print("Datos de la tabla Persona:")
            for row in result:
                print(row)
        else:
            print("No se encontraron datos en la tabla Persona.")
    else:
        print("La conexión a la base de datos falló.")





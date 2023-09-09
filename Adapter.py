# Clase abstracta donde defino la interfaz del objetivo que el adaptador debe cumplir.
class Target:
    def request(self) -> str:
        return

# Clase donde represento el objeto a adaptar. Trabaja con ASCII.
class Adaptee:
    def specific_request(self, ascii_text: str) -> str:
        return ascii_text

# Clase donde implemento el adaptador, convirtiendo el formato ASCII en texto legible.
class TextToAsciiAdapter(Target):
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee

    def request(self) -> str:
        ascii_text = self.adaptee.specific_request(input("Ingrese un valor de texto en formato ASCII: "))
        ascii_values = ascii_text.split()
        text = ''.join(chr(int(value)) for value in ascii_values)
        return f"Texto convertido por el adaptador: {text}"

# Función que simula ser el cliente, utilizando el adaptador para convertir ASCII a texto.
def client_code(target: "Target") -> None:
    print(target.request(), end="")

if __name__ == "__main__":
    target = Target() 
    adaptee = Adaptee() 
    adapter = TextToAsciiAdapter(adaptee)  

    client_code(adapter)  # Utilizo el adaptador para convertir y mostrar el texto.







  


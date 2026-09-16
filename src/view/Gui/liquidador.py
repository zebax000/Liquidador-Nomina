""""necesito hacer una gui para esta aplicacion de liquidar nomina en kivy con manejo de
excepciones que cada label pida lo que se necesite ya sea tasa valor e interes, y un boton de calcular al lado de un label para mostrar el resultado, ademas
un popup cuando un usuario falle en algo en una funcion mostrar error, que lo consiga con
try catch Exeption as error y lamar la funcion con error, ordenada, y legible para el usuario, buscando uenas practicas
en el codigo y legibilidad, usando en las exepciones la forma que paso donde y como solucionarlo
debe poder calcular lo que menciona la aplicacion, en este caso unicamente valor neto a pagar que es: def calcular_neto_pagar(total_devengado: float , total_deducciones: float)-> float:
    return total_devengado - total_deducciones, esto en kivy, te adjunto un codigo de ejemplo(guia) solo para guiarte, no tiene que ver con el proyecto actual."""
from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

import sys

sys.path.append("src")

# Logica de la tarjeta de credito
from model.Payments import CreditCardCalculator


class PaymentApp(App):
    def build(self):
        contenedor = GridLayout(cols=2, padding=20, spacing=20)

        contenedor.add_widget(Label(text="Valor de la compra"))
        self.compra = TextInput(font_size=30)
        contenedor.add_widget(self.compra)

        contenedor.add_widget(Label(text="Número de cuotas"))
        self.cuotas = TextInput(font_size=30)
        contenedor.add_widget(self.cuotas)

        contenedor.add_widget(Label(text="Tasa de Interés"))
        self.tasa = TextInput(font_size=30)
        contenedor.add_widget(self.tasa)

        self.resultado = Label()
        contenedor.add_widget(self.resultado)

        calcular = Button(text="Calcular", font_size=40)
        contenedor.add_widget(calcular)

        # Conectar con el callback con el evento press del boton
        calcular.bind(on_press=self.calcular_cuota)

        # Siempre se retorna el widget que contiene a todos los demás
        return contenedor

    # instance es el widget que generó el evento
    # value es el valor actual que tiene el widget
    def calcular_cuota(self, value):
        try:
            self.validar()
            cuota = CreditCardCalculator.calc_payment(amount=float(self.compra.text),
                                                      number_of_payments=int(self.cuotas.text),
                                                      interest=float(self.tasa.text))
            self.resultado.text = str(round(cuota, 2))

        except ValueError as err:
            self.resultado.text = "El valor ingresado no es un numero válido. Ingrese un numero correcto, por ejemplo 500000.00"
        except Exception as err:
            self.mostrar_error(err)

    def mostrar_error(self, err):
        """
        Abre una ventana emergente, con un texto y un botón para cerrar
        Parámetros:
        err: Mensaje de error que queremos mostrar en la ventana
        """

        # contenido es el contenedor donde vamos a agregar los widgets de la ventana
        contenido = GridLayout(cols=1)
        # Creamos el Label que contiene el mensaje de error
        contenido.add_widget(Label(text=str(err)))
        # Creamos el botón para cerrar la ventana
        cerrar = Button(text="Cerrar")
        contenido.add_widget(cerrar)
        # Creamos la ventana emergente con el widget Popup de Kivy
        popup = Popup(title="Error", content=contenido)
        # Conectamos el evento del botón con el método dismiss que cierra el popup
        cerrar.bind(on_press=popup.dismiss)
        # Mostramos la ventana emergente
        popup.open()

    def validar(self):
        """
        Verifica que todos datos ingresados por el usuario sean correctos
        """
        if (not (self.compra.text.isnumeric())):
            raise Exception("El Valor de la compra debe ser un número válido")

        if (not (self.cuotas.text.isnumeric())):
            raise Exception("El Número de Cuotas debe ser un número válido")

        if (not (self.tasa.text.isnumeric())):
            raise Exception("La tasa de interés debe ser un número válido, sin signo de porcentaje")


if __name__ == "__main__":
    PaymentApp().run()
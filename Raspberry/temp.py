import Adafruit_DHT
import json
import datetime

class Temperatura:
    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12
        self._sensor = sensor
        self._data_pin = pin
    def datos_sensor(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, self._data_pin)
        return {'Temperatura': temperatura, 'Humedad': humedad, 'Fecha': datetime.datetime.now().strftime("%c")}

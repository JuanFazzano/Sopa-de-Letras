import RPi.GPIO as GPIO
import time

class Sonido:
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)

    def evento_detectado(self, funcion):
        if GPIO.event_detected(self._canal):
            return True
        else:
            return False
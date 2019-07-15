import PySimpleGUI as sg
from Raspberry.sound import Sonido
from Raspberry.matriz import Matriz
from Raspberry.temp  import Temperatura

def main():
    sonido = Sonido()
    temp = Temperatura()
    matriz = Matriz()

    while True:
        if sonido.evento_detectado():
            tempe = temp.datos_sensor()
            mensaje = 'Temperatura' + str(tempe['Temperatura']) + 'Humedad ' + str(tempe['Humedad'])
            matriz.mostrar_mensaje(msg = mensaje)
            value = sg.PopupOKCancel('Quiere parar de tomar la temperatura?', title='Terminar')
            if value == 'OK':
                break

if __name__ == '__main__':
    main()


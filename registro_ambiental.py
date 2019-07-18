import time
import PySimpleGUI as sg
#from Raspberry.temp import Temperatura
import os.path
import json


def guardar_temp(temperatura):
	'''
	GUARDAR LA TEMPERATURA TOMADA EN UN ARCHIVO JSON
	'''
	with open('archivos/datos-oficinas.json','r+') as f:
		json.dump(temperatura, f, indent=4, sort_keys=True)

def cargar():
	'''
	CARGAR LOS DATOS DE LA TEMEPERATURA DESDE UN ARCHIVO JSON EN CASO DE QUE HAYAN TALES DATOS.
	'''
	if os.path.getsize(os.path.join(os.getcwd(),'archivos','datos-oficinas.json')) != 0:
		with open('archivos/datos-oficinas.json','r') as f:
			return json.load(f)
	else:
		return dict()

def leer_oficina():
	'''
	SE LEE LA OFICINA DONDE SE TOMA LA TEMPERATURA
    '''
	layout = [
			[sg.Text('Ingrese la oficina de la que se tomará la temperatura.')],
			[sg.In('')],
			[sg.Submit('Tomar Temperatura',key='tomar')]
			]

	window = sg.Window('Oficina').Layout(layout)
	while True:
		event, buttons= window.Read()
		if event == 'tomar' and buttons[0] != '':
			oficina = buttons[0]
			window.Close()
			break
		sg.Popup('Ingrese una oficina válida.')

	return oficina
def tomar_temperatura(oficina):
	'''
	TOMAR LA TEMPERATURA DE LA OFICINA EN LA QUE ESTA LA RASPBERRY.
	'''
	#temp = Temperatura()
	dic = cargar()
	if oficina not in dic.keys():
		dic[oficina] = list()
	while True:
		tempe = temp.datos_sensor()
		dic[oficina].append(temp.datos_sensor())
		guardar_temp(dic)
		time.sleep(60)
		value = sg.PopupOKCancel('Quiere parar de tomar la temperatura?', title='Terminar')
		if value == 'OK':
			break

def main():
	oficina = leer_oficina()
	tomar_temperatura(oficina)

if __name__ == '__main__':
	main()

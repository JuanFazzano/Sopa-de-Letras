'''
Fazzano, Juan Manuel
Baudino Zoya, Fermín
Comba, Sebastian


Menu del manejo de palabras, se podrán agregar y eliminar palabras, y acceder a las opciones del juego
'''



# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from Juego import opcionesJuego, verificarPalabra
import csv


def verificar_cantidad(button,file):
    '''
    VERIFICAR QUE EL USUARIO HAYA INGRESADO CORRECTAMENTE LA CANTIDAD DE PALABRAS A USAR EN LA SOPA
    '''
    vb,jj,nn = 0,0,0
    with open(file, 'r', encoding='utf-8') as CSVfile:
        reader = csv.reader(CSVfile)
        next(reader)
        for line in reader:
            if line[1] == 'VB': vb+=1
            elif line[1] == 'JJ': jj+=1
            elif line[1] == 'NN': nn+=1
    if button['__cantVB__'] > vb: button['__cantVB__'] = vb #elegir_azar(vb,'__cantVB__',button)
    elif button['__cantNN__'] > nn: button['__cantNN__'] = nn #elegir_azar(nn,'__cantNN__',button)
    elif button['__cantJJ__'] > nn: button['__cantJJ__'] = jj#elegir_azar(jj,'__cantJJ__',button)

    if button['__cantVB__'] + button['__cantNN__'] + button['__cantJJ__'] == 0:
        maximo = max(vb,jj,nn)
        if maximo == vb: tipo = '__cantVB__'
        elif maximo == nn: tipo = '__cantNN__'
        elif maximo == jj: tipo = '__cantJJ__'

        elegir_azar(maximo,tipo,button)
def elegir_azar(maximo,tipo,button):
    from random import randint
    sg.Popup('Eligió una cantidad inválida de palabras, se configurará automaticamente una cantidad válida por usted.')
    if maximo > 6: maximo =6
    button[tipo] += randint(1, maximo+1)

def verificacion():
    '''
    CREACION DE LOS ARCHIVOS QUE SE VAN A UTILIZAR PARA EL JUEGO
    '''

    verificarPalabra.verificar_archivos(file_palabras, 'Palabra', 'Tipo', 'Definicion')
    verificarPalabra.verificar_archivos(file_reporte)

def eliminarPalabra(file,palabra):
    '''
    ELIMINAR LA PALABRA QUE ELIJA EL JUGADOR DEL ARCHIVO
    '''

    with open(file, "r",encoding='utf-8') as f:
        lineas = f.readlines()
    with open(file, "w",encoding='utf-8') as f:
        for linea in lineas:
            if linea.split(',')[0] != palabra:
                f.write(linea)
            else:
                f.truncate()

def validar(palabra):
    '''
    VALIDA LAS PALABRAS INGRESADAS POR EL USUARIO
    UNA PALABRA ES VALIDA ES CONSIDERADA UNA PALABRA SIN SIMBOLOS
    '''

    for i in palabra:
        if not i.isalpha():
            return False
    return True

def tomarPalabras(file):
    '''
    DEVUELVE UNA LISTA CON TODAS LAS PALABRAS
    '''

    with open(file, 'r',encoding='utf-8') as CSVfile:
        lista = []
        reader = csv.reader(CSVfile)
        next(reader)
        for line in reader:
            lista.append(line[0])
    return lista

def eliminarTodo(file):
    '''
    ELIMINA TODAS LAS PALABRAS DEL ARCHIVO DE PALABRAS
    '''

    headers = [['Palabra','Tipo','Definicion']]
    with open(file, 'w',newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(headers)


def elegir_oficina():
    '''
    DEVUELVE UN STRING CON EL "LookAndFeel"  QUE SE VA A USAR
    '''
    from Raspberry.registro_ambiental import cargar
    lookAndFeel = 'SystemDefault'
    dic = cargar()
    if len(list(dic.values())) > 0:
        layout = [
                [sg.T('Seleccione una de las oficinas de la lista.')],
                [sg.InputCombo(list(dic.keys()), size=(20, 10), key='ofi')],
                [sg.CloseButton('Seleccionar')]
                 ]
        window = sg.Window('Elegir Oficina').Layout(layout)
        event, buttons = window.Read()
        if event == 'Seleccionar':
            oficina = buttons['ofi']
            tempe = dic[oficina][-1]
            temperatura = tempe['Temperatura']
            if temperatura <= 10:
                lookAndFeel = 'TealMono'
            elif temperatura > 10 and temperatura <= 30:
                lookAndFeel = 'DarkBlue'
            else:
                lookAndFeel = 'Reddit'

    return lookAndFeel

# MAIN
sg.ChangeLookAndFeel(elegir_oficina())
lay_imagen = [[sg.Image('archivos/sopa_img.png')],
              [sg.CloseButton('Jugar')]]
window = sg.Window('Sopa de Letras').Layout(lay_imagen)
window.Read()

sg.SetOptions(element_padding=(10,10),background_color='#C0C0C0',element_background_color='#C0C0C0')

file_palabras = 'archivos/palabras.csv'
file_reporte = 'archivos/reporte.txt'
palabras = tomarPalabras(file_palabras)

f_palabras = [
            [sg.T('Verbos'), sg.T('Adjetivos',pad=(100,10)), sg.T('Sustantivos',pad=(20,10))],
            [sg.Slider(range=(0, 5),orientation='h',size=(15, 20),key='__cantVB__'),
             sg.Slider(range=(0, 5),orientation='h',size=(15, 20),key='__cantJJ__'),
             sg.Slider(range=(0, 5),orientation='h',size=(15, 20),key='__cantNN__')]
            ]

f_list = [[sg.Listbox(palabras,select_mode=True,size=(30,6),key='listado')]]

f_lectura = [
            [sg.Input('',size=(20,3),do_not_clear=False)],
            [sg.Button('Agregar palabra',key='add'),sg.Button('Eliminar palabra',key='del'),sg.Button('Eliminar todo',key= 'del_all')]
            ]

layout= [
            [sg.Frame('Ingrese una palabra',f_lectura),sg.Frame('Palabras Guardadas',f_list)],
            [sg.Frame('Cantidad de palabras a Mostrar',f_palabras)],
            [sg.Button('Continuar'), sg.Exit('Salir')]
        ]
window = sg.Window('Configuración de palabras').Layout(layout)

while True:
    event, button = window.Read()
    pal = button[0]
    if event == None or event == 'Salir':
        exit()
    elif event == 'Continuar':
        if not len(palabras) < 1:
            verificar_cantidad(button,file_palabras)
            break
        sg.Popup('No hay palabras cargadas en el archivo, por favor ingrese al menos una',title='ADVERTENCIA',)
    elif event == 'del_all':
        event = sg.PopupOKCancel('Esta seguro de que quiere elimar todas las palabras', title='Advertencia',
                                 background_color='#C0C0C0')
        if event == 'OK':
            eliminarTodo(file_palabras)
            palabras.clear()
            window.FindElement('listado').Update(values=palabras)
    elif validar(pal):
        if pal != '':
            if event == 'add':
                verificarPalabra.main(pal.lower())
            elif event == 'del':
                if pal in palabras:
                    eliminarPalabra(file_palabras,pal.lower())
                else:
                    sg.Popup('La palabra ingresada no existe en la lista de palabras')
            # ACTUALIZAR LISTADO DE PALABRAS
            palabras = tomarPalabras(file_palabras)
            window.FindElement('listado').Update(values=palabras)
        else:
            sg.Popup('No se ingreso una palabra')
    else:
        sg.Popup('Ingrese una palabra valida')

window.Close()
opcionesJuego.main(button['__cantVB__'], button['__cantNN__'], button['__cantJJ__'])

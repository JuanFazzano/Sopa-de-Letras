'''
Fazzano, Juan Manuel
Baudino Zoya, Fermín
Comba, Sebastian


Menu del manejo de palabras, se podrán agregar y eliminar palabras, y acceder a las opciones del juego
'''



# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import verificarPalabra, opcionesJuego
import csv


def verificacion():
    '''
    CREACION DE LOS ARCHIVOS QUE SE VAN A UTILIZAR PARA EL JUEGO
    '''

    verificarPalabra.verificar_archivos(file_palabras,'Palabra','Tipo','Definicion')
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

# MAIN
lay_imagen = [[sg.Image('archivos/sopa_img.png')],
              [sg.CloseButton('Jugar')]]
window = sg.Window('Sopa de Letras').Layout(lay_imagen)
window.Read()

sg.SetOptions(element_padding=(10,10),background_color='#C0C0C0',element_background_color='#C0C0C0')

file_palabras = 'archivos/palabras.csv'
file_reporte = 'archivos/reporte.txt'
palabras = tomarPalabras(file_palabras)

f_list = [[sg.Listbox(palabras,select_mode=True,size=(30,6),key='listado')]]
f_lectura = [
            [sg.Input('',size=(20,3),do_not_clear=False)],
            [sg.Button('Agregar palabra',key='add'),sg.Button('Eliminar palabra',key='del'),sg.Button('Eliminar todo',key= 'del_all')]
            ]

layout= [
            [sg.Frame('Palabras Guardadas',f_list)],
            [sg.Frame('Ingrese una palabra',f_lectura)],
            [sg.Button('Continuar'), sg.Exit('Salir')]
        ]
window = sg.Window('Configuración de palabras').Layout(layout)

while True:
    event, button = window.Read()
    pal = button[0]
    if event == None or event == 'Salir':
        exit()
    elif event == 'Continuar':
        break
    elif event == 'del_all':
        event = sg.PopupOKCancel('Esta seguro de que quiere elimar todas las palabras',title='Advertencia',background_color='#C0C0C0')
        if event == 'OK':
            eliminarTodo(file_palabras)
            window.FindElement('listado').Update(values=[])
    elif validar(pal):
        if pal != '':
            if event == 'add':
                verificarPalabra.main(pal)
            elif event == 'del':
                if pal in palabras:
                    eliminarPalabra(file_palabras,pal)
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
opcionesJuego.main()

'''
Fazzano, Juan Manuel
Baudino Zoya, Fermín
Comba, Sebastian


Manejo de las opciones a tener en la sopa de letras
'''

# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import csv
from Juego import sopaDeLetras


def listadoPalabras (file,cantVB,cantNN,cantJJ):
    '''
    RETORNA UN DICCIONARIO CON LA INFORMACION DE LAS PALABRAS
    palabra : [tipo, definicion]
    '''
    with open(file,encoding='utf-8') as CSV:
        csvReader = csv.DictReader(CSV)
        vecCont = [0,0,0] # VB, NN, JJ
        dic = {}
        for fila in csvReader:
            if fila['Tipo'] == 'VB':
                if vecCont[0] < cantVB:
                    dic[fila['Palabra']] = [fila['Tipo'],fila['Definicion']]
                    vecCont[0] +=1

            elif fila['Tipo'] == 'NN':
                if vecCont[1] < cantNN:
                    dic[fila['Palabra']] = [fila['Tipo'],fila['Definicion']]
                    vecCont[1] +=1

            elif fila['Tipo'] == 'JJ':
                if vecCont[2] < cantJJ:
                    dic[fila['Palabra']] = [fila['Tipo'],fila['Definicion']]
                    vecCont[2] +=1

        return dic

def main(cantVB,cantNN,cantJJ):
    sg.SetOptions(element_padding=(10,10),background_color='#C0C0C0',element_background_color='#C0C0C0')

    file_palabras = 'archivos/palabras.csv'

    f_colores = [
            [sg.ColorChooserButton('Verbos',key='__cVB__',size=(10,3), button_color=None),
             sg.ColorChooserButton('Sustantivos',key='__cNN__',size=(10,3), button_color=None),
             sg.ColorChooserButton('Adjetivos',key='__cJJ__',size=(10,3), button_color=None)]
            ]

    f_orientacion = [[sg.Combo(['horizontal','vertical'],key='__ORIENTACION__',readonly=True)]]

    tipografias = ['Helvetica', 'Times', 'Arial', 'Georgia', 'Verdana','Tahoma', 'Times New Roman','Trebuchet', 'Courier', 'Comic','Fixedsys']
    f_tipografia = [[sg.T('Titulo'),sg.Combo(tipografias,key='TIPOGRAFIA_TIT',readonly=True)],
                    [sg.T('Texto'),sg.Combo(tipografias,key='TIPOGRAFIA_TEX',readonly=True)]]

    f_grafia = [[sg.Combo(['minusculas','MAYUSCULAS'],key='__CAPITALIZACION__',readonly=True,size=(20,3))]]

    layout= [
                [sg.Frame('Seleccionar color para los tipos de palabra',f_colores),
                 sg.Frame('Elegir orientacion para jugar',f_orientacion)],
                [sg.Frame('Seleccione la tipografia a usar en el reporte',f_tipografia),
                 sg.Frame('Seleccion de Grafía a usar',f_grafia,size=(100,3))],
                [sg.Checkbox('Mostrar Ayuda',key='ayuda')],
                [sg.Submit('Empezar a Jugar'), sg.Exit('Salir')]
            ]


    window = sg.Window('Menu de Juego').Layout(layout)
    event, buttons = window.Read()

    if event == 'Salir':
        exit()
    elif event == 'Empezar a Jugar':
        dic = listadoPalabras(file_palabras,cantVB, cantNN, cantJJ)

        window.Close()
        sopaDeLetras.main(dic, buttons)


if __name__ == '__main__':
    import sys
    sys.exit(main(1,1,1))

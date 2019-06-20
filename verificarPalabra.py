# -*- coding: utf-8 -*-
from pattern.text.es import tag, parse
from pattern.web import Wiktionary, SEARCH
from pattern.web import URLTimeout, URLError
import csv
import PySimpleGUI as sg
from bs4 import BeautifulSoup

def creacion(file,*fieldnames):
    l = []
    f = open(file,'w',encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(fieldnames)

    f.close()

def verificar_archivos(file,*fieldnames):
    import os
    if not os.path.exists(file):
        creacion(file, *fieldnames)

def limpiar(source):
    for i in source('ul'):
        i.decompose()
    for i in source('sup'):
        i.decompose()
    return source

def tipoPal(articulo):
    for i in articulo.sections:         # Itera por cada objeto WiktionarySection y se fija de que tipo es
        if "adjetivo" in i.title.lower():
            defi = limpiar(BeautifulSoup(i.source,"html.parser").find("dd"))
            return 'JJ',defi.text.split('\n')[0]
        if "sustantivo" in i.title.lower():
            defi = limpiar(BeautifulSoup(i.source,"html.parser").find("dd"))
            return 'NN',defi.text.split('\n')[0]
        if "verbo" in i.title.lower():
            defi = limpiar(BeautifulSoup(i.source,"html.parser").find("dd"))
            return 'VB',defi.text.split('\n')[0]

def guardarReporte(lis,error=''):
    with open('reporte.csv','a',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        lis.append(error)
        writer.writerow(lis)

def guardarPalabra(lis):
    with open('palabras.csv','a',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(lis)
        
def pedirDefinicion(palabra):
    layout_definicion =[
            [sg.T('La palabra ingresada no se ha podido identificar. Por favor ingrese una definicion de la palabra')],
            [sg.Input()],
            [sg.Ok()]
                        ]
    window_def = sg.Window('Palabra No Identificada').Layout(layout_definicion)
    event, definicion = window_def.Read()
    return definicion[0]

def main(palabra):
    defPal = [palabra]
    wik = Wiktionary(language="es")

    try:
        seccion = wik.search(palabra,type=SEARCH)
    except (URLTimeout, URLError):
        exit('Se acabó el tiempo de espera en la conexión. Por favor revise su conexión a internet e intente nuevamente.')

    if seccion != None:    # Wikcionario valido
        try:
            tipo, definicion = tipoPal(seccion)
        except TypeError:
            sg.Popup('La palabra ingresada no es Verbo, Sustantivo o Adjetivo.',title='Tipo no identificado')
            return
        defPal.append(tipo)
        defPal.append(definicion)
        if tag(palabra)[0][1] != defPal[1]:  #Si la palabra no coincide con el pattern se guarda en el reporta
            guardarReporte(defPal,'Pattern no coincide con Wiktionary')
        else: # Guarda la palabra en el archivo de palabras
            guardarPalabra(defPal)
    else: #No se encontro en el Wiktionary
        if (tag(palabra)[0][1] != 'NN'):    #Pattern detecta palabras invalidas como NN
            defPal.append(tag(palabra)[0][1])
            defPal.append(pedirDefinicion(palabra))
            guardarPalabra(defPal)
            guardarReporte(defPal,"La palabra no se encontro en Wiktionary")
        else:
            defPal.append('-')
            defPal.append('-')
            guardarReporte(defPal,"Palabra desconocida por Wiktionary y Pattern")

if __name__ == '__main__':
    import sys
    sys.exit(main(palabra))

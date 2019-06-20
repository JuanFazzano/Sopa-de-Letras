'''
Fazzano, Juan Manuel
Baudino Zoya, Fermín
Comba, Sebastian


Display de la sopa de letras
'''



# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from random import randint
from casillero import Casillero


def generarMatriz(g,dic,columnas,filas,listc,cap):
    '''
    LE DA VALORES A LA MATRIZ, NO LA IMPRIME
    '''
    for x in range(columnas):
        for y in range(filas):
            letra = chr(randint(97,122))
            if cap == 'MAYUSCULAS':
                letra = letra.upper()

            # SE CREA UN OBJETO Y SE GUARDA EN UN DICCIONARIO CON LA COORDENADA EN LA QUE PERTENECE
            c = Casillero (x,y,listc[0],listc[0],letra,True)
            dic[(x,y)] = c
def agregarVertical (dic,palabra,listc,delta,x,tipo):
    '''
    ORDENA LAS PALABRAS VERTICALMENTE
    '''
    d = randint(0,delta)
    for letra,y in zip (palabra,range(len(palabra)+delta)):
        dic[(x,y+d)].set_letra(letra)
        dic[(x,y+d)].set_OK(False)

        #se guarda el color que tiene que tener al terminar el juego
        if tipo[0] == 'VB':
            dic[(x,y+d)].set_cOK(listc[2])
        elif tipo[0] == 'JJ':
            dic[(x,y+d)].set_cOK(listc[3])
        else:
            dic[(x,y+d)].set_cOK(listc[4])

def agregarHorizontal (dic,palabra,listc,delta,y,tipo):
    '''
    ORDENA LAS PALABRAS HORIZONTALMENTE
    '''
    d = randint(0,delta)
    for letra,x in zip (palabra,range(len(palabra)+delta)):
        dic[(x+d,y)].set_letra(letra)
        dic[(x+d,y)].set_OK(False)

        #se guarda el color que tiene que tener al terminar el juego
        if tipo[0] == 'VB':
            dic[(x+d,y)].set_cOK(listc[2])
        elif tipo[0] == 'JJ':
            dic[(x+d,y)].set_cOK(listc[3])
        else:
            dic[(x+d,y)].set_cOK(listc[4])

def agregarPalabras (dic,dicPalabras,listc,d,orientacion,cap):
    '''
    AGREGA ALEATORIAMENTE LAS PALABRAS ELEGIDAS
    '''
    delta = d -1
    lista = []
    for palabra,tipo  in dicPalabras.items():

        if cap == 'MAYUSCULAS':
            palabra = palabra.upper()

        # ELEGIR UNA COORDENADA NO REPITENTE
        a = randint(0,len(dicPalabras)+delta)
        while True:
            if a in lista:
                a = randint(0,len(dicPalabras) + delta)
            else:
                lista.append(a)
                break
        if orientacion == 'vertical':
            agregarVertical (dic,palabra,listc,delta,a,tipo)
        else:
            agregarHorizontal (dic,palabra,listc,delta,a,tipo)

def dibujar(g,px,dic,columnas,filas):
    '''
    ESCRIBE EN EL GRAPH LAS LETRAS DE LA MATRIZ
    '''
    for x in range(columnas):
        for y in range(filas):
            dic[(x,y)].draw(g,px)

def terminar(g, dic, px, columnas, filas, listc):
    '''
    COLOREA LAS PALABRAS QUE FALTARON ENCONTRAR
    DETERMINAR EL PORCENTAJE CORRECTO DE CASILLERO CORRECTOS
    '''

    total = columnas*filas
    errores = 0
    for x in range(columnas):
        for y in range(filas):
            dic[(x,y)].comparar(g,px,listc)
            if dic[(x,y)].get_OK() != False:
                errores += 1

    porcentaje = errores * 100 / total
    sg.Popup('Lograste un {}% correctamente' .format(int(porcentaje)))



def setSize(orientacion,cantidadPalabras,palabraMasLarga):
    '''
    DETERMINAR EL ANCHO Y LARGO DEL DISPLAY
    '''
    if orientacion == 'vertical':
        columnas,filas = cantidadPalabras,palabraMasLarga
    else:
        columnas,filas = palabraMasLarga,cantidadPalabras
    return columnas,filas
def datosPalabras (dicPalabras):
    '''
    DEVUELVE EL LARGO DE LA PALABRA MAS LARGA Y LA CANTIDAD TOTAL DE PALABRAS + UN DELTA RANDOM
    '''
    palabraMasLarga=0
    for palabra in dicPalabras:
        if len(palabra)>palabraMasLarga:
            palabraMasLarga = len(palabra)

    cantidadPalabras = len(dicPalabras)
    # delta > 1
    delta = randint(2,5)
    palabraMasLarga += delta
    cantidadPalabras += delta
    return palabraMasLarga,cantidadPalabras,delta

def ayuda (dicPalabras):
    '''
    DEVUELVE UN TEXTO CON TODAS LAS DEFINICIONES DE LAS PALABRAS AGREGADAS
    '''
    texto = ''
    for i in dicPalabras.values():
        texto += i[1] + '\n'
    return texto

def leerReporte():
    '''
    DEVUELVE EL REPORTE DE LAS PALABRAS ERRONEAS COMO LISTA
    '''
    with open('reporte.txt',encoding='utf-8') as f:
        lineas =  f.readlines()
    return ''.join(lineas)


def mostrarReporte(fTit,fTex):
    '''
    MOSTRAR EN PANTALLA EL REPORTE DE LAS PALABRAS ERRONEAS
    '''
    # lista = verificarPalabra.mostrarReporte()
    layout_reporte = [[sg.Multiline(leerReporte(),font=fTex,disabled=True)],
                      [sg.CloseButton('Cerrar')]]
    window_reporte = sg.Window('Reporte de Palabras Erroneas',font=fTit).Layout(layout_reporte)
    window_reporte.Read()

def main(dicPalabras,datos):

    cap = datos['__CAPITALIZACION__']


    # DATOS DEL DISPLAY
    orientacion = datos['__ORIENTACION__']
    px = 40

    # DATOS DE LAS PALABRAS

    palabraMasLarga,cantidadPalabras,delta = datosPalabras(dicPalabras)
    columnas,filas = setSize(orientacion,cantidadPalabras,palabraMasLarga)
    ancho,alto = filas * px, columnas * px

    # DATOS DEL REPORTE
    fTIT = datos['TIPOGRAFIA_TIT']
    fTEX = datos['TIPOGRAFIA_TEX']

    # COLORES
    if datos['__cVB__'] == '':
        cVB = 'red'
    else:
        cVB = datos['__cVB__']

    if datos['__cJJ__'] == '':
        cJJ = 'blue'
    else:
        cJJ = datos['__cJJ__']

    if datos['__cNN__'] == '':
        cNN = 'green'
    else:
        cNN = datos['__cNN__']

    cFondo = 'white'
    cAct = cFondo
    listc = [cFondo,cAct,cVB,cJJ,cNN]

    sg.SetOptions(button_color=('white', 'black'))

    # dic[(x,y)] : OBJETO
    dic = dict()


    # CONFIGURACION DEL LAYOUT
    layout = [
                [sg.Text('Sopa de letras'), sg.Text('', key='_OUTPUT_')],
                [sg.Graph((alto,ancho), (0,ancho), (alto,0), background_color = cFondo, key='_GRAPH_', change_submits=True, drag_submits=False)],
                [sg.Button('Verbo',size=(15,2), button_color=(cFondo, listc[2])),sg.Button('Adjetivo',size=(15,2), button_color=(cFondo, listc[3])), sg.Button('Sustantivo',size=(15,2), button_color=(cFondo, listc[4]))],
                [sg.Submit('Mostrar Resultados',size=(15, 1)),
                 sg.Button('Ayuda',size=(15, 1)),
                 sg.Button('Mostrar Reporte',key='reporte',),
                 sg.Cancel('Salir',size=(15, 1))]
             ]
    window = sg.Window('Sopa de letras').Layout(layout).Finalize()
    g = window.FindElement('_GRAPH_')



    # GENERACION Y CREACION DE LA MATRIZ
    generarMatriz(g,dic,columnas,filas,listc,cap)
    agregarPalabras(dic,dicPalabras,listc,delta,orientacion,cap)
    dibujar(g,px,dic,columnas,filas)


    cAct = cFondo
    fin = False
    while True:
        event, values = window.Read()
        # TERMINAR JUEGO
        if event is None or event == 'Salir':
            break

        if fin != True:
            if event == 'Terminar Juego':
                terminar(g, dic, px, columnas, filas, listc)
                fin = True
            elif event == 'reporte':
                mostrarReporte(fTIT,fTEX)
            # CAMBIO DE COLORES
            elif event == 'Verbo':
                cAct = cVB
            elif event == 'Adjetivo':
                cAct = cJJ
            elif event == 'Sustantivo':
                cAct = cNN

            elif event == 'Ayuda':
                texto = ayuda(dicPalabras)
                sg.Popup(texto)




            # CLICK EN LA MATRIZ
            elif event == '_GRAPH_':
                mouse = values['_GRAPH_']
                if mouse == (None, None):
                    continue
                try:
                    click = (mouse[0] // px,mouse[1] // px)
                    c = dic[click]
                    c.click(g,px,cAct)
                except KeyError:
                    pass

if __name__ == '__main__':
    import sys
    sys.exit(main(dicPalabras,datos))

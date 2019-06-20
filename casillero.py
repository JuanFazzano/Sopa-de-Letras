# -*- coding: utf-8 -*-
import PySimpleGUI

class Casillero():
    def __init__(self,x,y,cFondo,cOK,letra,OK):
        '''
        CONSTRUCTOR
        '''
        # COORDENADAS
        self.__x = x
        self.__y = y
        self.__coordenadas = (self.__x,self.__y)

        # COLORES
        self.__cFondo = cFondo
        self.__cFondoOriginal = cFondo
        self.__cOK = cOK

        # OTROS
        self.__letra = letra
        self.__OK = True

    '''
    SETTER
    '''
    def set_x (self,x):
        self.__x = x
    def set_y (self,y):
        self.__y = y
    def set_coordenadas (self, coordenadas):
        self.__coordenadas = coordenadas

    def set_cFondo (self,cFondo):
        self.__cFondo = cFondo
    def set_cOK (self,cOK):
        self.__cOK = cOK
    def set_cFondoOriginal (self,cFondoOriginal):
        self.__cFondoOriginal = cFondoOriginal

    def set_letra (self,letra):
        self.__letra = letra
    def set_OK (self,OK):
        self.__OK = OK


    '''
    GETTER
    '''
    def get_x (self):
        return self.__x
    def get_y (self):
        return self.__y
    def get_coordenadas (self):
        return self.__coordenadas

    def get_cFondo (self):
        return self.__cFondo
    def get_cOK (self):
        return self.__cOK
    def get_cFondoOriginal(self):
        return self.__cFondoOriginal

    def get_letra (self):
        return self.__letra
    def get_OK (self):
        return self.__OK


    '''
    METODOS
    '''
    def drawRect (self,g,px,color = None):
        '''
        DIBUJA UN CUADRADO DE COLOR EN LA POSICION CORRESPONDIENTE
        '''
        if color == None:
            color= self.get_cFondo()
        g.DrawRectangle((self.get_x() * px,self.get_y() * px), (self.get_x() * px + px, self.get_y() * px + px), line_color='black',fill_color = color)

    def drawLetra (self,g,px):
        '''
        DIBUJA UNA LETRA CENTRADA EN LA POSICION CORRESPONDIENTE
        '''
        g.DrawText('{}'.format(self.get_letra()), (self.get_x() * px + (px // 2), self.get_y() * px + (px // 2)),font = 'Arial')

    def draw (self,g,px):
        '''
        DIBUJA LAS PALABRAS AL INICIAR EL JUEGO
        '''
        self.drawRect(g,px)
        self.drawLetra(g,px)

    def comparar (self,g,px,listc):
        '''
        COLOREA DE MANERA CORRECTA LAS PALABRAS VALIDAS
        '''
        if self.get_cOK() == self.get_cFondoOriginal():
            self.drawRect(g,px,self.get_cFondoOriginal())
        else:
            if self.get_cOK() == listc[2]:      # ES VERBO
                self.drawRect(g,px,listc[2])
            elif self.get_cOK() == listc[3]:    # ES ADJETIVO
                self.drawRect(g,px,listc[3])
            else:                               # ES SUSTANTIVO
                self.drawRect(g,px,listc[4])

            self.drawLetra(g,px)

    def __evaluar (self):
        '''
        EVALUA QUE ESTE BIEN COLOREADO EL FONDO
        '''
        if self.get_cFondo() == self.get_cOK():
            self.set_OK(True)
        else:
            self.set_OK(False)

    def click (self,g,px,cAct):
        '''
        PINTA LA CUADRICULA DEL FONDO
        '''
        if self.get_cFondo() == self.get_cFondoOriginal():
            self.drawRect(g,px,cAct)
            self.set_cFondo(cAct)

        else:
            self.drawRect(g,px,self.get_cFondoOriginal())
            self.set_cFondo(self.get_cFondoOriginal())

        self.drawLetra(g,px)
        self.__evaluar()

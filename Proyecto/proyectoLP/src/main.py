'''
Created on 31/07/2013

@author: Keylis
'''

import sys

from PyQt4 import QtCore, QtGui
from numero import *
from sudoku import Ui_Sudoku
import random
    
class Main(QtGui.QMainWindow):
    global coorX
    global coorY
    global criptar
    global celdaSeleccionada
    global casilla
    global valorPad
    global ficheroActual
    global ruta    
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Sudoku()
        self.ui.setupUi(self)
        self.casilla = []
        self.valorPad = []
        self.celdaSeleccionada = False
        self.ficheroActual =" "
        self.ruta = " "
        self.criptar = " "
        self.iniciarArreglo()
        self.iniciarValorPad()
        self.initGui()
        self.ui.actionQuit.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'),  QtGui.qApp, QtCore.SLOT('quit()'))
        self.ui.actionNew.connect(self.ui.actionNew, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT(self.actionNew()))
        #self.ui.actionClose.connect(self.ui.actionClose, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT(self.cerrar()) )
        self.ui.actionSave.connect(self.ui.actionSave, QtCore.SIGNAL('triggered()'),QtCore.SLOT(self.guardarPartida(self.encriptar())))
        
    def iniciarArreglo (self):
        del self.casilla [:]
        for i in range (9):
            self.casilla.append ([])
            for j in range(9):
                celda = numero()
                self.casilla[i]. append ([])
                celda = numero()
                celda.setFila(i)
                celda.setColumna(j)
                celda.setNumReal(0)
                celda.setNumAsignado(0)
                celda.setColor(0)
                celda.setEsConstante(False)
                self.casilla [i][j] = celda
    
    def iniciarValorPad(self):
        for i in range(9):
            numSelec = QPushButton()
            numSelec.setText(str(i+1))
            self.valorPad.append(numSelec)
                
    def initGui(self):
        
        self.coorX = -1
        self.coorY = -1
        
        flag = False
        for i in range(9):
            for j in range(9):
                celda = self.casilla [i][j]
                if(flag):
                    celda.setColor(0)
                    celda.setStyleSheet('QPushButton {background-color: red}' )
               
                else:
                    celda.setColor(1)
                    celda.setStyleSheet('QPushButton {background-color: blue}' )

                #self.connect(self.casilla[i][j], QtCore.SIGNAL('clicked()'), QtCore.SLOT(self.celdaClicked(i,j)))
                self.ui.gridLayout.addWidget(self.casilla[i][j],i,j)
                
                if(j % 3 == 2):
                    flag = not(flag)
            
            if(i % 3 != 2):
                flag = not (flag)
        
        for i in range(9):
            self.ui.numberPad.addWidget(self.valorPad[i],i/3, i%3)
            self.valorPad[i].setStyleSheet('QPushButton {background-color: black; color: white}')
            # self.connect(self.valorPad[i], QtCore.SIGNAL('clicked()'), QtCore.SLOT(self.numeroClicked(self.valorPad[i].text())))
            
        self.ui.nullButton.setText('Borrar')
        self.ui.nullButton.setEnabled(False)
        self.ui.nullButton.setStyleSheet('QPushButton {background-color: black; color: white}')
        self.celdaSeleccionada = False
        self.ventanaInvalida()
    
    def celdaClicked(self, fil, colum):
        if (not (self.celdaSeleccionada)):
            self.celdaSeleccionada = True
        else:
            celda = self.casilla[self.coorX][self.coorY]
            
            if(celda.getColor == 0):
                celda.setStyleSheet('QPushButton {background-color: red}')
            else:
                celda.setStyleSheet('QPushButton {background-color: blue}')

        celda = self.casilla[fil][colum]
        celda.sender() 
        self.coorX = celda.getFila()
        self.coorY = celda.getColumna()
        print self.coorX
        print self.coorY
        if (celda.getNumReal() == celda.getNumeroAsignado()):
            self.ui.radioButton.setChecked(True)
        else:
            self.ui.radioButton.setChecked(False)
        
        for i in range(9):
            numSelec = self.valorPad[i] 
            numSelec.setEnabled(True)
        if(self.ui.hintButton.isChecked()):
            self.validarCelda()
            
        celda.setStyleSheet('QPushButton {background-color: orange}')
        
    def numeroClicked(self, valor):
        if(self.celdaSeleccionada):
            celda = self.casilla[self.coorX][self.coorY]
            print celda.getNumeroAsignado()
            numSelec = self.valorPad[celda.getNumeroAsignado() -1]
            numSelec.setEnabled(True)
            celda.setText(str(valor))
            celda.setNumeroAsignado(valor)
            
            if (celda.getNumReal() == celda.getNumeroAsignado()):  
                self.ui.radioButton.setChecked(True)         
            else:
                self.ui.radioButton.setChecked(False)
            if(self.ui.hintButton.isChecked()):
                numSelec.setEnabled(False)
                 
            self.ui.nullButton.setEnabled(True)
            if(self.sudokuCompleto()):
                self.ventanaInvalida()
        else:
            if(self.ui.clueButton.isChecked()):
                self.ventanaInvalida()
                self.ui.groupBox_2.setEnabled(True)
                
            for k in range(9):
                for l in range(9):
                    celda = self.casilla[k][l]
                    celda.setStyleSheet('background-color: yellow')
            for k in range(9):
                for l in range(9):
                    celda = self.casilla[k][l]
                    if (celda.getNumeroAsignado()):    
                        if (celda.getNumeroAsignado() == valor):
                            centerX = k/3
                            centerY = l/3
                            for i in range(9):
                                for j in range(9):
                                    celda1 = self.casilla[i][i]
                                    if((i == k | j == l | (i/3 == centerX & j/3 == centerY ))):
                                        if (not celda1.getNumeroAsignado):
                                            if(celda1.getColor == 0):
                                                celda1.setStyleSheet('QPushButton {background-color: red}' )
                                            else:
                                                celda1.setStyleSheet('QPushButton {background-color: blue}' )
                        if(celda.getColor == 0):
                            celda.setStyleSheet('QPushButton {background-color: red}' )
                        else:
                            celda.setStyleSheet('QPushButton {background-color: blue}' )
            for i in range(9):
                numero = self.valorPad[i]               
                numero.setEnabled(True)        
            
    def sudokuCompleto(self):
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                if (celda.getNumReal() != celda.getNumeroAsignado()):
                    return False
        return True
            
    def generadorSudoku(self, fila):
        if(fila > 8):
            return
        
        digitArray = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       
        temp = [0] * 9
        random.shuffle(digitArray)
            
        flag = False
        for i in range(9):
            for j in range(9):
                flag = False
                if (digitArray[j] >= 1):
                    if(self.asignarNumero(0, fila, i, digitArray[j])):
                        digitArray[j] = -1
                        flag = True
                    
                    if (flag):
                        break
        
        for k in range(9):
            celda = self.casilla[fila][k]
            temp[k] = celda.getNumReal()
            
        self.generadorSudoku(fila+1)
    
    def validarCeldaConNum(self, fila, columna, valor, cont):
        centerX = fila/3
        centerY = columna/3
        
        for i in range(9):
            for j in range(9):
                if((i == fila | j == columna | (i/3 == centerX & j/3 == centerY))):
                    celda = self.casilla[i][j]
                    if(celda.getNumReal()):
                        if( not(i == fila & j == columna - cont) & valor == celda.getNumReal()):
                            return False
        return True     
                   
    def asignarNumero(self,cont, fila, columna, valor):
        
        if(cont > columna):
            return False
        else:
            celda = self.casilla[fila][columna - cont]
            if((not cont & self.validarCeldaConNum(fila, columna, valor, 0)) | (cont & self.validarCeldaConNum(fila, columna, celda.getNumReal(), cont) & self.validarCeldaConNum(fila, columna - cont, valor, 0))):
                if(not (cont)):
                    celda = self.casilla[fila][columna]
                    celda.setNumReal(valor)
                else:
                    celda = self.casilla[fila][columna-cont]
                    asign = self.casilla[fila][columna]
                    asign.setNumReal(celda.getNumReal())
                    
                    celda.setNumReal(valor)
                return True
            else:
                cont += 1
                return self.asignarNumero(cont, fila, columna, valor)
    
    def limpiarTablero(self):
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                celda.setNumReal(0)
                celda.setNumAsignado(0)
                celda.setText("")
                
    def comprobarTableroVacio(self):
        for i in range(9):
            for j in range(9):
                celda = self.casilla [i][j]
                if(not (celda.getNumReal())):
                    return False
        return True
    
    def actionNew(self):
        self.limpiarTablero()
        
        while(not(self.comprobarTableroVacio())):
            self.limpiarTablero()
            self.generadorSudoku(0)
        
        for k in range(0, 30):
            fila = random.randint(0,8)
            columna = random.randint(0,8)
            cont = 0
            
            for i in range(9):
                for j in range(9):
                    if(i == fila | j == columna | (i/3 == fila/3 & j/3 == columna/3)):
                        celda = self.casilla[i][j]
                        if(celda.getEsConstante()):
                            cont +=1
                if(cont < 5):
                    celda = self.casilla[fila][columna]
                    celda.setEsConstante(True)
                    celda.setEnabled(False)
                    celda.setText(str(celda.getNumReal()))
                    celda.setNumAsignado(celda.getNumReal())
            
                else:
                    k -= 1    
                    
        self.ventanaInvalida()
        self.ventanaValida()
            
    
                    
                
     #int(x) Returns x converted to an int; x may be a string or a number   
            
    def validarCelda(self):
        self.centerX = self.coorX/3
        self.centerY = self.coorY/3
        
        for i in range(9):
            for j in range(9):
                if(i == self.coorX | j == self.coorY | (i/3 == self.centerX & j/3 == self.centerY )):
                    celda = self.casilla[i][j]
                    if (celda.getNumeroAsignado()):
                        valor = celda.getNumeroAsignado()
                        numSelec = self.valorPad[valor -1]
                        numSelec.setEnabled(False)
        
        celda = self.casilla[self.coorX][self.coorY]
        if(not(celda.getNumeroAsignado())):
            self.ui.nullButton.setEnabled(False)
        else:
            self.ui.nullButton.setEnabled(True)
            
    def ventanaInvalida(self):
        self.coorX = -1
        self.coorY = -1
        
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                celda.setEnabled(False)
                
                if(celda.getColor() == 0):
                    celda.setStyleSheet('QPushButton {background-color: red}')
                else:
                    celda.setStyleSheet('QPushButton {background-color: blue}')
            
            numSelec = self.valorPad[i]
            numSelec.setEnabled(False)
        
        self.ui.nullButton.setEnabled(False)
        self.ui.radioButton.setChecked(False)
        self.celdaSeleccionada = False
        
        self.ui.groupBox_2.setEnabled(False)     
        
    def ventanaValida(self):
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                if (not(celda.getEsConstante())):
                    celda.setEnabled(True)
        
        self.ui.groupBox_2.setEnabled(True)
             
    def cerrar(self):
        self.limpiarTablero()
        self.ventanaInvalida()
        
    def boton_nulo_clicked(self):
        celda = self.casilla[self.coorX][self.coorY]
        valor = celda.getNumeroAsignado()
        self.valorPad[valor -1].setEnabled(True)
        celda.setText("")
        celda.setNumAsignado(0)
        self.ui.nullButton.setEnabled(False)
        self.ui.radioButton.setChecked(False)
        
    def encriptar(self):
        codigo = []
        key = []
        hint = [""]*9
        binaryBuffer = 0
        self.criptar = QtCore.QString()
        delta = 0
        #chr(i) Returns a one-character str whose ASCII value is given by int i
        if(not(self.comprobarTableroVacio())):
            return
        for i in range(9):
            for j in range(9):
                if(not(j)):
                    codigo.append([])
                    hint.append([])
                    key.append([])
                    celda = self.casilla[i][j]
                    delta = celda.getNumReal()
                    codigo[i] = QtCore.QString(delta + 96)
                else:
                    celda1 = self.casilla[i][j - 1]
                    delta = celda.getNumReal() - celda1.getNumReal()
                    valor = int
                    valor = valor.__abs__(delta + 96)
                    codigo[i] = QtCore.QString(valor)

                if (delta > 0):
                    raiz = int
                    raiz = raiz.__pow__(2, 8- j)
                    binaryBuffer += raiz
                    
                celda = self.casilla[8 - i][8 - j]    
                num = celda.getNumeroAsignado()
                hint[i] += str(num)
                
            valor = QtCore.QString()
            valor.setNum(binaryBuffer, 16)
            key[i] = valor

            delta = 0
            binaryBuffer = 0
            self.criptar += ("%s\n" % codigo[i]) + ("%s\n" % key[i]) + ("%s\n" % hint[i])
            
            #print self.criptar 
        
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                if (celda.getEsConstante()):
                    numI = str(i)
                    numJ = str(j)
                    self.criptar += ("%s\n" % numI) + ("%s\n" % numJ)
        
        return self.criptar
        
    def guardarPartida(self, crip):
        if (self.ficheroActual):
            ruta_guardar = self.ficheroActual
        else:
            ruta_guardar = self.ruta
                        
        nombre_fichero =QtGui.QFileDialog.getSaveFileName(self, "Guardar fichero", ruta_guardar)
        guardar = open(nombre_fichero, 'w')
        guardar.write(crip)
        guardar.close()   
             
    def abrirPartida(self):
        codigo = []
        key = []
        hint = [""] *9
        
        self.criptar = " "
        decimal = 0
        digito = 0
        
        self.limpiarTablero()
        
        nombre_open = QtGui.QFileDialog.getOpenFileName(self ,  'Abrir Archivo' , '' )
        abrir = open(nombre_open, 'r')
        contenido = abrir.read()
        seguidor = 0
        
        for linea in abrir:
            linea = QtCore.QString()
            linea = abrir.readline()
            print linea
            
        #if(len(linea)):
            #linea.replace("\n", "")
            #if(seguidor > 27):
                #lineaI = linea / 10
                #print lineaI
                #lineaJ = linea % 10
                #print lineaJ
                #celda = self.casilla[lineaI][lineaJ]
                #celda.setEsConstante(True)
            #else:
                #if (seguidor % 3 == 0):
                    #codigo [seguidor / 3] = linea
                    #print linea
                #else:
                    #if (seguidor % 3 == 1):
                        #key [seguidor / 3] = linea
                        #print linea
                    #else:
                        #if (seguidor % 3 == 2):
                            #hint [seguidor / 3] = linea
                            #print linea
            #seguidor += 1
        
        
           
if __name__ == "__main__":
    app= QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
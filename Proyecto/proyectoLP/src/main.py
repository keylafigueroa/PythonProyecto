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
    global encriptar
    global celdaSeleccionada
    global casilla
    global valorPad
        
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Sudoku()
        self.ui.setupUi(self)
        self.casilla = []
        self.valorPad = [0 for j in range(9)]
        self.iniciarValorPad()
        self.iniciarArreglo()
        self.celdaSeleccionada = False
        self.ui.actionQuit.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'),  QtGui.qApp, QtCore.SLOT('quit()'))
        self.ui.actionNew.connect(self.ui.actionNew, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT(self.action_New()))
        self.initGui()
        
        
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
                celda.setEsConstante(False)
                self.casilla [i][j] = celda
    
    def iniciarValorPad(self):
        for i in range(9):
            numSelec = QPushButton()
            numSelec.setText(str(i+1))
            self.valorPad [i]= numSelec
            self.ui.numberPad.addWidget(self.valorPad[i],i/3, i%3)
            numSelec.setStyleSheet('QPushButton {background-color: black; color: white}')
                  
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

                #celda.connect(celda, QtCore.SIGNAL('clicked()'), QtCore.SLOT(self.celda_clicked()))
                self.ui.gridLayout.addWidget(self.casilla[i][j],i,j)
                
                if(j % 3 == 2):
                    flag = not(flag)
            
            if(i % 3 != 2):
                flag = not (flag)
        
        self.ui.nullButton.setText('Borrar')
        self.ui.nullButton.setEnabled(False)
        self.ui.nullButton.setStyleSheet('QPushButton {background-color: black; color: white}')
        self.celdaSeleccionada = False
        self.ventana_invalida()
        
    def numero_clicked(self):
        if(self.celdaSeleccionada):
            numeroButton = QPushButton.sender()
            celda = self.casilla[self.coorX][self.coorY]
            numSelec = self.valorPad[celda.getNumeroAsignado -1]
            numSelec.setEnabled(True)
            celda.setText(str(numeroButton))
            celda
            
    def Generador_sudoku(self, fila):
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
            
        self.Generador_sudoku(fila+1)
    
    def validarCeldaConNum(self, fila, columna, valor, cont):
        centerX = fila/3
        centerY = columna/3
        
        for i in range(9):
            for j in range(9):
                if((i == fila or j == columna or (i/3 == centerX and j/3 == centerY))):
                    celda = self.casilla[i][j]
                    if(celda.getNumReal()):
                        if( valor == celda.getNumReal() and not(i == fila and j == columna - cont) ):
                            return False
        return True     
                   
    def asignarNumero(self,cont, fila, columna, valor):
        
        if(cont > columna):
            return False
        else:
            celda = self.casilla[fila][columna - cont]
            if((not cont and self.validarCeldaConNum(fila, columna, valor, 0)) or (cont and self.validarCeldaConNum(fila, columna, celda.getNumReal(), cont) and self.validarCeldaConNum(fila, columna - cont, valor, 0))):
                if(not cont):
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
    
    def limpiar_tablero(self):
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                celda.setNumReal(0)
                celda.setNumAsignado(0)
                celda.setText("")
                
    def comprobar_tablero_vacio(self):
        for i in range(9):
            for j in range(9):
                celda = self.casilla [i][j]
                if(not celda.getNumReal()):
                    return False
        return True
    
    def action_New(self):
        self.limpiar_tablero()
        
        while(not(self.comprobar_tablero_vacio())):
            self.limpiar_tablero()
            self.Generador_sudoku(0)
        
        for k in range(0, 30):
            fila = random.randint(0,8)
            columna = random.randint(0,8)
            cont = 0
            
            for i in range(9):
                for j in range(9):
                    if(i == fila or j == columna or (i/3 == fila/3 and j/3 == columna/3)):
                        celda = self.casilla[i][j]
                        if(celda.getEsConstante):
                            cont +=1
                if(cont < 5):
                    celda = self.casilla[fila][columna]
                    celda.setEsConstante(True)
                    celda.setEnabled(False)
                    celda.setText(str(celda.getNumReal()))
                    celda.setNumAsignado(celda.getNumReal())
            
                else:
                    k -= 1    
                    
        #self.ventana_invalida()
        #self.validar_Ventana()
            
    
                    
                
     #int(x) Returns x converted to an int; x may be a string or a number   
            
    def celda_clicked(self):
        if (not (self.celdaSeleccionada)):
            self.celdaSeleccionada = True
        else:
            celda = self.casilla[self.coorX][self.coorY]
>>>>>>> main modificado
            if(celda.getColor == 0):
                celda.setStyleSheet('QPushButton {background-color: red}')
            else:
                celda.setStyleSheet('QPushButton {background-color: blue}')
<<<<<<< HEAD
        celda = numero()
        celda.sender()
        coorX = celda.getFila()
        coorY = celda.getColumna()
        
=======
        
        celda = numero() 
        celda = self.sender()
        self.coorX = celda.getFila()
        self.coorY = celda.getColumna()
            
>>>>>>> main modificado
        if (celda.getNumReal() == celda.getNumeroAsignado()):
            self.ui.radioButton.setChecked(True)
        else:
            self.ui.radioButton.setChecked(False)
<<<<<<< HEAD
            numSelec = QPushButton() 
        for i in range(0,9):
            numSelec = valorPad[i] 
            numSelec.setEnabled(True)
        if(self.ui.radioButton.isChecked()):
            self.validarCelda()
        
        celda.setStyleSheet('QPushButton {background-color: orange}')
            
    def validarCelda(self):
        centerX = coorX/3
        centerY = coorY/3
        celda = numero()
        for i in range(0,9):
            for j in range(0,9):
                if(i == coorX | j == coorY | (i/3 == centerX & j/3 == centerY )):
                    celda = casilla[i][j]
                    if (celda.getNumeroAsignado()):
                        numSelec = QPushButton()
                        valor = celda.getNumeroAsignado()
                        numSelec = valorPad[valor -1]
                        numSelec.setEnabled(False)
        
        celda = casilla[coorX][coorY]
=======
        
        for i in range(9):
            numSelec = self.valorPad[i] 
            numSelec.setEnabled(True)
        if(self.ui.hintButton.isChecked()):
            self.validar_celda()
            
            celda.setStyleSheet('QPushButton {background-color: orange}')
            
    def validar_celda(self):
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
>>>>>>> main modificado
        if(not(celda.getNumeroAsignado())):
            self.ui.nullButton.setEnabled(False)
        else:
            self.ui.nullButton.setEnabled(True)
            
<<<<<<< HEAD
=======
    def ventana_invalida(self):
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
        
    def validar_Ventana(self):
        self.coorX = -1
        self.coorY = -1
        
        for i in range(9):
            for j in range(9):
                celda = self.casilla[i][j]
                celda.setEnabled(False)
                if(celda.getColor == 0):
                    celda.setStyleSheet('QPushButton {background-color: red}')
                else:
                    celda.setStyleSheet('QPushButton {background-color: blue}')
             
            numSelec = self.valorPad[i]
            numSelec.setEnabled(False)
        
        self.ui.nullButton.setEnabled(False)
        self.ui.radioButton.setChecked(False)
        self.celdaSeleccionada = False
        
        self.ui.groupBox_2.setEnabled(False)
             
        
>>>>>>> main modificado
if __name__ == "__main__":
    app= QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
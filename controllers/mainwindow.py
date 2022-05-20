import time
from PySide2.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QApplication
from views.Ui_main import Ui_MainWindow
from PySide2.QtCore import Slot


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.columnasTablas()

        self.numeroProcesos = 0
        self.procesoActual = 1
        self.loteActual = 1
        self.totalLote = 0
        self.contadorProcesos = 0
        self.numeroEjecucion = 0
        self.tiempoTotal = 0
        self.listaRegistro = []
        self.listaEjecuccion = []
        self.listaTerminados = []

        self.ui.Empezar_pushButton.clicked.connect(self.empezar)
        self.ui.agregar_pushButton.clicked.connect(self.agregar)
        self.ui.iniciar_pushButton.clicked.connect(self.iniciar)

    def llenarTablaRegistro(self):
        self.ui.captura_tableWidget.setRowCount(len(self.listaRegistro))

        for (index_row, row) in enumerate(self.listaRegistro):
            for(index_cell, cell) in enumerate(row):
                self.ui.captura_tableWidget.setItem(index_row,index_cell,QTableWidgetItem(str(cell)))
    
    def llenarTablaEjecucion(self):
        self.ui.ejecuccion_tableWidget.setRowCount(len(self.listaEjecuccion))

        for (index_row, row) in enumerate(self.listaEjecuccion):
            for(index_cell, cell) in enumerate(row):
                self.ui.ejecuccion_tableWidget.setItem(index_row,index_cell,QTableWidgetItem(str(cell)))

    def llenarTablaTerminados(self):
        self.ui.finalizados_tableWidget.setRowCount(len(self.listaTerminados))

        for (index_row, row) in enumerate(self.listaTerminados):
            for(index_cell, cell) in enumerate(row):
                self.ui.finalizados_tableWidget.setItem(index_row,index_cell,QTableWidgetItem(str(cell)))
    
    def columnasTablas(self):
        self.ui.captura_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.ejecuccion_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.finalizados_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def buscarId(self, Id):
        for proceso in self.listaRegistro:
            if proceso[1] == Id:
                return False
        return True
    
    def ejecucion(self):
        while len(self.listaEjecuccion) > 0:
            proceso = self.listaEjecuccion.pop(0)
            self.llenarTablaEjecucion()
            self.ui.Nombre_label.setText(proceso[4])
            self.ui.Id_label.setText(str(proceso[1]))
            self.ui.operacion_label.setText(proceso[2])
            self.ui.tiempo_label.setText(str(proceso[3]))
            i = 0
            j = proceso[3]
            while i <= proceso[3]:
                self.ui.transcurrido_lcdNumber.display(i)
                self.ui.restante_lcdNumber.display(j)
                self.ui.total_lcdNumber.display(self.tiempoTotal)
                QApplication.processEvents()
                time.sleep(1)
                if self.numeroEjecucion == 0 or i != 0:
                    self.tiempoTotal += 1
                i += 1
                j -= 1
            operacion = proceso[2].split()
            resultado = 0
            if operacion[1] == "+":
                resultado = int(operacion[0]) + int(operacion[2])
            elif operacion[1] == "-":
                resultado = int(operacion[0]) - int(operacion[2])
            elif operacion[1] == "*":
                resultado = int(operacion[0]) * int(operacion[2])
            elif operacion[1] == "/":
                resultado = int(operacion[0]) / int(operacion[2])
            else:
                resultado = int(operacion[0]) % int(operacion[2])
            proceso.insert(3, resultado)
            self.listaTerminados.append(proceso)
            self.llenarTablaTerminados()
            self.numeroEjecucion += 1


    @Slot()
    def empezar(self):
        procesos = self.ui.N_Procesos.value()
        if procesos > 0:
            self.ui.procesos_Totales.setText(str(procesos))
            self.ui.proceso_Actual.setText(str(self.procesoActual))
            self.ui.Empezar_pushButton.setEnabled(False)
            self.ui.agregar_pushButton.setEnabled(True)
            self.numeroProcesos = procesos
        else:
           self.ui.Error.setText('Numero de procesos invalido')

    @Slot()
    def agregar(self):
        nombre = self.ui.Nombre_lineEdit.text()
        signo = self.ui.operacion_comboBox.currentText()
        if signo != '':
            n2 = self.ui.N_2_spinBox.value()
            if (signo == '/' and n2 == 0) or (signo == '%' and n2 == 0):
                self.ui.Error.setText('Operación Invalida')
            else:
                n1 =self.ui.N_1_spinBox.value()
                operacion = str(n1) + ' ' + signo + ' ' + str(n2)
                tiempo = self.ui.Tiempo_spinBox.value()
                if tiempo > 0:
                    Id = self.ui.Id_spinBox.value()
                    if self.buscarId(Id):
                        if self.contadorProcesos < 5:
                            self.contadorProcesos += 1
                        else:
                            self.loteActual += 1
                            self.contadorProcesos = 1
                        self.listaRegistro.append([self.loteActual, Id, operacion, tiempo, nombre])
                        if self.numeroProcesos == self.procesoActual:
                            self.ui.agregar_pushButton.setEnabled(False)
                            self.ui.iniciar_pushButton.setEnabled(True)
                            self.totalLote = self.loteActual
                        else:
                            self.procesoActual += 1
                            self.ui.proceso_Actual.setText(str(self.procesoActual))
                        self.llenarTablaRegistro()
                        self.ui.Error.setText('')
                    else:
                        self.ui.Error.setText('ID ya registrado')
                else:
                    self.ui.Error.setText('Tiempo Invalido')
        else:
            self.ui.Error.setText('Escoja una operación valida')
    
    @Slot()
    def iniciar(self):
        self.ui.lote_Total.setText(str(self.totalLote))
        self.loteActual = 1
        self.ui.iniciar_pushButton.setEnabled(False)
        while self.loteActual <= self.totalLote:
            self.ui.lote_Actual.setText(str(self.loteActual))
            for procesos in reversed(self.listaRegistro):
                if procesos[0] == self.loteActual:
                    self.listaEjecuccion.insert(0, procesos)
                    self.listaRegistro.pop(self.listaRegistro.index(procesos))
            self.llenarTablaRegistro()
            self.llenarTablaEjecucion()
            self.ejecucion()
            self.loteActual += 1
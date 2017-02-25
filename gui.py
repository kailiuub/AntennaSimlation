import sys, time
import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import math
from random import randint

import plot

# **** Implement Algorithms ****
class FF (FigureCanvas):
    def __init__(self,parent=None):
        self.nl=20 # number of scanned points for length
        self.nr=10 # number of scanned points for radius
        self.l0=0.2  # start of scanned length
        self.l1=5.0  # end of scanned length
        self.r0=0.002  # start of scanned radius
        self.r1=0.01  # end of scanned radius
        lengths=np.linspace(self.l0, self.l1, self.nl)
        radii=np.linspace(self.r0, self.r1, self.nr)
        self.z0=50.0 # instrinsic impedance
        reflections=np.zeros((self.nr,self.nl))
        reflections=plot.compute(self.nl,self.nr,lengths,radii,self.z0)
        self.fig1, self.ax1, self.ax2, self.cb1, self.cb2, self.axcb1, self.axcb2=plot.plot(lengths, radii, reflections)
        FigureCanvas.__init__(self,self.fig1)
        self.setParent(parent) 
    def updatefig(self):
        lengths=np.linspace(self.l0, self.l1, self.nl)
        radii=np.linspace(self.r0, self.r1, self.nr)
        L, R = np.meshgrid(lengths, radii)
        reflections=np.zeros((self.nr,self.nl))
        reflections=np.round(plot.compute(self.nl,self.nr,lengths,radii,self.z0),3)
        self.ax1.cla()    # clear plots and axis
        self.ax2.cla()
        #c=self.ax1.contourf(L, R, reflections, cmap=cm.plasma)    # replot the figures
        c=self.ax1.imshow(reflections, origin="lower", interpolation="bilinear", extent=[np.amin(lengths),np.amax(lengths),np.amin(radii),np.amax(radii)], cmap=cm.plasma, aspect=(np.amax(lengths)-np.amin(lengths))/(np.amax(radii)-np.amin(radii)) )
        s=self.ax2.plot_surface(L, R, reflections, cmap=cm.plasma)
        self.ax1.set_xlabel("Antenna length (m)")
        self.ax1.set_ylabel("Radius (m)")
        self.ax2.set_xlabel("Antenna length (m)")
        self.ax2.set_ylabel("Radius (m)")
        self.ax2.set_zlabel("Reflection Coefficient")
        # update colorbars
        self.cb1.on_mappable_changed(c)  # update cmap
        self.cb2.on_mappable_changed(s)
        self.cb1.set_ticklabels(np.linspace(np.amin(reflections),np.amax(reflections),10), update_ticks=True)  # update ticks immediately
        self.cb2.set_ticklabels(np.linspace(np.amin(reflections),np.amax(reflections),10), update_ticks=True)
        self.draw()
        

class App(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Antenna EM Simulation GUI')
        self.setGeometry(50,50,1150,600)

        # **** Create Menu ****
        self.menu=self.menuBar()
        self.file=self.menu.addMenu('File')
        self.edit=self.menu.addMenu('Edit')
        self.help=self.menu.addMenu('Help')

        self.exit=QAction(QIcon(''),'Exit',self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.triggered.connect(self.close)
        self.file.addAction(self.exit)

        self.about=QAction(QIcon(''),'About',self)
        self.about.setShortcut('Ctrl+T')
        self.about.triggered.connect(self.aboutact)
        self.help.addAction(self.about)

        # **** Create 4 Tabs to show Equations, Codes and GUI ****
        self.mainW1=QWidget(self)
        self.layout1=QVBoxLayout(self.mainW1)
        
        # initiate tabs
        self.tabs=QTabWidget()
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tab4=QWidget()
        self.tab5=QWidget()
        # add tab1 and tab2 to tabs
        self.tabs.addTab(self.tab1,'Introduction')
        self.tabs.addTab(self.tab2,'Code 1: NECPP')
        self.tabs.addTab(self.tab3,'Code 2: GUI INIT')
        self.tabs.addTab(self.tab4,'Code 3: GUI')
        self.tabs.addTab(self.tab5,'GUI')
	
        # create tab1 for intro with pdf file scroll bar      
        
        self.tab1_layout=QVBoxLayout()
        self.textedit0=QPlainTextEdit(readOnly=True)
        self.text0=open('README.md').read()
        self.textedit0.setPlainText(self.text0)
        self.tab1_layout.addWidget(self.textedit0)
        self.tab1.setLayout(self.tab1_layout)
        
        # create tab2 for Code1 
        self.tab2_layout=QVBoxLayout()
        self.textedit1=QPlainTextEdit(readOnly=True)
        self.text1=open('impedance.py').read()
        self.textedit1.setPlainText(self.text1)
        self.tab2_layout.addWidget(self.textedit1)
        self.tab2.setLayout(self.tab2_layout)

        # create tab3 for Code2 
        self.tab3_layout=QVBoxLayout()
        self.textedit2=QPlainTextEdit(readOnly=True)
        self.text2=open('plot.py').read()
        self.textedit2.setPlainText(self.text2)
        self.tab3_layout.addWidget(self.textedit2)
        self.tab3.setLayout(self.tab3_layout)
       
        # create tab4 for Code3 
        self.tab4_layout=QVBoxLayout()
        self.textedit3=QPlainTextEdit(readOnly=True)
        self.text3=open('gui.py').read()
        self.textedit3.setPlainText(self.text3)
        self.tab4_layout.addWidget(self.textedit3)
        self.tab4.setLayout(self.tab4_layout)

        # create tab5 for GUI  (input textboxs and button and results)
        self.tab5_layout=QGridLayout()
        self.fig=FF()
        self.tab5_layout.addWidget(self.fig,0,0,6,6)
        self.label2=QLabel('number of steps of length(nl)')
        self.label3=QLabel('start of length (l0)')
        self.label4=QLabel('end of length (l1)')
        self.label5=QLabel('number of steps of radius (nr)')
        self.label6=QLabel('start of radius (r0)')
        self.label7=QLabel('end of radius (r1)')
        self.label8=QLabel('intrinsic impedance (z0')
        self.tab5_layout.addWidget(self.label2,7,0)
        self.tab5_layout.addWidget(self.label3,8,0)
        self.tab5_layout.addWidget(self.label4,9,0)
        self.tab5_layout.addWidget(self.label5,7,2)
        self.tab5_layout.addWidget(self.label6,8,2)
        self.tab5_layout.addWidget(self.label7,9,2)
        self.tab5_layout.addWidget(self.label8,7,4)
        self.textin2=QLineEdit("20")   # nl
        self.textin3=QLineEdit("0.2")   # l0
        self.textin4=QLineEdit("5.0")   # l1
        self.textin5=QLineEdit("10")   # nr
        self.textin6=QLineEdit("0.002")   # r0
        self.textin7=QLineEdit("0.01")   # r1
        self.textin8=QLineEdit("50.0")   # z0
        self.tab5_layout.addWidget(self.textin2,7,1)
        self.tab5_layout.addWidget(self.textin3,8,1)
        self.tab5_layout.addWidget(self.textin4,9,1)
        self.tab5_layout.addWidget(self.textin5,7,3)
        self.tab5_layout.addWidget(self.textin6,8,3)
        self.tab5_layout.addWidget(self.textin7,9,3)
        self.tab5_layout.addWidget(self.textin8,7,5)
        # set up button to trigger the action
        self.but1=QPushButton('Click to Refresh Plot')
        self.but1.setStyleSheet("font-size:20px;background-color:#FFFFFF")
        self.but1.setFixedSize(400,25)
        self.but1.clicked.connect(self.plotting)
        self.tab5_layout.addWidget(self.but1,8,4,1,2) 
        # set up progress bar     
        self.progress=QProgressBar()
        self.tab5_layout.addWidget(self.progress,9,4,1,2)
        # add tab5_layout to tab5
        self.tab5.setLayout(self.tab5_layout)
        # add tabs to layout1 and add layout1 to mainW1
        self.layout1.addWidget(self.tabs)
        self.layout1.setAlignment(Qt.AlignCenter)
        self.mainW1.setLayout(self.layout1)
        # adjust size and position of mainW1
        self.mainW1.resize(1100,560)
        self.mainW1.move(10,30)

    def updatebar(self):
        self.progress.setValue(plot.prog)
        self.but1.setText('Click to Refresh Plot')
        
    @pyqtSlot()
    def aboutact(self):
        resp=QMessageBox.question(self,'About','This GUI is designed to demonstrate Navier-Stokes-based Channel Flow Analysis',QMessageBox.Ok)
 
    @pyqtSlot()
    def plotting(self):
        #reset progressbar
        self.but1.setText('Updating ...')
        self.progress.setValue(0)
        
        #collect values from textinputs adn assign to navierstokes.vars
        self.fig.nl=int(self.textin2.text())
        self.fig.l0=float(self.textin3.text())
        self.fig.l1=float(self.textin4.text())
        self.fig.nr=int(self.textin5.text())
        self.fig.r0=float(self.textin6.text())
        self.fig.r1=float(self.textin7.text())
        self.fig.z0=float(self.textin8.text())
        #place recomputation function to a THREAD object       
        self.threadobj1=ThreadClass1()
        self.threadobj1.val.connect(self.updatebar)   # update plots (!only write func name in ())
        self.threadobj1.finished.connect(self.threadobj1.deleteLater)  # delete thread objects (not self.) after executing
        self.threadobj1.start()
        self.fig.updatefig()   # progressBar will update after the main thread finished

# ****** Thread Class for Loop Execution******

class ThreadClass1(QThread):
    val=pyqtSignal()    
    def __init__(self, parent=None):
      super(ThreadClass1, self).__init__(parent)
    def run(self):
        self.val.emit()

                                
if __name__=="__main__":
	qApp = QApplication(sys.argv)
	aw = App()
	aw.show()
	sys.exit(qApp.exec_())



import sys
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

import plot


class App(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Channel Flow - Navier-Stokes')
        self.setGeometry(50,50,800,600)

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
        # add tab1 and tab2 to tabs
        self.tabs.addTab(self.tab1,'Introduction')
        self.tabs.addTab(self.tab2,'Code 1: Navier-Stokes')
        self.tabs.addTab(self.tab3,'Code 2: GUI')
        self.tabs.addTab(self.tab4,'GUI')
	
        # create tab1 for intro with pdf file scroll bar      
        '''
        self.tab1_layout=QVBoxLayout()
        self.scrollArea=QScrollArea()
        self.pix1=QPixmap('eq.jpg')
        self.pix1r=self.pix1.scaledToWidth(700)            # rescale pixmap
        self.label1=QLabel()
        self.label1.setAlignment(Qt.AlignCenter)            # Center Alignment of Label
        self.label1.setPixmap(self.pix1r)
        self.scrollArea.setWidget(self.label1)
        self.tab1_layout.addWidget(self.scrollArea)
        self.tab1.setLayout(self.tab1_layout)
       
         # create tab2 for Code1 Scrollbar
        self.tab2_layout=QVBoxLayout()
        self.textedit1=QPlainTextEdit(readOnly=True)
        self.text1=open('navierstokes.py').read()
        self.textedit1.setPlainText(self.text1)
        self.tab2_layout.addWidget(self.textedit1)
        self.tab2.setLayout(self.tab2_layout)

        # create tab3 for Code2 Scrollbar
        self.tab3_layout=QVBoxLayout()
        self.textedit2=QPlainTextEdit(readOnly=True)
        self.text2=open('gui.py').read()
        self.textedit2.setPlainText(self.text2)
        self.tab3_layout.addWidget(self.textedit2)
        self.tab3.setLayout(self.tab3_layout)'''

        # create tab4 for GUI  (input textboxs and button and results)
        self.tab4_layout=QGridLayout()
        nl=20 # number of scanned points for length
        nr=10 # number of scanned points for radius
        lengths=np.linspace(0.2, 5.0, nl)
        radii=np.linspace(0.002, 0.01, nr)
        z0=50 # instrinsic impedance
        reflections=np.zeros((nl,nr))
        reflections=plot.compute(nl,nr,lengths,radii,z0)
        self.fig1, self.fig2=plot.plot(lengths, radii, reflections)
        self.tab4_layout.addWidget(self.fig1,0,0,6,4)
        # define labels and textinputs to accept the updated vars
        self.label2=QLabel('width of channel (wd)')        
        self.label3=QLabel('height of channel (ht)')
        self.label4=QLabel('viscosity (nu)')
        self.label5=QLabel('density (rho)')
        self.label6=QLabel('initial condition (F)')
        self.tab4_layout.addWidget(self.label2,7,0)
        self.tab4_layout.addWidget(self.label3,7,2)
        self.tab4_layout.addWidget(self.label4,8,0)
        self.tab4_layout.addWidget(self.label5,8,2)
        self.tab4_layout.addWidget(self.label6,9,0)
        self.textin2=QLineEdit("3.0")   # wd
        self.textin3=QLineEdit("5.0")   # ht
        self.textin4=QLineEdit("0.1")   # nu
        self.textin5=QLineEdit("1.0")   # rho
        self.textin6=QLineEdit("1.0")   # F
        self.tab4_layout.addWidget(self.textin2,7,1)
        self.tab4_layout.addWidget(self.textin3,7,3)
        self.tab4_layout.addWidget(self.textin4,8,1)
        self.tab4_layout.addWidget(self.textin5,8,3)
        self.tab4_layout.addWidget(self.textin6,9,1)
        # set up button to trigger the action
        self.but1=QPushButton('Plot')
        self.but1.clicked.connect(self.plotting)
        self.tab4_layout.addWidget(self.but1,10,0,2,4) 
        # add tab4_layout to tab4
        self.tab4.setLayout(self.tab4_layout)

        # add tabs to layout1 and add layout1 to mainW1
        self.layout1.addWidget(self.tabs)
        self.layout1.setAlignment(Qt.AlignCenter)
        self.mainW1.setLayout(self.layout1)
        # adjust size and position of mainW1
        self.mainW1.resize(760,560)
        self.mainW1.move(10,30)

    @pyqtSlot()
    def aboutact(self):
        resp=QMessageBox.question(self,'About','This GUI is designed to demonstrate Navier-Stokes-based Channel Flow Analysis',QMessageBox.Ok)
     
    @pyqtSlot()
    def plotting(self):
        #collect values from textinputs adn assign to navierstokes.vars
        navierstokes.wd=float(self.textin2.text())
        navierstokes.ht=float(self.textin3.text())
        navierstokes.nu=float(self.textin4.text())
        navierstokes.rho=float(self.textin5.text())
        navierstokes.F=float(self.textin6.text())
        #recompute and redraw the plot       
        self.fig.updatefig()   # update plots
                                
if __name__=="__main__":
	qApp = QApplication(sys.argv)
	aw = App()
	aw.show()
	sys.exit(qApp.exec_())



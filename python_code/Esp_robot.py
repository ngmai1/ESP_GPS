##################################################
# AIPS - Asia integrated planning system
# Author: ngmai1
# Email: ngoi.mai1@hanes.com
# Build window application for supporting personal task
# Important!!!-----> This is starting file to open UI
##################################################
from PyQt5.QtWidgets import (QWidget, QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QMessageBox, QTableWidget, QHeaderView)
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QPoint, QDateTime, QRect
from PyQt5 import (QtWidgets, QtGui, QtCore)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

import pandas as pd
from main_ui import Ui_MainWindow
import time
# import pyodbc
from datetime import datetime, timedelta,date
import os, sys
# =============> for local ap start from here
# import sqlite3
# import requests
# import json

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QtGui.QIcon('bom.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        url = QUrl.fromUserInput("D:/Git/ESP_GPS/python_code/map.html")
        self.ui.widget_web.load(url)
        self.init_event()

    def init_event(self):
        self.load_form()



    def load_form(self):
        print('form have been load')



    # def thread_get_sku_signal(self,style,color,acolor,asize,apack):
    #     if color=='':
    #         self.ui.cb_bom_color.blockSignals(True)
    #         self.ui.cb_bom_color.clear()
    #         self.ui.cb_bom_color.addItems(sorted(acolor))
    #         self.ui.cb_bom_color.blockSignals(False)
    #     if len(acolor)==0:
    #         self.ui.cb_bom_color.clear()
    #         cmd=f"""========>   Finised refresh SKU for selling {style} have no BOM APS set up"""
    #     self.ui.cb_bom_size.clear()
    #     size_array=sorted(asize)
    #     size_array.append('ALL')
    #     self.ui.cb_bom_size.addItems(size_array)
    #     self.ui.cb_bom_packaging.clear()
    #     self.ui.cb_bom_packaging.addItems(sorted(apack))
    #     cmd=f"""========>   Finised refresh SKU for selling {style}"""
    #     self.ui.lbl_bom_status.setText(cmd)

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app=QApplication([])
# app.setAttribute(Qt.AA_EnableHighDpiScaling)
application=MyWindow()
application.setWindowIcon(QtGui.QIcon('bom.ico'))
trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('bom.ico'), app)
trayIcon.show()
application.show()
sys.exit(app.exec())
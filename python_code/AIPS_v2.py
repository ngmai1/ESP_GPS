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

import pandas as pd
from AIPS_UI import Ui_MainWindow
import time
import pyodbc
from datetime import datetime, timedelta,date
import os, sys
# =============> for local ap start from here
import sqlite3
import requests
import json

source_server='HBIVM-953/local-app'

path_new='C:/AIPS/'
link='C:\\AIPS_Local_Data'
if os.path.exists(link):
    print('second time')
else:
    os.mkdir(link)
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QtGui.QIcon('bom.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tb_bom_data=pd.DataFrame()
        self.tb_bom_name=''
        self.excel_bom_selected=''
        self.init_event()

    def init_event(self):
        self.load_form()
        self.ui.btn_bom_preview.clicked.connect(self.preview_bom_btn_clicked)
        self.ui.txt_bom_selling.returnPressed.connect(lambda:self.get_selling_sku(1))
        self.ui.cb_bom_color.currentTextChanged.connect(lambda:self.get_selling_sku(2))
        self.ui.btn_bom_export_excel.clicked.connect(self.export_excel_bom_btn_clicked)
        self.ui.btn_bom_explosion_excel.clicked.connect(self.explosion_bom_btn_clicked)


    def load_form(self):
        print('form have been load')
        self.ui.lbl_bom_status.setText('========>   Welcome to AIPS application!!!')
        # self.ui.cb_bom_plant.addItems(['90','93','95'])
        self.ui.cb_bom_plant.addItems(['93'])
        self.ui.txt_bom_selling.setText('')


    def select_from_sqlite(query):
        local_db = sqlite3.connect('AIPS_local_db.sqlite3')
        data = pd.read_sql(query, local_db)
        local_db.close()
        return data


    def loadData_tbl_bom(self,data):
        self.tb_bom_data=data
        header=data.columns.values
        self.ui.tbl_bom.setRowCount(0)
        self.ui.tbl_bom.setColumnCount(len(header))
        for i in range(0,len(data)):
            self.ui.tbl_bom.insertRow(i)
            for j in range(0,len(header)):
                cell_value=str(data.iloc[i,j])
                if str(data.iloc[i,j])=='None':
                    cell_value=''
                self.ui.tbl_bom.setItem(i,j,QtWidgets.QTableWidgetItem(cell_value))
        self.ui.tbl_bom.setHorizontalHeaderLabels(header)
        self.ui.tbl_bom.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Customize header font size
        headers = self.ui.tbl_bom.horizontalHeader()  # Access the horizontal header
        font = headers.font()  # Get the current font
        font.setPointSize(13)  # Set the font size to 14 points
        font.setBold(True)
        headers.setFont(font)  # Apply the modified font to the header

    def export_excel_bom_btn_clicked(self):
        data_export=self.tb_bom_data
        if len(data_export)==0:
            QMessageBox.about(self, 'Attention',"No data to export to Excel")
        else:
            cmd=f"""========>   Start writing file......"""
            self.ui.lbl_bom_status.setText(cmd)
            runtime=datetime.now()
            rtime=runtime.strftime('%y%m%d_%H%M%S')
            filename=link+'\\'+self.tb_bom_name+rtime+'.xlsx'
            writer = pd.ExcelWriter(filename, engine='openpyxl')
            data_export.to_excel(writer, sheet_name="tb_bom_data", index=False)  # done, update to db
            writer.close()
            cmd=f"""========>   file saved\n
                {filename}
            """
            self.ui.lbl_bom_status.setText(cmd)

    def get_selling_sku(self,action):
        style=self.ui.txt_bom_selling.text()
        style=str(style).upper()
        self.ui.txt_bom_selling.setText(style)
        if action==1:
            color=''
            self.loadData_tbl_bom(pd.DataFrame())
        if action==2:
            color=self.ui.cb_bom_color.currentText()
        self.ui.lbl_bom_status.setText('========>   start query sku')
        self.thread_get_sku = thread_query_Bom_sku(style,color)
        self.thread_get_sku.signal.connect(self.thread_get_sku_signal)
        self.thread_get_sku.start()
    
    def thread_get_sku_signal(self,style,color,acolor,asize,apack):
        if color=='':
            self.ui.cb_bom_color.blockSignals(True)
            self.ui.cb_bom_color.clear()
            self.ui.cb_bom_color.addItems(sorted(acolor))
            self.ui.cb_bom_color.blockSignals(False)
        if len(acolor)==0:
            self.ui.cb_bom_color.clear()
            cmd=f"""========>   Finised refresh SKU for selling {style} have no BOM APS set up"""
        self.ui.cb_bom_size.clear()
        size_array=sorted(asize)
        size_array.append('ALL')
        self.ui.cb_bom_size.addItems(size_array)
        self.ui.cb_bom_packaging.clear()
        self.ui.cb_bom_packaging.addItems(sorted(apack))
        cmd=f"""========>   Finised refresh SKU for selling {style}"""
        self.ui.lbl_bom_status.setText(cmd)

    def preview_bom_btn_clicked(self):
        style=self.ui.txt_bom_selling.text()
        color=self.ui.cb_bom_color.currentText()
        size=self.ui.cb_bom_size.currentText()
        pack=self.ui.cb_bom_packaging.currentText()
        plant=self.ui.cb_bom_plant.currentText()
        self.tb_bom_name=f"""BOM_{style}_{color}_{size}_{pack}_{plant}_detail_"""
        cmd=f"""========>   Finding BOM {style} - {color} - {size} - {pack} - {plant}. please wait...."""
        self.ui.lbl_bom_status.setText(cmd)
        self.loadData_tbl_bom(pd.DataFrame())
        if style=='' or color=='' or size=='' or pack=='':
            QMessageBox.about(self, 'Attention',"Please type in selling style and press enter to refresh sku first!!!")
        else:
            self.thread_query_BOM_preview = thread_query_BOM_preview(style,color,size,pack,plant)
            self.thread_query_BOM_preview.signal.connect(self.thread_query_BOM_preview_signal)
            self.thread_query_BOM_preview.start()
    
    def thread_query_BOM_preview_signal(self,datatable):
        cmd=f"""========>   Finised get BOM with {len(datatable)} rows"""
        self.ui.lbl_bom_status.setText(cmd)
        self.loadData_tbl_bom(datatable)
            
    def explosion_bom_btn_clicked(self):
        print('select file')
        filenames, _ = QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileNames()",
            "",
            "All Files (*);;Text Files (*.xlsx)",
        )
        if filenames:
            # for filename in filenames:
            file_select = str(filenames[0]).replace('/', '\\')
            print(file_select)
            if file_select[-5:]==".xlsx":
                cmd='excel file selected \n'+file_select
                self.ui.lbl_bom_status.setText(cmd)
                self.excel_bom_selected=file_select
                input_data=pd.read_excel(file_select)
                self.loadData_tbl_bom(input_data)
                conn = sqlite3.connect('AIPS_local_db.sqlite3')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM SKU_EXCEL_BOM_EXPLOSION')
                conn.commit()
                conn.close()
                # Disable all user interaction
                self.setEnabled(False)
                self.thread_excel_bom_explosion = excel_bom_explosion(input_data)
                self.thread_excel_bom_explosion.signal.connect(self.thread_excel_bom_explosion_signal)
                self.thread_excel_bom_explosion.start()
                # self.thread_excel_bom_explosion.wait()
                # Enable all user interaction
                
            else:
                cmd='Opps!\nPlease select xlsx file in right format'
                self.ui.lbl_bom_status.setText(cmd)
        else:
            self.ui.lbl_bom_status.setText('No file selected')     
    
    def thread_excel_bom_explosion_signal(self,cmd):
        self.ui.lbl_bom_status.setText(cmd)
        print(cmd)
        if 'save data at' in cmd:
            link='C:\\AIPS_Local_Data\\Excel_BOM_Explosion\\'
            cmd='Finished export BOM explosion to excel file\n'+link
            self.ui.lbl_bom_status.setText(cmd)
            # export bom explosion to excel
            print('start export bom explosion to excel')
            local_db = sqlite3.connect('AIPS_local_db.sqlite3')
            query_exp=f"""SELECT * FROM SKU_EXCEL_BOM_EXPLOSION"""
            data_exp = pd.read_sql(query_exp, local_db)
            local_db.close()
            if len(data_exp)>0:
                link='C:\\AIPS_Local_Data\\Excel_BOM_Explosion\\'
                if os.path.exists(link):
                    print('second time')
                else:
                    os.mkdir(link)
                current_time=datetime.now().strftime('%y%m%d_%H%M%S')
                file_export=link+'\\Excel_BOM_Explosion_'+current_time+'.xlsx'
                writer = pd.ExcelWriter(file_export, engine='openpyxl')
                data_exp.to_excel(writer, sheet_name="excel_bom_data", index=False)  # done, update to db
                writer.close()
                cmd='Finished export BOM explosion to excel file\n'+file_export
                self.ui.lbl_bom_status.setText(cmd)
                self.setEnabled(True)




class excel_bom_explosion(QtCore.QThread):
    signal = pyqtSignal(str)
    def __init__(self,input_data):
        super(excel_bom_explosion, self).__init__()
        self.input_data=input_data

    def insert_into_sqlite(self,query):
        conn = sqlite3.connect('AIPS_local_db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def run(self):
        self.signal.emit('đang tổng hợp dữ liệu ...')
        sku_input=self.input_data
        for s in range(0,len(sku_input)):
            wo=('000000'+str(sku_input.iloc[s,0]))[-6:]
            style=str(sku_input.iloc[s,1])
            color=str(sku_input.iloc[s,2])
            size=str(sku_input.iloc[s,3])
            pack=str(sku_input.iloc[s,4])
            plant=str(sku_input.iloc[s,5])
            qty=int(sku_input.iloc[s,6])
            cmd=f"""---> Processing BOM {s+1} / {len(sku_input)} ==> {style} - {color} - {size} - {pack} - {plant}. please wait...."""
            self.signal.emit(cmd)
            url='http://hbivm-953/local-app/get_bom_sku_detail_by_size'
            data={'style':style,'color':color,'size':size,'pack':pack,'plant':plant}
            print(data)
            response=requests.post(url,data=data)
            try:
                response_dict = json.loads(response.text)
                data_frame=pd.DataFrame(response_dict)
            except:
                data_frame=pd.DataFrame()
            # print(data_frame)
            data_frame['ACT_CONSUMP']=data_frame['ACT_CONSUMP']*qty/data_frame['ORDERED']
            data_frame['MFG_QTY']=(data_frame['MFGU']*qty/data_frame['PACK_QTY']).astype(int)
            data_frame['ORDERED']=qty
            data_frame['WORKORDER']=wo
            cmd=f"""========> {s+1} / {len(sku_input)}   Finised get BOM with {len(data_frame)} rows"""
            for d in range(0,len(data_frame)):
                value_x="'"
                header=data_frame.columns.values
                for x in range(0,len(header)-1):
                    value_x=value_x+str(data_frame.iloc[d,x])+"','"
                last_value=int(len(header)-1)
                value_x=value_x+str(data_frame.iloc[d,last_value])+"'"
                sql_insert=f"""
                INSERT INTO SKU_EXCEL_BOM_EXPLOSION VALUES
                ({value_x})
                """
                sql_insert=sql_insert.replace("'None'","NULL")
                # print(sql_insert)
                self.insert_into_sqlite(sql_insert)
        self.signal.emit('đã xử lý xong dữ liệu ---> save data at ...')


        
class thread_query_Bom_sku(QtCore.QThread):
    signal = pyqtSignal(str,str,list,list,list)
    def __init__(self,style,color):
        super(thread_query_Bom_sku, self).__init__()
        self.style=style
        self.color=color
    def run(self):
        acolor=[]
        asize=[]
        apack=[]
        url='http://hbivm-953/local-app/get_prod1_sku_by_selling'
        data={'selling':self.style,'color':self.color}
        response=requests.post(url,data=data)
        response_dict = json.loads(response.text)

        for x in response_dict:
            if len(acolor)==0:
                acolor.append(x['PARENT_COLOR'])
                asize.append(x['PARENT_SIZE'])
                apack.append(x['COMP_STYLE_CD'])
            else:
                if x['PARENT_COLOR'] not in acolor:
                    acolor.append(x['PARENT_COLOR'])
                if x['PARENT_SIZE'] not in asize:
                    asize.append(x['PARENT_SIZE'])
                if x['COMP_STYLE_CD'] not in apack:
                    apack.append(x['COMP_STYLE_CD'])
        self.signal.emit(self.style,self.color,acolor,asize,apack)


class thread_query_BOM_preview(QtCore.QThread):
    signal = pyqtSignal(pd.DataFrame)
    def __init__(self,style,color,size,pack,plant):
        super(thread_query_BOM_preview, self).__init__()
        self.style=style
        self.color=color
        self.size=size
        self.pack=pack
        self.plant=plant
    def run(self):
        url='http://hbivm-953/local-app/get_bom_sku_detail_by_size'
        data={'style':self.style,'color':self.color,'size':self.size,'pack':self.pack,'plant':self.plant}
        response=requests.post(url,data=data)
        response_dict = json.loads(response.text)
        data_frame=pd.DataFrame(response_dict)
        self.signal.emit(data_frame)



app=QApplication([])
app.setAttribute(Qt.AA_EnableHighDpiScaling)
application=MyWindow()
application.setWindowIcon(QtGui.QIcon('bom.ico'))
trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('bom.ico'), app)
trayIcon.show()
application.show()
sys.exit(app.exec())
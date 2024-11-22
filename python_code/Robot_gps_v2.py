import sys
import subprocess
import folium
from PyQt5.QtWidgets import (QWidget, QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QMessageBox, QTableWidget, QHeaderView)
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QPoint, QDateTime, QRect, pyqtSlot
from PyQt5 import (QtWidgets, QtGui, QtCore)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

import time
import socket
import netifaces

from flask import Flask,request,jsonify
import pandas as pd
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine

from main_ui import Ui_MainWindow

import os
# Get the current working directory
current_path = os.getcwd()
print(f"The current working directory is: {current_path}")
current_path.replace("\\","/")
current_map=current_path+'/map_render/map.html'
export_map=current_path+'/exported_map/map_report_expoted.html'
print(current_map)


engine_ttp = create_engine('mysql+mysqlconnector://ttpdept:plcgpsd@localhost:3306/ttp', echo=False)
mydb=mysql.connector.connect(host="localhost", user='ttpdept', passwd='plcgpsd', database="ttp")
myCursor=mydb.cursor()
rs_angle_server="OK"
time_query="xxxx-xx-xx xx:xx:xx"
connected_esp=0
global_ip='192.168.8.250'
# global_ip='127.0.0.1'
# Flask app
# flask_app = Flask(__name__)

sql_update_stop=f"""
    update ttp.tracking_log set stoptime=now() where stoptime is null;
"""
myCursor.execute(sql_update_stop)
mydb.commit()



def get_all_ip_addresses():
    ip_addresses = []
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ip_addresses.append(addresses[netifaces.AF_INET][0]['addr'])


    return ip_addresses


ip_address=get_all_ip_addresses()
print(ip_address)


class FlaskThread(QThread):
    update_log = pyqtSignal(str,str,str,str,str,str)

    def __init__(self, parent=None):
        super(FlaskThread, self).__init__(parent)
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route('/')
        def index():
            return "Server ESP server is running!"

        @self.flask_app.route('/esp32', methods=['POST'])
        def esp32():
            # Get the posted data
            global rs_angle_server
            data = request.get_json()  # Assuming the client sends JSON data
            print('Data received from client:')
            print(data)
            latitude=data.get('latitude')
            longitude=data.get('longitude')
            angle=data.get('angle')
            rs_angle=data.get('rs_angle')
            if rs_angle=="OK1":
                rs_angle_server="OK"
            utc=data.get('utc')
            gps_date=data.get('gps_date')
            print(latitude,longitude,angle,rs_angle,utc,gps_date)
            self.update_log.emit(latitude,longitude,angle,rs_angle,utc,gps_date)
            print('emmited')
            if longitude!="" and latitude !="" and "." in latitude and "." in longitude:
                sql_insert=f"""
                insert into ttp.robot_wifi_gps
                (timeupdate,latitude,longitude,utc,gps_date,angle,rs_status)
                values
                (now(),"{latitude}","{longitude}","{utc}","{gps_date}","{angle}","{rs_angle}")
                """
                myCursor.execute(sql_insert)
                mydb.commit()
                print(sql_insert)
            if rs_angle_server=="RS":
                return jsonify({"rs_angle": rs_angle_server})
            else:
                return 'Data received!', 200

    @pyqtSlot()
    def run(self):
        self.flask_app.run(host=global_ip, port=3000,debug=True, use_reloader=False)
        print('server have run')

    # def emit_data(self,latitude,longitude,angle,rs_angle,utc,gps_date):
    #     self.update_log.emit(latitude,longitude,angle,rs_angle,utc,gps_date)

    # @pyqtSlot()

    


class refresh_time_sys(QThread):
    time_string = pyqtSignal(str)

    def __init__(self, parent=None):
        super(refresh_time_sys, self).__init__(parent)

    @pyqtSlot()
    def run(self):
        while True:
            # Get the current date and time
            now = datetime.now()
            # Format it as "yyyy-mm-dd HH:MM:SS"
            formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            # print(formatted_date_time)
            self.time_string.emit(formatted_date_time)
            time.sleep(1)

class export_data_excel(QThread):
    exported_path = pyqtSignal(str)

    def __init__(self, starttime):
        super(export_data_excel, self).__init__()
        self.starttime=starttime

    @pyqtSlot()
    def run(self):
        stoptime_qr=f"""select stoptime,tracking_note from ttp.tracking_log where starttime="{self.starttime}"
        """
        # while True:
        #     # Get the current date and time
        #     now = datetime.now()
        #     # Format it as "yyyy-mm-dd HH:MM:SS"
        #     formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #     self.exported_path.emit(formatted_date_time)
        #     time.sleep(1)



class draw_map(QThread):
    map_exported = pyqtSignal(str)
    map_data = pyqtSignal(pd.DataFrame)

    def __init__(self, data=None):
        super(draw_map, self).__init__(data)

    @pyqtSlot()
    def run(self):
        global time_query
        global connected_esp
        m=4
        while True:
            try:
            # if 1>0:
                if m<4:
                    m=m+1
                    time.sleep(5)
                    continue
                m=1
                if connected_esp==0:
                    time.sleep(5)
                    continue
                print("draw map time",time_query)
                if time_query=="xxxx-xx-xx xx:xx:xx":
                    last_10_sql="""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps where latitude like '%.%' and longitude like '%.%'
                    order by timeupdate desc limit 300;
                    """
                else:
                    last_10_sql=f"""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps 
                    where timeupdate>="{time_query}" and latitude like '%.%' and longitude like '%.%' 
                    order by timeupdate desc limit 300;
                    """
                print(last_10_sql)
                data=pd.read_sql(last_10_sql,engine_ttp)

                var_lat=0.08
                var_long=0.08
                # process lọc dữ liệu
                fdata=pd.DataFrame()
                if len(data)>1:
                    last_lat=float(data.iloc[0,1])
                    last_long=float(data.iloc[0,2])
                    i=1
                    while i<len(data)-1:
                        pre_lat=float(data.iloc[i,1])
                        pre_long=float(data.iloc[i,2])
                        if abs(last_lat-pre_lat)<var_lat and abs(last_long-pre_long)<var_long:
                            temp_row=data.iloc[[i]]
                            fdata=pd.concat([fdata,temp_row], axis=0, ignore_index=True)
                            last_lat=float(data.iloc[i,1])
                            last_long=float(data.iloc[i,2])
                        i=i+1




                    data=fdata
                    top_20_data=data.head(15)
                    print(top_20_data)
                    top_20_data['latitude']=top_20_data['latitude']+" N"
                    top_20_data['longitude']=top_20_data['longitude']+" E"
                    # print(top_20_data)
                    self.map_data.emit(top_20_data)

                    data['lat_x']=data['latitude'].str.split('.').str[0]
                    data['lat_3']=data['latitude'].str.split('.').str[1]
                    data['lat_1']=data['lat_x'].str[:-2]
                    data['lat_2']=data['lat_x'].str[-2:]
                    data['lat_4']=data['lat_2']+'.'+data['lat_3']
                    data['lat']=data['lat_1'].astype(float)+data['lat_4'].astype(float)/60

                    data['lon_x']=data['longitude'].str.split('.').str[0]
                    data['lon_3']=data['longitude'].str.split('.').str[1]
                    data['lon_1']=data['lon_x'].str[:-2]
                    data['lon_2']=data['lon_x'].str[-2:]
                    data['lon_4']=data['lon_2']+'.'+data['lon_3']
                    data['lon']=data['lon_1'].astype(float)+data['lon_4'].astype(float)/60

                    # Convert DataFrame to a list of coordinates
                    coordinates = data[['lat', 'lon']].values.tolist()
                    # Create a polyline and add it to the map


                    # # List of coordinates (latitude, longitude)
                    # coordinates = [
                    #     (16.4564251667, 107.5851955),
                    #     (16.467700, 107.591703),
                    #     # Add more coordinates as needed
                    # ]

                    # Create a map centered around the first coordinate
                    my_map = folium.Map(location=coordinates[0], zoom_start=16)

                    # Add points to the map
                    for coordinate in coordinates:
                        folium.Marker(location=coordinate).add_to(my_map)
                        break

                    # Add a line connecting the points
                    folium.PolyLine(locations=coordinates, color="blue", weight=5).add_to(my_map)



                    # Save the map to an HTML file
                    
                    my_map.save(current_map)

                    if 1>2:
                        # Read the generated map.html file
                        with open('map.html', 'r') as file:
                            map_html = file.read()

                        # JavaScript for auto-refresh
                        auto_refresh_script = '''
                        <script type="text/javascript">
                            // Function to refresh the page every 60 seconds
                            function autoRefresh() {
                                setTimeout(function() {
                                    location.reload();
                                }, 15000); // 30000 milliseconds = 60 seconds
                            }
                            // Call the function when the page loads
                            window.onload = autoRefresh;
                        </script>
                        '''

                        # Insert the auto-refresh script before the closing </head> tag
                        map_html = map_html.replace('</head>', auto_refresh_script + '</head>')

                        # Save the modified HTML back to the file
                        with open('map.html', 'w') as file:
                            file.write(map_html)
                    self.map_exported.emit('finished update map')
            except:
            # else:
                self.map_exported.emit('map update error')
                time.sleep(5)




class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('direct.ico'))
        self.flask_thread = FlaskThread()
        self.draw_map= draw_map()
        self.refresh_time_sys=refresh_time_sys()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        url = QUrl.fromUserInput(current_map)
        self.ui.widget_web.load(url)
        self.init_event()

    def init_event(self):
        if 1>2: #test draw map
            # Connect signals
            self.flask_thread.update_log.connect(self.append_log_flask)
            # # Start threads
            self.flask_thread.start()
        # connect draw map signal
        self.draw_map.map_exported.connect(self.update_map)
        self.draw_map.map_data.connect(self.loadData_tbl)
        self.draw_map.start()

        self.refresh_time_sys.time_string.connect(self.update_time)
        self.refresh_time_sys.start()

        self.load_form()

    def load_form(self):
        print('form have been load')

        self.ui.btn_rs_angle.clicked.connect(self.reset_angle)
        self.ui.btn_start_record.clicked.connect(self.start_record)
        self.ui.btn_stop_record.clicked.connect(self.stop_record)
        self.ui.btn_connect_esp.clicked.connect(self.turn_on_web_server)
        self.ui.tabWidget.currentChanged.connect(self.load_time_start)
        self.ui.btn_export_map.clicked.connect(self.export_map_preview)
        self.ui.btn_export_report.clicked.connect(self.export_report_excel)
        print('should be work if get here')

    def export_report_excel(self):
        time_start=self.ui.combo_start_time_2.currentText()
        # get time stop
        query_tstop=f"""
            SELECT DATE_FORMAT(stoptime, '%Y-%m-%d %H:%i:%s') AS formatted_datetime,tracking_note
            FROM ttp.tracking_log where starttime='{time_start}';
        """
        tstop=pd.read_sql(query_tstop,engine_ttp)
        time_stop=time_start
        tracking_note=''
        if len(tstop)>0:
            time_stop=tstop.iloc[0,0]
            tracking_note=str(tstop.iloc[0,1])
            self.ui.lbl_track_note_export_2.setText(tracking_note)
        if time_start!=time_stop:
            last_report_sql=f"""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps 
                    where timeupdate>="{time_start}" and timeupdate<"{time_stop}" and latitude like '%.%' and longitude like '%.%' 
                    order by timeupdate desc;
                    """
        else:
            last_report_sql=f"""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps 
                    where timeupdate>="{time_start}" and timeupdate<="{time_stop}" and latitude like '%.%' and longitude like '%.%' 
                    order by timeupdate desc;
                    """
        print(last_report_sql)
        rdata=pd.read_sql(last_report_sql,engine_ttp)

        var_lat=0.08
        var_long=0.08
        try:
            var_lat=float(self.ui.txt_lat_var)
            var_long=float(self.ui.txt_long_var)
        except:
            print('wrong value setup for lat - long')
        # process lọc dữ liệu
        rfdata=pd.DataFrame()
        if len(rdata)>1:
            rlast_lat=float(rdata.iloc[0,1])
            rlast_long=float(rdata.iloc[0,2])
            ri=1
            while ri<len(rdata)-1:
                rpre_lat=float(rdata.iloc[ri,1])
                rpre_long=float(rdata.iloc[ri,2])
                if abs(rlast_lat-rpre_lat)<var_lat and abs(rlast_long-rpre_long)<var_long:
                    rtemp_row=rdata.iloc[[ri]]
                    rfdata=pd.concat([rfdata,rtemp_row], axis=0, ignore_index=True)
                    rlast_lat=float(rdata.iloc[ri,1])
                    rlast_long=float(rdata.iloc[ri,2])
                ri=ri+1
        file_name=current_path+'/report/GPS_DATA_'+time_start.replace(":","")+'.xlsx'
        print(file_name)
        rfdata.to_excel(file_name,index=False)
        msg_txt="file data đã được lưu tại\n"+file_name
        QMessageBox.about(self, 'Chú ý',msg_txt)
        

    def export_map_preview(self):
        time_start=self.ui.combo_start_time_2.currentText()
        # get time stop
        query_tstop=f"""
            SELECT DATE_FORMAT(stoptime, '%Y-%m-%d %H:%i:%s') AS formatted_datetime,tracking_note
            FROM ttp.tracking_log where starttime='{time_start}';
        """
        tstop=pd.read_sql(query_tstop,engine_ttp)
        time_stop=time_start
        tracking_note=''
        if len(tstop)>0:
            time_stop=tstop.iloc[0,0]
            tracking_note=str(tstop.iloc[0,1])
            self.ui.lbl_track_note_export_2.setText(tracking_note)
        if time_start!=time_stop:
            last_report_sql=f"""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps 
                    where timeupdate>="{time_start}" and timeupdate<"{time_stop}" and latitude like '%.%' and longitude like '%.%' 
                    order by timeupdate desc;
                    """
        else:
            last_report_sql=f"""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps 
                    where timeupdate>="{time_start}" and timeupdate<="{time_stop}" and latitude like '%.%' and longitude like '%.%' 
                    order by timeupdate desc;
                    """
        print(last_report_sql)
        rdata=pd.read_sql(last_report_sql,engine_ttp)

        var_lat=0.08
        var_long=0.08
        try:
            var_lat=float(self.ui.txt_lat_var)
            var_long=float(self.ui.txt_long_var)
        except:
            print('wrong value setup for lat - long')
        # process lọc dữ liệu
        rfdata=pd.DataFrame()
        if len(rdata)>1:
            rlast_lat=float(rdata.iloc[0,1])
            rlast_long=float(rdata.iloc[0,2])
            ri=1
            while ri<len(rdata)-1:
                rpre_lat=float(rdata.iloc[ri,1])
                rpre_long=float(rdata.iloc[ri,2])
                if abs(rlast_lat-rpre_lat)<var_lat and abs(rlast_long-rpre_long)<var_long:
                    rtemp_row=rdata.iloc[[ri]]
                    rfdata=pd.concat([rfdata,rtemp_row], axis=0, ignore_index=True)
                    rlast_lat=float(rdata.iloc[ri,1])
                    rlast_long=float(rdata.iloc[ri,2])
                ri=ri+1




            rdata=rfdata
            top_20_data=rdata.head(15)
            print(top_20_data)
            top_20_data['latitude']=top_20_data['latitude']+" N"
            top_20_data['longitude']=top_20_data['longitude']+" E"

            rdata['lat_x']=rdata['latitude'].str.split('.').str[0]
            rdata['lat_3']=rdata['latitude'].str.split('.').str[1]
            rdata['lat_1']=rdata['lat_x'].str[:-2]
            rdata['lat_2']=rdata['lat_x'].str[-2:]
            rdata['lat_4']=rdata['lat_2']+'.'+rdata['lat_3']
            rdata['lat']=rdata['lat_1'].astype(float)+rdata['lat_4'].astype(float)/60

            rdata['lon_x']=rdata['longitude'].str.split('.').str[0]
            rdata['lon_3']=rdata['longitude'].str.split('.').str[1]
            rdata['lon_1']=rdata['lon_x'].str[:-2]
            rdata['lon_2']=rdata['lon_x'].str[-2:]
            rdata['lon_4']=rdata['lon_2']+'.'+rdata['lon_3']
            rdata['lon']=rdata['lon_1'].astype(float)+rdata['lon_4'].astype(float)/60

            # Convert DataFrame to a list of coordinates
            rcoordinates = rdata[['lat', 'lon']].values.tolist()
            # Create a polyline and add it to the map


            # # List of coordinates (latitude, longitude)
            # coordinates = [
            #     (16.4564251667, 107.5851955),
            #     (16.467700, 107.591703),
            #     # Add more coordinates as needed
            # ]

            # Create a map centered around the first coordinate
            rmy_map = folium.Map(location=rcoordinates[0], zoom_start=16)

            # Add points to the map
            for coordinate in rcoordinates:
                folium.Marker(location=coordinate).add_to(rmy_map)
                break

            # Add a line connecting the points
            folium.PolyLine(locations=rcoordinates, color="blue", weight=5).add_to(rmy_map)



            # Save the map to an HTML file
            rmy_map.save(export_map)
            url = QUrl.fromUserInput(export_map)
            self.ui.widget_web_preview.load(url)
        
        # draw map



    def load_time_start(self,index):
        # load list start time
        current_tab_text = self.ui.tabWidget.tabText(index)
        print(f"Tab '{current_tab_text}' activated.")

        # Trigger an alert (you can customize this to your needs)
        if current_tab_text == "Báo cáo":
            print("Tab 2 is active!")
            sql_time_start="""
            SELECT DATE_FORMAT(starttime, '%Y-%m-%d %H:%i:%s') AS formatted_datetime
            FROM ttp.tracking_log order by starttime desc;
            """
            time_data=pd.read_sql(sql_time_start,engine_ttp)
            if len(time_data)>0:
                self.ui.combo_start_time_2.clear()
                t=0
                while t<len(time_data):
                    t_data=str(time_data.iloc[t,0])
                    self.ui.combo_start_time_2.addItem(t_data)
                    t=t+1

    def turn_on_web_server(self):
        ip_address=get_all_ip_addresses()
        print(ip_address)
        # if '192.168.8.250' not in ip_address:
        if global_ip not in ip_address:
            QMessageBox.about(self, 'Chú ý',"cần kết nối với router wifi")
        else:
                        # Connect signals
            self.flask_thread.update_log.connect(self.append_log_flask)
            # # Start threads
            self.flask_thread.start()
            global connected_esp
            connected_esp=1


    def reset_angle(self):
        global rs_angle_server
        print(rs_angle_server)
        rs_angle_server="RS"
        print('reset angle clicked', rs_angle_server)

    def append_log_flask(self, lat,lon,angle,rs_angle,utc,gps_date):
        self.ui.lbl_latitude.setText("Vĩ độ: "+lat+" N")
        self.ui.lbl_longitude.setText("Kinh độ: "+lon+" E")
        self.ui.lbl_angle.setText("độ Sâu: "+angle)
        self.ui.lbl_rs_angle.setText("trạng thái rs: "+rs_angle)
        self.ui.lbl_utc_date_time.setText(utc+" - "+gps_date)
        timeupdate=self.ui.lbl_system_datetime.text()
        text_log=self.ui.lbl_web_logs.text()
        text_log+="\n"
        text_log+=f"""-{timeupdate} : {lat} N - {lon} E - Góc Trục Quay : {angle} - Rs_Angle: {rs_angle}"""
        text_log=text_log[-960:]
        self.ui.lbl_web_logs.setText(text_log)

    def update_map(self,text):
        print(text)
        url = QUrl.fromUserInput(current_map)
        self.ui.widget_web.load(url)

    def update_time(self,time_string):
        self.ui.lbl_system_datetime.setText(time_string)

    def loadData_tbl(self,data):
        self.tb_bom_data=data
        header=data.columns.values
        self.ui.tb_widget_log.setRowCount(0)
        self.ui.tb_widget_log.setColumnCount(len(header))
        for i in range(0,len(data)):
            self.ui.tb_widget_log.insertRow(i)
            for j in range(0,len(header)):
                cell_value=str(data.iloc[i,j])
                if str(data.iloc[i,j])=='None':
                    cell_value=''
                self.ui.tb_widget_log.setItem(i,j,QtWidgets.QTableWidgetItem(cell_value))
        self.ui.tb_widget_log.setHorizontalHeaderLabels(header)
        self.ui.tb_widget_log.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Customize header font size
        headers = self.ui.tb_widget_log.horizontalHeader()  # Access the horizontal header
        font = headers.font()  # Get the current font
        font.setPointSize(13)  # Set the font size to 14 points
        font.setBold(True)
        headers.setFont(font)  # Apply the modified font to the header

    def start_record(self):
        if connected_esp==0:
            QMessageBox.about(self, 'Chú ý',"Bạn cần kết nối đến Robot GPS trước")
            return
        global time_query
        print('start record')
        cr_dt=self.ui.lbl_system_datetime.text()
        print('time_query',time_query)
        note_trk=self.ui.txt_note_tracking.text()


        if note_trk=="":
            QMessageBox.about(self, 'Chú ý',"cần ghi chú lại nội dung tracking (tracking note)")
        else:
            sql_insert=f"""
            insert into ttp.tracking_log (starttime,tracking_note)
            values
            ("{cr_dt}","{note_trk}")
            """
            myCursor.execute(sql_insert)
            mydb.commit()
            self.ui.lbl_time_start.setText(cr_dt)
            time_query=cr_dt
    
    def stop_record(self):
        global time_query
        print('stop record')
        cr_dt=self.ui.lbl_system_datetime.text()
        sql_stop_record=f"""
        update ttp.tracking_log set stoptime=now() where starttime="{cr_dt}"
        """
        myCursor.execute(sql_stop_record)
        mydb.commit()
        self.ui.lbl_time_start.setText("xxxx-xx-xx xx:xx:xx")
        time_query="xxxx-xx-xx xx:xx:xx"






QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app=QApplication([])
# app.setAttribute(Qt.AA_EnableHighDpiScaling)
application=MyWindow()
application.setWindowIcon(QtGui.QIcon('direct.ico'))
trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('direct.ico'), app)
trayIcon.show()
application.show()
sys.exit(app.exec())
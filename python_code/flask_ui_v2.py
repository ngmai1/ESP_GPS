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


from flask import Flask,request,jsonify
import pandas as pd
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine

from main_ui import Ui_MainWindow


engine_ttp = create_engine('mysql+mysqlconnector://ttpdept:plcgpsd@localhost:3306/ttp', echo=False)
mydb=mysql.connector.connect(host="localhost", user='ttpdept', passwd='plcgpsd', database="ttp")
myCursor=mydb.cursor()
rs_angle_server="OK"
time_query="xxxx-xx-xx xx:xx:xx"
# Flask app
# flask_app = Flask(__name__)

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
        self.flask_app.run(host='192.168.8.250', port=3000,debug=True, use_reloader=False)

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
        m=1
        while True:
            try:
            # if 1>0:
                print("draw map time",time_query)
                if time_query=="xxxx-xx-xx xx:xx:xx":
                    last_10_sql="""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps where latitude like '%.%' and longitude like '%.%' order by timeupdate desc limit 300;
                    """
                else:
                    last_10_sql=f"""
                    select timeupdate,latitude,longitude,angle,rs_status from ttp.robot_wifi_gps 
                    where timeupdate>="{time_query}" and latitude like '%.%' and longitude like '%.%' 
                    order by timeupdate desc limit 300;
                    """
                print(last_10_sql)
                data=pd.read_sql(last_10_sql,engine_ttp)
                top_20_data=data.head(15)
                top_20_data['latitude']=top_20_data['latitude']+" N"
                top_20_data['longitude']=top_20_data['longitude']+" E"
                # print(top_20_data)
                self.map_data.emit(top_20_data)
                if m<4:
                    m=m+1
                    continue
                m=1
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
                folium.PolyLine(locations=coordinates, color="blue").add_to(my_map)



                # Save the map to an HTML file
                my_map.save('map.html')

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
                        }, 30000); // 30000 milliseconds = 60 seconds
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
                time.sleep(9)
            except:
                self.map_exported.emit('map update error')
                time.sleep(5)




class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('bom.ico'))
        self.flask_thread = FlaskThread()
        self.draw_map= draw_map()
        self.refresh_time_sys=refresh_time_sys()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        url = QUrl.fromUserInput("D:/Git/ESP_GPS/python_code/map.html")
        self.ui.widget_web.load(url)
        self.init_event()

    def init_event(self):
        # Connect signals
        self.flask_thread.update_log.connect(self.append_log_flask)
        # Start threads
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
application.setWindowIcon(QtGui.QIcon('bom.ico'))
trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('bom.ico'), app)
trayIcon.show()
application.show()
sys.exit(app.exec())
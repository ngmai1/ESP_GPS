
from flask import Flask,request,jsonify
import pandas as pd
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine

# Create a Flask app
app = Flask(__name__)
engine_ttp = create_engine('mysql+mysqlconnector://ttpdept:plcgpsd@localhost:3306/ttp', echo=False)
mydb=mysql.connector.connect(host="localhost", user='ttpdept', passwd='plcgpsd', database="ttp")
myCursor=mydb.cursor()
rs_angle_server="OK"


# Define a route for the Flask app
@app.route('/')
def index():
    return "Server ESP server is running!"


# Define a route for the POST endpoint
@app.route('/esp32', methods=['POST'])
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
    if longitude!="":
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
        return jsonify({"rs_angle": rs_angle})
    else:
        return 'Data received!', 200



# Run the server
if __name__ == '__main__':
    print('Starting server...')
    app.run(host='192.168.8.250', port=3000,debug=True)

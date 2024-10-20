# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_sc_vw2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1167, 884)
        MainWindow.setStyleSheet("background-color: rgb(0, 72, 106);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_view = QtWidgets.QWidget()
        self.tab_view.setObjectName("tab_view")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_view)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lbl_ttp = QtWidgets.QLabel(self.tab_view)
        self.lbl_ttp.setText("")
        self.lbl_ttp.setPixmap(QtGui.QPixmap("TTP.png"))
        self.lbl_ttp.setScaledContents(True)
        self.lbl_ttp.setObjectName("lbl_ttp")
        self.verticalLayout_5.addWidget(self.lbl_ttp)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.verticalLayout_5.setStretch(0, 5)
        self.verticalLayout_5.setStretch(1, 5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_utc_date_time = QtWidgets.QLabel(self.tab_view)
        self.lbl_utc_date_time.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_utc_date_time.setFont(font)
        self.lbl_utc_date_time.setStyleSheet("color: rgb(0, 255, 0);\n"
"")
        self.lbl_utc_date_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_utc_date_time.setObjectName("lbl_utc_date_time")
        self.verticalLayout_3.addWidget(self.lbl_utc_date_time)
        self.lbl_latitude = QtWidgets.QLabel(self.tab_view)
        self.lbl_latitude.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_latitude.setFont(font)
        self.lbl_latitude.setStyleSheet("color: rgb(0, 255, 0);\n"
"")
        self.lbl_latitude.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_latitude.setObjectName("lbl_latitude")
        self.verticalLayout_3.addWidget(self.lbl_latitude)
        self.lbl_longitude = QtWidgets.QLabel(self.tab_view)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_longitude.setFont(font)
        self.lbl_longitude.setStyleSheet("color: rgb(0, 255, 0);\n"
"")
        self.lbl_longitude.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_longitude.setObjectName("lbl_longitude")
        self.verticalLayout_3.addWidget(self.lbl_longitude)
        self.lbl_angle = QtWidgets.QLabel(self.tab_view)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_angle.setFont(font)
        self.lbl_angle.setStyleSheet("color: rgb(0, 255, 0);\n"
"")
        self.lbl_angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_angle.setObjectName("lbl_angle")
        self.verticalLayout_3.addWidget(self.lbl_angle)
        self.lbl_rs_angle = QtWidgets.QLabel(self.tab_view)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_rs_angle.setFont(font)
        self.lbl_rs_angle.setStyleSheet("color: rgb(0, 255, 0);\n"
"")
        self.lbl_rs_angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_rs_angle.setObjectName("lbl_rs_angle")
        self.verticalLayout_3.addWidget(self.lbl_rs_angle)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.verticalLayout_4.setStretch(0, 9)
        self.verticalLayout_4.setStretch(1, 6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_robot_pic = QtWidgets.QLabel(self.tab_view)
        self.lbl_robot_pic.setMaximumSize(QtCore.QSize(200, 200))
        self.lbl_robot_pic.setText("")
        self.lbl_robot_pic.setPixmap(QtGui.QPixmap("sim/dd.jpg"))
        self.lbl_robot_pic.setScaledContents(True)
        self.lbl_robot_pic.setObjectName("lbl_robot_pic")
        self.gridLayout_2.addWidget(self.lbl_robot_pic, 0, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.setStretch(0, 100)
        self.horizontalLayout_6.setStretch(1, 51)
        self.horizontalLayout_6.setStretch(2, 300)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem4 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.tab_view)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(241, 154, 33);\n"
"")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.lbl_system_datetime = QtWidgets.QLabel(self.tab_view)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_system_datetime.setFont(font)
        self.lbl_system_datetime.setStyleSheet("color: rgb(0, 255, 0);\n"
"")
        self.lbl_system_datetime.setObjectName("lbl_system_datetime")
        self.horizontalLayout_3.addWidget(self.lbl_system_datetime)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.cb_date_select = QtWidgets.QComboBox(self.tab_view)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.cb_date_select.sizePolicy().hasHeightForWidth())
        self.cb_date_select.setSizePolicy(sizePolicy)
        self.cb_date_select.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cb_date_select.setFont(font)
        self.cb_date_select.setStyleSheet("color: rgb(255, 170, 0);")
        self.cb_date_select.setObjectName("cb_date_select")
        self.cb_date_select.addItem("")
        self.horizontalLayout_4.addWidget(self.cb_date_select)
        self.groupBox = QtWidgets.QGroupBox(self.tab_view)
        self.groupBox.setStyleSheet("color: rgb(255, 170, 0);")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radio_manual = QtWidgets.QRadioButton(self.groupBox)
        self.radio_manual.setStyleSheet("color: rgb(255, 170, 0);")
        self.radio_manual.setObjectName("radio_manual")
        self.verticalLayout_2.addWidget(self.radio_manual)
        self.radio_auto = QtWidgets.QRadioButton(self.groupBox)
        self.radio_auto.setStyleSheet("color: rgb(255, 170, 0);")
        self.radio_auto.setObjectName("radio_auto")
        self.verticalLayout_2.addWidget(self.radio_auto)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.btn_refresh_map = QtWidgets.QPushButton(self.tab_view)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.btn_refresh_map.sizePolicy().hasHeightForWidth())
        self.btn_refresh_map.setSizePolicy(sizePolicy)
        self.btn_refresh_map.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_refresh_map.setFont(font)
        self.btn_refresh_map.setStyleSheet("background-color: rgb(252, 168, 0);\n"
"border-radius: 5%;")
        self.btn_refresh_map.setObjectName("btn_refresh_map")
        self.horizontalLayout_4.addWidget(self.btn_refresh_map)
        self.horizontalLayout_4.setStretch(0, 8)
        self.horizontalLayout_4.setStretch(1, 3)
        self.horizontalLayout_4.setStretch(2, 2)
        self.horizontalLayout_4.setStretch(3, 2)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.setStretch(0, 150)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 300)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tb_widget_log = QtWidgets.QTableWidget(self.tab_view)
        self.tb_widget_log.setObjectName("tb_widget_log")
        self.tb_widget_log.setColumnCount(0)
        self.tb_widget_log.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tb_widget_log)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.widget_web = QtWebEngineWidgets.QWebEngineView(self.tab_view)
        self.widget_web.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_web.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.widget_web.setObjectName("widget_web")
        self.horizontalLayout_2.addWidget(self.widget_web)
        self.horizontalLayout_2.setStretch(0, 150)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 300)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 20)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_view, "")
        self.tab_setting = QtWidgets.QWidget()
        self.tab_setting.setObjectName("tab_setting")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_setting)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem9)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lbl_history = QtWidgets.QLabel(self.tab_setting)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_history.setFont(font)
        self.lbl_history.setStyleSheet("color: rgb(255, 170, 0);")
        self.lbl_history.setObjectName("lbl_history")
        self.horizontalLayout_7.addWidget(self.lbl_history)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem10)
        self.btn_rs_angle = QtWidgets.QPushButton(self.tab_setting)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_rs_angle.setFont(font)
        self.btn_rs_angle.setStyleSheet("background-color: rgb(255, 170, 0);\n"
"")
        self.btn_rs_angle.setObjectName("btn_rs_angle")
        self.horizontalLayout_7.addWidget(self.btn_rs_angle)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.line = QtWidgets.QFrame(self.tab_setting)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.lbl_web_logs = QtWidgets.QLabel(self.tab_setting)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_web_logs.setFont(font)
        self.lbl_web_logs.setStyleSheet("color: rgb(0, 255, 0);")
        self.lbl_web_logs.setObjectName("lbl_web_logs")
        self.verticalLayout_6.addWidget(self.lbl_web_logs)
        self.verticalLayout_6.setStretch(0, 3)
        self.verticalLayout_6.setStretch(1, 1)
        self.verticalLayout_6.setStretch(2, 1)
        self.verticalLayout_6.setStretch(3, 8)
        self.gridLayout_4.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_setting, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot GPS"))
        self.lbl_utc_date_time.setText(_translate("MainWindow", "UTC-GPS-date"))
        self.lbl_latitude.setText(_translate("MainWindow", "Latitude"))
        self.lbl_longitude.setText(_translate("MainWindow", "Longitude"))
        self.lbl_angle.setText(_translate("MainWindow", "Angle"))
        self.lbl_rs_angle.setText(_translate("MainWindow", "rs_angle"))
        self.label.setText(_translate("MainWindow", "Robot status"))
        self.lbl_system_datetime.setText(_translate("MainWindow", "System datetime"))
        self.cb_date_select.setItemText(0, _translate("MainWindow", "2024-10-16"))
        self.groupBox.setTitle(_translate("MainWindow", "Maps option"))
        self.radio_manual.setText(_translate("MainWindow", "Manual"))
        self.radio_auto.setText(_translate("MainWindow", "Auto"))
        self.btn_refresh_map.setText(_translate("MainWindow", "Refresh"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_view), _translate("MainWindow", "Visualization view"))
        self.lbl_history.setText(_translate("MainWindow", "ESP POST LOG HISTORY"))
        self.btn_rs_angle.setText(_translate("MainWindow", ">>>Reset _ Angle<<<"))
        self.lbl_web_logs.setText(_translate("MainWindow", "Web logs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setting), _translate("MainWindow", "Robot Setting"))
from PyQt5 import QtWebEngineWidgets

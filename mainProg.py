# Pendant Application v0.1 (Alpha)

import sys
import sqlite3
import serial
import serial.tools.list_ports as PortDetect
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
from time import sleep

from PendantApp import *
from portError import *
from DataApp import *

global curs
global con
global loopState

# Frontend Visualization
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
Ui_MainWindow = Ui_MainWindow()
Ui_MainWindow.setupUi(MainWindow)
MainWindow.show()

MainWindow_error = QtWidgets.QMainWindow()
Ui_error = Ui_Error()
Ui_error.setupUi(MainWindow_error)

MainWindow_data = QtWidgets.QMainWindow()
Ui_DataWindow = Ui_DataWindow()
Ui_DataWindow.setupUi(MainWindow_data)

con = sqlite3.connect('Robot_Database.db')
curs = con.cursor()

curs.execute("CREATE TABLE IF NOT EXISTS Data1 (ID INTEGER not null primary key autoincrement, Base INTEGER, Arm1 INTEGER, Arm2 INTEGER, Roll INTEGER, Pitch INTEGER, Gripper INTEGER, Speed INTEGER)")
curs.execute("CREATE TABLE IF NOT EXISTS Data2 (ID INTEGER not null primary key autoincrement, Base INTEGER, Arm1 INTEGER, Arm2 INTEGER, Roll INTEGER, Pitch INTEGER, Gripper INTEGER, Speed INTEGER)")
curs.execute("CREATE TABLE IF NOT EXISTS Data3 (ID INTEGER not null primary key autoincrement, Base INTEGER, Arm1 INTEGER, Arm2 INTEGER, Roll INTEGER, Pitch INTEGER, Gripper INTEGER, Speed INTEGER)")
curs.execute("CREATE TABLE IF NOT EXISTS Data4 (ID INTEGER not null primary key autoincrement, Base INTEGER, Arm1 INTEGER, Arm2 INTEGER, Roll INTEGER, Pitch INTEGER, Gripper INTEGER, Speed INTEGER)")
curs.execute("CREATE TABLE IF NOT EXISTS Data5 (ID INTEGER not null primary key autoincrement, Base INTEGER, Arm1 INTEGER, Arm2 INTEGER, Roll INTEGER, Pitch INTEGER, Gripper INTEGER, Speed INTEGER)")
curs.execute("CREATE TABLE IF NOT EXISTS MemoryTBL (ID INTEGER not null primary key autoincrement, Base INTEGER, Arm1 INTEGER, Arm2 INTEGER, Roll INTEGER, Pitch INTEGER, Gripper INTEGER, Speed INTEGER)")

con.commit()

memory_for_point = []
global_readed_data = []
loop_data = ""
loop_state = False

# PORT FUNCTIONS #
def SearchPorts():
    
    portData = PortDetect.comports()
    
    for i in range(0, len(portData)):
        portName = str(portData[i])
        portName = portName.split(" ")
        portName = str(portName[0])
        Ui_MainWindow.comboBox_port.addItem(portName)
        
def OpenPort():
    
    global ser
    
    portName = str(Ui_MainWindow.comboBox_port.currentText())
    portBaud = int(Ui_MainWindow.comboBox_baud.currentText())
    
    try:
        ser = serial.Serial(port = portName, baudrate = portBaud, timeout = 1)
    except (NameError, serial.SerialException, ModuleNotFoundError):
        MainWindow_error.show()
        Ui_error.label.setText("Failed to Connect!")
    else:
        sleep(1.1)
        Ui_MainWindow.label_portStatus.setText("Connected!")

def ClosePort():
    
    try:
        ser.close()
    except (NameError, serial.SerialException, ModuleNotFoundError):
        MainWindow_error.show()
        Ui_error.label.setText("Please connect first!")
    else:
        Ui_MainWindow.label_portStatus.setText("Disconnected!")

# ---------------------------------------------------------------------------------- #

# Data Functions
def StartLoop():
    global loop_data
    try:
        for i in range(len(global_readed_data)):
            loop_data = str(global_readed_data[i])
            loop_data = loop_data.replace(' ', '')
            loop_data = loop_data[1:-1]
            ser.write(loop_data.encode('utf-8'))
            
    except: 
        MainWindow_error.show()
        Ui_error.label.setText("Connect First!")
   
    sleep(delayCalculation(global_readed_data))
    print(delayCalculation(global_readed_data))
    
def delayCalculation(data):
    delta_Time = 0
    for i in range(len(data)):
        try:
            delta_Time += (abs(data[i][0] - data [i + 1][0])) * data[0][6]
            delta_Time += (abs(data[i][1] - data [i + 1][1])) * data[1][6]
            delta_Time += (abs(data[i][2] - data [i + 1][2])) * data[2][6]
            delta_Time += (abs(data[i][3] - data [i + 1][3])) * data[3][6]
            delta_Time += (abs(data[i][4] - data [i + 1][4])) * data[4][6]
            delta_Time += (abs(data[i][5] - data [i + 1][5])) * data[5][6]
        except (IndexError):
            pass
    delta_Time += 250
    delta_Time = float(delta_Time / 1000)
    
    return delta_Time
      
def SendData():
    
    d_s1 = str(Ui_MainWindow.servo1_slider.value())
    d_s2 = str(Ui_MainWindow.servo2_slider.value())
    d_s3 = str(Ui_MainWindow.servo3_slider.value())
    d_s4 = str(Ui_MainWindow.servo4_slider.value())
    d_s5 = str(Ui_MainWindow.servo5_slider.value())
    d_s6 = str(Ui_MainWindow.servo6_slider.value())
    d_speed = str(Ui_MainWindow.verticalSlider_Speed.value())
    
    data = d_s1 + "," + d_s2 + "," + d_s3 + "," + d_s4 + "," + d_s5 + "," + d_s6 + "," + d_speed
    
    try:
        ser.write(data.encode('utf-8'))  
    except: 
        MainWindow_error.show()
        Ui_error.label.setText("Connect First!")

def SaveSinglePoint():
        
    d_s1 = str(Ui_MainWindow.servo1_slider.value())
    d_s2 = str(Ui_MainWindow.servo2_slider.value())
    d_s3 = str(Ui_MainWindow.servo3_slider.value())
    d_s4 = str(Ui_MainWindow.servo4_slider.value())
    d_s5 = str(Ui_MainWindow.servo5_slider.value())
    d_s6 = str(Ui_MainWindow.servo6_slider.value())
    d_speed = str(Ui_MainWindow.verticalSlider_Speed.value())
    
    data = d_s1 + "," + d_s2 + "," + d_s3 + "," + d_s4 + "," + d_s5 + "," + d_s6 + "," + d_speed
    
    memory_for_point.append(data)
    
    Ui_MainWindow.textBrowser_points.insertPlainText(data)
    Ui_MainWindow.textBrowser_points.insertPlainText('\n')
    
    return memory_for_point

def SaveData1():
    global memory_for_point
    curs.execute("DELETE FROM Data1")
    for i in range(len(memory_for_point)):
        memory_j = memory_for_point[i].split(',')
        curs.execute("INSERT INTO Data1(Base, Arm1, Arm2, Roll, Pitch, Gripper, Speed) VALUES(?, ?, ?, ?, ?, ?, ?)", (memory_j[0], memory_j[1], memory_j[2], memory_j[3], memory_j[4], memory_j[5], memory_j[6]))
        con.commit()
    memory_for_point = []
    return memory_for_point

def SaveData2():
    global memory_for_point
    curs.execute("DELETE FROM Data2")
    for i in range(len(memory_for_point)):
        memory_j = memory_for_point[i].split(',')
        curs.execute("INSERT INTO Data2(Base, Arm1, Arm2, Roll, Pitch, Gripper, Speed) VALUES(?, ?, ?, ?, ?, ?, ?)", (memory_j[0], memory_j[1], memory_j[2], memory_j[3], memory_j[4], memory_j[5], memory_j[6]))
        con.commit()
    memory_for_point = []
    return memory_for_point
    
def SaveData3():
    global memory_for_point
    curs.execute("DELETE FROM Data3")
    for i in range(len(memory_for_point)):
        memory_j = memory_for_point[i].split(',')
        curs.execute("INSERT INTO Data3(Base, Arm1, Arm2, Roll, Pitch, Gripper, Speed) VALUES(?, ?, ?, ?, ?, ?, ?)", (memory_j[0], memory_j[1], memory_j[2], memory_j[3], memory_j[4], memory_j[5], memory_j[6]))
        con.commit()
    memory_for_point = []
    return memory_for_point

def SaveData4():
    global memory_for_point
    curs.execute("DELETE FROM Data4")
    for i in range(len(memory_for_point)):
        memory_j = memory_for_point[i].split(',')
        curs.execute("INSERT INTO Data4(Base, Arm1, Arm2, Roll, Pitch, Gripper, Speed) VALUES(?, ?, ?, ?, ?, ?, ?)", (memory_j[0], memory_j[1], memory_j[2], memory_j[3], memory_j[4], memory_j[5], memory_j[6]))
        con.commit()
    memory_for_point = []
    return memory_for_point

def SaveData5():
    global memory_for_point
    curs.execute("DELETE FROM Data5")
    for i in range(len(memory_for_point)):
        memory_j = memory_for_point[i].split(',')
        curs.execute("INSERT INTO Data5(Base, Arm1, Arm2, Roll, Pitch, Gripper, Speed) VALUES(?, ?, ?, ?, ?, ?, ?)", (memory_j[0], memory_j[1], memory_j[2], memory_j[3], memory_j[4], memory_j[5], memory_j[6]))
        con.commit()
    memory_for_point = []
    return memory_for_point


def ReadData1():
    global global_readed_data
    Ui_MainWindow.textBrowser_points_2.clear()
    
    data = curs.execute("SELECT * FROM Data1")
    fdata = data.fetchall()
    
    readed_data = []
    mini_chars = []
    for i in range(len(fdata)):
        mini_chars = []
        for j in range(len(fdata[i])):
            mini_chars.append(fdata[i][j])
        readed_data.append(mini_chars)
    
    for i in range(len(readed_data)):
        readed_data[i].remove(readed_data[i][0])
    
    for i in range(len(readed_data)):
        Ui_MainWindow.textBrowser_points_2.insertPlainText(str(readed_data[i]))
        Ui_MainWindow.textBrowser_points_2.insertPlainText('\n')
    global_readed_data = readed_data

def ReadData2():
    global global_readed_data
    Ui_MainWindow.textBrowser_points_2.clear()
    
    data = curs.execute("SELECT * FROM Data2")
    fdata = data.fetchall()
    
    readed_data = []
    mini_chars = []
    for i in range(len(fdata)):
        mini_chars = []
        for j in range(len(fdata[i])):
            mini_chars.append(fdata[i][j])
        readed_data.append(mini_chars)
        
    for i in range(len(readed_data)):
        readed_data[i].remove(readed_data[i][0])
    
    for i in range(len(readed_data)):
        Ui_MainWindow.textBrowser_points_2.insertPlainText(str(readed_data[i]))
        Ui_MainWindow.textBrowser_points_2.insertPlainText('\n')
        
    global_readed_data = readed_data

def ReadData3():
    global global_readed_data
    Ui_MainWindow.textBrowser_points_2.clear()
    
    data = curs.execute("SELECT * FROM Data3")
    fdata = data.fetchall()
    
    readed_data = []
    mini_chars = []
    for i in range(len(fdata)):
        mini_chars = []
        for j in range(len(fdata[i])):
            mini_chars.append(fdata[i][j])
        readed_data.append(mini_chars)
        
    for i in range(len(readed_data)):
        readed_data[i].remove(readed_data[i][0])
    
    for i in range(len(readed_data)):
        Ui_MainWindow.textBrowser_points_2.insertPlainText(str(readed_data[i]))
        Ui_MainWindow.textBrowser_points_2.insertPlainText('\n')
    global_readed_data = readed_data

def ReadData4():
    global global_readed_data
    Ui_MainWindow.textBrowser_points_2.clear()
    
    data = curs.execute("SELECT * FROM Data4")
    fdata = data.fetchall()
    
    readed_data = []
    mini_chars = []
    for i in range(len(fdata)):
        mini_chars = []
        for j in range(len(fdata[i])):
            mini_chars.append(fdata[i][j])
        readed_data.append(mini_chars)
        
    for i in range(len(readed_data)):
        readed_data[i].remove(readed_data[i][0])
    
    for i in range(len(readed_data)):
        Ui_MainWindow.textBrowser_points_2.insertPlainText(str(readed_data[i]))
        Ui_MainWindow.textBrowser_points_2.insertPlainText('\n')
    global_readed_data = readed_data    

def ReadData5():
    global global_readed_data
    Ui_MainWindow.textBrowser_points_2.clear()
    
    data = curs.execute("SELECT * FROM Data5")
    fdata = data.fetchall()
    
    readed_data = []
    mini_chars = []
    for i in range(len(fdata)):
        mini_chars = []
        for j in range(len(fdata[i])):
            mini_chars.append(fdata[i][j])
        readed_data.append(mini_chars)
        
    for i in range(len(readed_data)):
        readed_data[i].remove(readed_data[i][0])
    
    for i in range(len(readed_data)):
        Ui_MainWindow.textBrowser_points_2.insertPlainText(str(readed_data[i]))
        Ui_MainWindow.textBrowser_points_2.insertPlainText('\n')
    global_readed_data = readed_data

def reWrite():
    Ui_MainWindow.textBrowser_points.clear()
    
    for i in range(len(memory_for_point)):
        memory_j = memory_for_point[i].split(',')
        curs.execute("INSERT INTO MemoryTBL(Base, Arm1, Arm2, Roll, Pitch, Gripper, Speed) VALUES(?, ?, ?, ?, ?, ?, ?)", (memory_j[0], memory_j[1], memory_j[2], memory_j[3], memory_j[4], memory_j[5], memory_j[6]))
        con.commit()
    
    data = curs.execute("SELECT * FROM MemoryTBL")
    
    fdata = data.fetchall()
    Ui_DataWindow.tableWidget.setRowCount(len(fdata))
    
    for row, columnvalues in enumerate(fdata):
        for column, value in enumerate(columnvalues):
            Ui_DataWindow.tableWidget.setItem(row, column, QTableWidgetItem(str(value)))

    curs.execute("DELETE FROM MemoryTBL")
    con.commit()

# Slider Sync #
def sliderSync():
    Ui_MainWindow.label_s1.setText(str(Ui_MainWindow.servo1_slider.value()))
    Ui_MainWindow.label_s2.setText(str(Ui_MainWindow.servo2_slider.value()))
    Ui_MainWindow.label_s3.setText(str(Ui_MainWindow.servo3_slider.value()))
    Ui_MainWindow.label_s4.setText(str(Ui_MainWindow.servo4_slider.value()))
    Ui_MainWindow.label_s5.setText(str(Ui_MainWindow.servo5_slider.value()))
    Ui_MainWindow.label_s6.setText(str(Ui_MainWindow.servo6_slider.value()))
    Ui_MainWindow.label_Speed.setText(str(Ui_MainWindow.verticalSlider_Speed.value()))

# Window Functions
def openSaveWindow():
    MainWindow_data.show()
    reWrite()
    
# Slider Sync Connect Calls
Ui_MainWindow.servo1_slider.valueChanged.connect(sliderSync)
Ui_MainWindow.servo2_slider.valueChanged.connect(sliderSync)
Ui_MainWindow.servo3_slider.valueChanged.connect(sliderSync)
Ui_MainWindow.servo4_slider.valueChanged.connect(sliderSync)
Ui_MainWindow.servo5_slider.valueChanged.connect(sliderSync)
Ui_MainWindow.servo6_slider.valueChanged.connect(sliderSync)
Ui_MainWindow.verticalSlider_Speed.valueChanged.connect(sliderSync)

# Port Connect Calls
Ui_MainWindow.pushButton_openPort.clicked.connect(OpenPort)
Ui_MainWindow.pushButton_closePort.clicked.connect(ClosePort)
Ui_MainWindow.pushButton_searchPorts.clicked.connect(SearchPorts)

# Data Connect Call
Ui_MainWindow.pushButton_StartProg.clicked.connect(StartLoop)
Ui_MainWindow.pushButton_sendData.clicked.connect(SendData)
Ui_MainWindow.pushButton_Save_Single.clicked.connect(SaveSinglePoint)

Ui_MainWindow.pushButton_data1.clicked.connect(ReadData1)
Ui_MainWindow.pushButton_data2.clicked.connect(ReadData2)
Ui_MainWindow.pushButton_data3.clicked.connect(ReadData3)
Ui_MainWindow.pushButton_data4.clicked.connect(ReadData4)
Ui_MainWindow.pushButton_data5.clicked.connect(ReadData5)

Ui_DataWindow.pushButton_1.clicked.connect(SaveData1)
Ui_DataWindow.pushButton_2.clicked.connect(SaveData2)
Ui_DataWindow.pushButton_3.clicked.connect(SaveData3)
Ui_DataWindow.pushButton_4.clicked.connect(SaveData4)
Ui_DataWindow.pushButton_5.clicked.connect(SaveData5)

# Window Connect Calls
Ui_MainWindow.pushButton_Save_All.clicked.connect(openSaveWindow)

#Ui_MainWindow.pushButton_Save_All.clicked.connect(SaveWork)
#Ui_MainWindow.pushButton_data1.clicked.connect(WorkData1)
#-----------------------#
sys.exit(app.exec_())
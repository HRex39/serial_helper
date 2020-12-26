#main.py
#SERIAL
import sys
import threading
from time import sleep

import serial
from PyQt5.QtWidgets import QApplication, QMainWindow

import serial_helper
#GLOBAL VARIABLE
SERIAL_STATUS = 0
ser = None
num_data = 0
num_stop = 0
num_parity_check = 0
timex = 0.5
#VARIABLE ENDS

def data_send():
    global ser, SERIAL_STATUS
    if SERIAL_STATUS == 1:
        try:
            data_send = ui.textEdit.toPlainText()
            # WRITE
            result = ser.write(data_send.encode("utf-8"))
            ui.text_send_stage.setText("发送成功！")
        except Exception as e:
            ui.text_send_stage.setText("发送失败！")
    else:
        ui.text_send_stage.setText("串口未开启！")

def data_received(thread_name):
    global ser, SERIAL_STATUS
    while True:
        if SERIAL_STATUS == 1:
            try:
                if ser.in_waiting:
                    data_recv = ser.read(ser.in_waiting).decode("utf-8")
                    sleep(0.02)
                    ui.textBrowser.insertPlainText(data_recv)
                else:
                    ui.text_recv_stage.setText("暂无数据...")
            except Exception as e:
                sleep(0.5)
            data_recv = None
        else:
            ui.text_recv_stage.setText("串口未开启！")
            sleep(1)

def serial_open():
    global ser, SERIAL_STATUS
    if SERIAL_STATUS == 0:
        try:
            # DATA PROCEED
            portx = ui.comboBox_2.currentText()
            bps = ui.comboBox.currentText()
            num_data = ui.comboBox_4.currentText()
            if num_data == "5": num_data = serial.FIVEBITS
            if num_data == "6": num_data = serial.SIXBITS
            if num_data == "7": num_data = serial.SEVENBITS
            if num_data == "8": num_data = serial.EIGHTBITS
            num_stop = ui.comboBox_3.currentText()
            if num_stop == "1": num_stop = serial.STOPBITS_ONE
            if num_stop == "1.5": num_stop = serial.STOPBITS_ONE_POINT_FIVE
            if num_stop == "2": num_stop = serial.STOPBITS_TWO
            num_parity_check = ui.comboBox_5.currentText()
            if num_parity_check == "无校验": num_parity_check = serial.PARITY_NONE
            if num_parity_check == "奇校验": num_parity_check = serial.PARITY_ODD
            if num_parity_check == "偶校验": num_parity_check = serial.PARITY_EVEN
            print(portx, bps, num_data, num_stop, num_parity_check)

            # OPEN SERIES
            ser = serial.Serial(port=portx, baudrate=bps, bytesize=num_data,
                                parity=num_parity_check, stopbits=num_stop, timeout=timex)
            ui.serial_now.setText("已连接上" + portx)
            SERIAL_STATUS = 1
            ui.pushButton.setText("关闭串口")
        except serial.SerialException:
            ui.serial_now.setText("连接" + portx + "失败")
            SERIAL_STATUS = 0
    else:
        try:
            ser.close()
            ui.serial_now.setText("关闭成功")
            ui.pushButton.setText("打开串口")
            SERIAL_STATUS = 0
        except Exception as e:
            ui.serial_now.setText("关闭失败")
            SERIAL_STATUS = 1

def data_send_clean():
    ui.textEdit.clear()

def data_recv_clean():
    ui.textBrowser.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = serial_helper.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # Thread
    Received_Thread = threading.Thread(target=data_received, args=("Received_Thread",))
    Received_Thread.setDaemon(True)
    Received_Thread.start()
    # Set default num
    ui.comboBox.setCurrentIndex(3)
    ui.comboBox_3.setCurrentIndex(0)
    ui.comboBox_4.setCurrentIndex(3)
    ui.comboBox_5.setCurrentIndex(0)
    # LINK
    ui.pushButton.clicked.connect(serial_open)
    ui.text_send.clicked.connect(data_send)
    ui.text_send_clean.clicked.connect(data_send_clean)
    ui.text_recv_clean.clicked.connect(data_recv_clean)
    sys.exit(app.exec_())

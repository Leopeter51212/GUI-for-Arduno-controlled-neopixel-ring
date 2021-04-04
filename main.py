import sys, os
import time
import serial

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *

from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    # initialise
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # create the signal and slot
        self.createSignalSlot()

        self.send_LED_index = []

        # self.initialSlider()

        # Disable all the display function before open the port
        self.Red_pushButton.setEnabled(False)
        self.Green_pushButton.setEnabled(False)
        self.Blue_pushButton.setEnabled(False)
        self.White_pushButton.setEnabled(False)
        self.AllLEDOn_pushButton.setEnabled(False)
        self.AllLEDOff_pushButton.setEnabled(False)
        self.LeftOn_pushButton.setEnabled(False)
        self.RightOn_pushButton.setEnabled(False)
        self.OddBlink_pushButton.setEnabled(False)
        self.EvenBlink_pushButton.setEnabled(False)
        self.IndividualBlink_pushButton.setEnabled(False)
        self.reset_small_pushButton.setEnabled(False)
        self.reset_large_pushButton.setEnabled(False)
        self.LargeRingApply_pushButton.setEnabled(False)
        self.SmallRingApply_pushButton.setEnabled(False)
        self.Short_loop_pushButton.setEnabled(False)
        self.Medium_loop_pushButton.setEnabled(False)
        self.Long_loop_pushButton.setEnabled(False)

    # create the slot and connect them with corresponding button
    def createSignalSlot(self):
        self.AutoScan_pushButton.clicked.connect(self.auto_scan)
        self.OpenPort_pushButton.clicked.connect(self.open_port)
        self.ClosePort_pushButton.clicked.connect(self.close_port)
        self.White_pushButton.clicked.connect(self.white_wipe)
        self.Red_pushButton.clicked.connect(self.red_wipe)
        self.Green_pushButton.clicked.connect(self.green_wipe)
        self.Blue_pushButton.clicked.connect(self.blue_wipe)
        self.AllLEDOn_pushButton.clicked.connect(self.all_on)
        self.AllLEDOff_pushButton.clicked.connect(self.all_off)
        self.LeftOn_pushButton.clicked.connect(self.left_on)
        self.RightOn_pushButton.clicked.connect(self.right_on)
        self.OddBlink_pushButton.clicked.connect(self.odd_blink)
        self.EvenBlink_pushButton.clicked.connect(self.even_blink)
        self.IndividualBlink_pushButton.clicked.connect(self.individual_blink)

        self.Short_loop_pushButton.clicked.connect(self.short_loop_display)
        self.Medium_loop_pushButton.clicked.connect(self.medium_loop_display)
        self.Long_loop_pushButton.clicked.connect(self.long_loop_display)
        # checkbox group for small ring
        self.checkBox1.stateChanged.connect(self.small1)  # b
        self.checkBox2.stateChanged.connect(self.small2)  # c
        self.checkBox3.stateChanged.connect(self.small3)  # d
        self.checkBox4.stateChanged.connect(self.small4)  # e
        self.checkBox5.stateChanged.connect(self.small5)  # f
        self.checkBox6.stateChanged.connect(self.small6)  # g
        self.checkBox7.stateChanged.connect(self.small7)  # h
        self.checkBox8.stateChanged.connect(self.small8)  # i
        self.checkBox9.stateChanged.connect(self.small9)  # j
        # checkbox group for large ring
        self.checkBox_1.stateChanged.connect(self.large1)  # b
        self.checkBox_2.stateChanged.connect(self.large2)  # c
        self.checkBox_3.stateChanged.connect(self.large3)  # d
        self.checkBox_4.stateChanged.connect(self.large4)  # e
        self.checkBox_5.stateChanged.connect(self.large5)  # f
        self.checkBox_6.stateChanged.connect(self.large6)  # g
        self.checkBox_7.stateChanged.connect(self.large7)  # h
        self.checkBox_8.stateChanged.connect(self.large8)  # i
        self.checkBox_9.stateChanged.connect(self.large9)  # j
        self.checkBox_10.stateChanged.connect(self.large10)  # k
        self.checkBox_11.stateChanged.connect(self.large11)  # l
        self.checkBox_12.stateChanged.connect(self.large12)  # m
        self.checkBox_13.stateChanged.connect(self.large13)  # n
        self.checkBox_14.stateChanged.connect(self.large14)  # o
        self.checkBox_15.stateChanged.connect(self.large15)  # p
        self.checkBox_16.stateChanged.connect(self.large16)  # q
        # reset and apply signal for checkbox group
        self.reset_small_pushButton.clicked.connect(self.reset_small_ring)
        self.reset_large_pushButton.clicked.connect(self.reset_large_ring)
        self.SmallRingApply_pushButton.clicked.connect(self.small_on)
        self.LargeRingApply_pushButton.clicked.connect(self.large_on)
        # self.Brightness_horizontalSlider.sliderMoved.connect(self.set_brightness)

    # Arduino configuration code
    # auto scan the port and write the result in the combobox
    def auto_scan(self):
        # clear all the content in the combobox to except refresh2
        self.PortNumber_comboBox.clear()

        # build an serial port object
        port = QSerialPort()
        # get all the available ports
        port_list = QSerialPortInfo.availablePorts()

        # add all available ports to the combobox
        for port_number in port_list:
            port.setPort(port_number)
            # scan which one is using and display it in the combobox
            if port.open(QSerialPort.ReadWrite):
                self.PortNumber_comboBox.addItem(port.portName())
                port.close()

    # open the port
    def open_port(self):
        # get the port properties from the corresponding combobox
        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())
        print("Settings：Port number=%s ，Port rate=%d" % (port_name, port_rate))

        if port_rate != 4800:
            QMessageBox.critical(self, 'ERROR',
                                 'Failed to open the serial port. Please check Arduino program port rate')
            return
        else:
            QMessageBox.information(self, 'Port', 'Port has been opened.')

        # after open the port then the user can do the display
        self.PortNumber_comboBox.setEnabled(False)
        self.PortRate_comboBox.setEnabled(False)
        self.AutoScan_pushButton.setEnabled(False)
        self.OpenPort_pushButton.setEnabled(False)
        self.ClosePort_pushButton.setEnabled(True)
        self.enable_all()

    # close the port
    def close_port(self):
        self.port.close()

        # close all the display mode
        self.PortNumber_comboBox.setEnabled(True)
        self.PortRate_comboBox.setEnabled(True)
        self.AutoScan_pushButton.setEnabled(True)
        self.OpenPort_pushButton.setEnabled(True)
        self.disable_all()

    # Default display mode code
    # white wipe function
    def white_wipe(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0
        # white
        while 1:
            serial_port.write(b"0")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 0 to the serial port
            if i > 30:
                self.White_pushButton.setEnabled(False)
                break

    # red wipe function
    def red_wipe(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # red
            serial_port.write(b"1")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 1 to the serial port
            if i > 30:
                self.Red_pushButton.setEnabled(False)
                break

    # green wipe function
    def green_wipe(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0
        while 1:
            # green
            serial_port.write(b"2")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 2 to the serial port
            if i > 30:
                self.Green_pushButton.setEnabled(False)
                break

    # blue wipe function
    def blue_wipe(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # blue
            serial_port.write(b"3")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 3 to the serial port
            if i > 30:
                self.Blue_pushButton.setEnabled(False)
                break

    # turn on all LED
    def all_on(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # all turn on is send 4
            serial_port.write(b"4")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 4 to the serial port
            if i > 30:
                self.AllLEDOn_pushButton.setEnabled(False)
                break

    # turn on all LED
    def all_off(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # all turn off is send 5
            serial_port.write(b"5")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 5 to the serial port
            if i > 30:
                self.AllLEDOff_pushButton.setEnabled(False)
                break

    # turn on left hand side LED
    def left_on(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # turn on left hand side LED is send 6
            serial_port.write(b"6")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 6 to the serial port
            if i > 30:
                self.LeftOn_pushButton.setEnabled(False)
                break

    # turn on right hand side LED
    def right_on(self):
        # enable all the function including the last call
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # turn on right hand side LED is send 7
            serial_port.write(b"7")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 6 to the serial port
            if i > 30:
                self.RightOn_pushButton.setEnabled(False)
                break

    # odd index blink
    def odd_blink(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # odd blink LED is send 8
            serial_port.write(b"8")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 8 to the serial port
            if i > 30:
                self.OddBlink_pushButton.setEnabled(False)
                break

    # even index blink
    def even_blink(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # turn on right hand side LED is send 9
            serial_port.write(b"9")
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 9 to the serial port
            if i > 30:
                self.EvenBlink_pushButton.setEnabled(False)
                break

    # individual blink
    def individual_blink(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # turn on right hand side LED is send 'a'

            send_data = 'a'
            serial_port.write(send_data.encode('UTF-8'))
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty 10 to the serial port
            if i > 30:
                self.IndividualBlink_pushButton.setEnabled(False)
                break

    # Loop display mode
    def short_loop_display(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # short loop display is send 'r'
            send_data = 'r'
            serial_port.write(send_data.encode('UTF-8'))
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty r to the serial port
            if i > 30:
                self.Short_loop_pushButton.setEnabled(False)
                break

    def medium_loop_display(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # medium loop display is send 's'
            send_data = 's'
            serial_port.write(send_data.encode('UTF-8'))
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty s to the serial port
            if i > 30:
                self.Medium_loop_pushButton.setEnabled(False)
                break

    def long_loop_display(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            # long loop display is send 't'
            send_data = 't'
            serial_port.write(send_data.encode('UTF-8'))
            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send thirty t to the serial port
            if i > 30:
                self.Long_loop_pushButton.setEnabled(False)
                break

    # Arbitrary display mode
    def small1(self):
        self.send_LED_index.append('b')

    def small2(self):
        self.send_LED_index.append('c')

    def small3(self):
        self.send_LED_index.append('d')

    def small4(self):
        self.send_LED_index.append('e')

    def small5(self):
        self.send_LED_index.append('f')

    def small6(self):
        self.send_LED_index.append('g')

    def small7(self):
        self.send_LED_index.append('h')

    def small8(self):
        self.send_LED_index.append('i')

    def small9(self):
        self.send_LED_index.append('j')

    def large1(self):
        self.send_LED_index.append('b')

    def large2(self):
        self.send_LED_index.append('c')

    def large3(self):
        self.send_LED_index.append('d')

    def large4(self):
        self.send_LED_index.append('e')

    def large5(self):
        self.send_LED_index.append('f')

    def large6(self):
        self.send_LED_index.append('g')

    def large7(self):
        self.send_LED_index.append('h')

    def large8(self):
        self.send_LED_index.append('i')

    def large9(self):
        self.send_LED_index.append('j')

    def large10(self):
        self.send_LED_index.append('k')

    def large11(self):
        self.send_LED_index.append('l')

    def large12(self):
        self.send_LED_index.append('m')

    def large13(self):
        self.send_LED_index.append('n')

    def large14(self):
        self.send_LED_index.append('o')

    def large15(self):
        self.send_LED_index.append('p')

    def large16(self):
        self.send_LED_index.append('q')

    def small_on(self):
        print(self.send_LED_index)
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            length = len(self.send_LED_index)
            for j in range(0, length):
                serial_port.write(self.send_LED_index[j].encode('UTF-8'))

            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send ten group of index to the serial port
            if i > 50:
                self.SmallRingApply_pushButton.setEnabled(False)
                self.send_LED_index.clear()
                break

        self.send_LED_index.clear()

    def large_on(self):
        self.enable_all()

        port_name = str(self.PortNumber_comboBox.currentText())
        port_rate = int(self.PortRate_comboBox.currentText())

        serial_port = serial.Serial(port_name, port_rate, timeout=.1)

        i = 0

        while 1:
            length = len(self.send_LED_index)
            for j in range(0, length):
                serial_port.write(self.send_LED_index[j].encode('UTF-8'))

            # delay 0.05s for each send
            time.sleep(0.05)

            i += 1

            # send ten group of index to the serial port
            if i > 50:
                self.LargeRingApply_pushButton.setEnabled(False)
                self.send_LED_index.clear()
                break

        self.send_LED_index.clear()

    def reset_small_ring(self):
        self.send_LED_index.clear()
        print(self.send_LED_index)
        # enable all the function including the last call
        self.enable_all()

        self.checkBox1.setChecked(False)
        self.checkBox2.setChecked(False)
        self.checkBox3.setChecked(False)
        self.checkBox4.setChecked(False)
        self.checkBox5.setChecked(False)
        self.checkBox6.setChecked(False)
        self.checkBox7.setChecked(False)
        self.checkBox8.setChecked(False)
        self.checkBox9.setChecked(False)

        self.send_LED_index.clear()

        self.SmallRingApply_pushButton.setEnabled(True)
        self.all_off()

    def reset_large_ring(self):
        # enable all the function including the last call
        self.enable_all()

        self.send_LED_index.clear()
        self.checkBox_1.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_11.setChecked(False)
        self.checkBox_12.setChecked(False)
        self.checkBox_13.setChecked(False)
        self.checkBox_14.setChecked(False)
        self.checkBox_15.setChecked(False)
        self.checkBox_16.setChecked(False)

        self.send_LED_index.clear()

        self.LargeRingApply_pushButton.setEnabled(True)
        self.all_off()

    # enable all display function
    def enable_all(self):
        self.Red_pushButton.setEnabled(True)
        self.Green_pushButton.setEnabled(True)
        self.Blue_pushButton.setEnabled(True)
        self.White_pushButton.setEnabled(True)
        self.AllLEDOn_pushButton.setEnabled(True)
        self.AllLEDOff_pushButton.setEnabled(True)
        self.LeftOn_pushButton.setEnabled(True)
        self.RightOn_pushButton.setEnabled(True)
        self.OddBlink_pushButton.setEnabled(True)
        self.EvenBlink_pushButton.setEnabled(True)
        self.IndividualBlink_pushButton.setEnabled(True)
        self.SmallRingApply_pushButton.setEnabled(True)
        self.LargeRingApply_pushButton.setEnabled(True)
        self.reset_large_pushButton.setEnabled(True)
        self.reset_small_pushButton.setEnabled(True)
        self.Short_loop_pushButton.setEnabled(True)
        self.Medium_loop_pushButton.setEnabled(True)
        self.Long_loop_pushButton.setEnabled(True)

    # disable all display function
    def disable_all(self):
        self.Red_pushButton.setEnabled(False)
        self.Green_pushButton.setEnabled(False)
        self.Blue_pushButton.setEnabled(False)
        self.White_pushButton.setEnabled(False)
        self.AllLEDOn_pushButton.setEnabled(False)
        self.AllLEDOff_pushButton.setEnabled(False)
        self.LeftOn_pushButton.setEnabled(False)
        self.RightOn_pushButton.setEnabled(False)
        self.OddBlink_pushButton.setEnabled(False)
        self.EvenBlink_pushButton.setEnabled(False)
        self.IndividualBlink_pushButton.setEnabled(False)
        self.SmallRingApply_pushButton.setEnabled(False)
        self.LargeRingApply_pushButton.setEnabled(False)
        self.Short_loop_pushButton.setEnabled(False)
        self.Medium_loop_pushButton.setEnabled(False)
        self.Long_loop_pushButton.setEnabled(False)

    # # initial all the slider in the gui
    # def initialSlider(self):
    #     self.Brightness_horizontalSlider.setMinimum(0)
    #     self.Brightness_horizontalSlider.setMaximum(255)
    #     self.Brightness_horizontalSlider.setSingleStep(51)
    #     self.Brightness_horizontalSlider.setValue(51)
    #     self.Brightness_horizontalSlider.setTickPosition(QSlider.TicksBelow)
    #     self.Brightness_horizontalSlider.setTickInterval(51)

    # # set the brightness according to the QSlider
    # def set_brightness(self):
    #     brightness = self.Brightness_horizontalSlider.value()
    #     self.Brightness_Value.setNum(51)
    #
    #     if 0 <= brightness <= 51:
    #         brightness = 51
    #         self.Brightness_Value.setNum(brightness)
    #
    #     elif 51 < brightness <= 102:
    #         brightness = 102
    #         self.Brightness_Value.setNum(brightness)
    #
    #     elif 102 < brightness <= 153:
    #         brightness = 153
    #         self.Brightness_Value.setNum(brightness)
    #
    #     elif 153 < brightness <= 204:
    #         brightness = 204
    #         self.Brightness_Value.setNum(brightness)
    #
    #     elif 204 < brightness <= 255:
    #         brightness = 255
    #         self.Brightness_Value.setNum(brightness)
    #
    #     self.send_brightness(self, brightness)
    #
    # # send the brightness
    # def send_brightness(self, brightness):
    #
    #     port_name = str(self.PortNumber_comboBox.currentText())
    #     port_rate = int(self.PortRate_comboBox.currentText())
    #     serial_port = serial.Serial(port_name, port_rate, timeout=.1)
    #
    #     if brightness == 51:
    #         i = 0
    #
    #         while 1:
    #             # set brightness as 51 is send 'b'
    #             send_data = 'b'
    #             serial_port.write(send_data.encode('UTF-8'))
    #             # delay 0.05s for each send
    #             time.sleep(0.05)
    #
    #             i += 1
    #
    #             # send twenty b to the serial port
    #             if i > 20:
    #                 self.Brightness_Value.setNum(brightness)
    #                 break
    #
    #     elif brightness == 102:
    #         i = 0
    #
    #         while 1:
    #             # set brightness as 102 is send 'c'
    #             send_data = 'c'
    #             serial_port.write(send_data.encode('UTF-8'))
    #             # delay 0.05s for each send
    #             time.sleep(0.05)
    #
    #             i += 1
    #
    #             # send twenty c to the serial port
    #             if i > 20:
    #                 self.Brightness_Value.setNum(brightness)
    #                 break
    #
    #     elif brightness == 153:
    #         i = 0
    #
    #         while 1:
    #             # set brightness as 51 is send 'c'
    #             send_data = 'c'
    #             serial_port.write(send_data.encode('UTF-8'))
    #             # delay 0.05s for each send
    #             time.sleep(0.05)
    #
    #             i += 1
    #
    #             # send twenty 10 to the serial port
    #             if i > 20:
    #                 self.Brightness_Value.setNum(brightness)
    #                 break
    #
    #     elif brightness == 204:
    #         i = 0
    #
    #         while 1:
    #             # set brightness as 51 is send 'd'
    #             send_data = 'd'
    #             serial_port.write(send_data.encode('UTF-8'))
    #             # delay 0.05s for each send
    #             time.sleep(0.05)
    #
    #             i += 1
    #
    #             # send twenty 10 to the serial port
    #             if i > 20:
    #                 self.Brightness_Value.setNum(brightness)
    #                 break
    #
    #     elif brightness == 255:
    #         i = 0
    #
    #         while 1:
    #             # set brightness as 51 is send 'e'
    #             send_data = 'e'
    #             serial_port.write(send_data.encode('UTF-8'))
    #             # delay 0.05s for each send
    #             time.sleep(0.05)
    #
    #             i += 1
    #
    #             # send twenty 10 to the serial port
    #             if i > 20:
    #                 self.Brightness_Value.setNum(brightness)
    #                 break

    # enable all display function


# show the GUI
if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())

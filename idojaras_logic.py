__author__ = 'Shane DiNozzo'

import sys
import time
import urllib
import json
import codecs

# Try to import PyQt5 module
try:
    # noinspection PyUnresolvedReferences
    import PyQt5
except ImportError:
    print('\nThe PyQt5 module not found! Please install it!')
    exit()


# noinspection PyUnresolvedReferences
from PyQt5 import QtWidgets, uic, QtGui, QtCore
# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *
# noinspection PyUnresolvedReferences
from PyQt5.QtGui import *

# Try to import pywapi module
try:
    # noinspection PyUnresolvedReferences
    import pywapi
except ImportError:
    print('The pywapi module not found! Please install it!')
    exit()

# Load Qt Designer .ui file as GUI for the app
form_class = uic.loadUiType('idojaras.ui')[0]


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class MainWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.setFixedSize(388, 468)

        QApplication.setStyle(QStyleFactory.create('Fusion'))

        # Set icon
        self.iconres = QtGui.QPixmap(str(':/Icon/wicon.ico'))
        self.icon = QtGui.QIcon(self.iconres)

        self.idojaras_label = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap(str(':/Banner/wbanner2.jpg'))

        self.progressBar.setRange(0, 1)
        self.myLongTask = TaskThread()
        self.myLongTask2 = TaskThread2()
        self.myLongTask.taskFinished.connect(self.onfinished)
        self.myLongTask2.taskFinished.connect(self.onfinished2)

        self.varosbevitel = self.varosBevitel_lineEdit
        self.erezheto = self.erezheto_homerseklet_label
        self.infoallomas = self.info_allomas_label
        self.jelenlegi_hom = self.jelenlegi_homerseklet_label
        self.paratartalom = self.paratartalom_label
        self.szel = self.szel_adatok_label
        self.last_upd = self.utoljara_frissitve_label
        self.locat_date = self.varos_datum_label

        self.varosKereses_pushButton.clicked.connect(self.onstart2)
        self.get_location_pushButton.clicked.connect(self.onstart)

    def onstart(self):
        self.progressBar.setRange(0, 0)
        self.myLongTask.start()

    def onstart2(self):
        self.progressBar.setRange(0, 0)
        self.myLongTask2.start()

    def onfinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0, 1)

    def onfinished2(self):
        # Stop the pulsation
        self.progressBar.setRange(0, 1)

    def clear_ui(self):
        self.locat_date.setText('')
        self.erezheto.setText('')
        self.infoallomas.setText('')
        self.jelenlegi_hom.setText('')
        self.paratartalom.setText('')
        self.szel.setText('')
        self.last_upd.setText('')

    def auto_location(self):
        # Automatically geolocate the connecting IP
        try:
            self.jsonfile = urllib.request.urlopen(str('http://ip-api.com/json'))
        except urllib.error.URLError:
            self.erezheto.setText('Can\'t get IP location! Please check your internet connection!')
            self.erezheto.setStyleSheet('QLabel#erezheto_homerseklet_label {color: red}')
        else:
            self.reader = codecs.getreader("utf-8")
            self.loadjson = json.load(self.reader(self.jsonfile))
            self.jsonfile.close()
        try:
            self.check_if_city_available(self.loadjson['city'])
        except KeyError:
            self.erezheto.setText('The service provider is not available at this time!\nPlease try again later!')
            self.erezheto.setStyleSheet('QLabel#erezheto_homerseklet_label {color: red}')
            return None
        
    def check_if_city_available(self, location):
        self.location_getter = pywapi.get_loc_id_from_weather_com(location)
        try:
            self.get_weather_info(self.location_getter[0][1], self.location_getter[0][0])
        except KeyError:
            self.erezheto.setText('City not found!')
            self.erezheto.setStyleSheet('QLabel#erezheto_homerseklet_label {color: red}')

    def get_weather_info(self, input_location, location_id):
        self.city = input_location
        self.weather = pywapi.get_weather_from_weather_com(location_id)

        self.current_date = time.strftime('%Y.%m.%d.')
        self.weather_temp = self.weather['current_conditions']['temperature']
        self.weather_text = self.weather['current_conditions']['text']
        self.weather_windspeed = self.weather['current_conditions']['wind']['speed']
        self.weather_windtext = self.weather['current_conditions']['wind']['text']
        self.weather_last_updated = self.weather['current_conditions']['last_updated']
        self.weather_humidity = self.weather['current_conditions']['humidity']
        self.weather_station = self.weather['current_conditions']['station']
        self.weather_felslike = self.weather['current_conditions']['feels_like']

        self.erezheto.setText('Érezhető hőmérséklet: ' + self.weather_felslike + '°C')
        self.erezheto.setStyleSheet('QLabel#erezheto_homerseklet_label {color: black}')
        self.infoallomas.setText('Info. állomás: ' + self.weather_station)
        self.jelenlegi_hom.setText(self.weather_temp + '°C    ' + self.weather_text)
        self.paratartalom.setText('Páratartalom: ' + self.weather_humidity)
        self.szel.setText('Szélerősség: ' + self.weather_windspeed + ' km/h    Szélirány: ' + self.weather_windtext)
        self.last_upd.setText('Utoljára frissítve: ' + self.weather_last_updated)
        self.locat_date.setText(self.city + ' | ' + self.current_date)


class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()

    def run(self):
        myWindow.clear_ui()
        myWindow.auto_location()
        self.taskFinished.emit()


class TaskThread2(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()

    def run(self):
        myWindow.clear_ui()

        if myWindow.varosbevitel.text() == '':
            myWindow.erezheto.setText('Please enter a city or use the IP based location option!')
            myWindow.erezheto.setStyleSheet('QLabel#erezheto_homerseklet_label {color: red}')
            self.taskFinished.emit()
            return None
        else:
            myWindow.check_if_city_available(myWindow.varosbevitel.text())

        self.taskFinished.emit()

app = QtWidgets.QApplication(sys.argv)
myWindow = MainWindowClass(None)
myWindow.show()
app.exec()

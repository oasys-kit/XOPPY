__author__ = 'labx'

import os
import urllib
from PyQt4.QtCore import Qt
from  orangewidget import gui

XRAY_SERVER_URL = "http://x-server.gmca.aps.anl.gov/"

class HttpManager():

    @classmethod
    def send_xray_server_request(cls, application, parameters):

        data = urllib.parse.urlencode(parameters)
        data = data.encode('utf-8') # data should be bytes
        req = urllib.request.Request(XRAY_SERVER_URL + application, data)
        resp = urllib.request.urlopen(req)

        return resp.read()


class XoppyGui():

    @classmethod
    def lineEdit(cls, widget, master, value, label=None, labelWidth=None,
             orientation='vertical', box=None, callback=None,
             valueType=str, validator=None, controlWidth=None,
             callbackOnType=False, focusInCallback=None,
             enterPlaceholder=False, **misc):

        lEdit = gui.lineEdit(widget, master, value, label, labelWidth, orientation, box, callback, valueType, validator, controlWidth, callbackOnType, focusInCallback, enterPlaceholder, **misc)

        if value:
            if (valueType != str):
                lEdit.setAlignment(Qt.AlignRight)

        return lEdit

    @classmethod
    def widgetBox(cls, widget, box=None, orientation='vertical', margin=None, spacing=4, height=None, width=None, **misc):

        box = gui.widgetBox(widget, box, orientation, margin, spacing, **misc)
        box.layout().setAlignment(Qt.AlignTop)

        if not height is None:
            box.setFixedHeight(height)
        if not width is None:
            box.setFixedWidth(width)

        return box

    @classmethod
    def tabWidget(cls, widget, height=None, width=None):
        tabWidget = gui.tabWidget(widget)

        if not height is None:
            tabWidget.setFixedHeight(height)
        if not width is None:
            tabWidget.setFixedWidth(width)

        return tabWidget

    @classmethod
    def createTabPage(cls, tabWidget, name, widgetToAdd=None, canScroll=False, height=None, width=None):

        tab = gui.createTabPage(tabWidget, name, widgetToAdd, canScroll)
        tab.layout().setAlignment(Qt.AlignTop)

        if not height is None:
            tab.setFixedHeight(height)
        if not width is None:
            tab.setFixedWidth(width)

        return tab

    @classmethod
    def checkNumber(cls, value, field_name):
        try:
            float(value)
        except ValueError:
            raise Exception(str(field_name) + " is not a number")

        return value

    @classmethod
    def checkPositiveNumber(cls, value, field_name):
        value = XoppyGui.checkNumber(value, field_name)
        if (value < 0): raise Exception(field_name + " should be >= 0")

        return value

    @classmethod
    def checkStrictlyPositiveNumber(cls, value, field_name):
        value = XoppyGui.checkNumber(value, field_name)
        if (value <= 0): raise Exception(field_name + " should be > 0")

        return value

    @classmethod
    def checkStrictlyPositiveAngle(cls, value, field_name):
        value = XoppyGui.checkNumber(value, field_name)
        if value <= 0 or value >= 360: raise Exception(field_name + " should be > 0 and < 360 deg")

        return value

    @classmethod
    def checkPositiveAngle(cls, value, field_name):
        value = XoppyGui.checkNumber(value, field_name)
        if value < 0 or value > 360: raise Exception(field_name + " should be >= 0 and <= 360 deg")

        return value

    @classmethod
    def checkEmptyString(cls, string, field_name):

        if string is None: raise Exception(field_name + " should not be an empty string")
        if string.strip() == "": raise Exception(field_name + " should not be an empty string")

        return string

    @classmethod
    def checkFile(cls, fileName):

        if fileName is None: raise Exception("File '" + fileName + "' not existing")
        if fileName.strip() == "": raise Exception("File '" + fileName + "' not existing")

        if fileName.startswith('/'):
            filePath = fileName
        else:
            filePath = os.getcwd() + '/' + fileName

        if not os.path.exists(filePath):
            raise Exception("File " + fileName + " not existing")

        return fileName

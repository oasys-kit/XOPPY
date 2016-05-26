__author__ = "Luca Rebuffi"

from oasys.widgets import widget
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui

import urllib
from http import server

from orangecontrib.xoppy.util.xoppy_util import HttpManager

from PyQt4 import QtGui

APPLICATION = "cgi/WWW_dbli.exe"

class ListUtility:
    @classmethod
    def get_list(cls, x0hdb=""):

        parameters = {}
        parameters.update({"x0hdb" : x0hdb})
        parameters.update({"textout" : "1" })
        parameters.update({"namesonly" : "1"})

        try:
            response = HttpManager.send_xray_server_request_POST(APPLICATION, parameters).decode('ascii')

            list = response.split('\n')
            return [x.strip() for x in list[1:len(list)-1]]

        except Exception as e:
            return []


    @classmethod
    def get_help(cls, x0hdb=""):

        parameters = {}
        parameters.update({"x0hdb" : x0hdb})

        try:
            return HttpManager.send_xray_server_request_POST(APPLICATION, parameters).decode('ascii')

        except Exception as e:
            return ""

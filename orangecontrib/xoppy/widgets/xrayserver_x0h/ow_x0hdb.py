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

class X0hList(widget.OWWidget):
    name = "X0h List"
    description = "X0h: X0h List"
    icon = "icons/x0hlist.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "luca.rebuffi(@at@)elettra.eu"
    priority = 1
    category = "X0h"
    keywords = ["data", "file", "load", "read"]


    want_main_area = 1

    selection = Setting(0)
    details = Setting(0)

    outputs = [{"name": "List",
                "type": object,
                "doc": "X0h List",
                "id": "list"}, ]

    def __init__(self):
        self.setFixedWidth(1200)
        self.setFixedHeight(600)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "X0h List Parameters", addSpace=True, orientation="vertical",
                                         width=300, height=500)


        gui.comboBox(left_box_1, self, "selection", label="Selection", labelWidth=50,
                     items=["Crystals",
                            "Amorphous Materials",
                            "Atoms",
                            "All: crystal, amorphous materials and atoms",
                            "Cubic crystals",
                            "Amorphous materials and atoms",
                            "Crystals and amorphous materials",
                            "Characteristic X-ray lines"
                            ],
                     sendSelectedValue=False, orientation="horizontal")

        gui.comboBox(left_box_1, self, "details", label="Details", labelWidth=50,
                     items=["Dump",
                            "List",
                            ],
                     sendSelectedValue=False, orientation="horizontal")

        button = gui.button(self.controlArea, self, "Submit query", callback=self.submit)
        button.setFixedHeight(45)

        gui.rubber(self.controlArea)

        self.x0h_output = QtGui.QTextEdit()
        self.x0h_output.setReadOnly(True)

        out_box = gui.widgetBox(self.mainArea, "Query Results", addSpace=True, orientation="horizontal")
        out_box.layout().addWidget(self.x0h_output)

        self.x0h_output.setFixedHeight(500)
        self.x0h_output.setFixedWidth(850)


    def decode_selection(self):

        if self.selection == 0:
            return "crystals"
        elif self.selection == 1:
            return "amorphous"
        elif self.selection == 2:
            return "atoms"
        elif self.selection == 3:
            return "all+atoms"
        elif self.selection == 4:
            return "cubic-crystals"
        elif self.selection == 5:
            return "amorphous+atoms"
        elif self.selection == 6:
            return "all"
        elif self.selection == 7:
            return "waves"

    def submit(self):
        self.setStatusMessage("")

        self.x0h_output.clear()

        parameters = {}

        parameters.update({"x0hdb" : self.decode_selection()})
        parameters.update({"textout" : "1" })
        parameters.update({"namesonly" : str(self.details)})

        try:
            response = HttpManager.send_xray_server_request(APPLICATION, parameters).decode('ascii')

            self.x0h_output.setText(response)

            self.send("List", response)
        except urllib.error.HTTPError as e:
            self.x0h_output.setText('The server couldn\'t fulfill the request.\nError Code: '
                                    + str(e.code) + "\n\n" +
                                    server.BaseHTTPRequestHandler.responses[e.code][1])
        except urllib.error.URLError as e:
            self.x0h_output.setText('We failed to reach a server.\nReason: '
                                    + e.reason)






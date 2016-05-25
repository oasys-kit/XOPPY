__author__ = "Luca Rebuffi"

from oasys.widgets import widget
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui

import urllib
from http import server

from orangecontrib.xoppy.util.xoppy_util import HttpManager, ShowTextDialog, XoppyPhysics
import orangecontrib.xoppy.widgets.xrayserver as module

from PyQt4 import QtGui

APPLICATION = "cgi/X0h_form.exe"

class X0h(widget.OWWidget):
    name = "X0h"
    description = "X0h"
    icon = "icons/x0h.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "luca.rebuffi(@at@)elettra.eu"
    priority = 2
    category = "X0h"
    keywords = ["data", "file", "load", "read"]


    want_main_area = 1

    outputs = [{"name": "X0h_Result",
                "type": object,
                "doc": "X0h",
                "id": "x0h_result"}, ]


    xway = Setting(0)
    wave = Setting(0.0)
    line = Setting("Cu-Ka1")

    coway = Setting(0)
    code = Setting("Silicon")
    amor = Setting("")
    chem = Setting("")
    rho = Setting(0.0)

    def __init__(self):
        self.setFixedWidth(1200)
        self.setFixedHeight(600)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "X0h Request Form", addSpace=True, orientation="vertical",
                                         width=400, height=500)

        left_box_2 = oasysgui.widgetBox(left_box_1, "X-rays", addSpace=True, orientation="horizontal", width=380, height=110)

        left_box_2_1 = oasysgui.widgetBox(left_box_2, "", addSpace=True, orientation="vertical", width=150, height=150)

        gui.radioButtons(left_box_2_1, self, "xway", ["Wavelength (Å)", "Energy (keV)", "Characteristic line"], callback=self.set_xway )

        self.box_wave = oasysgui.widgetBox(left_box_2, "", addSpace=True, orientation="vertical", width=190)
        gui.separator(self.box_wave, height=10)
        gui.lineEdit(self.box_wave, self, "wave", label="", labelWidth=0, addSpace=False, valueType=float, orientation="horizontal")

        self.box_line = oasysgui.widgetBox(left_box_2, "", addSpace=True, orientation="horizontal", width=190, height=150)
        gui.separator(self.box_line, height=120)
        items = self.get_lines()
        combo = gui.comboBox(self.box_line, self, "line", label="", labelWidth=0,
                     items=items,
                     sendSelectedValue=True, orientation="horizontal")
        try:
            combo.setCurrentIndex(items.index(self.line))
        except:
            pass

        button = gui.button( self.box_line, self, "?", callback=self.help_lines)
        button.setFixedWidth(15)

        self.set_xway()

        left_box_3 = oasysgui.widgetBox(left_box_1, "Target", addSpace=True, orientation="horizontal", width=380, height=180)

        left_box_3_1 = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="vertical", width=150, height=150)

        gui.radioButtons(left_box_3_1, self, "coway", ["Crystal", "Other Material", "Chemical Formula"], callback=self.set_coway )

        self.box_crystal = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="horizontal", width=190)
        gui.comboBox(self.box_crystal, self, "code", label="", labelWidth=0,
                     items=self.get_crystals(),
                     sendSelectedValue=True, orientation="horizontal")
        button = gui.button( self.box_crystal, self, "?", callback=self.help_crystals)
        button.setFixedWidth(15)

        self.box_other = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="horizontal", width=190)
        gui.separator(self.box_other, height=75)
        gui.comboBox(self.box_other, self, "amor", label="", labelWidth=0,
                     items=self.get_others(),
                     sendSelectedValue=True, orientation="horizontal")
        button = gui.button( self.box_other, self, "?", callback=self.help_others)
        button.setFixedWidth(15)

        self.set_coway()


        button = gui.button(self.controlArea, self, "Get X0h!", callback=self.submit)
        button.setFixedHeight(45)

        gui.rubber(self.controlArea)

        self.x0h_output = QtGui.QTextEdit()
        self.x0h_output.setReadOnly(True)

        out_box = gui.widgetBox(self.mainArea, "Query Results", addSpace=True, orientation="horizontal")
        out_box.layout().addWidget(self.x0h_output)

        self.x0h_output.setFixedHeight(500)
        self.x0h_output.setFixedWidth(750)

    def set_xway(self):
        self.box_wave.setVisible(self.xway!=2)
        self.box_line.setVisible(self.xway==2)

    def set_coway(self):
        self.box_crystal.setVisible(self.coway==0)
        self.box_other.setVisible(self.coway==1)


    def submit(self):
        self.setStatusMessage("")

        self.checkFields()

        self.x0h_output.clear()

        parameters = {}

        parameters.update({"xway" : str(self.xway + 1)})
        parameters.update({"wave" : str(self.wave)})
        parameters.update({"line" : self.line})
        parameters.update({"coway" : str(self.coway)})
        parameters.update({"code" : self.code})
        parameters.update({"amor" : self.amor})
        parameters.update({"chem" : self.chem})
        parameters.update({"rho" : str(self.rho)})

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

    def checkFields(self):
        pass

    ''' ---------------------------------------------------------------------
        ---------------------------------------------------------------------
        ---------------------------------------------------------------------'''

    def get_lines(self):
        return module.ow_list.List.get_list("waves")

    def help_lines(self):
        ShowTextDialog.show_text("Help Waves", module.ow_list.List.get_help("waves"), width=350, parent=self)

    def get_crystals(self):
        return module.ow_list.List.get_list("crystals")

    def help_crystals(self):
        ShowTextDialog.show_text("Help Crystals", module.ow_list.List.get_help("crystals"), parent=self)

    def get_others(self):
        return module.ow_list.List.get_list("amorphous+atoms")

    def help_others(self):
        ShowTextDialog.show_text("Help Others", module.ow_list.List.get_help("amorphous+atoms"), parent=self)

    def set_Rho(self):
        if not self.chem is None:
            if not self.chem.strip() == "":
                self.chem = self.chem.strip()
                self.rho = XoppyPhysics.getMaterialDensity(self.chem)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = X0h()
    w.show()
    app.exec()
    w.saveSettings()



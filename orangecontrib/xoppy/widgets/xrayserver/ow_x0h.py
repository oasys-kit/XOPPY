__author__ = "Luca Rebuffi"

import numpy

from oasys.widgets import widget
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from PyMca5.PyMcaGui.plotting.PlotWindow import PlotWindow

import urllib
from http import server

from orangecontrib.xoppy.util.xoppy_util import HttpManager, ShowTextDialog, XoppyPhysics, XoppyGui, XoppyPlot
from orangecontrib.xoppy.widgets.xrayserver.list_utility import ListUtility

from PyQt4 import QtGui

APPLICATION = "/cgi/X0h_form.exe"

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


    xway = Setting(2)
    wave = Setting(0.0)
    line = Setting("Cu-Ka1")

    coway = Setting(0)
    code = Setting("Silicon")
    amor = Setting("")
    chem = Setting("")
    rho = Setting(0.0)

    i1 = Setting(1)
    i2 = Setting(1)
    i3 = Setting(1)

    df1df2 = Setting(1)
    detail = Setting(1)

    def __init__(self):
        self.setFixedWidth(1200)
        self.setFixedHeight(700)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "X0h Request Form", addSpace=True, orientation="vertical",
                                         width=400, height=630)

        left_box_2 = oasysgui.widgetBox(left_box_1, "X-rays", addSpace=True, orientation="horizontal", width=380, height=110)

        left_box_2_1 = oasysgui.widgetBox(left_box_2, "", addSpace=True, orientation="vertical", width=150, height=110)

        gui.radioButtons(left_box_2_1, self, "xway", ["Wavelength (Å)", "Energy (keV)", "Characteristic line"], callback=self.set_xway )

        self.box_wave = oasysgui.widgetBox(left_box_2, "", addSpace=True, orientation="vertical", width=190)
        gui.separator(self.box_wave, height=10)
        gui.lineEdit(self.box_wave, self, "wave", label="", labelWidth=0, addSpace=False, valueType=float, orientation="horizontal")

        self.box_line = oasysgui.widgetBox(left_box_2, "", addSpace=True, orientation="horizontal", width=190, height=110)
        gui.separator(self.box_line, height=120)
        XoppyGui.combobox_text(self.box_line, self, "line", label="", labelWidth=0,
                               items=self.get_lines(),
                               sendSelectedValue=True, orientation="horizontal", selectedValue=self.line)

        button = gui.button( self.box_line, self, "?", callback=self.help_lines)
        button.setFixedWidth(15)

        self.set_xway()

        left_box_3 = oasysgui.widgetBox(left_box_1, "Target", addSpace=True, orientation="horizontal", width=380, height=140)

        left_box_3_1 = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="vertical", width=125, height=110)

        gui.radioButtons(left_box_3_1, self, "coway", ["Crystal", "Other Material", "Chemical Formula"], callback=self.set_coway )

        self.box_crystal = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="horizontal", width=210)
        XoppyGui.combobox_text(self.box_crystal, self, "code", label="", labelWidth=0,
                               items=self.get_crystals(),
                               sendSelectedValue=True, orientation="horizontal", selectedValue=self.code)


        button = gui.button( self.box_crystal, self, "?", callback=self.help_crystals)
        button.setFixedWidth(15)

        self.box_other = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="horizontal", width=210)
        gui.separator(self.box_other, height=75)
        XoppyGui.combobox_text(self.box_other, self, "amor", label="", labelWidth=0,
                               items=self.get_others(),
                               sendSelectedValue=True, orientation="horizontal", selectedValue=self.amor)

        button = gui.button( self.box_other, self, "?", callback=self.help_others)
        button.setFixedWidth(15)

        self.box_chemical = oasysgui.widgetBox(left_box_3, "", addSpace=True, orientation="vertical", width=210, height=140)
        gui.separator(self.box_chemical, height=50)

        gui.lineEdit(self.box_chemical, self, "chem", label=" ", labelWidth=1, addSpace=False, valueType=str, orientation="horizontal", callback=self.set_Rho)
        gui.lineEdit(self.box_chemical, self, "rho", label=u"\u03C1" + " (g/cm3)", labelWidth=60, addSpace=False, valueType=float, orientation="horizontal")

        self.set_coway()

        left_box_4 = oasysgui.widgetBox(left_box_1, "Reflection", addSpace=True, orientation="horizontal", width=380, height=60)

        gui.lineEdit(left_box_4, self, "i1", label="Miller indices", labelWidth=200, addSpace=False, valueType=int, orientation="horizontal")
        gui.lineEdit(left_box_4, self, "i2", label=" ", labelWidth=1, addSpace=False, valueType=int, orientation="horizontal")
        gui.lineEdit(left_box_4, self, "i3", label=" ", labelWidth=1, addSpace=False, valueType=int, orientation="horizontal")

        left_box_5 = oasysgui.widgetBox(left_box_1, "Database Options for dispersion corrections df1, df2", addSpace=True, orientation="vertical", width=380, height=185)

        gui.radioButtons(left_box_5, self, "df1df2", ["Auto (Henke at low energy, X0h at mid, Brennan-Cowan\nat high)",
                                                      "Use X0h data (5-25 keV or 0.5-2.5 A), recommended for\nBragg diffraction",
                                                      "Use Henke data (0.01-30 keV or 0.4-1200 A),\nrecommended for soft x-rays",
                                                      "Use Brennan-Cowan data (0.03-700 keV or 0.02-400 A)",
                                                      "Compare results for all of the above sources"])

        left_box_6 = oasysgui.widgetBox(left_box_1, "Output Options", addSpace=True, orientation="vertical", width=380, height=50)

        gui.checkBox(left_box_6, self, "detail", "Print atomic coordinates", labelWidth=250)

        button = gui.button(self.controlArea, self, "Get X0h!", callback=self.submit)
        button.setFixedHeight(30)

        gui.rubber(self.controlArea)

        self.tabs = []
        self.tabs_widget = gui.tabWidget(self.mainArea)
        self.initializeTabs()

        self.x0h_output = QtGui.QTextEdit()
        self.x0h_output.setReadOnly(True)

        self.tabs[0].layout().addWidget(self.x0h_output)

        self.x0h_output.setFixedHeight(640)
        self.x0h_output.setFixedWidth(740)

    def set_xway(self):
        self.box_wave.setVisible(self.xway!=2)
        self.box_line.setVisible(self.xway==2)

    def set_coway(self):
        self.box_crystal.setVisible(self.coway==0)
        self.box_other.setVisible(self.coway==1)
        self.box_chemical.setVisible(self.coway==2)

    def initializeTabs(self):
        current_tab = self.tabs_widget.currentIndex()

        size = len(self.tabs)

        for index in range(0, size):
            self.tabs_widget.removeTab(size-1-index)

        self.tabs = [gui.createTabPage(self.tabs_widget, "X-ray Server Ouput"),
                     gui.createTabPage(self.tabs_widget, "Critical Angle for TER"),
                     gui.createTabPage(self.tabs_widget, "Darwin Curve (" + u"\u03C3" + " Pol.)"),
                     gui.createTabPage(self.tabs_widget, "Darwin Curve (" + u"\u03C0" + " Pol.)"),
                     ]

        for tab in self.tabs:
            tab.setFixedHeight(650)
            tab.setFixedWidth(750)

        self.plot_canvas = [None, None, None]

        self.tabs_widget.setCurrentIndex(current_tab)

    def submit(self):
        self.progressBarInit()
        self.setStatusMessage("Submitting Request")
        
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

        parameters.update({"i1" : str(self.i1)})
        parameters.update({"i2" : str(self.i2)})
        parameters.update({"i3" : str(self.i3)})
        parameters.update({"df1df2" : self.decode_df1df2()})

        parameters.update({"modeout" : "1" })
        parameters.update({"detail" : str(self.detail)})

        try:
            response = HttpManager.send_xray_server_request_POST(APPLICATION, parameters)
            response = response.split("</table></font></center>")[0] + "\n</body></html>"

            self.tabs_widget.setCurrentIndex(0)
            self.x0h_output.setText(response)

            data = self.extract_plots(response)

            self.send("X0h_Result", data)

        except urllib.error.HTTPError as e:
            self.x0h_output.setText('The server couldn\'t fulfill the request.\nError Code: '
                                    + str(e.code) + "\n\n" +
                                    server.BaseHTTPRequestHandler.responses[e.code][1])
        except urllib.error.URLError as e:
            self.x0h_output.setText('We failed to reach a server.\nReason: '
                                    + e.reason)

        self.setStatusMessage("")
        self.progressBarFinished()

    def checkFields(self):
        pass

    def decode_df1df2(self):
        if self.df1df2 == 0: return "-1"
        elif self.df1df2 == 1: return "0"
        elif self.df1df2 == 2: return "2"
        elif self.df1df2 == 3: return "4"
        elif self.df1df2 == 4: return "10"


    def extract_plots(self, response):
        form_1_begin = False
        form_2_begin = False
        form_3_begin = False

        form_1 = None
        form_2 = None
        form_3 = None

        rows = response.split("\n")

        for row in rows:
            if form_1_begin:
                if "<pre>" in row:
                    form_1_begin = False
            elif form_2_begin:
                if "<pre>" in row:
                    form_2_begin = False
            elif form_3_begin:
                if "<pre>" in row:
                    form_3_begin = False

            if form_1_begin:
                form_1.append(row)
            elif form_2_begin:
                form_2.append(row)
            elif form_3_begin:
                form_3.append(row)

            if "/cgi/ter_form.pl" in row:
                if form_1 is None:
                    form_1 = []
                    form_1_begin = True

            if "/cgi/gid_form.pl" in row:
                if form_2 is None:
                    form_2 = []
                    form_2_begin = True
                elif form_3 is None:
                    form_3 = []
                    form_3_begin = True

        self.setStatusMessage("Plotting Results")

        if not form_1 is None:
            x_1, y_1 = self.get_plots_from_form("/cgi/ter_form.pl", form_1)

            self.plot_histo(x_1, y_1, 40, 0, "Critical Angle for TER")
            self.tabs_widget.setCurrentIndex(1)
        else:
            x_1 = None
            y_1 = None
            
        if not form_2 is None:
            x_2, y_2 = self.get_plots_from_form("/cgi/gid_form.pl", form_2)

            self.plot_histo(x_2, y_2, 60, 1, "Darwin Curve ($\sigma$ Pol.)")
            self.tabs_widget.setCurrentIndex(2)
        else:
            x_2 = None
            y_2 = None

        if not form_3 is None:
            x_3, y_3 = self.get_plots_from_form("/cgi/gid_form.pl", form_3)

            self.plot_histo(x_3, y_3, 80, 2, "Darwin Curve ($\pi$ Pol.)")
            self.tabs_widget.setCurrentIndex(3)
        else:
            x_3 = None
            y_3 = None

        return [x_1, y_1], [x_2, y_2], [x_3, y_3]
    
    def get_plots_from_form(self, application, form):
        response = HttpManager.send_xray_server_request_POST(application, self.get_parameters_from_form(form))

        return self.get_data_file_from_response(response)
        
    
    def get_parameters_from_form(self, form):
        parameters = {}

        for row in form:
            temp = (row.split("name=\"")[1]).split("\"")
            key = temp[0]

            if len(temp) == 2:
                value = ((temp[1].split("value=")[1]).split(">")[0]).strip()
            else:
                value = temp[2].strip()

            parameters.update({key : value})

        return parameters

    def get_data_file_from_response(self, response):
        rows = response.split("\n")

        job_id = None
        data = None

        for row in rows:
            if "Job ID" in row:
                job_id = (row.split("<b>"))[1].split("</b>")[0]

            if not job_id is None:
                if job_id+".dat" in row:
                    data = HttpManager.send_xray_server_direct_request((row.split("href=\"")[1]).split("\"")[0])

        if not data is None:
            rows = data.split("\r\n")

            x = []
            y = []

            for row in rows:
                temp = row.strip().split(" ")

                if len(temp) > 1:
                    x.append(float(temp[0].strip()))
                    y.append(float(temp[len(temp)-1].strip()))

            return x, y
        else:
            return None, None

    def plot_histo(self, x, y, progressBarValue, plot_canvas_index, title="", xtitle="", ytitle=""):
        if self.plot_canvas[plot_canvas_index] is None:
            self.plot_canvas[plot_canvas_index] = PlotWindow(roi=False, control=False, position=False, plugins=False)
            self.plot_canvas[plot_canvas_index].setDefaultPlotLines(True)
            self.plot_canvas[plot_canvas_index].setActiveCurveColor(color='darkblue')
            self.plot_canvas[plot_canvas_index].setYAxisLogarithmic(True)

            self.tabs[plot_canvas_index+1].layout().addWidget(self.plot_canvas[plot_canvas_index])

        XoppyPlot.plot_histo(self.plot_canvas[plot_canvas_index], x, y, title, xtitle, ytitle)

        self.progressBarSet(progressBarValue)



    ''' ---------------------------------------------------------------------
        ---------------------------------------------------------------------
        ---------------------------------------------------------------------'''

    def get_lines(self):
        return ListUtility.get_list("waves")

    def help_lines(self):
        ShowTextDialog.show_text("Help Waves", ListUtility.get_help("waves"), width=350, parent=self)

    def get_crystals(self):
        return ListUtility.get_list("crystals")

    def help_crystals(self):
        ShowTextDialog.show_text("Help Crystals", ListUtility.get_help("crystals"), parent=self)

    def get_others(self):
        return ListUtility.get_list("amorphous+atoms")

    def help_others(self):
        ShowTextDialog.show_text("Help Others", ListUtility.get_help("amorphous+atoms"), parent=self)

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



from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget
from orangecontrib.xoppy.util.python_script import PythonScript

from xoppylib.crystals.mare_calc import mare_calc
from xraylib import Crystal_GetCrystalsList

class OWmare(XoppyWidget):
    name = "MARE"
    id = "orange.widgets.datamare"
    description = "Crystal Multiple Diffraction"
    icon = "icons/xoppy_mare.png"
    priority = 9
    category = ""
    keywords = ["xoppy", "mare"]

    CRYSTAL = Setting(2)
    H = Setting(2)
    K = Setting(2)
    L = Setting(2)
    HMAX = Setting(3)
    KMAX = Setting(3)
    LMAX = Setting(3)
    FHEDGE = Setting(1e-08)
    DISPLAY = Setting(0)
    LAMBDA = Setting(1.54)
    DELTALAMBDA = Setting(0.01)
    PHI = Setting(-20.0)
    DELTAPHI = Setting(0.1)

    number_of_scripts = 0

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=Crystal_GetCrystalsList(),
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "H",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "L",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "HMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "KMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "LMAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "FHEDGE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "DISPLAY",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Spaghetti', 'Spaghetti+Umweg', 'Spaghetti+Glitches', 'All'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "LAMBDA",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DELTALAMBDA",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "PHI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "DELTAPHI",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal:','h main','k main','l main','h max','k max','l max','Eliminate reflection with fh less than ','Display','Wavelength [A] (for Unweg)','Delta Wavelength [A]','Phi [deg] (for Glitches)','Delta Phi [deg]']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','self.DISPLAY  ==  1 or self.DISPLAY  ==  3','self.DISPLAY  ==  1 or self.DISPLAY  ==  3','self.DISPLAY  ==  2 or self.DISPLAY  ==  3','self.DISPLAY  ==  2 or self.DISPLAY  ==  3']

    def get_help_name(self):
        return 'mare'

    def check_fields(self):
        self.H = congruence.checkNumber(self.H, "h main")
        self.K = congruence.checkNumber(self.K, "k main")
        self.L = congruence.checkNumber(self.L, "l main")
        self.HMAX = congruence.checkNumber(self.HMAX, "h max")
        self.KMAX = congruence.checkNumber(self.KMAX, "k max")
        self.LMAX = congruence.checkNumber(self.LMAX, "l max")
        self.FHEDGE = congruence.checkNumber(self.FHEDGE, "Fh less than")

        if self.DISPLAY == 1 or self.DISPLAY == 3:
            self.LAMBDA = congruence.checkStrictlyPositiveNumber(self.LAMBDA, "Wavelength")
            self.DELTALAMBDA = congruence.checkStrictlyPositiveNumber(self.DELTALAMBDA, "Delta Wavelength")

        if self.DISPLAY == 2 or self.DISPLAY == 3:
            self.PHI = congruence.checkNumber(self.PHI, "Phi")
            self.DELTAPHI = congruence.checkStrictlyPositiveNumber(self.DELTALAMBDA, "Delta Phi")

    def do_xoppy_calculation(self):
        descriptor = Crystal_GetCrystalsList()[self.CRYSTAL]

        # Note that the output is a list of python scripts.
        # TODO: see how to send a script. TO be sent to the "python script" widget?
        # For the moment, this widget does not send anything!!

        list_of_scripts = mare_calc(descriptor,self.H,self.K,self.L,
                                               self.HMAX,self.KMAX,self.LMAX,self.FHEDGE,self.DISPLAY,
                                               self.LAMBDA,self.DELTALAMBDA,self.PHI,self.DELTAPHI)


        self.number_of_scripts = len(list_of_scripts)
        self.initializeTabs()
        return list_of_scripts

    def extract_data_from_xoppy_output(self, calculation_output):
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("xoppy_data", calculation_output)

        return calculated_data

    def get_data_exchange_widget_name(self):
        return "MARE"

    def getTitles(self):
        titles = []

        #'Spaghetti', 'Spaghetti+Umweg', 'Spaghetti+Glitches', 'All'
        if self.DISPLAY == 0:
            what = ["Spaghetti"]
        elif self.DISPLAY == 1:
            what = ["Spaghetti","Umweg"]
        elif self.DISPLAY == 2:
            what = ["Spaghetti", "Glitches"]
        elif self.DISPLAY == 3:
            what = ["Spaghetti", "Umweg","Glitches"]

        for index in range(0, self.number_of_scripts):
            titles.append("Python script # %d (%s)"%(index+1,what[index]) )

        return titles

    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:
                self.view_type_combo.setEnabled(False)

                list_of_scripts = calculated_data.get_content("xoppy_data")

                titles = self.getTitles()

                progress_bar_step = (100-progressBarValue)/len(titles)

                for index in range(0, len(titles)):

                    try:
                        self.write_script(list_of_scripts[index],
                                          progressBarValue + ((index+1)*progress_bar_step),
                                          tabs_canvas_index=index,
                                          plot_canvas_index=index)

                        self.tabs.setCurrentIndex(index)
                    except Exception as e:
                        self.view_type_combo.setEnabled(True)

                        raise Exception("Results not writable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)
            else:
                raise Exception("Empty Data")


    def write_script(self, script, progressBarValue, tabs_canvas_index, plot_canvas_index):
        if self.plot_canvas[plot_canvas_index] is None:
            # self.plot_canvas[plot_canvas_index] = QtWidgets.QTextEdit(self.tab[tabs_canvas_index])
            #SRIOSRIO
            self.plot_canvas[plot_canvas_index] = PythonScript()
            self.plot_canvas[plot_canvas_index].code_area.setFixedHeight(400)
            #TO DO: get it working with PythonWidget!!!
            # self.plot_canvas[plot_canvas_index] = PythonWidget(self.tab[tabs_canvas_index])
            self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])

        script1 = script.replace("nan", "numpy.nan")
        # self.plot_canvas[plot_canvas_index].setText(script1)
        self.plot_canvas[plot_canvas_index].set_code(script1)
        exec(script1)
        self.progressBarSet(progressBarValue)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = OWmare()
    w.show()
    app.exec()
    w.saveSettings()

    # list_of_scripts = mare_calc("Si2",2,2,2,3,3,3,2e-8,3,1.54,0.01,-20.0,0.1)
    # for script in list_of_scripts:
    #     exec(script)

    # app = QApplication(sys.argv)
    # w = PythonWidget(None)
    # w.setText("import numpy\nprint(numpy.arange(10))")
    # w.show()
    # app.exec()

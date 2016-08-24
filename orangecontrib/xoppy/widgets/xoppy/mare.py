import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget
from orangecontrib.xoppy.util import xoppy_util
from orangecontrib.xoppy.widgets.xoppy.xoppy_xraylib_util import mare_calc
from xraylib import Crystal_GetCrystalsList

class OWmare(widget.OWWidget):
    name = "mare"
    id = "orange.widgets.datamare"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_mare.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 8
    category = ""
    keywords = ["xoppy", "mare"]

    #TODO: see how a python script can be send as a signel
    # outputs = [{"name": "xoppy_data",
    #             "type": numpy.ndarray,
    #             "doc": ""},
    #            {"name": "xoppy_specfile",
    #             "type": str,
    #             "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

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


    def __init__(self):
        super().__init__()

        box0 = gui.widgetBox(self.controlArea, " ",orientation="horizontal") 
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Defaults", callback=self.defaults)
        gui.button(box0, self, "Help", callback=self.help1)
        self.process_showers()
        box = gui.widgetBox(self.controlArea, " ",orientation="vertical") 
        
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=Crystal_GetCrystalsList(),
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "H",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "L",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "KMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FHEDGE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "DISPLAY",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Spaghetti', 'Spaghetti+Umweg', 'Spaghetti+Glitches', 'All'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DELTALAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "PHI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DELTAPHI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal:','h main','k main','l main','h max','k max','l max','Eliminate reflection with fh less than ','Display','Wavelength [A] (for Unweg)','Delta Wavelength [A]','Phi [deg] (for Glitches)','Delta Phi [deg]']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','self.DISPLAY  ==  1 or self.DISPLAY  ==  3','self.DISPLAY  ==  1 or self.DISPLAY  ==  3','self.DISPLAY  ==  2 or self.DISPLAY  ==  3','self.DISPLAY  ==  2 or self.DISPLAY  ==  3']

    def compute(self):

        descriptor = Crystal_GetCrystalsList()[self.CRYSTAL]

        # Note that the output is a list of python scripts.
        # TODO: see how to send a script. TO be sent to the "python script" widget?
        # For the moment, this widget does not send anything!!

        list_of_scripts = mare_calc(descriptor,self.H,self.K,self.L,
                                               self.HMAX,self.KMAX,self.LMAX,self.FHEDGE,self.DISPLAY,
                                               self.LAMBDA,self.DELTALAMBDA,self.PHI,self.DELTAPHI)

        for script in list_of_scripts:
            exec(script)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('mare')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWmare()
    w.show()
    app.exec()
    w.saveSettings()

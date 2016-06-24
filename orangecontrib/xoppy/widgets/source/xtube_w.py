import sys, os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from PyMca5.PyMcaIO import specfilewrapper as specfile
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets.widget import OWWidget
from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.util.xoppy_util import locations

from orangecontrib.xoppy.util import xoppy_util

class OWxtube_w(OWWidget):
    name = "xtube_w"
    id = "orange.widgets.dataxtube_w"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xtube_w.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 8
    category = ""
    keywords = ["xoppy", "xtube_w"]
    outputs = [{"name": "xoppy_data",
                "type": numpy.ndarray,
                "doc": ""},
               {"name": "xoppy_specfile",
                "type": str,
                "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    VOLTAGE = Setting(100.0)
    RIPPLE = Setting(0.0)
    AL_FILTER = Setting(0.0)


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
        gui.lineEdit(box1, self, "VOLTAGE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "RIPPLE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "AL_FILTER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Voltage 30<V<140 (kV)','Voltage ripple (%)','Al filter [mm]']


    def unitFlags(self):
         return ['True','True','True']


    #def unitNames(self):
    #     return ['VOLTAGE','RIPPLE','AL_FILTER']


    def compute(self):
        fileName = xoppy_calc_xtube_w(VOLTAGE=self.VOLTAGE,RIPPLE=self.RIPPLE,AL_FILTER=self.AL_FILTER)
        #send specfile

        if fileName == None:
            print("Nothing to send")
        else:
            self.send("xoppy_specfile",fileName)
            sf = specfile.Specfile(fileName)
            if sf.scanno() == 1:
                #load spec file with one scan, # is comment
                print("Loading file:  ",fileName)
                out = numpy.loadtxt(fileName)
                print("data shape: ",out.shape)
                #get labels
                txt = open(fileName).readlines()
                tmp = [ line.find("#L") for line in txt]
                itmp = numpy.where(numpy.array(tmp) != (-1))
                labels = txt[itmp[0]].replace("#L ","").split("  ")
                print("data labels: ",labels)
                self.send("xoppy_data",out)
            else:
                print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xtube_w')


def xoppy_calc_xtube_w(VOLTAGE=100.0,RIPPLE=0.0,AL_FILTER=0.0):
    print("Inside xoppy_calc_xtube_w. ")

    try:
        with open("xoppy.inp","wt") as f:
            f.write("%f\n%f\n%f\n"%(VOLTAGE,RIPPLE,AL_FILTER))
    
        command = os.path.join(locations.home_bin(), 'tasmip') + " < xoppy.inp"
        print("Running command '%s' in directory: %s \n"%(command,locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

        return "tasmip_tmp.dat"
    except Exception as e:
        raise e




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtube_w()
    w.show()
    app.exec()
    w.saveSettings()

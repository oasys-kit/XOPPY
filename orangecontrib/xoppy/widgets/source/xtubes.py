import sys, os
import numpy 
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from PyMca5.PyMcaIO import specfilewrapper as specfile
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets.widget import OWWidget
from oasys.widgets.exchange import DataExchangeObject
from orangewidget.widget import OWAction
from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.util import xoppy_util

class OWxtubes(OWWidget):
    name = "xtubes"
    id = "orange.widgets.dataxtubes"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xtubes.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 9
    category = ""
    keywords = ["xoppy", "xtubes"]
    outputs = [{"name": "xoppy_data",
                "type": numpy.ndarray,
                "doc": ""},
               {"name": "xoppy_specfile",
                "type": str,
                "doc": ""},
               {"name": "xoppy_exchange_data",
               "type": DataExchangeObject,
               "doc": ""},]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    ITUBE = Setting(0)
    VOLTAGE = Setting(30.0)


    def __init__(self):
        super().__init__()

        self.runaction = OWAction("Compute", self)
        self.runaction.triggered.connect(self.compute)
        self.addAction(self.runaction)

        box0 = gui.widgetBox(self.controlArea, "Input",orientation="horizontal")
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
        gui.comboBox(box1, self, "ITUBE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Mo', 'Rh', 'W'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "VOLTAGE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Target element ','Voltage  [kV] (18<V<42)']


    def unitFlags(self):
         return ['True','True']


    #def unitNames(self):
    #     return ['ITUBE','VOLTAGE']


    def compute(self):
        fileName = xoppy_calc_xtubes(ITUBE=self.ITUBE,VOLTAGE=self.VOLTAGE)
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

                exchange_data = DataExchangeObject("XOPPY", "XTUBES")

                exchange_data.add_content("xoppy_specfile", fileName)
                exchange_data.add_content("xoppy_data", out)

                self.send("xoppy_exchange_data", exchange_data)
            else:
                print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xtubes')



def xoppy_calc_xtubes(ITUBE=0,VOLTAGE=30.0):
    print("Inside xoppy_calc_xtubes. ")

    try:
        with open("xoppy.inp","wt") as f:
            f.write("%d\n%f\n"%(ITUBE+1,VOLTAGE))
    
        command = os.path.join(locations.home_bin(), "xtubes") + " < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

        return os.path.join(locations.home_bin_run(), "xtubes_tmp.dat")
    except Exception as e:
        raise e



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxtubes()
    w.show()
    app.exec()
    w.saveSettings()

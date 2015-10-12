import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np
from PyMca5.PyMcaIO import specfilewrapper as specfile

try:
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise

try:
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xfilter
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xfilter")
    raise

class OWxfilter(widget.OWWidget):
    name = "xfilter"
    id = "orange.widgets.dataxfilter"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xfilter.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xfilter"]
    outputs = [#{"name": "xoppy_data",
               # "type": np.ndarray,
               # "doc": ""},
               {"name": "xoppy_table",
                "type": Table,
                "doc": ""},
               {"name": "xoppy_specfile",
                "type": str,
                "doc": ""}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    EMPTY1 = Setting("              ")
    EMPTY2 = Setting("              ")
    NELEMENTS = Setting(1)
    SOURCE = Setting(0)
    ENER_MIN = Setting(1000.0)
    ENER_MAX = Setting(50000.0)
    ENER_N = Setting(100)
    SOURCE_FILE = Setting("SRCOMPW")
    EL1_SYM = Setting("Be")
    EL1_THI = Setting(500.0)
    EL2_SYM = Setting("Al")
    EL2_THI = Setting(50.0)
    EL3_SYM = Setting("Pt")
    EL3_THI = Setting(10.0)
    EL4_SYM = Setting("Au")
    EL4_THI = Setting(10.0)
    EL5_SYM = Setting("Cu")
    EL5_THI = Setting(10.0)


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
        gui.lineEdit(box1, self, "EMPTY1",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMPTY2",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "NELEMENTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['1', '2', '3', '4', '5'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SOURCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Normalized to 1           ', 'From external file.       ', 'xop/source SRCOMPE (Flux) ', 'xop/source SRCOMPW (Power)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENER_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENER_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENER_N",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SOURCE_FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_SYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL1_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_SYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL2_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_SYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL3_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_SYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL4_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_SYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EL5_THI",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True','True']


    #def unitNames(self):
    #     return ['EMPTY1','EMPTY2','NELEMENTS','SOURCE','ENER_MIN','ENER_MAX','ENER_N','SOURCE_FILE','EL1_SYM','EL1_THI','EL2_SYM','EL2_THI','EL3_SYM','EL3_THI','EL4_SYM','EL4_THI','EL5_SYM','EL5_THI']


    def compute(self):
        fileName = xoppy_calc_xfilter(EMPTY1=self.EMPTY1,EMPTY2=self.EMPTY2,NELEMENTS=self.NELEMENTS,SOURCE=self.SOURCE,ENER_MIN=self.ENER_MIN,ENER_MAX=self.ENER_MAX,ENER_N=self.ENER_N,SOURCE_FILE=self.SOURCE_FILE,EL1_SYM=self.EL1_SYM,EL1_THI=self.EL1_THI,EL2_SYM=self.EL2_SYM,EL2_THI=self.EL2_THI,EL3_SYM=self.EL3_SYM,EL3_THI=self.EL3_THI,EL4_SYM=self.EL4_SYM,EL4_THI=self.EL4_THI,EL5_SYM=self.EL5_SYM,EL5_THI=self.EL5_THI)
        #send specfile

        if fileName == None:
            print("Nothing to send")
        else:
            self.send("xoppy_specfile",fileName)
            sf = specfile.Specfile(fileName)
            if sf.scanno() == 1:
                #load spec file with one scan, # is comment
                print("Loading file:  ",fileName)
                out = np.loadtxt(fileName)
                print("data shape: ",out.shape)
                #get labels
                txt = open(fileName).readlines()
                tmp = [ line.find("#L") for line in txt]
                itmp = np.where(np.array(tmp) != (-1))
                labels = txt[itmp[0]].replace("#L ","").split("  ")
                print("data labels: ",labels)
                #
                # build and send orange table
                #
                domain = Domain([ ContinuousVariable(i) for i in labels ])
                table = Table.from_numpy(domain, out)
                self.send("xoppy_table",table)
            else:
                print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('xfilter')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxfilter()
    w.show()
    app.exec()
    w.saveSettings()

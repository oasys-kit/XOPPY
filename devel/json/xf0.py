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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xf0
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xf0")
    raise

class OWxf0(widget.OWWidget):
    name = "xf0"
    id = "orange.widgets.dataxf0"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xf0.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xf0"]
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

    DATASETS = Setting(0)
    MAT_FLAG = Setting(0)
    MAT_LIST = Setting(0)
    DESCRIPTOR = Setting("Si")
    GRID = Setting(0)
    GRIDSTART = Setting(0.0)
    GRIDEND = Setting(4.0)
    GRIDN = Setting(100)


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
        gui.comboBox(box1, self, "DATASETS",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['all', 'f0_xop.dat'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Element(formula)', 'Mixture(formula)', 'Mixture(table)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MAT_LIST",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['B4C', 'BeO', 'BN', 'Cr2O3', 'CsI', 'GaAs', 'LiF', 'MgO', 'MoSi2', 'TiN', 'Sapphire', 'Polyimide', 'Polypropylene', 'PMMA', 'Polycarbonate', 'Kimfol', 'Mylar', 'Teflon', 'Parylene-C', 'Parylene-N', 'Fluorite', 'Salt', 'NiO', 'SiC', 'Si3N4', 'Silica', 'Quartz', 'Rutile', 'ULE', 'Zerodur', 'water', 'protein', 'lipid', 'nucleosome', 'dna', 'helium', 'chromatin', 'air', 'pmma', 'nitride', 'graphite', 'nickel', 'beryl', 'copper', 'quartz', 'aluminum', 'gold', 'ice', 'carbon', 'polystyrene', 'A-150 TISSUE-EQUIVALENT PLASTIC', 'ADIPOSE TISSUE (ICRU-44)', 'AIR, DRY (NEAR SEA LEVEL)', 'ALANINE', 'B-100 BONE-EQUIVALENT PLASTIC', 'BAKELITE', 'BLOOD, WHOLE (ICRU-44)', 'BONE, CORTICAL (ICRU-44)', 'BRAIN, GREY/WHITE MATTER (ICRU-44)', 'BREAST TISSUE (ICRU-44)', 'C-552 AIR-EQUIVALENT PLASTIC', 'CADMIUM TELLURIDE', 'CALCIUM FLUORIDE', 'CALCIUM SULFATE', '15e-3 M CERIC AMMONIUM SULFATE SOLUTION', 'CESIUM IODIDE', 'CONCRETE, ORDINARY', 'CONCRETE, BARITE (TYPE BA)', 'EYE LENS (ICRU-44)', 'FERROUS SULFATE (STANDARD FRICKE)', 'GADOLINIUM OXYSULFIDE', 'GAFCHROMIC SENSOR', 'GALLIUM ARSENIDE', 'GLASS, BOROSILICATE (PYREX)', 'GLASS, LEAD', 'LITHIUM FLUORIDE', 'LITHIUM TETRABORATE', 'LUNG TISSUE (ICRU-44)', 'MAGNESIUM TETRABORATE', 'MERCURIC IODIDE', 'MUSCLE, SKELETAL (ICRU-44)', 'OVARY (ICRU-44)', 'PHOTOGRAPHIC EMULSION (KODAK TYPE AA)', 'PHOTOGRAPHIC EMULSION (STANDARD NUCLEAR)', 'PLASTIC SCINTILLATOR (VINYLTOLUENE)', 'POLYETHYLENE', 'POLYETHYLENE TEREPHTHALATE (MYLAR)', 'POLYMETHYL METHACRYLATE', 'POLYSTYRENE', 'POLYTETRAFLUOROETHYLENE (TEFLON)', 'POLYVINYL CHLORIDE', 'RADIOCHROMIC DYE FILM (NYLON BASE)', 'TESTIS (ICRU-44)', 'TISSUE, SOFT (ICRU-44)', 'TISSUE, SOFT (ICRU FOUR-COMPONENT)', 'TISSUE-EQUIVALENT GAS (METHANE BASED)', 'TISSUE-EQUIVALENT GAS (PROPANE BASED)', 'WATER, LIQUID'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTOR",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Standard', 'User defined'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['datasets:','material','table','formula','sin_theta/lambda grid:','From: ','To: ','Number of points']


    def unitFlags(self):
         return ['True','True','self.MAT_FLAG  ==  2','self.MAT_FLAG  !=  2','True','self.GRID  !=  0','self.GRID  !=  0','self.GRID  !=  0']


    #def unitNames(self):
    #     return ['DATASETS','MAT_FLAG','MAT_LIST','DESCRIPTOR','GRID','GRIDSTART','GRIDEND','GRIDN']


    def compute(self):
        fileName = xoppy_calc_xf0(DATASETS=self.DATASETS,MAT_FLAG=self.MAT_FLAG,MAT_LIST=self.MAT_LIST,DESCRIPTOR=self.DESCRIPTOR,GRID=self.GRID,GRIDSTART=self.GRIDSTART,GRIDEND=self.GRIDEND,GRIDN=self.GRIDN)
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
        xoppy_doc('xf0')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxf0()
    w.show()
    app.exec()
    w.saveSettings()

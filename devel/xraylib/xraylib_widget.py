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
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_xraylib_widget
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_xraylib_widget")
    raise

class OWxraylib_widget(widget.OWWidget):
    name = "xraylib_widget"
    id = "orange.widgets.dataxraylib_widget"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xraylib_widget.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xraylib_widget"]
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

    FUNCTION = Setting(0)
    ELEMENT = Setting(26)
    ELEMENTORCOMPOUND = Setting("FeSO4")
    COMPOUND = Setting("Ca5(PO4)3")
    TRANSITION_IUPAC_OR_SIEGBAHN = Setting(1)
    TRANSITION_IUPAC_TO = Setting(0)
    TRANSITION_IUPAC_FROM = Setting(0)
    TRANSITION_SIEGBAHN = Setting(0)
    SHELL = Setting(0)
    ENERGY = Setting(10.0)


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
        gui.comboBox(box1, self, "FUNCTION",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['0 Fluorescence line energy', '1 Absorption edge energy', '2 Atomic weight', '3 Elemental density', '4 Total absorption cross section', '5 Photoionization cross section', '6 Partial photoionization cross section', '7 Rayleigh scattering cross section', '8 Compton scattering cross section', '9 Klein-Nishina cross section', '10 Mass energy-absorption cross section', '11 Differential unpolarized Klein-Nishina cross section', '12 Differential unpolarized Thomson cross section', '13 Differential unpolarized Rayleigh cross section', '14 Differential unpolarized Compton cross section', '15 Differential polarized Klein-Nishina cross section', '16 Differential polarized Thomson cross section', '17 Differential polarized Rayleigh cross section', '18 Differential polarized Compton cross section', '19 Atomic form factor', '20 Incoherent scattering function', '21 Momentum transfer function', '22 Coster-Kronig transition probability', '23 Fluorescence yield', '24 Jump factor', '25 Radiative transition probability', '26 Energy after Compton scattering', '27 Anomalous scattering factor &phi;&prime;', '28 Anomalous scattering factor &phi;&Prime;', '29 Electronic configuration', '30 X-ray fluorescence production cross section (with full cascade)', '31 X-ray fluorescence production cross section (with radiative cascade)', '32 X-ray fluorescence production cross section (with non-radiative cascade)', '33 X-ray fluorescence production cross section (without cascade)', '34 Atomic level width', '35 Auger yield', '36 Auger rate', '37 Refractive index', '38 Compton broadening profile', '39 Partial Compton broadening profile', '40 List of NIST catalog compounds', '41 Get composition of NIST catalog compound', '42 List of X-ray emitting radionuclides', '43 Get excitation profile of X-ray emitting radionuclide', '44 Compoundparser'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELEMENT",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ELEMENTORCOMPOUND",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "COMPOUND",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_IUPAC_OR_SIEGBAHN",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['IUPAC', 'SIEGBAHN', 'ALL TRANSITIONS'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_IUPAC_TO",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_IUPAC_FROM",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_SIEGBAHN",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['KA1_LINE', 'KA2_LINE', 'KB1_LINE', 'KB2_LINE', 'KB3_LINE', 'KB4_LINE', 'KB5_LINE', 'LA1_LINE', 'LA2_LINE', 'LB1_LINE', 'LB2_LINE', 'LB3_LINE', 'LB4_LINE', 'LB5_LINE', 'LB6_LINE', 'LB7_LINE', 'LB9_LINE', 'LB10_LINE', 'LB15_LINE', 'LB17_LINE', 'LG1_LINE', 'LG2_LINE', 'LG3_LINE', 'LG4_LINE', 'LG5_LINE', 'LG6_LINE', 'LG8_LINE', 'LE_LINE', 'LL_LINE', 'LS_LINE', 'LT_LINE', 'LU_LINE', 'LV_LINE'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SHELL",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['All shells', 'K_SHELL', 'L1_SHELL', 'L2_SHELL', 'L3_SHELL', 'M1_SHELL', 'M2_SHELL', 'M3_SHELL', 'M4_SHELL', 'M5_SHELL', 'N1_SHELL', 'N2_SHELL', 'N3_SHELL', 'N4_SHELL', 'N5_SHELL', 'N6_SHELL', 'N7_SHELL', 'O1_SHELL', 'O2_SHELL', 'O3_SHELL', 'O4_SHELL', 'O5_SHELL', 'O6_SHELL', 'O7_SHELL', 'P1_SHELL', 'P2_SHELL', 'P3_SHELL', 'P4_SHELL', 'P5_SHELL', 'Q1_SHELL', 'Q2_SHELL', 'Q3_SHELL'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ["Calculate", "Atomic number", "Element or compound name", "Compound name", "Transition notation", "Transition to (iupac)","Transition from (iupac)","Transition (Siegbahn)","Shell","Energy [keV]"]


    def unitFlags(self):
         return ["True", "self.FUNCTION <= 3 or self.FUNCTION == 6", "self.FUNCTION == 4 or self.FUNCTION == 5 or self.FUNCTION == 7 or self.FUNCTION == 8 or self.FUNCTION == 10", "self.FUNCTION > 100","self.FUNCTION == 0", "(self.FUNCTION == 0 and self.TRANSITION_IUPAC_OR_SIEGBAHN == 0)", "(self.FUNCTION == 0 and self.TRANSITION_IUPAC_OR_SIEGBAHN == 0)", "(self.FUNCTION == 0 and self.TRANSITION_IUPAC_OR_SIEGBAHN == 1)","self.FUNCTION == 1 or self.FUNCTION == 6","self.FUNCTION >= 4 "]


    #def unitNames(self):
    #     return ["FUNCTION", "ELEMENT", "ELEMENTORCOMPOUND", "COMPOUND","TRANSITION_IUPAC_OR_SIEGBAHN","TRANSITION_IUPAC_TO","TRANSITION_IUPAC_FROM","TRANSITION_SIEGBAHN","SHELL","ENERGY"]


    def compute(self):
        fileName = xoppy_calc_xraylib_widget(FUNCTION=self.FUNCTION,ELEMENT=self.ELEMENT,ELEMENTORCOMPOUND=self.ELEMENTORCOMPOUND,COMPOUND=self.COMPOUND,TRANSITION_IUPAC_OR_SIEGBAHN=self.TRANSITION_IUPAC_OR_SIEGBAHN,TRANSITION_IUPAC_TO=self.TRANSITION_IUPAC_TO,TRANSITION_IUPAC_FROM=self.TRANSITION_IUPAC_FROM,TRANSITION_SIEGBAHN=self.TRANSITION_SIEGBAHN,SHELL=self.SHELL,ENERGY=self.ENERGY)
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
        xoppy_doc('xraylib_widget')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxraylib_widget()
    w.show()
    app.exec()
    w.saveSettings()

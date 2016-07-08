import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util import xoppy_util


from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.xoppy.xoppy_xraylib_util import cross_calc,cross_calc_mix
import xraylib


class OWxcrosssec(widget.OWWidget):
    name = "xcrosssec"
    id = "orange.widgets.dataxcrosssec"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xcrosssec.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xcrosssec"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    MAT_FLAG = Setting(0)
    MAT_LIST = Setting(0)
    DESCRIPTOR = Setting("Si")
    DENSITY = Setting(1.0)
    CALCULATE = Setting(1)
    GRID = Setting(0)
    GRIDSTART = Setting(100.0)
    GRIDEND = Setting(10000.0)
    GRIDN = Setting(200)
    UNIT = Setting(0)


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
        items = xraylib.GetCompoundDataNISTList()
        gui.comboBox(box1, self, "MAT_LIST",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=items,
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
        gui.lineEdit(box1, self, "DENSITY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        # gui.lineEdit(box1, self, "CALCULATE",
        #              label=self.unitLabels()[idx], addSpace=True)
        # self.show_at(self.unitFlags()[idx], box1)
        gui.comboBox(box1, self, "CALCULATE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['Total','PhotoElectric','Rayleigh','Compton','Total-Rayleigh'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Standard', 'User defined', 'Single Value'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDSTART",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDEND",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "UNIT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['barn/atom [Cross Section] *see help*', 'cm^2 [Cross Section] *see help*', 'cm^2/g [Mass abs coef]', 'cm^-1 [Linear abs coef]'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material','table','formula','density','Cross section','Energy [eV] grid:','Starting Energy [eV]: ','To: ','Number of points','Units']


    def unitFlags(self):
         return ['True','self.MAT_FLAG  ==  2','self.MAT_FLAG  <=  1 ','self.MAT_FLAG  ==  1  &  self.UNIT  ==  3','True','True','self.GRID  !=  0','self.GRID  ==  1','self.GRID  ==  1','True']

    def compute(self):
        out_dict = self.xoppy_calc_xcrosssec()

        if "info" in out_dict.keys():
            print(out_dict["info"])

        #send exchange
        tmp = DataExchangeObject("xoppy_calc_crosssec","xcrosssec")
        try:
            tmp.add_content("data",out_dict["data"])
            tmp.add_content("plot_x_col",0)
            tmp.add_content("plot_y_col",-1)
        except:
            pass
        try:
            tmp.add_content("labels",out_dict["labels"])
        except:
            pass
        try:
            tmp.add_content("info",out_dict["info"])
        except:
            pass


        self.send("ExchangeData",tmp)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xcrosssec')


    def xoppy_calc_xcrosssec(self):

        MAT_FLAG = self.MAT_FLAG
        MAT_LIST = self.MAT_LIST
        DESCRIPTOR = self.DESCRIPTOR
        density = self.DENSITY
        CALCULATE = self.CALCULATE
        GRID = self.GRID
        GRIDSTART = self.GRIDSTART
        GRIDEND = self.GRIDEND
        GRIDN = self.GRIDN
        UNIT = self.UNIT


        if MAT_FLAG == 0: # element
            descriptor = DESCRIPTOR
            density = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(DESCRIPTOR))
        elif MAT_FLAG == 1: # formula
            descriptor = DESCRIPTOR
        elif MAT_FLAG == 2:
            tmp = xraylib.GetCompoundDataNISTByIndex(MAT_LIST)
            descriptor = tmp["name"]
            density = tmp["density"]

        print("xoppy_calc_xcrosssec: using density = %g g/cm3"%density)
        if GRID == 0:
            energy = numpy.arange(0,500)
            elefactor = numpy.log10(10000.0 / 30.0) / 300.0
            energy = 10.0 * 10**(energy * elefactor)
        elif GRID == 1:
            if GRIDN == 1:
                energy = numpy.array([GRIDSTART])
            else:
                energy = numpy.linspace(GRIDSTART,GRIDEND,GRIDN)
        elif GRID == 2:
            energy = numpy.array([GRIDSTART])

        if MAT_FLAG == 0: # element
            out =  cross_calc(descriptor,energy,calculate=CALCULATE,density=density)
        elif MAT_FLAG == 1: # compound parse
            out =  cross_calc_mix(descriptor,energy,calculate=CALCULATE,density=density,parse_or_nist=0)
        elif MAT_FLAG == 2: # NIST compound
            out =  cross_calc_mix(descriptor,energy,calculate=CALCULATE,density=density,parse_or_nist=1)

        calculate_items = ['Total','PhotoElectric','Rayleigh','Compton','Total minus Rayleigh']
        unit_items = ['barn/atom','cm^2','cm^2/g','cm^-1']
        if energy.size > 1:
            tmp_x = out[0,:].copy()
            tmp_y = out[UNIT+1,:].copy()
            tmp = numpy.vstack((tmp_x,tmp_y))
            labels = ["Photon energy [eV]","%s cross section [%s]"%(calculate_items[CALCULATE],unit_items[UNIT])]
            to_return = {"application":"xoppy","name":"xcrosssec","data":tmp,"labels":labels}
        else:
            tmp = None
            txt = "xoppy_calc_xcrosssec: Calculated %s cross section: %g %s"%(calculate_items[CALCULATE],out[UNIT+1,0],unit_items[UNIT])
            print(txt)
            to_return  = {"application":"xoppy","name":"xcrosssec","info":txt}

        return to_return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxcrosssec()
    w.show()
    app.exec()
    w.saveSettings()

import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util import xoppy_util


from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.xoppy.xoppy_xraylib_util import f1f2_calc,f1f2_calc_mix
import xraylib


class OWxf1f2(widget.OWWidget):
    name = "xf1f2"
    id = "orange.widgets.dataxf1f2"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xf1f2.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "xf1f2"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    # DATASETS = Setting(1)
    MAT_FLAG = Setting(0)
    DESCRIPTOR = Setting("Si")
    DENSITY = Setting(1.0)
    CALCULATE = Setting(1)
    GRID = Setting(0)
    GRIDSTART = Setting(5000.0)
    GRIDEND = Setting(25000.0)
    GRIDN = Setting(100)
    THETAGRID = Setting(0)
    ROUGH = Setting(0.0)
    THETA1 = Setting(2.0)
    THETA2 = Setting(5.0)
    THETAN = Setting(50)


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
                    items=['Element(formula)', 'Mixture(formula)'],
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
        gui.comboBox(box1, self, "CALCULATE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['f1', 'f2', 'delta', 'beta *see help*', 'mu [cm^-1] *see help*', 'mu [cm^2/g] *see help*', 'Cross Section[barn] *see help*', 'reflectivity-s', 'reflectivity-p', 'reflectivity-unpol', 'delta/beta **see help**'],
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
        gui.comboBox(box1, self, "THETAGRID",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Single value', 'User Defined'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ROUGH",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THETA1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "THETA2",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "THETAN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1)

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['material',                        #   True',
                 'formula',                         #   self.MAT_FLAG  <=  1',
                 'density',                         #   self.MAT_FLAG  ==  1  &  (s
                 'Calculate',                       #   True',
                 'Energy [eV] grid:',               #   True',
                 'Starting Energy [eV]: ',          #   self.GRID  !=  0',
                 'To: ',                            #   self.GRID  ==  1',
                 'Number of points',                #   self.GRID  ==  1',
                 'Grazing angle',                   #   self.CALCULATE  ==  0 or (s
                 'Roughness rms [A]',               #   self.CALCULATE  ==  0 or (s
                 'Starting Graz angle [mrad]',      #   self.CALCULATE  ==  0 or (s
                 'To [mrad]',                       #   (self.CALCULATE  ==  0 or (
                 'Number of angular points']        #   (self.CALCULATE  ==  0 or (


    def unitFlags(self):
         return ['True',
                 'self.MAT_FLAG  <=  1',
                 'self.MAT_FLAG  ==  1  or (self.MAT_FLAG  ==  1 and  (self.CALCULATE  ==  2 or self.CALCULATE  ==  3 or self.CALCULATE  ==  4 or self.CALCULATE  ==  7 or self.CALCULATE  ==  8 or self.CALCULATE  ==  9 or self.CALCULATE  ==  10 ))  ',
                 'True',
                 'True',
                 'self.GRID  !=  0',
                 'self.GRID  ==  1',
                 'self.GRID  ==  1',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 'self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9',
                 '(self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9)  &  self.THETAGRID  ==  1',
                 '(self.CALCULATE  == 7 or  self.CALCULATE == 8 or self.CALCULATE  == 9)  &  self.THETAGRID  ==  1']



    def compute(self):

        MAT_FLAG   = self.MAT_FLAG
        DESCRIPTOR = self.DESCRIPTOR
        density    = self.DENSITY
        CALCULATE  = self.CALCULATE
        GRID       = self.GRID
        GRIDSTART  = self.GRIDSTART
        GRIDEND    = self.GRIDEND
        GRIDN      = self.GRIDN
        THETAGRID  = self.THETAGRID
        ROUGH      = self.ROUGH
        THETA1     = self.THETA1
        THETA2     = self.THETA2
        THETAN     = self.THETAN




        if MAT_FLAG == 0: # element
            descriptor = DESCRIPTOR
            density = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(DESCRIPTOR))
        elif MAT_FLAG == 1: # formula
            descriptor = DESCRIPTOR


        if GRID == 0: # standard energy grid
            energy = numpy.arange(0,500)
            elefactor = numpy.log10(10000.0 / 30.0) / 300.0
            energy = 10.0 * 10**(energy * elefactor)
        elif GRID == 1: # user energy grid
            if GRIDN == 1:
                energy = numpy.array([GRIDSTART])
            else:
                energy = numpy.linspace(GRIDSTART,GRIDEND,GRIDN)
        elif GRID == 2: # single energy point
            energy = numpy.array([GRIDSTART])

        if THETAGRID == 0:
            theta = numpy.array([THETA1])
        else:
            theta = numpy.linspace(THETA1,THETA2,THETAN)


        CALCULATE_items=['f1', 'f2', 'delta', 'beta', 'mu [cm^-1]', 'mu [cm^2/g]', 'Cross Section[barn]', 'reflectivity-s', 'reflectivity-p', 'reflectivity-unpol', 'delta/beta ']

        out = numpy.zeros((energy.size,theta.size))
        for i,itheta in enumerate(theta):
            if MAT_FLAG == 0: # element
                tmp = f1f2_calc(descriptor,energy,1e-3*itheta,F=1+CALCULATE,rough=ROUGH,density=density)
                out[:,i] = tmp
            else:
                tmp = f1f2_calc_mix(descriptor,energy,1e-3*itheta,F=1+CALCULATE,rough=ROUGH,density=density)
                out[:,i] = tmp

        if ((energy.size == 1) and (theta.size == 1)):
            info = "** Single value calculation E=%g eV, theta=%g mrad, Result(F=%d)=%g "%(energy[0],theta[0],1+CALCULATE,out[0,0])
            out_dict = {"application":"xoppy","name":"xf12","info":info}
        elif theta.size == 1:
            tmp = numpy.vstack((energy,out[:,0]))
            labels = ["Energy [eV]",CALCULATE_items[CALCULATE]]
            out_dict = {"application":"xoppy","name":"xf12","data":tmp,"labels":labels}
        elif energy.size == 1:
            tmp = numpy.vstack((theta,out[0,:]))
            labels = ["Theta [mrad]",CALCULATE_items[CALCULATE]]
            out_dict = {"application":"xoppy","name":"xf12","data":tmp,"labels":labels}
        else:
            labels = [r"energy[eV]",r"theta [mrad]"]
            out_dict = {"application":"xoppy","name":"xf12","data2D":out,"dataX":energy,"dataY":theta,"labels":labels}

        #
        #
        #
        if "info" in out_dict.keys():
            print(out_dict["info"])

        #send exchange
        tmp = DataExchangeObject("xoppy_calc_xf12","xf12")

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
        try:
            tmp.add_content("data2D",out_dict["data2D"])
            tmp.add_content("dataX",out_dict["dataX"])
            tmp.add_content("dataY",out_dict["dataY"])
        except:
            pass

        self.send("ExchangeData",tmp)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('xf1f2')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxf1f2()
    w.show()
    app.exec()
    w.saveSettings()

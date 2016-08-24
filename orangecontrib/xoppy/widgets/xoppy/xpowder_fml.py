import sys,os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject


class OWxpowder_fml(widget.OWWidget):
    name = "xpowder_fml"
    id = "orange.widgets.dataxpowder_fml"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xpowder_fml.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 9
    category = ""
    keywords = ["xoppy", "xpowder_fml"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    FILE = Setting("/scisoft/xop2.4/examples/icsd_31142_sepiolite_BraunerPreisinger.cif")
    TITLE = Setting("powder pattern using crysFML")
    LAMBDA = Setting(1.54056)
    JOB = Setting(0)
    U = Setting(0.0002)
    V = Setting(-0.0002)
    W = Setting(0.012)
    X = Setting(0.0019)
    LS = Setting(1900.0)
    THMIN = Setting(1.0)
    STEP = Setting(0.05)
    THMAX = Setting(135.0)


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
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LAMBDA",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "JOB",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['X rays', 'Neutrons'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "U",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "V",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "W",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "X",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "LS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "STEP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['CIF File [? for Browser]: ','Title:','Lambda [A]: ','Radiation:','U: ','V: ','W: ','X: ','Ls:','TwoTheta from [deg]','TwoTheta step: ','TwoTheta to','None']


    def unitFlags(self):
         return ['1','1','1','1','1','1','1','1','1','1','1','1','1']


    #def unitNames(self):
    #     return ['FILE','TITLE','LAMBDA','JOB','U','V','W','X','LS','THMIN','STEP','THMAX','NONE']


    def compute(self):



        with open("xoppy.inp", "wt") as f:
            f.write("%s\n"% (self.FILE))
            f.write("%s\n"%(self.TITLE))
            f.write("%g\n"%(self.LAMBDA))
            f.write("%s\n"%(self.JOB))
            f.write("%g\n"%(self.U))
            f.write("%g\n"%(self.V))
            f.write("%g\n"%(self.W))
            f.write("%g\n"%(self.X))
            f.write("%g\n"%(self.LS))
            f.write("%g\n"%(self.THMIN))
            f.write("%g\n"%(self.STEP))
            f.write("%s\n"%(self.THMAX))



        command = os.path.join(locations.home_bin(), 'xpowder_fml') + " < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")


        print("Files written to disk: xpowder_fml.par (text output), xpowder_fml.ref (reflections), xpowder_fml.out (diffractogram)",)

        data = numpy.loadtxt("xpowder_fml.out",skiprows=3).T

        print(">>>>>>>>>>>",data.shape)


        #send exchange
        tmp = DataExchangeObject("xoppy_xpowder_fml","xpowder_fml")

        try:
            tmp.add_content("data",numpy.loadtxt("xpowder_fml.out",skiprows=3).T)
            tmp.add_content("plot_x_col",0)
            tmp.add_content("plot_y_col",-1)
        except:
            pass
        try:
            tmp.add_content("labels",["TwoTheta[Deg]","Intensity[a.u.]"])
        except:
            pass
        try:
            with open("xpowder_fml.par") as f:
                info = f.readlines()
            info = [line[:-1] for line in info]  # remove "\n"
            tmp.add_content("info",info)
        except:
            pass
        print(info)
        self.send("ExchangeData",tmp)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('xpowder_fml')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxpowder_fml()
    w.show()
    app.exec()
    w.saveSettings()

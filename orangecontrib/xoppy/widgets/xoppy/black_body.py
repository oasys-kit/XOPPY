import sys
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util import xoppy_util
from oasys.widgets.exchange import DataExchangeObject

class OWblack_body(widget.OWWidget):
    name = "black_body"
    id = "orange.widgets.datablack_body"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_black_body.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "black_body"]
    outputs = [{"name": "ExchangeData",
                "type": DataExchangeObject,
                "doc": "send ExchangeData"}]

    #inputs = [{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}]

    want_main_area = False

    TITLE = Setting("Thermal source: Planck distribution")
    TEMPERATURE = Setting(1200000.0)
    E_MIN = Setting(10.0)
    E_MAX = Setting(1000.0)
    NPOINTS = Setting(500)


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
        gui.lineEdit(box1, self, "TITLE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEMPERATURE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_MIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "E_MAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Title','Temperature [K]','Min energy [eV]','Max energy [eV]','Number of points ']


    def unitFlags(self):
         return ['True','True','True','True','True']


    #def unitNames(self):
    #     return ['TITLE','TEMPERATURE','E_MIN','E_MAX','NPOINTS']


    def compute(self):
        out_dict = self.xoppy_calc_black_body()

        if "info" in out_dict.keys():
            print(out_dict["info"])

        #send exchange
        tmp = DataExchangeObject("black_body","black_body")
        tmp.add_content("data",out_dict["data"])
        tmp.add_content("labels",out_dict["labels"])
        tmp.add_content("info",out_dict["info"])
        tmp.add_content("plot_x_col",0)
        tmp.add_content("plot_y_col",-1)
        self.send("ExchangeData",tmp)


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_util.xoppy_doc('black_body')



    def xoppy_calc_black_body(self):

        TITLE = self.TITLE
        TEMPERATURE = self.TEMPERATURE
        E_MIN = self.E_MIN
        E_MAX = self.E_MAX
        NPOINTS = self.NPOINTS
        try:

            import scipy.constants as codata

            #
            # text info
            #
            kb = codata.Boltzmann / codata.e # eV/K
            txt = ' \n'
            txt += 'Results of Black Body Radiation: Planck distribution\n'
            txt += 'TITLE: %s'%TITLE
            txt += ' \n'
            txt += '-------------------------------------------------------------\n'
            txt += 'Temperature           = %g K\n'%(TEMPERATURE)
            txt += 'Minimum photon energy = %g eV\n'%(E_MIN)
            txt += 'Maximum photon energy = %g eV\n'%(E_MAX)
            txt += '-------------------------------------------------------------\n'
            txt += 'Kb*T                = %g eV\n'%(TEMPERATURE*kb)
            txt += 'Peak at 2.822*Kb*T  = %g eV\n'%(2.822*TEMPERATURE*kb)
            txt += '-------------------------------------------------------------\n'

            # print(txt)

            #
            # calculation data
            #
            e_ev = numpy.linspace(E_MIN,E_MAX,NPOINTS)
            e_kt = e_ev/(TEMPERATURE*kb)
            brightness=3.146e11*(TEMPERATURE*kb)**3*e_kt**3/(numpy.exp(e_kt)-1)
            a3 = numpy.zeros((4,NPOINTS))
            a3[0,:] = e_ev
            a3[1,:] = e_kt
            a3[2,:] = brightness
            a3[3,:] = brightness*1e3*codata.e

            labels = ["Photon energy [eV]","Photon energy/(Kb*T)","Brightness [Photons/sec/mm2/mrad2/0.1%bw]","Spectral Power [Watts/eV/mrad2/mm2]"]

            return {"application":"xoppy","name":"black_body","data":a3,"labels":labels,"info":txt}


        except Exception as e:
            raise e

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWblack_body()
    w.show()
    app.exec()
    w.saveSettings()

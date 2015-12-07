import sys, os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication
from PyMca5.PyMcaIO import specfilewrapper as specfile
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.xoppy.util.xoppy_util import locations

try:
    from orangecontrib.xoppy.util.xoppy_util import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise

class OWxinpro(widget.OWWidget):
    name = "xinpro"
    id = "orange.widgets.dataxinpro"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xinpro.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 7
    category = ""
    keywords = ["xoppy", "xinpro"]
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

    CRYSTAL_MATERIAL = Setting(0)
    MODE = Setting(0)
    ENERGY = Setting(8000.0)
    MILLER_INDEX_H = Setting(1)
    MILLER_INDEX_K = Setting(1)
    MILLER_INDEX_L = Setting(1)
    ASYMMETRY_ANGLE = Setting(0.0)
    THICKNESS = Setting(500.0)
    TEMPERATURE = Setting(300.0)
    NPOINTS = Setting(100)
    SCALE = Setting(0)
    XFROM = Setting(-50.0)
    XTO = Setting(50.0)


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
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Silicon', 'Germanium', 'Diamond', 'GaAs', 'GaP', 'InAs', 'InP', 'InSb', 'SiC', 'CsF', 'KCl', 'LiF', 'NaCl', 'Graphite', 'Beryllium'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MODE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Reflectivity in Bragg case', 'Transmission in Bragg case', 'Reflectivity in Laue case', 'Transmission in Laue case'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_INDEX_H",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_INDEX_K",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MILLER_INDEX_L",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ASYMMETRY_ANGLE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "THICKNESS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TEMPERATURE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPOINTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int, validator=QIntValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCALE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Automatic', 'External'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XFROM",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XTO",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float, validator=QDoubleValidator())
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Crystal material: ','Calculation mode:','Energy [eV]:','Miller index H:','Miller index K:','Miller index L:','Asymmetry angle:','Crystal thickness [microns]:','Crystal temperature [K]:','Number of points: ','Angular limits: ','Theta min [arcsec]:','Theta max [arcsec]:']


    def unitFlags(self):
         return ['True','True','True','True','True','True','True','True','True','True','True','self.SCALE  ==  1','self.SCALE  ==  1']


    #def unitNames(self):
    #     return ['CRYSTAL_MATERIAL','MODE','ENERGY','MILLER_INDEX_H','MILLER_INDEX_K','MILLER_INDEX_L','ASYMMETRY_ANGLE','THICKNESS','TEMPERATURE','NPOINTS','SCALE','XFROM','XTO']


    def compute(self):
        fileName = xoppy_calc_xinpro(CRYSTAL_MATERIAL=self.CRYSTAL_MATERIAL,MODE=self.MODE,ENERGY=self.ENERGY,MILLER_INDEX_H=self.MILLER_INDEX_H,MILLER_INDEX_K=self.MILLER_INDEX_K,MILLER_INDEX_L=self.MILLER_INDEX_L,ASYMMETRY_ANGLE=self.ASYMMETRY_ANGLE,THICKNESS=self.THICKNESS,TEMPERATURE=self.TEMPERATURE,NPOINTS=self.NPOINTS,SCALE=self.SCALE,XFROM=self.XFROM,XTO=self.XTO)
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
        xoppy_doc('xinpro')

def xoppy_calc_xinpro(CRYSTAL_MATERIAL=0,MODE=0,ENERGY=8000.0,MILLER_INDEX_H=1,MILLER_INDEX_K=1,MILLER_INDEX_L=1,\
                      ASYMMETRY_ANGLE=0.0,THICKNESS=500.0,TEMPERATURE=300.0,NPOINTS=100,SCALE=0,XFROM=-50.0,XTO=50.0):
    print("Inside xoppy_calc_xinpro. ")

    try:
        with open("xoppy.inp", "wt") as f:
            f.write("%s\n"% (os.path.join(locations.home_data(), "inpro" + os.sep)))
            if MODE == 0:
                f.write("+1\n")
            elif MODE == 1:
                f.write("-1\n")
            elif MODE == 2:
                f.write("+2\n")
            elif MODE == 3:
                f.write("-1\n")
            else:
                f.write("ERROR!!\n")

            f.write("%f\n%d\n"%(THICKNESS,CRYSTAL_MATERIAL+1))
            f.write("%s\n%f\n"%("EV",ENERGY))
            f.write("%d\n%d\n%d\n"%(MILLER_INDEX_H,MILLER_INDEX_K,MILLER_INDEX_L))
            f.write("%f\n%f\n%s\n"%(ASYMMETRY_ANGLE,TEMPERATURE, "inpro.dat"))
            if SCALE == 0:
                f.write("1\n")
            else:
                f.write("%d\n%f\n%f\n"%(2,XFROM,XTO))
            f.write("%d\n"%(NPOINTS))

        command = os.path.join(locations.home_bin(), 'inpro') + " < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command, locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")

        #add SPEC header
        txt = open("inpro.dat").read()
        outFile = "inpro.spec"

        f = open(outFile,"w")
        f.write("#F inpro.spec\n")
        f.write("\n")
        f.write("#S 1 inpro results\n")
        f.write("#N 3\n")
        f.write("#L Theta-TetaB  s-polarized reflectivity  p-polarized reflectivity\n")
        f.write(txt)
        f.close()
        print("File written to disk: inpro.dat, inpro.par, inpro.spec")

        return outFile
    except Exception as e:
        raise e




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxinpro()
    w.show()
    app.exec()
    w.saveSettings()

import sys, os
import numpy
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
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

class OWxxcom(widget.OWWidget):
    name = "xxcom"
    id = "orange.widgets.dataxxcom"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_xxcom.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 3
    category = ""
    keywords = ["xoppy", "xxcom"]
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

    NAME = Setting("Pyrex Glass")
    SUBSTANCE = Setting(3)
    DESCRIPTION = Setting("SiO2:B2O3:Na2O:Al2O3:K2O")
    FRACTION = Setting("0.807:0.129:0.038:0.022:0.004")
    GRID = Setting(1)
    GRIDINPUT = Setting(0)
    GRIDDATA = Setting("0.0804:0.2790:0.6616:1.3685:2.7541")
    ELEMENTOUTPUT = Setting(0)


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
        gui.lineEdit(box1, self, "NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SUBSTANCE",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Element (Atomic number)', 'Element (Symbol)', 'Compound (Formula)', 'Mixture (F1:F2:F3...)'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTION",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FRACTION",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Standard', 'Standard+points', 'Points only'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRIDINPUT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['From Keyboard', 'From file'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDDATA",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ELEMENTOUTPUT",
                     label=self.unitLabels()[idx], addSpace=True,
                    items=['Cross section [b/atom]', 'Cross section [b/atom] & Attenuation coeff [cm2/g]', 'Partial interaction coeff & Attenuation coeff [cm2/g]'],
                    valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ['Name','Substance:','Description:','fraction','grid','grid points','grid points [MeV]/file name','Output quantity']


    def unitFlags(self):
         return ['True','True','True','self.SUBSTANCE  ==  3','True','self.GRID  !=  0','(self.GRID  !=  0)','self.SUBSTANCE  <=  1']


    #def unitNames(self):
    #     return ['NAME','SUBSTANCE','DESCRIPTION','FRACTION','GRID','GRIDINPUT','GRIDDATA','ELEMENTOUTPUT']


    def compute(self):
        fileName = xoppy_calc_xxcom(NAME=self.NAME,SUBSTANCE=self.SUBSTANCE,DESCRIPTION=self.DESCRIPTION,FRACTION=self.FRACTION,GRID=self.GRID,GRIDINPUT=self.GRIDINPUT,GRIDDATA=self.GRIDDATA,ELEMENTOUTPUT=self.ELEMENTOUTPUT)
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
        xoppy_doc('xxcom')



def xoppy_calc_xxcom(NAME="Pyrex Glass",SUBSTANCE=3,DESCRIPTION="SiO2:B2O3:Na2O:Al2O3:K2O",\
                     FRACTION="0.807:0.129:0.038:0.022:0.004",GRID=1,GRIDINPUT=0,\
                     GRIDDATA="0.0804:0.2790:0.6616:1.3685:2.7541",ELEMENTOUTPUT=0):
    print("Inside xoppy_calc_xxcom. ")

    try:
        with open("xoppy.inp","wt") as f:
            f.write(os.path.join(locations.home_data(), 'xcom')+ os.sep + "\n" )
            f.write( NAME+"\n" )
            f.write("%d\n"%(1+SUBSTANCE))
            if (1+SUBSTANCE) != 4:
                f.write( DESCRIPTION+"\n")
                if (1+SUBSTANCE) <= 2:
                    f.write("%d\n"%(1+ELEMENTOUTPUT))
            else:
                nn = DESCRIPTION.split(":")
                mm = FRACTION.split(":")
                f.write("%d\n"%( len(nn)))
                print(">>>>>>>",nn,len(nn))
                for i in range(len(nn)):
                    print("<><><><>",i,nn[i],mm[i])
                    f.write(nn[i]+"\n")
                    f.write(mm[i]+"\n")
                f.write("1\n")
            f.write("%d\n"%(1+GRID))
            if (1+GRID) != 1:
                f.write("%d\n"%(1+GRIDINPUT))
                if (1+GRIDINPUT) == 1:
                    nn = GRIDDATA.split(":")
                    f.write("%d\n"%( len(nn)))
                    for i in nn:
                        f.write(i+"\n")
                    if (1+GRID) != 1:
                        f.write("N\n")
            f.write("xcom.out\n")
            f.write("1\n")
            f.close()

        command = os.path.join(locations.home_bin(),'xcom') + " < xoppy.inp"
        print("Running command '%s' in directory: %s "%(command,locations.home_bin_run()))
        print("\n--------------------------------------------------------\n")
        os.system(command)
        print("\n--------------------------------------------------------\n")
        # write spec file

        if (1+SUBSTANCE) <= 2:
            if (1+ELEMENTOUTPUT) == 1:
                titles = "Photon Energy [Mev]  Coherent scat [b/atom]  " \
                         "Incoherent scat [b/atom]  Photoel abs [b/atom]  " \
                         "Pair prod in nucl field [b/atom]  Pair prod in elec field [b/atom]  " \
                         "Tot atten with coh scat [b/atom]  Tot atten w/o coh scat [b/atom]"
            elif (1+ELEMENTOUTPUT) == 2:
                titles = "Photon Energy [Mev]  Coherent scat [b/atom]  " \
                         "Incoherent scat [b/atom]  Photoel abs [b/atom]  " \
                         "Pair prod in nucl field [b/atom]  Pair prod in elec field [b/atom]  " \
                         "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"
            elif (1+ELEMENTOUTPUT) == 3:
                titles = "Photon Energy [Mev]  Coherent scat [cm2/g]  " \
                         "Incoherent scat [cm2/g]  Photoel abs [cm2/g]  " \
                         "Pair prod in nucl field [cm2/g]  Pair prod in elec field [cm2/g]  " \
                         "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"
            else:
                titles = "Photon Energy [Mev]  Coherent scat [cm2/g]  " \
                         "Incoherent scat [cm2/g]  Photoel abs [cm2/g]  " \
                         "Pair prod in nucl field [cm2/g]  Pair prod in elec field [cm2/g]  " \
                         "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"
        else:
           titles = "Photon Energy [Mev]  Coherent scat [cm2/g]  " \
                    "Incoherent scat [cm2/g]  Photoel abs [cm2/g]  " \
                    "Pair prod in nucl field [cm2/g]  Pair prod in elec field [cm2/g]  " \
                    "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"


        txt = open("xcom.out").readlines()
        outFile = "xcom.spec"

        f = open(outFile, "w")

        f.write("#F xcom.spec\n")
        f.write("\n")
        f.write("#S 1 xcom results\n")
        f.write("#N 8\n")
        f.write("#L  "+titles+"\n")
        for i in txt:
            tmp = i.strip(" ")
            if tmp[0].isdigit():
               f.write(tmp)
            else:
               f.write("#UD "+tmp)
        f.close()
        print("File written to disk: xcom.spec")

        return outFile
    except Exception as e:
        raise e


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxxcom()
    w.show()
    app.exec()
    w.saveSettings()

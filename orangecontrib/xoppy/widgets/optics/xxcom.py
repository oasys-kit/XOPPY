import sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

class OWxxcom(XoppyWidget):
    name = "XCOM"
    id = "orange.widgets.dataxxcom"
    description = "X-ray Matter Cross Sections"
    icon = "icons/xoppy_xxcom.png"
    priority = 21
    category = ""
    keywords = ["xoppy", "xxcom"]

    NAME = Setting("Pyrex Glass")
    SUBSTANCE = Setting(3)
    DESCRIPTION = Setting("SiO2:B2O3:Na2O:Al2O3:K2O")
    FRACTION = Setting("0.807:0.129:0.038:0.022:0.004")
    GRID = Setting(1)
    GRIDINPUT = Setting(0)
    GRIDDATA = Setting("0.0804:0.2790:0.6616:1.3685:2.7541")
    ELEMENTOUTPUT = Setting(0)


    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NAME",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=80)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SUBSTANCE",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Element (Atomic number)', 'Element (Symbol)', 'Compound (Formula)', 'Mixture (F1:F2:F3...)'],
                    valueType=int, orientation="horizontal", callback=self.set_SUBSTANCE)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "DESCRIPTION",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=80)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "FRACTION",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=80)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRID",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Standard', 'Standard+points', 'Points only'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GRIDINPUT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['From Keyboard', 'From file'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "GRIDDATA",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ELEMENTOUTPUT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Cross section [b/atom]', 'Cross section [b/atom] & Attenuation coeff [cm2/g]', 'Partial interaction coeff & Attenuation coeff [cm2/g]'],
                    valueType=int, orientation="horizontal", callback=self.set_ELEMENTOUTPUT)
        self.show_at(self.unitFlags()[idx], box1) 

        gui.rubber(self.controlArea)

    def set_SUBSTANCE(self):
        self.initializeTabs()

    def set_ELEMENTOUTPUT(self):
        self.initializeTabs()

    def unitLabels(self):
         return ['Name','Substance:','Description:','fraction','grid','grid points','grid points [MeV]/file name','Output quantity']

    def unitFlags(self):
         return ['True','True','True','self.SUBSTANCE  ==  3','True','self.GRID  !=  0','(self.GRID  !=  0)','self.SUBSTANCE  <=  1']
    
    def get_help_name(self):
        return 'xcom'

    def check_fields(self):
        self.DESCRIPTION = congruence.checkEmptyString(self.DESCRIPTION, "Description")

        if self.SUBSTANCE == 3:
            self.FRACTION = congruence.checkEmptyString(self.FRACTION, "fraction")

        if self.GRID != 0:
            if self.GRIDINPUT == 0:
                self.GRIDDATA = congruence.checkEmptyString(self.GRIDDATA, "grid points")
            else:
                congruence.checkFile(self.GRIDDATA)

    def do_xoppy_calculation(self):
        return xoppy_calc_xxcom(NAME=self.NAME,SUBSTANCE=self.SUBSTANCE,DESCRIPTION=self.DESCRIPTION,FRACTION=self.FRACTION,GRID=self.GRID,GRIDINPUT=self.GRIDINPUT,GRIDDATA=self.GRIDDATA,ELEMENTOUTPUT=self.ELEMENTOUTPUT)

    def get_data_exchange_widget_name(self):
        return "XXCOM"

    def getTitles(self):
        return ["Coherent scat",
                "Incoherent scat",
                "Photoel abs",
                "Pair prod in nucl field]",
                "Pair prod in elec field]",
                "Tot atten with coh scat]",
                "Tot atten w/o coh scat"]

    def getXTitles(self):
        return ["Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]",
                "Photon Energy [Mev]"]

    def getYTitles(self):
        if (1+self.SUBSTANCE) <= 2:
            if (1+self.ELEMENTOUTPUT) == 1:
                return ["Coherent scat [b/atom]",
                        "Incoherent scat [b/atom]",
                        "Photoel abs [b/atom]",
                        "Pair prod in nucl field [b/atom]",
                        "Pair prod in elec field [b/atom]",
                        "Tot atten with coh scat [b/atom]",
                        "Tot atten w/o coh scat [b/atom]"]
            elif (1+self.ELEMENTOUTPUT) == 2:
                return ["Coherent scat [b/atom]",
                        "Incoherent scat [b/atom]",
                        "Photoel abs [b/atom]",
                        "Pair prod in nucl field [b/atom]",
                        "Pair prod in elec field [b/atom]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]
            elif (1+self.ELEMENTOUTPUT) == 3:
                return ["Coherent scat [cm2/g]",
                        "Incoherent scat [cm2/g]",
                        "Photoel abs [cm2/g]",
                        "Pair prod in nucl field [cm2/g]",
                        "Pair prod in elec field [cm2/g]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]
            else:
                return ["Coherent scat [cm2/g]",
                        "Incoherent scat [cm2/g]",
                        "Photoel abs [cm2/g]",
                        "Pair prod in nucl field [cm2/g]",
                        "Pair prod in elec field [cm2/g]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]
        else:
                return ["Coherent scat [cm2/g]",
                        "Incoherent scat [cm2/g]",
                        "Photoel abs [cm2/g]",
                        "Pair prod in nucl field [cm2/g]",
                        "Pair prod in elec field [cm2/g]",
                        "Tot atten with coh scat [cm2/g]",
                        "Tot atten w/o coh scat [cm2/g]"]

    def getVariablesToPlot(self):
        return [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]

    def getLogPlot(self):
        return [(False, False), (False, False), (False, False), (False, False), (False, False), (False, False), (False, False)]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

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
                for i in range(len(nn)):
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

        command = "'" + os.path.join(locations.home_bin(),'xcom') + "' < xoppy.inp"
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

        # copy to standard output
        for line in txt:
            print(line,end="")

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

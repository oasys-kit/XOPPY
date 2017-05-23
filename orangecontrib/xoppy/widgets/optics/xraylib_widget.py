import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QTextEdit, QMessageBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QTextCursor

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget
from oasys.widgets import gui as oasysgui

import xraylib

from orangecontrib.xoppy.util import xoppy_util

class OWxraylib_widget(widget.OWWidget):
    name = "Xraylib"
    id = "orange.widgets.dataxraylib_widget"
    description = "XRAYLIB data"
    icon = "icons/xraylib.png"
    author = "Manuel Sanchez del Rio, Luca Rebuffi "
    maintainer_email = "srio@esrf.eu"
    priority = 25
    category = ""
    keywords = ["xoppy", "xraylib_widget"]

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

    MAX_WIDTH = 700
    MAX_HEIGHT = 700
    CONTROL_AREA_WIDTH = 690

    def __init__(self):
        super().__init__()

        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())

        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        box0 = gui.widgetBox(self.controlArea, "", orientation="horizontal")
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Defaults", callback=self.defaults)
        gui.button(box0, self, "Help", callback=self.help1)

        gui.separator(self.controlArea, height=10)

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters",orientation="vertical", width=self.CONTROL_AREA_WIDTH-5, height=150)

        self.xoppy_output = QTextEdit()
        self.xoppy_output.setReadOnly(True)
        self.xoppy_output.setFixedHeight(440)
        self.xoppy_output.setFixedWidth(self.CONTROL_AREA_WIDTH-25)

        out_box = gui.widgetBox(self.controlArea, "Calculation Output", addSpace=True, orientation="horizontal")
        out_box.layout().addWidget(self.xoppy_output)

        idx = -1
        
        #widget index 0 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "FUNCTION",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['0 Fluorescence line energy', '1 Absorption edge energy', '2 Atomic weight', '3 Elemental density', '4 Total absorption cross section', '5 Photoionization cross section', '6 Partial photoionization cross section', '7 Rayleigh scattering cross section', '8 Compton scattering cross section', '9 Klein-Nishina cross section', '10 Mass energy-absorption cross section', '11 Differential unpolarized Klein-Nishina cross section', '12 Differential unpolarized Thomson cross section', '13 Differential unpolarized Rayleigh cross section', '14 Differential unpolarized Compton cross section', '15 Differential polarized Klein-Nishina cross section', '16 Differential polarized Thomson cross section', '17 Differential polarized Rayleigh cross section', '18 Differential polarized Compton cross section', '19 Atomic form factor', '20 Incoherent scattering function', '21 Momentum transfer function', '22 Coster-Kronig transition probability', '23 Fluorescence yield', '24 Jump factor', '25 Radiative transition probability', '26 Energy after Compton scattering', '27 Anomalous scattering factor &phi;&prime;', '28 Anomalous scattering factor &phi;&Prime;', '29 Electronic configuration', '30 X-ray fluorescence production cross section (with full cascade)', '31 X-ray fluorescence production cross section (with radiative cascade)', '32 X-ray fluorescence production cross section (with non-radiative cascade)', '33 X-ray fluorescence production cross section (without cascade)', '34 Atomic level width', '35 Auger yield', '36 Auger rate', '37 Refractive index', '38 Compton broadening profile', '39 Partial Compton broadening profile', '40 List of NIST catalog compounds', '41 Get composition of NIST catalog compound', '42 List of X-ray emitting radionuclides', '43 Get excitation profile of X-ray emitting radionuclide', '44 Compoundparser'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 1 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ELEMENT",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, validator=QIntValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ELEMENTORCOMPOUND",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "COMPOUND",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_IUPAC_OR_SIEGBAHN",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['IUPAC', 'SIEGBAHN', 'ALL TRANSITIONS'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_IUPAC_TO",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_IUPAC_FROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "TRANSITION_SIEGBAHN",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['KA1_LINE', 'KA2_LINE', 'KB1_LINE', 'KB2_LINE', 'KB3_LINE', 'KB4_LINE', 'KB5_LINE', 'LA1_LINE', 'LA2_LINE', 'LB1_LINE', 'LB2_LINE', 'LB3_LINE', 'LB4_LINE', 'LB5_LINE', 'LB6_LINE', 'LB7_LINE', 'LB9_LINE', 'LB10_LINE', 'LB15_LINE', 'LB17_LINE', 'LG1_LINE', 'LG2_LINE', 'LG3_LINE', 'LG4_LINE', 'LG5_LINE', 'LG6_LINE', 'LG8_LINE', 'LE_LINE', 'LL_LINE', 'LS_LINE', 'LT_LINE', 'LU_LINE', 'LV_LINE'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SHELL",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['All shells', 'K_SHELL', 'L1_SHELL', 'L2_SHELL', 'L3_SHELL', 'M1_SHELL', 'M2_SHELL', 'M3_SHELL', 'M4_SHELL', 'M5_SHELL', 'N1_SHELL', 'N2_SHELL', 'N3_SHELL', 'N4_SHELL', 'N5_SHELL', 'N6_SHELL', 'N7_SHELL', 'O1_SHELL', 'O2_SHELL', 'O3_SHELL', 'O4_SHELL', 'O5_SHELL', 'O6_SHELL', 'O7_SHELL', 'P1_SHELL', 'P2_SHELL', 'P3_SHELL', 'P4_SHELL', 'P5_SHELL', 'Q1_SHELL', 'Q2_SHELL', 'Q3_SHELL'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, validator=QDoubleValidator(), orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 


        self.process_showers()

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return ["Calculate", "Atomic number", "Element or compound name", "Compound name", "Transition notation", "Transition to (iupac)","Transition from (iupac)","Transition (Siegbahn)","Shell","Energy [keV]"]


    def unitFlags(self):
         return ["True", "self.FUNCTION <= 3 or self.FUNCTION == 6", "self.FUNCTION == 4 or self.FUNCTION == 5 or self.FUNCTION == 7 or self.FUNCTION == 8 or self.FUNCTION == 10", "self.FUNCTION > 100","self.FUNCTION == 0", "(self.FUNCTION == 0 and self.TRANSITION_IUPAC_OR_SIEGBAHN == 0)", "(self.FUNCTION == 0 and self.TRANSITION_IUPAC_OR_SIEGBAHN == 0)", "(self.FUNCTION == 0 and self.TRANSITION_IUPAC_OR_SIEGBAHN == 1)","self.FUNCTION == 1 or self.FUNCTION == 6","self.FUNCTION >= 4 "]


    def compute(self):
        self.setStatusMessage("Running XRAYLIB")

        try:
            sys.stdout = xoppy_util.EmittingStream(textWritten=self.writeStdOut)

            xoppy_calc_xraylib_widget(FUNCTION=self.FUNCTION,ELEMENT=self.ELEMENT,ELEMENTORCOMPOUND=self.ELEMENTORCOMPOUND,COMPOUND=self.COMPOUND,TRANSITION_IUPAC_OR_SIEGBAHN=self.TRANSITION_IUPAC_OR_SIEGBAHN,TRANSITION_IUPAC_TO=self.TRANSITION_IUPAC_TO,TRANSITION_IUPAC_FROM=self.TRANSITION_IUPAC_FROM,TRANSITION_SIEGBAHN=self.TRANSITION_SIEGBAHN,SHELL=self.SHELL,ENERGY=self.ENERGY)

            self.setStatusMessage("")

        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

            self.setStatusMessage("Error!")

            raise  exception

    def defaults(self):
         self.resetSettings()

    def help1(self):
        xoppy_util.xoppy_doc('xraylib_widget')

    def writeStdOut(self, text):
        cursor = self.xoppy_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.xoppy_output.setTextCursor(cursor)
        self.xoppy_output.ensureCursorVisible()

def xoppy_calc_xraylib_widget(FUNCTION=0,ELEMENT=26,ELEMENTORCOMPOUND="FeSO4",COMPOUND="Ca5(PO4)3",TRANSITION_IUPAC_OR_SIEGBAHN=1,\
                              TRANSITION_IUPAC_TO=0,TRANSITION_IUPAC_FROM=0,TRANSITION_SIEGBAHN=0,SHELL=0,ENERGY=10.0):

    functions=['0 Fluorescence line energy', '1 Absorption edge energy', '2 Atomic weight', '3 Elemental density', '4 Total absorption cross section', '5 Photoionization cross section', '6 Partial photoionization cross section', '7 Rayleigh scattering cross section', '8 Compton scattering cross section', '9 Klein-Nishina cross section', '10 Mass energy-absorption cross section', '11 Differential unpolarized Klein-Nishina cross section', '12 Differential unpolarized Thomson cross section', '13 Differential unpolarized Rayleigh cross section', '14 Differential unpolarized Compton cross section', '15 Differential polarized Klein-Nishina cross section', '16 Differential polarized Thomson cross section', '17 Differential polarized Rayleigh cross section', '18 Differential polarized Compton cross section', '19 Atomic form factor', '20 Incoherent scattering function', '21 Momentum transfer function', '22 Coster-Kronig transition probability', '23 Fluorescence yield', '24 Jump factor', '25 Radiative transition probability', '26 Energy after Compton scattering', '27 Anomalous scattering factor &phi;&prime;', '28 Anomalous scattering factor &phi;&Prime;', '29 Electronic configuration', '30 X-ray fluorescence production cross section (with full cascade)', '31 X-ray fluorescence production cross section (with radiative cascade)', '32 X-ray fluorescence production cross section (with non-radiative cascade)', '33 X-ray fluorescence production cross section (without cascade)', '34 Atomic level width', '35 Auger yield', '36 Auger rate', '37 Refractive index', '38 Compton broadening profile', '39 Partial Compton broadening profile', '40 List of NIST catalog compounds', '41 Get composition of NIST catalog compound', '42 List of X-ray emitting radionuclides', '43 Get excitation profile of X-ray emitting radionuclide', '44 Compoundparser']

    print("\nInside xoppy_calc_xraylib with FUNCTION = %s. "%(functions[FUNCTION]))

    if FUNCTION == 0:
        if TRANSITION_IUPAC_OR_SIEGBAHN == 0:
            lines = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
            line = lines[TRANSITION_IUPAC_TO]+lines[TRANSITION_IUPAC_FROM]+"_LINE"
            command = "result = xraylib.LineEnergy(%d,xraylib.%s)"%(ELEMENT,line)
            print("executing command: ",command)
            line = getattr(xraylib,line)
            result = xraylib.LineEnergy(ELEMENT,line)
            print("result: %f keV"%(result))
        if TRANSITION_IUPAC_OR_SIEGBAHN == 1:
            lines = ['KA1_LINE', 'KA2_LINE', 'KB1_LINE', 'KB2_LINE', 'KB3_LINE', 'KB4_LINE', 'KB5_LINE', 'LA1_LINE', 'LA2_LINE', 'LB1_LINE', 'LB2_LINE', 'LB3_LINE', 'LB4_LINE', 'LB5_LINE', 'LB6_LINE', 'LB7_LINE', 'LB9_LINE', 'LB10_LINE', 'LB15_LINE', 'LB17_LINE', 'LG1_LINE', 'LG2_LINE', 'LG3_LINE', 'LG4_LINE', 'LG5_LINE', 'LG6_LINE', 'LG8_LINE', 'LE_LINE', 'LL_LINE', 'LS_LINE', 'LT_LINE', 'LU_LINE', 'LV_LINE']
            line = lines[TRANSITION_SIEGBAHN]
            command = "result = xraylib.LineEnergy(%d,xraylib.%s)"%(ELEMENT,line)
            print("executing command: ",command)
            line = getattr(xraylib,line)
            result = xraylib.LineEnergy(ELEMENT,line)
            print("result: %f keV"%(result))
        if TRANSITION_IUPAC_OR_SIEGBAHN == 2:
            lines = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
            for i1,l1 in enumerate(lines):
                for i2,l2 in enumerate(lines):
                    if i1 != i2:
                        line = l1+l2+"_LINE"

                        try:
                            line = getattr(xraylib,line)
                            result = xraylib.LineEnergy(ELEMENT,line)
                        except:
                            pass
                        else:
                            if result != 0.0: print("%s%s  %f   keV"%(l1, l2, result))
    elif FUNCTION == 1:
        shells = ['All shells', 'K_SHELL', 'L1_SHELL', 'L2_SHELL', 'L3_SHELL', 'M1_SHELL', 'M2_SHELL', 'M3_SHELL', 'M4_SHELL', 'M5_SHELL', 'N1_SHELL', 'N2_SHELL', 'N3_SHELL', 'N4_SHELL', 'N5_SHELL', 'N6_SHELL', 'N7_SHELL', 'O1_SHELL', 'O2_SHELL', 'O3_SHELL', 'O4_SHELL', 'O5_SHELL', 'O6_SHELL', 'O7_SHELL', 'P1_SHELL', 'P2_SHELL', 'P3_SHELL', 'P4_SHELL', 'P5_SHELL', 'Q1_SHELL', 'Q2_SHELL', 'Q3_SHELL']
        if SHELL == 0: #"all"
            for i,myshell in enumerate(shells):
                if i >= 1:
                    # command = "result = xraylib.EdgeEnergy(%d,xraylib.%s)"%(ELEMENT,myshell)
                    # print("executing command: ",command)
                    shell_index = getattr(xraylib,myshell)
                    try:
                        result = xraylib.EdgeEnergy(ELEMENT,shell_index)
                    except:
                        pass
                    else:
                        if result != 0.0: print("%s  %f   keV"%(myshell, result))
                        else: print("No result")
        else:
            shell_index = getattr(xraylib,shells[SHELL])
            try:
                command = "result = xraylib.EdgeEnergy(%d,xraylib.%s)"%(ELEMENT,shells[SHELL])
                print("executing command: ",command)
                result = xraylib.EdgeEnergy(ELEMENT,shell_index)
            except:
                pass
            else:
                if result != 0.0: print("Z=%d %s : %f   keV"%(ELEMENT, shells[SHELL], result))
                else: print("No result")
    elif FUNCTION == 2:
        result = xraylib.AtomicWeight(ELEMENT)
        if result != 0.0: print("Atomic weight for Z=%d : %f  g/mol"%(ELEMENT,result))
    elif FUNCTION == 3:
        result = xraylib.ElementDensity(ELEMENT)
        if result != 0.0: print("Element density for Z=%d : %f  g/cm3"%(ELEMENT,result))
        else: print("No result")
    elif FUNCTION == 4:
        command = "result = xraylib.CS_Total_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Total_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Total absorption cross section: %f  g/cm3"%(result))
        else: print("No result")
    elif FUNCTION == 5:
        command = "result = xraylib.CS_Photo_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Photo_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Photoionization cross section: %f  g/cm3"%(result))
        else: print("No result")
    elif FUNCTION == 6:
        shells = ['All shells', 'K_SHELL', 'L1_SHELL', 'L2_SHELL', 'L3_SHELL', 'M1_SHELL', 'M2_SHELL', 'M3_SHELL', 'M4_SHELL', 'M5_SHELL', 'N1_SHELL', 'N2_SHELL', 'N3_SHELL', 'N4_SHELL', 'N5_SHELL', 'N6_SHELL', 'N7_SHELL', 'O1_SHELL', 'O2_SHELL', 'O3_SHELL', 'O4_SHELL', 'O5_SHELL', 'O6_SHELL', 'O7_SHELL', 'P1_SHELL', 'P2_SHELL', 'P3_SHELL', 'P4_SHELL', 'P5_SHELL', 'Q1_SHELL', 'Q2_SHELL', 'Q3_SHELL']
        if SHELL == 0: #"all"
            for index in range(1, len(shells)):
                shell_index = getattr(xraylib, shells[index])
                try:
                    command = "result = xraylib.xraylib.CS_Photo_Partial('%d',xraylib.%s,%f)"%(ELEMENT, shells[index],ENERGY)
                    print("executing command: ", command)
                    result = xraylib.CS_Photo_Partial(ELEMENT, shell_index, ENERGY)
                except:
                    pass
                else:
                    if result != 0.0: print("Z=%d, %s at E=%f keV: %f   cm2/g"%(ELEMENT,shells[index], ENERGY, result))
                    else: print("No result")
        else:
            shell_index = getattr(xraylib, shells[SHELL])
            try:
                command = "result = xraylib.xraylib.CS_Photo_Partial('%d',xraylib.%s,%f)"%(ELEMENT,shells[SHELL],ENERGY)
                print("executing command: ",command)
                result = xraylib.CS_Photo_Partial(ELEMENT, shell_index, ENERGY)
            except:
                pass
            else:
                if result != 0.0: print("Z=%d, %s at E=%f keV: %f   cm2/g"%(ELEMENT,shells[SHELL], ENERGY, result))
                else: print("No result")
    elif FUNCTION == 7:
        command = "result = xraylib.CS_Rayl_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Rayl_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Rayleigh cross section: %f  cm2/g"%(result))
        else: print("No result")
    elif FUNCTION == 8:
        command = "result = xraylib.CS_Compt_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Compt_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Compton cross section: %f  cm2/g"%(result))
        else: print("No result")
    elif FUNCTION == 9:
        command = "result = xraylib.CS_KN(%f)"%(ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_KN(ENERGY)
        if result != 0.0: print("Klein Nishina cross section: %f  cm2/g"%(result))
        else: print("No result")
    elif FUNCTION == 10:
        command = "result = xraylib.CS_Energy_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Energy_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Mass-energy absorption cross section: %f  cm2/g"%(result))
        else: print("No result")
    else:
        print("\n#### NOT YET IMPLEMENTED ####")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWxraylib_widget()
    w.show()
    app.exec()
    w.saveSettings()

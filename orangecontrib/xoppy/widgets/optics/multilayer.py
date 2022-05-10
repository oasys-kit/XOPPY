import numpy
from PyQt5.QtWidgets import QMessageBox

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.mlayer import MLayer
from xoppylib.xoppy_xraylib_util import density
from xoppylib.xoppy_xraylib_util import Refractive_Index_Re_Extended_NIST, Refractive_Index_Im_Extended_NIST

class OWMlultilayer(XoppyWidget):
    name = "Multilayer"
    id = "orange.widgets.datamlayer"
    description = "Multilayer Reflectivity"
    icon = "icons/xoppy_mlayer.png"
    priority = 11
    category = ""
    keywords = ["xoppy", "multilayer"]


    MATERIAL_S = Setting("Si")
    DENSITY_S = Setting("?")
    ROUGHNESS_S = Setting(0.0)


    MATERIAL_E = Setting("W")
    DENSITY_E = Setting("?")
    ROUGHNESS_E = Setting(0.0)

    MATERIAL_O = Setting("Si")
    DENSITY_O = Setting("?")
    ROUGHNESS_O = Setting(0.0)

    THICKNESS = Setting(50.0)
    GAMMA = Setting(0.5)
    NLAYERS = Setting(50)

    THETA_FLAG = Setting(1)
    THETA_N = Setting(600)
    THETA = Setting(0.0)
    THETA_END = Setting(6.0)

    ENERGY_FLAG = Setting(0)
    ENERGY_N = Setting(100)
    ENERGY = Setting(8050.)
    ENERGY_END = Setting(15000.0)

    DUMP_TO_FILE = Setting(0)
    FILE_NAME = Setting("multilayer.h5")

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box0 = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 

        #
        #
        #
        box = gui.widgetBox(box0, "Substrate", orientation="vertical")

        #widget index 0
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MATERIAL_S",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        #widget index 1
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DENSITY_S",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 2
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ROUGHNESS_S",
                    valueType=float,
                    label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #
        box = gui.widgetBox(box0, "Even layer (closer to substrate)", orientation="vertical")

        #widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "MATERIAL_E",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DENSITY_E",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ROUGHNESS_E",
                    valueType=float,
                    label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #
        box = gui.widgetBox(box0, "Odd layer (close to vacuum)", orientation="vertical")
        #widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "MATERIAL_O",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "DENSITY_O",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ROUGHNESS_O",
                    valueType=float,
                    label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #
        box = gui.widgetBox(box0, "Bilayers", orientation="vertical")
        #widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THICKNESS",
                    valueType=float,
                    label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "GAMMA",
                    valueType=float,
                    label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "NLAYERS",
                    valueType=int,
                    label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #
        box = gui.widgetBox(box0, "scan - angle", orientation="vertical")
        #widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "THETA_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Single Value', 'Scan'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETA",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETA_END",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THETA_N",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #
        #
        #
        box = gui.widgetBox(box0, "scan - energy", orientation="vertical")
        #widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "ENERGY_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Single Value', 'Scan'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 17
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENERGY",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        # widget index 18
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENERGY_END",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 19
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENERGY_N",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #
        #
        #
        box = gui.widgetBox(box0, "output", orientation="vertical")

        # widget index 20
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "DUMP_TO_FILE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["No", "Yes"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 21
        idx += 1
        box1 = gui.widgetBox(box,orientation="horizontal")
        gui.lineEdit(box1, self, "FILE_NAME",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)


        gui.button(box1, self, "...", callback=self.selectFile)

        gui.rubber(self.controlArea)

    def unitLabels(self):
         return [
                'material: ',
                'density [g/cm3]:',
                'roughness [A]',
                'material: ',
                'density [g/cm3]:',
                'roughness [A]',
                'material: ',
                'density [g/cm3]:',
                'roughness [A]',
                'Bilayer thickness [A]',
                'Bilayer gamma [t_even/(t_even+t_odd)]',
                'Number of bilayers:',
                'Grazing angle [deg]',
                'Start Graz angle [deg]',
                'End Graz angle [deg]',
                'Number of angular points',
                'Photon energy',
                'Start Energy [eV]: ',
                'End Energy [eV]: ',
                'Number of energy points',
                'Dump to file',
                'File name',
                 ]



    def unitFlags(self):
         return [
                "True",                   #  'material: ',
                "True",                   #  'density [g/cm3]:',
                "True",                   #  'roughness [A]',
                "True",                   #  'material: ',
                "True",                   #  'density [g/cm3]:',
                "True",                   #  'roughness [A]',
                "True",                   #  'material: ',
                "True",                   #  'density [g/cm3]:',
                "True",                   #  'roughness [A]',
                "True",                   #  'Bilayer thickness [A]',
                "True",                   #  'Bilayer gamma [t_even/(t_even+t_odd)]',,
                "True",                   #  'Number of bilayers:',
                "True",                   #  'Grazing angle [deg]',
                "True",                   #  'Start Graz angle [deg]',
                "self.THETA_FLAG == 1",   #  'End Graz angle [deg]',
                "self.THETA_FLAG == 1",   #  'Number of angular points',
                "True",                   #  'Photon energy',
                "True",                   #  'Start Energy [eV]: ',
                "self.ENERGY_FLAG == 1",  #  'End Energy [eV]: ',
                "self.ENERGY_FLAG == 1",  #  'Number of energy points',
                "True",                   #  'Dump to file',
                "self.DUMP_TO_FILE == 1", #  'File name',
                 ]


    def get_help_name(self):
        return 'multilayer'

    def selectFile(self):
        self.FILE_NAME.setText(oasysgui.selectFileFromDialog(self, self.FILE, "Open File For Output", file_extension_filter="*.h5 *.hdf"))

    def check_fields(self):
        self.MATERIAL_S = congruence.checkEmptyString(self.MATERIAL_S,  "Substrate")
        self.MATERIAL_E = congruence.checkEmptyString(self.MATERIAL_E, "Substrate")
        self.MATERIAL_O = congruence.checkEmptyString(self.MATERIAL_O, "Substrate")


        self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY, "Photon energy")
        self.THETA = congruence.checkPositiveNumber(self.THETA, "Grazing angle")

        if self.ENERGY_FLAG == 1:
            self.ENERGY_END = congruence.checkStrictlyPositiveNumber(self.ENERGY_END, "Photon energy")
            self.ENERGY_N = congruence.checkStrictlyPositiveNumber(self.ENERGY_N, "Number of energy points")

        if self.THETA_FLAG == 1:
            self.THETA_END = congruence.checkStrictlyPositiveNumber(self.THETA_END, "Grazing angle")
            self.THETA_N = congruence.checkStrictlyPositiveNumber(self.THETA_N, "Number of angle points")

        self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Bilayer thickness")
        self.GAMMA = congruence.checkStrictlyPositiveNumber(self.GAMMA, "Bilayer gamma")
        self.NLAYERS = congruence.checkStrictlyPositiveNumber(self.NLAYERS, "Number of bilayers")
        #
        self.ROUGHNESS_O = congruence.checkPositiveNumber(self.ROUGHNESS_O, "Roughness odd material")
        self.ROUGHNESS_E = congruence.checkPositiveNumber(self.ROUGHNESS_E, "Roughness even material")
        self.ROUGHNESS_S = congruence.checkPositiveNumber(self.ROUGHNESS_S, "Roughness substrate material")


    def do_xoppy_calculation(self):

        # density_S = self.DENSITY_S
        # density_E = self.DENSITY_E
        # density_O = self.DENSITY_O
        #
        # if density_S == "?": density_S = None
        # if density_E == "?": density_E = None
        # if density_O == "?": density_O = None

        try:
            density_S = float(self.DENSITY_S)
        except:
            density_S = density(self.MATERIAL_S)

        try:
            density_E = float(self.DENSITY_E)
        except:
            density_E = density(self.MATERIAL_E)

        try:
            density_O = float(self.DENSITY_O)
        except:
            density_O = density(self.MATERIAL_O)

        print("Using density:\n  substrate(%s): %f\n  even(%s): %f\n  odd(%s): %f" %
              (self.MATERIAL_S, density_S,
               self.MATERIAL_E, density_E,
               self.MATERIAL_O, density_O, ))

        out = MLayer.initialize_from_bilayer_stack(
            material_S=self.MATERIAL_S, density_S=density_S, roughness_S=self.ROUGHNESS_S,  # 2.33
            material_E=self.MATERIAL_E, density_E=density_E, roughness_E=self.ROUGHNESS_E,  # 19.3
            material_O=self.MATERIAL_O, density_O=density_O, roughness_O=self.ROUGHNESS_O,  # 2.33
            bilayer_pairs=self.NLAYERS,
            bilayer_thickness=self.THICKNESS,
            bilayer_gamma=self.GAMMA,
        )

        for key in out.pre_mlayer_dict.keys():
            print(key, out.pre_mlayer_dict[key])
        #
        if self.ENERGY_FLAG == 0:
            energyN = 1
        else:
            energyN = self.ENERGY_N

        if self.THETA_FLAG == 0:
            thetaN = 1
        else:
            thetaN = self.THETA_N

        if self.DUMP_TO_FILE:
            h5file = self.FILE_NAME
        else:
            h5file = ""

        if energyN * thetaN > 10000:
            result = QMessageBox.question(self,
                "Confirmation",
                "Are you sure you want to calculate %d points in E times %d points in theta (total: %d points):\n \n That will take long time... \n"%
                      (energyN,thetaN,energyN * thetaN),
                QMessageBox.Yes,QMessageBox.No)

            if result == QMessageBox.No:
                raise Exception("Calculation cancelled.")

        rs, rp, e, t = out.scan(h5file=h5file,
                                energyN=energyN, energy1=self.ENERGY, energy2=self.ENERGY_END,
                                thetaN=thetaN, theta1=self.THETA, theta2=self.THETA_END)

        #
        #
        #
        out_dict = {}

        if self.THETA_FLAG == 1 and self.ENERGY_FLAG == 0:   # theta scan
            out = numpy.zeros((t.size,3))

            out[:, 0] = t
            out[:, 1] = rs[0]**2
            out[:, 2] = rp[0]**2

            out_dict["data"] = out
            myscan = 0

        elif self.THETA_FLAG == 0 and self.ENERGY_FLAG == 1:  # energy scan
            out = numpy.zeros((e.size,3))

            out[:, 0] = e
            out[:, 1] = rs[:, 0]**2
            out[:, 2] = rp[:, 0]**2

            out_dict["data"] = out
            myscan = 1

        elif self.THETA_FLAG == 1 and self.ENERGY_FLAG == 1:  # double scan

            out_dict["data2D_rs"] = rs**2
            out_dict["data2D_rp"] = rs**2
            out_dict["dataX"] = e
            out_dict["dataY"] = t
            myscan = 2

        elif self.THETA_FLAG == 0 and self.ENERGY_FLAG == 0:  # single point
            out = numpy.zeros((t.size,3))
            out[:, 0] = t
            out[:, 1] = rs[0]**2
            out[:, 2] = rp[0]**2

            out_dict["data"] = out
            myscan = 0


        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", out_dict["data"])
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", 1)
        except:
            pass

        try:
            calculated_data.add_content("data2D_rs", out_dict["data2D_rs"])
            calculated_data.add_content("data2D_rp", out_dict["data2D_rp"])
            calculated_data.add_content("dataX", out_dict["dataX"])
            calculated_data.add_content("dataY", out_dict["dataY"])
        except:
            pass

        # script

        dict_parameters = {
            "material_S":    self.MATERIAL_S,
            "density_S":     density_S, \
            "roughness_S":   self.ROUGHNESS_S, \
            "material_E":    self.MATERIAL_E, \
            "density_E":     density_E, \
            "roughness_E":   self.ROUGHNESS_E, \
            "material_O":    self.MATERIAL_O, \
            "density_O":     density_O, \
            "roughness_O":   self.ROUGHNESS_O, \
            "bilayer_pairs": self.NLAYERS, \
            "bilayer_thickness": self.THICKNESS, \
            "bilayer_gamma":     self.GAMMA, \
            "energyN":           energyN, \
            "energy1":           self.ENERGY, \
            "energy2":           self.ENERGY_END, \
            "thetaN":            thetaN, \
            "theta1":            self.THETA,\
            "theta2":            self.THETA_END,
            "myscan":            myscan, \
            "h5file":            h5file, \
            }

        # write python script
        self.xoppy_script.set_code(self.script_template().format_map(dict_parameters))

        return calculated_data



    def script_template(self):
        return """
from xoppylib.mlayer import MLayer

out = MLayer.initialize_from_bilayer_stack(
    material_S="{material_S}", density_S={density_S}, roughness_S={roughness_S},
    material_E="{material_E}", density_E={density_E}, roughness_E={roughness_E},
    material_O="{material_O}", density_O={density_O}, roughness_O={roughness_O},
    bilayer_pairs={bilayer_pairs},
    bilayer_thickness={bilayer_thickness},
    bilayer_gamma={bilayer_gamma},
)

for key in out.pre_mlayer_dict.keys():
    print(key, out.pre_mlayer_dict[key])
# reflectivity is for amplitude
rs, rp, e, t = out.scan(h5file="{h5file}",
                energyN={energyN}, energy1={energy1}, energy2={energy2},
                thetaN={thetaN}, theta1={theta1}, theta2={theta2} )
                
#
# plot (example)
#
myscan = {myscan}
from srxraylib.plot.gol import plot,plot_image

if myscan == 0: # angle scan 
    plot(t, rs[0]**2, xtitle="angle [deg]", ytitle="Reflectivity-s", title="")
elif myscan == 1: # energy scan 
    plot(e,rs[:,0]**2,xtitle="Photon energy [eV]",ytitle="Reflectivity-s",title="")
elif myscan == 2: # double scan 
    plot_image(rs**2,e,t,xtitle="Photon energy [eV]",ytitle="Grazing angle [deg]",title="Reflectivity-s",aspect="auto")
               
"""



    def extract_data_from_xoppy_output(self, calculation_output):
        return calculation_output

    def get_data_exchange_widget_name(self):
        return "MULTILAYER"

    def getTitles(self):
        return ["Reflectivity-s","Reflectivity-p"]

    def getXTitles(self):
        if self.THETA_FLAG == 1 and self.ENERGY_FLAG == 0:   # theta scan
            return 2*["Grazing angle [deg]"]
        elif self.THETA_FLAG == 0 and self.ENERGY_FLAG == 1:  # energy scan
            return 2*["Photon energy [eV]"]
        elif self.THETA_FLAG == 1 and self.ENERGY_FLAG == 1:  # double scan
            pass
        elif self.THETA_FLAG == 0 and self.ENERGY_FLAG == 0:  # single point
            return 2*["Grazing angle [deg]"]

    def getYTitles(self):
        return ["reflectivity-s","reflectivity-p"]


    def getVariablesToPlot(self):
        return [(0, 1),(0, 2)]

    def getLogPlot(self):
        return [(False, False),(False, False)]

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):
        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        # place a big dot if there is only a single value
        if ((x.size == 1) and (y.size == 1)):
            self.plot_canvas[plot_canvas_index].setDefaultPlotLines(False)
            self.plot_canvas[plot_canvas_index].setDefaultPlotPoints(True)

    def plot_results(self, calculated_data, progressBarValue=80):
        self.initializeTabs()

        try:

            self.tab[0].layout().removeItem(self.tab[0].layout().itemAt(0))
            self.plot_canvas[0] = None

            super().plot_results(calculated_data, progressBarValue)

            if self.ENERGY_FLAG == 0 and self.THETA_FLAG == 0:  # single point
                tmp = calculated_data.get_content("xoppy_data")
                txt = ""
                txt += "------------------------------------------------------------------------\n"
                txt += "Inputs: \n"
                txt += "   energy [eV]:           %6.3f \n"%self.ENERGY
                txt += "   grazing angle [deg]:   %6.3f \n"%tmp[0,0]
                txt += "Outputs: \n"
                txt += "   R_S:    %5.2f  \n"%tmp[0,1]
                txt += "   R_P:    %5.2f  \n"%tmp[0,2]
                txt += "------------------------------------------------------------------------\n"

                QMessageBox.information(self,
                            "Calculation Result",
                            "Calculation Result:\n %s" % txt,
                            QMessageBox.Ok)
        except:
            try:
                data2D_rs = calculated_data.get_content("data2D_rs")
                data2D_rp = calculated_data.get_content("data2D_rp")
                dataX = calculated_data.get_content("dataX")
                dataY = calculated_data.get_content("dataY")

                self.plot_data2D(data2D_rs, dataX, dataY, 0, 0,
                                 xtitle='Energy [eV]',
                                 ytitle='Grazing angle [deg]',
                                 title='Reflectivity-s')

                self.plot_data2D(data2D_rp, dataX, dataY, 1, 0,
                                 xtitle='Energy [eV]',
                                 ytitle='Grazing angle [deg]',
                                 title='Reflectivity-p')
            except:
                raise Exception("Error retieving data.")


    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def get_help_name(self):
        return 'multilayer'


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = OWMlultilayer()
    w.show()
    app.exec()
    w.saveSettings()

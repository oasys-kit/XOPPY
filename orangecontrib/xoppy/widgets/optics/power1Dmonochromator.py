import sys
import numpy
from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from xoppylib.power.xoppy_calc_power_monochromator import xoppy_calc_power_monochromator

import scipy.constants as codata

class OWPower1DMonochromator(XoppyWidget):
    name = "Power1DMonochromator"
    id = "orange.widgets.dataxpower"
    description = "Power Absorbed and Transmitted by Monochromators"
    icon = "icons/power1_monochromator.png"
    priority = 2.1
    category = ""
    keywords = ["xoppy", "power", "monochromator"]

    inputs = [("ExchangeData", DataExchangeObject, "acceptExchangeData")]

    SOURCE = Setting(2)
    TYPE = Setting(3)
    N_REFLECTIONS = Setting(2)
    POLARIZATION = Setting(0)
    ENER_SELECTED = Setting(8000)
    H_MILLER = Setting (1)
    K_MILLER = Setting (1)
    L_MILLER = Setting (1)
    THICK = Setting(15)
    ENER_MIN = Setting(7990)
    ENER_MAX = Setting(8010)
    ENER_N = Setting(2000)
    SOURCE_FILE = Setting("?")
    FILE_DUMP = Setting(0)
    ML_H5_FILE = Setting("<none>")
    ML_GRAZING_ANGLE_DEG = Setting(0.2)
    METHOD = Setting(0) # Zachariasen

    input_spectrum = None
    input_script = None

    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()

        box_main = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        idx = -1

        box = oasysgui.widgetBox(box_main, "Input Beam Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)
        # widget index 1
        idx += 1
        box1 = gui.widgetBox(box)
        self.box_source = gui.comboBox(box1, self, "SOURCE",
                                       label=self.unitLabels()[idx], addSpace=False,
                                       items=['From Oasys wire', 'Normalized to 1',
                                              'From external file.                '],
                                       valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        # widget index 2
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENER_MIN",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENER_MAX",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENER_N",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 5 ***********   File Browser ******************
        idx += 1
        box1 = gui.widgetBox(box)
        file_box_id = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal")
        self.file_id = oasysgui.lineEdit(file_box_id, self, "SOURCE_FILE", self.unitLabels()[idx],
                                         labelWidth=100, valueType=str, orientation="horizontal")
        gui.button(file_box_id, self, "...", callback=self.select_input_file, width=25)
        self.show_at(self.unitFlags()[idx], box1)

        box = oasysgui.widgetBox(box_main, "Monochromator", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)
        # widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        self.box_source = gui.comboBox(box1, self, "TYPE",
                                       label=self.unitLabels()[idx], addSpace=False,
                                       items=['Empty','Si Bragg','Si Laue',
                                              'Multilayer'],
                                       valueType=int, orientation="horizontal", labelWidth=200)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "N_REFLECTIONS",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        self.box_source = gui.comboBox(box1, self, "POLARIZATION",
                                       label=self.unitLabels()[idx], addSpace=False,
                                       items=['Sigma','Pi','Unpolarized'],
                                       valueType=int, orientation="horizontal", labelWidth=200)
        self.show_at(self.unitFlags()[idx], box1)


        # widget index 9
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ENER_SELECTED",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 10
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "H_MILLER",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 11
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "K_MILLER",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 12
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "L_MILLER",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 13
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "THICK",
                                       label=self.unitLabels()[idx], addSpace=False,
                                       valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 14
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "METHOD",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=["Zachariasen", "Guigay"],
                     orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 15
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ML_H5_FILE",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=str, orientation="horizontal", labelWidth=200)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 16
        idx += 1
        box1 = gui.widgetBox(box)
        oasysgui.lineEdit(box1, self, "ML_GRAZING_ANGLE_DEG",
                          label=self.unitLabels()[idx], addSpace=False,
                          valueType=float, orientation="horizontal", labelWidth=200)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 17
        idx += 1
        box1 = gui.widgetBox(box)
        gui.separator(box1, height=7)

        gui.comboBox(box1, self, "FILE_DUMP",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes (monochromator.spec)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        self.input_spectrum = None

    def select_input_file(self):
        self.file_id.setText(oasysgui.selectFileFromDialog(self, self.SOURCE_FILE,
                                    "Open 2-columns file with spectral power",
                                    file_extension_filter="ascii dat (*.dat *.txt *spec)"))

    def unitLabels(self):
         return ['Input beam:',
                 'From energy [eV]:',
                 'To energy [eV]:',
                 'Energy points:  ',
                 'File with input beam spectral power:',
                 'Type Monochromator',
                 'Number of reflections',
                 'Polarization',
                 'Energy Selected [eV]',
                 'Miller index h','Miller index k','Miller index l','Crystal thickness [microns]',
                 "Calculation method",
                 "XOPPY/Multilayer h5 file",
                 "Grazing angle [deg]",
                 "Dump file",
                 ]

    def unitFlags(self):
         return ['True',
                 'self.SOURCE == 1',
                 'self.SOURCE == 1',
                 'self.SOURCE == 1',
                 'self.SOURCE == 2',
                 'True',
                 'True',
                 'True',
                 'self.TYPE == 1 or self.TYPE == 2',
                 'self.TYPE == 1 or self.TYPE == 2','self.TYPE == 1 or self.TYPE == 2','self.TYPE  ==  1 or self.TYPE  ==  2',
                 'self.TYPE == 2',
                 'self.TYPE == 1 or self.TYPE == 2',
                 'self.TYPE == 3',
                 'self.TYPE == 3',
                 'True']

    def get_help_name(self):
        return 'Monochromator'

    def selectFile(self):
        self.le_source_file.setText(oasysgui.selectFileFromDialog(self, self.SOURCE_FILE, "Open Source File", file_extension_filter="*.*"))

    def acceptExchangeData(self, exchangeData):  # the same as in xpower

        self.input_spectrum = None
        self.input_script = None
        self.SOURCE = 0

        try:
            if not exchangeData is None:
                if exchangeData.get_program_name() == "XOPPY":
                    no_bandwidth = False
                    if exchangeData.get_widget_name() =="UNDULATOR_FLUX" :
                        no_bandwidth = True
                        index_flux = 2
                    elif exchangeData.get_widget_name() == "BM" :
                        if exchangeData.get_content("is_log_plot") == 1:
                            raise Exception("Logaritmic X scale of Xoppy Energy distribution not supported")
                        if exchangeData.get_content("calculation_type") == 0 and exchangeData.get_content("psi") in [0,2]:
                            no_bandwidth = True
                            index_flux = 6
                        else:
                            raise Exception("Xoppy result is not a Flux vs Energy distribution integrated in Psi")
                    elif exchangeData.get_widget_name() =="XWIGGLER" :
                        no_bandwidth = True
                        index_flux = 2
                    elif exchangeData.get_widget_name() =="WS" :
                        no_bandwidth = True
                        index_flux = 2
                    elif exchangeData.get_widget_name() =="XTUBES" :
                        index_flux = 1
                        no_bandwidth = True
                    elif exchangeData.get_widget_name() =="XTUBE_W" :
                        index_flux = 1
                        no_bandwidth = True
                    elif exchangeData.get_widget_name() =="BLACK_BODY" :
                        no_bandwidth = True
                        index_flux = 2

                    elif exchangeData.get_widget_name() =="UNDULATOR_RADIATION" :
                        no_bandwidth = True
                        index_flux = 1
                    elif exchangeData.get_widget_name() =="POWER" :
                        no_bandwidth = True
                        index_flux = -1
                    elif exchangeData.get_widget_name() =="POWER3D" :
                        no_bandwidth = True
                        index_flux = 1

                    else:
                        raise Exception("Xoppy Source not recognized")

                    spectrum = exchangeData.get_content("xoppy_data")

                    if exchangeData.get_widget_name() =="UNDULATOR_RADIATION" or \
                        exchangeData.get_widget_name() =="POWER3D":
                        [p, e, h, v ] = spectrum
                        tmp = p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*codata.e*1e3
                        spectrum = numpy.vstack((e,p.sum(axis=2).sum(axis=1)*(h[1]-h[0])*(v[1]-v[0])*
                                                 codata.e*1e3))
                        self.input_spectrum = spectrum
                    else:

                        if not no_bandwidth:
                            spectrum[:,index_flux] /= 0.001*spectrum[:,0]

                        self.input_spectrum = numpy.vstack((spectrum[:,0],spectrum[:,index_flux]))

                    try:
                        self.input_script = exchangeData.get_content("xoppy_script")
                    except:
                        self.input_script = None

                    self.process_showers()
                    self.compute()
                elif exchangeData.get_program_name() == "SRW":
                    if exchangeData.get_widget_name() =="UNDULATOR_SPECTRUM" :
                        spectrum = exchangeData.get_content("srw_data")

                        self.input_spectrum = numpy.vstack((spectrum[:, 0], spectrum[:, 1]))
                        self.input_script = None

                        self.process_showers()
                        self.compute()

        except Exception as exception:
            QMessageBox.critical(self, "Error", str(exception), QMessageBox.Ok)

    def check_fields(self):
        if self.TYPE  ==  1:
            self.ENER_SELECTED = congruence.checkPositiveNumber(self.ENER_SELECTED, "Energy Selected [eV]")
            self.H_MILLER = congruence.checkNumber(self.H_MILLER, "H Miller")
            self.K_MILLER = congruence.checkNumber(self.K_MILLER, "K Miller")
            self.L_MILLER = congruence.checkNumber(self.H_MILLER, "L Miller")
        if self.TYPE == 2:
            self.ENER_SELECTED = congruence.checkPositiveNumber(self.ENER_SELECTED, "Energy Selected [eV]")
            self.H_MILLER = congruence.checkNumber(self.H_MILLER, "H Miller")
            self.K_MILLER = congruence.checkNumber(self.K_MILLER, "K Miller")
            self.L_MILLER = congruence.checkNumber(self.H_MILLER, "L Miller")
            self.THICK = congruence.checkPositiveNumber(self.THICK, "Laue crystal thickness [mm]")
        if self.TYPE == 3:
            self.ENER_SELECTED = congruence.checkPositiveNumber(self.ENER_SELECTED, "Energy Selected [eV]")

        if self.SOURCE == 1:
            self.ENER_MIN = congruence.checkPositiveNumber(self.ENER_MIN, "Energy from")
            self.ENER_MAX = congruence.checkStrictlyPositiveNumber(self.ENER_MAX, "Energy to")
            congruence.checkLessThan(self.ENER_MIN, self.ENER_MAX, "Energy from", "Energy to")
            self.NPOINTS = congruence.checkStrictlyPositiveNumber(self.ENER_N, "Energy Points")
        elif self.SOURCE == 2:
            congruence.checkFile(self.SOURCE_FILE)

    def do_xoppy_calculation(self):
        if self.SOURCE == 0:
            if self.input_spectrum is None:
                raise Exception("No input beam")
            else:
                energies = self.input_spectrum[0,:].copy()
                source = self.input_spectrum[1,:].copy()
            if self.input_script is None:
                script_previous = '#\n# >> MISSING SCRIPT TO CREATE (energy, spectral_power) <<\n#\n'
            else:
                script_previous = self.input_script
        elif self.SOURCE == 1:
            energies = numpy.linspace(self.ENER_MIN,self.ENER_MAX,self.ENER_N)
            source = numpy.ones(energies.size)
            tmp = numpy.vstack( (energies,source))
            self.input_spectrum = source
            script_previous = "import numpy\nenergy = numpy.linspace(%g,%g,%d)\nspectral_power = numpy.ones(%d)\n" % \
                        (self.ENER_MIN,self.ENER_MAX,self.ENER_N,self.ENER_N)
        elif self.SOURCE == 2:  # file contains energy_eV and spectral power (W/eV)
            source_file = self.SOURCE_FILE
            try:
                tmp = numpy.loadtxt(source_file)
                energies = tmp[:,0]
                source = tmp[:,1]
                self.input_spectrum = source
                script_previous = "import numpy\ntmp = numpy.loadtxt(%s)\nenergy = tmp[:,0]\nspectral_power = tmp[:,1]\n" % \
                                (source_file)
            except:
                print("Error loading file %s "%(source_file))
                raise
        elif self.SOURCE == 3:  # file contains energy_eV and flux (ph/s/0.1%bw
            source_file = self.SOURCE_FILE
            try:
                tmp = numpy.loadtxt(source_file)
                energies = tmp[:,0]
                source = tmp[:,1] * (codata.e * 1e3)
                self.input_spectrum = source
                script_previous = "import numpy\nimport scipy.constants as codata\ntmp = numpy.loadtxt(%s)\nenergy = tmp[:,0]\nspectral_power = tmp[:,1] / (codata.e * 1e3)\n" % \
                                (source_file)
            except:
                print("Error loading file %s "%(source_file))
                raise

        dict_parameters = {
            "TYPE"                : self.TYPE,
            "ENER_SELECTED"       : self.ENER_SELECTED,
            "METHOD"              : self.METHOD,
            "THICK"               : self.THICK,
            "ML_H5_FILE"          : self.ML_H5_FILE,
            "ML_GRAZING_ANGLE_DEG": self.ML_GRAZING_ANGLE_DEG,
            "N_REFLECTIONS"       : self.N_REFLECTIONS,
            "FILE_DUMP"           : self.FILE_DUMP,
            "polarization"        : self.POLARIZATION,
            "output_file"         : "monochromator.spec",
        }
        script_element = self.script_template().format_map(dict_parameters)
        script = script_previous + script_element
        self.xoppy_script.set_code(script)

        out_dictionary = xoppy_calc_power_monochromator(energies, source,
                                                        TYPE                 = self.TYPE,
                                                        ENER_SELECTED        = self.ENER_SELECTED,
                                                        METHOD               = self.METHOD,
                                                        THICK                = self.THICK,
                                                        ML_H5_FILE           = self.ML_H5_FILE,
                                                        ML_GRAZING_ANGLE_DEG =self.ML_GRAZING_ANGLE_DEG,
                                                        N_REFLECTIONS        = self.N_REFLECTIONS,
                                                        FILE_DUMP            = self.FILE_DUMP,
                                                        polarization         = self.POLARIZATION,
                                                        output_file          = "monochromator.spec",
                                                        )

        print(out_dictionary["info"])

        return out_dictionary, script

    def script_template(self):
        return """

#
# script to make the calculations (created by XOPPY:xpower)
#

import numpy
from xoppylib.power.xoppy_calc_power_monochromator import xoppy_calc_power_monochromator
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

out_dictionary = xoppy_calc_power_monochromator(
        energy, # array with energies in eV
        spectral_power, # array with source spectral density
        TYPE                 = {TYPE}, # 0=None, 1=Crystal Bragg, 2=Crystal Laue, 3=Multilayer
        ENER_SELECTED        = {ENER_SELECTED}, # Energy to set crystal monochromator
        METHOD               = {METHOD}, # For crystals, in crystalpy, 0=Zachariasem, 1=Guigay
        THICK                = {THICK}, # crystal thicknes Laur crystal in um
        ML_H5_FILE           = "{ML_H5_FILE}", # File with inputs from multilaters (from xoppy/Multilayer)
        ML_GRAZING_ANGLE_DEG = {ML_GRAZING_ANGLE_DEG}, # for multilayers the grazing angle in degrees
        N_REFLECTIONS        = {N_REFLECTIONS}, # number of reflections (crystals or multilayers)
        FILE_DUMP            = {FILE_DUMP}, # 0=No, 1=yes
        polarization         = {polarization}, # 0=sigma, 1=pi, 2=unpolarized
        output_file          = "{output_file}", # filename if FILE_DUMP=1
        )


# data to pass
energy = out_dictionary["data"][0,:]
spectral_power = out_dictionary["data"][-1,:]

#                       
# example plots
#
from srxraylib.plot.gol import plot
plot(out_dictionary["data"][0,:], out_dictionary["data"][1,:],
    out_dictionary["data"][0,:], out_dictionary["data"][-1,:],
    xtitle=out_dictionary["labels"][0],
    legend=[out_dictionary["labels"][1],out_dictionary["labels"][-1]],
    title='Spectral Power [W/eV]')

#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):
        out_dictionary, script = calculation_output

        # send exchange
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        try:
            calculated_data.add_content("xoppy_data", out_dictionary["data"].T)
        except:
            pass

        try:
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", -1)
        except:
            pass
        try:
            calculated_data.add_content("xoppy_script", script)
        except:
            pass
        try:
            calculated_data.add_content("labels", out_dictionary["labels"])
        except:
            pass
        try:
            calculated_data.add_content("info", out_dictionary["info"])
        except:
            pass

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "POWER"

    def getTitles(self):
        return ['Input Beam', 'Monochromator reflectivity', 'Spectral Power after Monochromator']

    def getXTitles(self):
        return ["Photon Energy [eV]", "Photon Energy [eV]", "Photon Energy [eV]"]

    def getYTitles(self):
        return ['Spectral Power [W/eV]', 'Reflectivity', 'Spectral Power [W/eV]']


    def getVariablesToPlot(self):
        return [(0, 1), (0, 2), (0, 3)]

    def getLogPlot(self):
        return [(False,False), (False, False), (False, False)]

if __name__ == "__main__":

    from oasys.widgets.exchange import DataExchangeObject


    input_data_type = "POWER"

    if input_data_type == "POWER":
        # create fake UNDULATOR_FLUX xoppy exchange data
        e = numpy.linspace(7900.0, 8100.0, 1500)
        source = e/10
        received_data = DataExchangeObject("XOPPY", "POWER")
        received_data.add_content("xoppy_data", numpy.vstack((e,e,source)).T)
        received_data.add_content("xoppy_code", "US")

    elif input_data_type == "POWER3D":
        # create unulator_radiation xoppy exchange data
        from xoppylib.sources.xoppy_undulators import xoppy_calc_undulator_radiation

        e, h, v, p, code = xoppy_calc_undulator_radiation(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                           ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                           ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                           PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,
                                           SETRESONANCE=0,HARMONICNUMBER=1,
                                           GAPH=0.001,GAPV=0.001,\
                                           HSLITPOINTS=41,VSLITPOINTS=41,METHOD=0,
                                           PHOTONENERGYMIN=7000,PHOTONENERGYMAX=8100,PHOTONENERGYPOINTS=20,
                                           USEEMITTANCES=1)
        received_data = DataExchangeObject("XOPPY", "POWER3D")
        received_data = DataExchangeObject("XOPPY", "UNDULATOR_RADIATION")
        received_data.add_content("xoppy_data", [p, e, h, v])
        received_data.add_content("xoppy_code", code)


    app = QApplication(sys.argv)
    w = OWPower1DMonochromator()
    w.acceptExchangeData(received_data)
    w.show()
    app.exec()
    w.saveSettings()

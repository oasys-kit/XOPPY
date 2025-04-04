import numpy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget


import scipy.constants as codata

import xraylib
from dabax.dabax_xraylib import DabaxXraylib

from xoppylib.crystals.tools import run_diff_pat, bragg_calc2

class OWxcrystal(XoppyWidget):
    name = "CRYSTAL"
    id = "orange.widgets.dataxcrystal"
    description = "Crystal Reflectivity (perfect, bent, mosaic)"
    icon = "icons/xoppy_xcrystal.png"
    priority = 5
    category = ""
    keywords = ["xoppy", "xcrystal"]
 
    CRYSTAL_MATERIAL = Setting(32)
    MILLER_INDEX_H = Setting(1)
    MILLER_INDEX_K = Setting(1)
    MILLER_INDEX_L = Setting(1)
    TEMPER = Setting("1.0")
    MOSAIC = Setting(0)
    GEOMETRY = Setting(0)
    SCAN = Setting(2)
    UNIT = Setting(1)
    SCANFROM = Setting(-100.0)
    SCANTO = Setting(100.0)
    SCANPOINTS = Setting(200)
    ENERGY = Setting(8000.0)
    ASYMMETRY_ANGLE = Setting(0.0)
    THICKNESS = Setting(0.7)
    MOSAIC_FWHM = Setting(0.1)
    RSAG = Setting(125.0)
    RMER = Setting(1290.0)
    ANISOTROPY = Setting(0)
    POISSON = Setting(0.22)
    CUT = Setting("2 -1 -1 ; 1 1 1 ; 0 0 0")
    FILECOMPLIANCE = Setting("mycompliance.dat")

    # new crystals  #todo: add to menus?
    material_constants_library_flag = Setting(2) # 0=xraylib, 1=dabax, 2=xraylib completed by dabax
    dx = None # DABAX object


    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=self.get_crystal_list(),
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_H",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_L",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TEMPER",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "MOSAIC",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Perfect crystal', 'Mosaic', 'Bent Crystal ML', 'Bent Crystal PP'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GEOMETRY",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['BRAGG: diffr beam', 'LAUE: diffr beam', 'BRAGG: transm beam', 'LAUE: transm beam'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCAN",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.unit_combo = gui.comboBox(box1, self, "UNIT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Radians', 'micro rads', 'Degrees', 'ArcSec'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANFROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANTO",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ASYMMETRY_ANGLE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THICKNESS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MOSAIC_FWHM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "RSAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "RMER",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "ANISOTROPY",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['None (isotropic)', 'Default cut', 'Cut directions', 'From file'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "POISSON",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "CUT",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box)

        file_box = oasysgui.widgetBox(box1, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file_compliance = oasysgui.lineEdit(file_box, self, "FILECOMPLIANCE",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        gui.button(file_box, self, "...", callback=self.selectFile)

    def unitLabels(self):
         return ['Crystal:','h Miller index','k Miller index','l Miller index','Temperature factor [see help]:', # 0-5
                 'Crystal Model:','Geometry:','Scan:','Scan Units:','Min Scan value:','Max Scan value:','Scan Points:', # 6-12
                 'Fix value (E[eV] or Theta[deg])','Asymmetry angle [deg] (to surf.)','Crystal Thickness [cm]:', # 13-15
                 'Mosaicity [deg, fwhm]: ', #16
                 'R sagittal [cm]: ','R meridional [cm]: ','Anisotropy: ','Poisson ratio','Valong ; Vnorm ; Vperp','File (compliance tensor)']


    def unitFlags(self):
         return ['True','True','True','True','True',
                 'True','True','True','self.SCAN  <=  2','True','True','True',
                 'True','(self.MOSAIC  ==  0) or (self.MOSAIC  >  1)','True',
                 'self.MOSAIC  ==  1',
                 'self.MOSAIC  >  1','self.MOSAIC  >  1','self.MOSAIC  >  1','self.MOSAIC  >  1  and  self.ANISOTROPY  ==  0','self.MOSAIC  >  1  and  self.ANISOTROPY  ==  2','self.MOSAIC  >  1  and  self.ANISOTROPY  ==  3']

    def get_help_name(self):
        return 'crystal'

    def selectFile(self):
        self.le_file_compliance.setText(oasysgui.selectFileFromDialog(self, self.FILECOMPLIANCE, "Open File (compliance tensor)", file_extension_filter="*.dat *.txt"))


    def check_fields(self):
        self.MILLER_INDEX_H = congruence.checkNumber(self.MILLER_INDEX_H, "Miller index H")
        self.MILLER_INDEX_K = congruence.checkNumber(self.MILLER_INDEX_K, "Miller index K")
        self.MILLER_INDEX_L = congruence.checkNumber(self.MILLER_INDEX_L, "Miller index L")
        self.TEMPER = congruence.checkNumber(self.TEMPER, "Temperature factor")

        if self.SCAN == 0 or self.SCAN == 3:
            self.SCANFROM = congruence.checkPositiveNumber(self.SCANFROM, "Min Scan value")
            self.SCANTO = congruence.checkStrictlyPositiveNumber(self.SCANTO, "Max Scan value")
        else:
            self.SCANFROM = congruence.checkNumber(self.SCANFROM, "Min Scan value")
            self.SCANTO = congruence.checkNumber(self.SCANTO, "Max Scan value")

        congruence.checkLessThan(self.SCANFROM, self.SCANTO, "Min Scan value", "Max Scan value")
        self.SCANPOINTS = congruence.checkStrictlyPositiveNumber(self.SCANPOINTS, "Scan points")

        if self.SCAN == 3:
            self.ENERGY = congruence.checkNumber(self.ENERGY, "Fix value")
        else:
            self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY , "Fix value")

        if self.MOSAIC == 0: #perfect
            self.ASYMMETRY_ANGLE = congruence.checkNumber(self.ASYMMETRY_ANGLE, "Asymmetry angle")
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
        elif self.MOSAIC == 1: #mosaic
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
            self.MOSAIC_FWHM = congruence.checkNumber(self.MOSAIC_FWHM, "Mosaicity")
        elif self.MOSAIC == 2 or self.MOSAIC == 3: #bent ML/PP
            self.ASYMMETRY_ANGLE = congruence.checkNumber(self.ASYMMETRY_ANGLE, "Asymmetry angle")
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
            self.RSAG = congruence.checkStrictlyPositiveNumber(self.RSAG, "R Sagittal")
            self.RMER = congruence.checkStrictlyPositiveNumber(self.RMER, "R meridional")

            if self.ANISOTROPY == 0:
                self.POISSON = congruence.checkStrictlyPositiveNumber(self.POISSON, "Poisson Ratio")
            elif self.ANISOTROPY == 2:
                congruence.checkEmptyString(self.CUT, "Valong; Vnorm; Vperp")
            elif self.ANISOTROPY == 3:
                congruence.checkFile(self.FILECOMPLIANCE)

    def get_crystal_list(self):
        crystal_list_xrl = list(xraylib.Crystal_GetCrystalsList())

        if self.material_constants_library_flag == 0:
            return crystal_list_xrl

        if self.dx is None:
            self.dx = DabaxXraylib()
        crystal_list_dabax = self.dx.Crystal_GetCrystalsList()

        if self.material_constants_library_flag == 1:
            return crystal_list_dabax

        crystal_list_combined = crystal_list_xrl
        for crystal in crystal_list_dabax:
            if crystal not in crystal_list_combined:
                crystal_list_combined.append(crystal)

        if self.material_constants_library_flag == 2:
            return crystal_list_combined

    def do_xoppy_calculation(self):
        # return self.xoppy_calc_xcrystal()

        descriptor = self.get_crystal_list()[self.CRYSTAL_MATERIAL]

        if self.material_constants_library_flag == 0:
            material_constants_library = xraylib
        elif self.material_constants_library_flag == 1:
            material_constants_library = self.dx
        elif self.material_constants_library_flag == 2:
            if descriptor in xraylib.Crystal_GetCrystalsList():
                material_constants_library = xraylib
            elif descriptor in self.dx.Crystal_GetCrystalsList():
                material_constants_library = self.dx
            else:
                raise Exception("Descriptor not found in material constants database")

        #
        # run bragg_calc (preprocessor) and create file xcrystal.bra
        #

        # for file in ["xcrystal.bra"]:
        #     try:
        #         os.remove(os.path.join(locations.home_bin_run(), file))
        #     except:
        #         pass

        if self.SCAN == 3:  # energy scan
            emin = self.SCANFROM - 1
            emax = self.SCANTO + 1
        else:
            emin = self.ENERGY - 100.0
            emax = self.ENERGY + 100.0

        estep = (emax - emin) / 500 # the preprocessor data is limited to NMAXENER=1000
        preprocessor_file = "xcrystal.bra"

        print("Using crystal descriptor: ", descriptor)

        bragg_dictionary = bragg_calc2(
            descriptor=descriptor,
            hh=self.MILLER_INDEX_H,
            kk=self.MILLER_INDEX_K,
            ll=self.MILLER_INDEX_L,
            temper=float(self.TEMPER),
            emin=emin,
            emax=emax,
            estep=estep,
            ANISO_SEL=0,
            fileout=preprocessor_file,
            do_not_prototype=0,  # 0=use site groups (recommended), 1=use all individual sites
            verbose=False,
            material_constants_library=material_constants_library,
        )

        #
        # run external (fortran) diff_pat
        #
        run_diff_pat(
            bragg_dictionary,
            preprocessor_file=preprocessor_file,
            descriptor=descriptor,
            MOSAIC=self.MOSAIC,
            GEOMETRY=self.GEOMETRY,
            SCAN=self.SCAN,
            UNIT=self.UNIT,
            SCANFROM=self.SCANFROM,
            SCANTO=self.SCANTO,
            SCANPOINTS=self.SCANPOINTS,
            ENERGY=self.ENERGY,
            ASYMMETRY_ANGLE=self.ASYMMETRY_ANGLE,
            THICKNESS=self.THICKNESS,
            MOSAIC_FWHM=self.MOSAIC_FWHM,
            RSAG=self.RSAG,
            RMER=self.RMER,
            ANISOTROPY=self.ANISOTROPY,
            POISSON=self.POISSON,
            CUT=self.CUT,
            FILECOMPLIANCE=self.FILECOMPLIANCE,
        )

        # show calculated parameters in standard output
        txt_info = open("diff_pat.par").read()
        for line in txt_info:
            print(line, end="")

        #
        # write python script
        #
        if isinstance(material_constants_library, DabaxXraylib):
            material_constants_library_txt = "DabaxXraylib()"
        else:
            material_constants_library_txt = "xraylib"

        dict_parameters = {
            'CRYSTAL_DESCRIPTOR': descriptor,
            'MILLER_INDEX_H': self.MILLER_INDEX_H,
            'MILLER_INDEX_K': self.MILLER_INDEX_K,
            'MILLER_INDEX_L': self.MILLER_INDEX_L,
            'TEMPER': self.TEMPER,
            'MOSAIC': self.MOSAIC,
            'GEOMETRY': self.GEOMETRY,
            'SCAN': self.SCAN,
            'UNIT': self.UNIT,
            'SCANFROM': self.SCANFROM,
            'SCANTO': self.SCANTO,
            'SCANPOINTS': self.SCANPOINTS,
            'ENERGY': self.ENERGY,
            'ASYMMETRY_ANGLE': self.ASYMMETRY_ANGLE,
            'THICKNESS': self.THICKNESS,
            'MOSAIC_FWHM': self.MOSAIC_FWHM,
            'RSAG': self.RSAG,
            'RMER': self.RMER,
            'ANISOTROPY': self.ANISOTROPY,
            'POISSON': self.POISSON,
            'CUT': self.CUT,
            'FILECOMPLIANCE': self.FILECOMPLIANCE,
            'material_constants_library_txt': material_constants_library_txt,
            'emin': emin,
            'emax': emax,
            'estep': estep,
            'preprocessor_file': preprocessor_file}

        script = self.script_template().format_map(dict_parameters)
        self.xoppy_script.set_code(script)

        return bragg_dictionary, "diff_pat.dat", script

    def get_units_to_degrees(self):
        if self.UNIT == 0:  # RADIANS
            return 57.2957795
        elif self.UNIT == 1:  # MICRORADIANS
            return 57.2957795e-6
        elif self.UNIT == 2:  # DEGREES
            return 1.0
        elif self.UNIT == 3:  # ARCSEC
            return 0.000277777805

    def script_template(self):
        return """
#
# script to calculate crystal diffraction profiles (created by XOPPY:crystal)
#

import numpy
from xoppylib.crystals.tools import bragg_calc2, run_diff_pat
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

#
# run bragg_calc (preprocessor) and create file xcrystal.bra
#
bragg_dictionary = bragg_calc2(
    descriptor = "{CRYSTAL_DESCRIPTOR}",
    hh         = {MILLER_INDEX_H}, 
    kk         = {MILLER_INDEX_K}, 
    ll         = {MILLER_INDEX_L}, 
    temper     = {TEMPER}, 
    emin       = {emin},
    emax       = {emax},
    estep      = {estep},
    ANISO_SEL  = 0,
    fileout    = "{preprocessor_file}",
    do_not_prototype = 0,  # 0=use site groups (recommended), 1=use all individual sites
    verbose = False,
    material_constants_library = {material_constants_library_txt},
    )

#
# run external (fortran) diff_pat (note that some parameters may not be used)
#
run_diff_pat( 
    bragg_dictionary,
    preprocessor_file  = "{preprocessor_file}",
    descriptor         = "{CRYSTAL_DESCRIPTOR}",
    MOSAIC             = {MOSAIC}, 
    GEOMETRY           = {GEOMETRY}, 
    SCAN               = {SCAN}, 
    UNIT               = {UNIT}, 
    SCANFROM           = {SCANFROM}, 
    SCANTO             = {SCANTO}, 
    SCANPOINTS         = {SCANPOINTS}, 
    ENERGY             = {ENERGY}, 
    ASYMMETRY_ANGLE    = {ASYMMETRY_ANGLE}, 
    THICKNESS          = {THICKNESS}, 
    MOSAIC_FWHM        = {MOSAIC_FWHM}, 
    RSAG               = {RSAG}, 
    RMER               = {RMER}, 
    ANISOTROPY         = {ANISOTROPY}, 
    POISSON            = {POISSON}, 
    CUT                = "{CUT}",
    FILECOMPLIANCE     = "{FILECOMPLIANCE}", 
    )

#                       
# example plot
#
if True:
    from srxraylib.plot.gol import plot
    data = numpy.loadtxt("diff_pat.dat", skiprows=5)
    plot(data[:,0], data[:,-1], data[:,0], data[:,-2], ytitle='Crystal reflectivity', legend=['s-polarization','p-polarization'])

#
# end script
#
"""

    def extract_data_from_xoppy_output(self, calculation_output):
        #
        # prepare outputs
        #
        bragg_dictionary, diff_pat_file, script = calculation_output

        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

        try:
            calculated_data.add_content("xoppy_data", numpy.loadtxt(diff_pat_file, skiprows=5))
            calculated_data.add_content("plot_x_col", 0)
            calculated_data.add_content("plot_y_col", -1)
            calculated_data.add_content("scan_type", self.SCAN)

            if self.SCAN in (1, 2):
                wavelength = codata.h * codata.c / codata.e / self.ENERGY * 1e2  # cm
                dspacing = float(bragg_dictionary["dspacing"])

                calculated_data.add_content("bragg_angle", numpy.degrees(numpy.arcsin(wavelength / (2 * dspacing))))
                calculated_data.add_content("asymmetry_angle", self.ASYMMETRY_ANGLE)

            if self.SCAN == 3:
                if self.ENERGY > 0:
                    calculated_data.add_content("bragg_angle", self.ENERGY)
                else:
                    wavelength = codata.h * codata.c / codata.e / numpy.abs(self.ENERGY) * 1e2  # cm
                    dspacing = float(bragg_dictionary["dspacing"])
                    calculated_data.add_content("bragg_angle", numpy.degrees(numpy.arcsin(wavelength / (2 * dspacing))))
                calculated_data.add_content("asymmetry_angle", self.ASYMMETRY_ANGLE)

            calculated_data.add_content("units_to_degrees", self.get_units_to_degrees())
        except Exception as e:
            raise Exception("Error loading diff_pat.dat :" + str(e))

        try:
            calculated_data.add_content("labels",
                                        ["Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                                         "Th-ThB{out} [" + self.unit_combo.itemText(self.UNIT) + "]",
                                         "phase_p[rad]",
                                         "phase_s[rad]", "Circ Polariz",
                                         "p-polarized reflectivity",
                                         "s-polarized reflectivity"])

        except:
            pass

        try:
            with open("diff_pat.par") as f:
                info = f.readlines()
            calculated_data.add_content("info", info)
        except:
            pass

        return calculated_data


    def get_data_exchange_widget_name(self):
        return "XCRYSTAL"

    def getTitles(self):
        return ["Phase_p","Phase_s","Circ. Polariz.","p-polarized reflectivity","s-polarized reflectivity"]

    def getXTitles(self):
        if self.SCAN < 3:
            return ["Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]"]
        elif self.SCAN == 3:
            return ["Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]"]
        else:
            return ["y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)"]


    def getYTitles(self):
        return ["phase_p [rad]","phase_s [rad]","Circ. Polariz.","p-polarized reflectivity","s-polarized reflectivity"]

    def getVariablesToPlot(self):
        return [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]

    def getLogPlot(self):
        return[(False, False), (False, False), (False, False), (False, False), (False, False)]

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):
        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        # ALLOW FIT BUTTON HERE
        self.plot_canvas[plot_canvas_index].fitAction.setVisible(True)

        # overwrite FWHM and peak values
        if title == "s-polarized reflectivity" or title == "p-polarized reflectivity":
            t = numpy.where(y>=max(y)*0.5)
            x_left,x_right =  x[t[0][0]], x[t[0][-1]]


            self.plot_canvas[plot_canvas_index].addMarker(x_left, 0.5, legend="G1", text="FWHM=%5.2f"%(x_right-x_left),
                                                          color="pink",selectable=False, draggable=False,
                                                          symbol="+", constraint=None)
            self.plot_canvas[plot_canvas_index].addMarker(x_right, 0.5, legend="G2", text=None, color="pink",
                                                          selectable=False, draggable=False, symbol="+", constraint=None)

            index_ymax = numpy.argmax(y)
            self.plot_canvas[plot_canvas_index].addMarker(x[index_ymax], y[index_ymax], legend="G3",
                                                          text=None, color="pink",
                                                          selectable=False, draggable=False, symbol="+", constraint=None)
            self.plot_canvas[plot_canvas_index].addMarker(x[index_ymax], y[index_ymax]-0.05, legend="G4",
                                                          text="Peak=%5.2f"%(y[index_ymax]), color="pink",
                                                          selectable=False, draggable=False, symbol=None, constraint=None)

#
#
#
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = OWxcrystal()
    w.show()
    app.exec()
    w.saveSettings()

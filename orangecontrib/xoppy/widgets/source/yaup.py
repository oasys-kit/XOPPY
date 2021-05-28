import sys,os
import numpy
import platform
from PyQt5.QtWidgets import QApplication

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from orangecontrib.xoppy.util.xoppy_util import locations
from oasys.widgets.exchange import DataExchangeObject

from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from syned.widget.widget_decorator import WidgetDecorator
import syned.beamline.beamline as synedb
from syned.storage_ring.magnetic_structures.insertion_device import InsertionDevice as synedid

import os
from orangecontrib.xoppy.util.text_window import TextWindow

class OWyaup(XoppyWidget):
    name = "yaup"
    id = "orange.widgets.datayaup"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_yaup.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "yaup"]

    # want_main_area = False

    TITLE = Setting("YAUP EXAMPLE (ESRF BL-8)")
    PERIOD = Setting(4.0)
    NPER = Setting(42)
    NPTS = Setting(40)
    EMIN = Setting(3000.0)
    EMAX = Setting(30000.0)
    NENERGY = Setting(100)
    ENERGY = Setting(6.039999961853027)
    CUR = Setting(0.100000001490116)
    SIGX = Setting(0.425999999046326)
    SIGY = Setting(0.08500000089407)
    SIGX1 = Setting(0.017000000923872)
    SIGY1 = Setting(0.008500000461936)
    D = Setting(30.0)
    XPC = Setting(0.0)
    YPC = Setting(0.0)
    XPS = Setting(2.0)
    YPS = Setting(2.0)
    NXP = Setting(0)
    NYP = Setting(0)
    MODE = Setting(4)
    NSIG = Setting(2)
    TRAJECTORY = Setting("new+keep")
    XSYM = Setting("yes")
    HANNING = Setting(0)
    BFILE = Setting("undul.bf")
    TFILE = Setting("undul.traj")

    # B field

    # PERIOD = Setting(4.0)
    # NPER = Setting(42)
    # NPTS = Setting(40)
    BFIELD_FLAG = Setting(0)
    IMAGNET = Setting(0)
    ITYPE = Setting(0)
    K = Setting(1.379999995231628)
    GAP = Setting(2.0)
    GAPTAP = Setting(10.0)
    FILE = Setting("undul.bf")

    I2TYPE = Setting(0)
    A1 = Setting(0.5)
    A2 = Setting(1.0)

    inputs = WidgetDecorator.syned_input_data()


    def build_gui(self):

        self.IMAGE_WIDTH = 850

        # box = oasysgui.widgetBox(self.controlArea, "Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)

        ##########################
        self.controls_tabs = oasysgui.tabWidget(self.controlArea)
        box = oasysgui.createTabPage(self.controls_tabs, "Input Parameters")
        ##########################


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
        gui.lineEdit(box1, self, "PERIOD",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 2 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPER",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NPTS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMIN",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "EMAX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 7 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "CUR",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 9 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGX1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "SIGY1",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "D",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPC",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "YPS",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=float)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NXP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 19 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NYP",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 20 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "MODE",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 21 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "NSIG",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 22 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TRAJECTORY",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 23 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "XSYM",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 24 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "HANNING",
                     label=self.unitLabels()[idx], addSpace=True,
                    valueType=int)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 25 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "BFILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 26 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.lineEdit(box1, self, "TFILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1) 


        ##########################
        box = oasysgui.createTabPage(self.controls_tabs, "B field")
        ##########################

        # # widget index 0
        # idx += 1
        # box1 = gui.widgetBox(box)
        # gui.lineEdit(box1, self, "PERIOD",
        #              label=self.unitLabels()[idx], addSpace=True,
        #              valueType=float)
        # self.show_at(self.unitFlags()[idx], box1)
        #
        # # widget index 1
        # idx += 1
        # box1 = gui.widgetBox(box)
        # gui.lineEdit(box1, self, "NPER",
        #              label=self.unitLabels()[idx], addSpace=True,
        #              valueType=int)
        # self.show_at(self.unitFlags()[idx], box1)
        #
        # # widget index 2
        # idx += 1
        # box1 = gui.widgetBox(box)
        # gui.lineEdit(box1, self, "NPTS",
        #              label=self.unitLabels()[idx], addSpace=True,
        #              valueType=int)
        # self.show_at(self.unitFlags()[idx], box1)

        # widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "BFIELD_FLAG",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['from ASCII file', 'from BFIELF preprocessor', 'linear B field'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "IMAGNET",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['Nd-Fe-B', 'Sm-Co'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 4
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "ITYPE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['planar undulator', 'tapered undulator'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 5
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "K",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 6
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "GAP",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "GAPTAP",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 8
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "FILE",
                     label=self.unitLabels()[idx], addSpace=True)
        self.show_at(self.unitFlags()[idx], box1)

        # linear B field
        # NPTS: yaupstr.npts, $
        # ITYPE: ['0', 'Magnetic field B [Tesla]', 'Deflection parameter K'], $
        # a1: 0.5, a2: 1.0, FILE: yaupstr.bfile}

        # widget index XX
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "I2TYPE",
                     label=self.unitLabels()[idx], addSpace=True,
                     items=['Magnetic field B [Tesla]', 'Deflection parameter K'],
                     valueType=int, orientation="horizontal")
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "A1",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)

        # widget index 7
        idx += 1
        box1 = gui.widgetBox(box)
        gui.lineEdit(box1, self, "A2",
                     label=self.unitLabels()[idx], addSpace=True,
                     valueType=float)
        self.show_at(self.unitFlags()[idx], box1)



        gui.rubber(self.controlArea)

    def unitLabels(self):
         # return ['Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title','Dummy_title']

        return [
            # 'TITLE', 'PERIOD', 'NPER', 'NPTS',
            #     'EMIN', 'EMAX', 'NENERGY',
            #     'ENERGY', 'CUR',
            #     'SIGX', 'SIGY', 'SIGX1', 'SIGY1',
            #     'D', 'XPC', 'YPC', 'XPS', 'YPS', 'NXP', 'NYP',
            #     'MODE', 'NSIG', 'TRAJECTORY', 'XSYM', 'HANNING', 'BFILE', 'TFILE',
            ' Title:  ',
            'PERIOD - magnet period (cm)',
            'NPER - number of periods',
            'NPTS - number of point/period',
            'EMIN - minimum energy (eV)',
            'EMAX - maximum energy (eV)',
            'NE - number of energy points',
            'ENERGY - e energy (GeV)',
            'CUR - e current (A)',
            'SIGX - H rms e beam (mm)',
            'SIGY - V rms e beam (mm)',
            'SIGX1 - rms H e div (mrad)',
            'SIGY1 - rms V e div (mrad)',
            'D - dist und-observator (m)',
            'XPC - H obs position (mm)',
            'YPC - V obs position (mm)',
            'XPS - H acceptance (mm\mrad)',
            'YPS - V acceptance (mm\mrad)',
            'NXP - no acceptance pts (H)',
            'NYP - no acceptance pts (V)',
            'MODE - (see help)',
            'NSIG - (see help)',
            'TRAJECTORY - calculation flag',
            'XSYM - horizontal symmetry',
            'HANNING - (see help)',
            'BFILE - B filename',
            'TFILE - Traj filename',
            'BFIELD_FLAG',
         # 'PERIOD', 'NPER', 'NPTS',
         #    'PERIOD - magnet period (cm)',
         #    'N - number of periods'      ,
         #    'NPTS - nb of point / period',
        # 'IMAGNET', 'ITYPE', 'K', 'GAP', 'GAPTAP', 'FILE',
            'Undulator Magnet: '         ,
            'Undulator type: '           ,
            'K - K field parameter'      ,
            'GAP - initial gap (cm)'     ,
            'GAPTAP - Gap taper (%)'     ,
            'FILE - Output file name'    ,
         #    aa       =  {PERIOD: yaupstr.period, NPER: yaupstr.nper, $
         # NPTS: yaupstr.npts, $
         # ITYPE: ['0', 'Magnetic field B [Tesla]', 'Deflection parameter K'], $
         # a1: 0.5, a2: 1.0, FILE: yaupstr.bfile}
         #
         # titles = ['PERIOD - magnet period (cm)', 'N - number of periods'  $
         # , 'NPTS - nb of point / period', 'Input parameter: '                 $
         # , 'From:', 'To:', 'FILE - Output (binary) file name'
            'Input parameter: ',
            'From:',
            'To:'
         ]

    def unitFlags(self):
         return ['True','True','True','True',
                 'True','True','True',
                 'True','True',
                 'True','True','True','True',
                 'True','True','True','True','True','True','True',
                 'True','True','True','True','True','True','True',
                 'True',
                 'True','True','True','True','True','True',
                 'True','True','True',]


    #def unitNames(self):
    #     return ['TITLE','PERIOD','NPER','NPTS','EMIN','EMAX','NENERGY','ENERGY','CUR','SIGX','SIGY','SIGX1','SIGY1','D','XPC','YPC','XPS','YPS','NXP','NYP','MODE','NSIG','TRAJECTORY','XSYM','HANNING','BFILE','TFILE']

    def receive_syned_data(self, data):

        if isinstance(data, synedb.Beamline):
            if not data._light_source is None and isinstance(data.get_light_source().get_magnetic_structure(), synedid):
                light_source = data.get_light_source()

                self.ENERGY = light_source.get_electron_beam().energy()
                self.ENERGY_SPREAD = light_source.get_electron_beam()._energy_spread
                self.CURRENT = 1000.0 * light_source._electron_beam.current()

                x, xp, y, yp = light_source.get_electron_beam().get_sigmas_all()

                self.SIGX = 1e3 * x
                self.SIGY = 1e3 * y
                self.SIGX1 = 1e3 * xp
                self.SIGY1 = 1e3 * yp
                self.PERIOD = 100.0 * light_source.get_magnetic_structure().period_length()
                self.NP = light_source.get_magnetic_structure().number_of_periods()

                self.EMIN = light_source.get_magnetic_structure().resonance_energy(gamma=light_source.get_electron_beam().gamma())
                self.EMAX = 5 * self.EMIN

                self.set_enabled(False)

            else:
                self.set_enabled(True)
                # raise ValueError("Syned data not correct")
        else:
            self.set_enabled(True)
            # raise ValueError("Syned data not correct")


    def compute(self):
        pass
        # fileName = xoppy_calc_yaup(TITLE=self.TITLE,PERIOD=self.PERIOD,NPER=self.NPER,NPTS=self.NPTS,EMIN=self.EMIN,EMAX=self.EMAX,NENERGY=self.NENERGY,ENERGY=self.ENERGY,CUR=self.CUR,SIGX=self.SIGX,SIGY=self.SIGY,SIGX1=self.SIGX1,SIGY1=self.SIGY1,D=self.D,XPC=self.XPC,YPC=self.YPC,XPS=self.XPS,YPS=self.YPS,NXP=self.NXP,NYP=self.NYP,MODE=self.MODE,NSIG=self.NSIG,TRAJECTORY=self.TRAJECTORY,XSYM=self.XSYM,HANNING=self.HANNING,BFILE=self.BFILE,TFILE=self.TFILE)
        # #send specfile
        #
        # if fileName == None:
        #     print("Nothing to send")
        # else:
        #     self.send("xoppy_specfile",fileName)
        #     sf = specfile.Specfile(fileName)
        #     if sf.scanno() == 1:
        #         #load spec file with one scan, # is comment
        #         print("Loading file:  ",fileName)
        #         out = np.loadtxt(fileName)
        #         print("data shape: ",out.shape)
        #         #get labels
        #         txt = open(fileName).readlines()
        #         tmp = [ line.find("#L") for line in txt]
        #         itmp = np.where(np.array(tmp) != (-1))
        #         labels = txt[itmp[0]].replace("#L ","").split("  ")
        #         print("data labels: ",labels)
        #         self.send("xoppy_data",out)
        #     else:
        #         print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return


    def get_help_name(self):
        return 'yaup'

    def help1(self):



        home_doc = locations.home_doc()

        filename1 = os.path.join(home_doc, self.get_help_name() + '.txt')

        TextWindow(file=filename1,parent=self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWyaup()
    w.show()
    app.exec()
    w.saveSettings()

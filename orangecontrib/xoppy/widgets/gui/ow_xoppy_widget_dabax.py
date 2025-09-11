from orangewidget import gui
from oasys.widgets import gui as oasysgui
from orangewidget.settings import Setting
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget

from dabax.dabax_files import dabax_f0_files, dabax_f1f2_files, dabax_crosssec_files

class XoppyWidgetDabax(XoppyWidget):

    MATERIAL_CONSTANT_LIBRARY_FLAG = Setting(0)

    DABAX_F0_FILE_INDEX = Setting(0)
    DABAX_F1F2_FILE_INDEX = Setting(0)
    DABAX_CROSSSEC_FILE_INDEX = Setting(0)


    def __init__(self, show_script_tab=False):


        super().__init__(show_script_tab=show_script_tab)


        # widget index xx
        box1 = gui.widgetBox(self.tab_dabax)
        gui.comboBox(box1, self, "MATERIAL_CONSTANT_LIBRARY_FLAG",
                     label='Material Library', addSpace=True,
                     items=["xraylib [default]", "dabax"],
                     orientation="horizontal",
                     callback=self.set_visibility)

        # widget index xx
        self.dabax_f0_box = gui.widgetBox(self.tab_dabax)
        gui.comboBox(self.dabax_f0_box, self, "DABAX_F0_FILE_INDEX",
                     label='dabax f0 file', addSpace=True,
                     items=dabax_f0_files(),
                     orientation="horizontal")

        # widget index xx
        self.dabax_f1f2_box = gui.widgetBox(self.tab_dabax)
        gui.comboBox(self.dabax_f1f2_box, self, "DABAX_F1F2_FILE_INDEX",
                     label="dabax f1f2 file", addSpace=True,
                     items=dabax_f1f2_files(),
                     orientation="horizontal")

        # widget index xx
        self.dabax_crosssec_box = gui.widgetBox(self.tab_dabax)
        gui.comboBox(self.dabax_crosssec_box, self, "DABAX_CROSSSEC_FILE_INDEX",
                     label="dabax cross sec file", addSpace=True,
                     items=dabax_crosssec_files(),
                     orientation="horizontal")

        self.set_visibility()

    def set_visibility(self):
        self.dabax_f0_box.setVisible(False)
        self.dabax_f1f2_box.setVisible(False)
        self.dabax_crosssec_box.setVisible(False)

        if self.MATERIAL_CONSTANT_LIBRARY_FLAG > 0:
            if self.dabax_show_f0():   self.dabax_f0_box.setVisible(True)
            if self.dabax_show_f1f2(): self.dabax_f1f2_box.setVisible(True)
            if self.dabax_show_crosssec(): self.dabax_crosssec_box.setVisible(True)

    def dabax_show_f0(self):
        return False

    def dabax_show_f1f2(self):
        return False

    def dabax_show_crosssec(self):
        return False

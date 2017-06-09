__author__ = 'labx'

import sys, os
import orangecanvas.resources as resources
from PyQt5 import QtGui, QtCore

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib import figure as matfig
    import pylab
except ImportError:
    print(sys.exc_info()[1])
    pass


import xraylib

from oasys.widgets import gui

# TODO: delete: srio commented this and it is never used
# import traceback
# from PyMca5.PyMcaGui import PyMcaQt as qt
# from PyMca5.PyMcaCore import PyMcaDirs
# from PyMca5.PyMcaIO import ArraySave
# from PyMca5.PyMcaGui.plotting.PyMca_Icons import IconDict
# from PyMca5.PyMcaGui.plotting.ImageView import ImageView

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class locations:
    @classmethod
    def home_bin(cls):
        return resources.package_dirname("orangecontrib.xoppy.util") + "/bin/" + str(sys.platform) + "/"

    @classmethod
    def home_doc(cls):
        return resources.package_dirname("orangecontrib.xoppy.util") + "/doc_txt/"

    @classmethod
    def home_data(cls):
        return resources.package_dirname("orangecontrib.xoppy.util") + "/data/"

    @classmethod
    def home_bin_run(cls):
        #return resources.package_dirname("orangecontrib.xoppy.util") + "/bin_run/"
        return os.getcwd()

def xoppy_doc(app):
    home_doc = locations.home_doc()

    filename1 = os.path.join(home_doc,app+'.txt')

    print("xoppy_doc: opening file %s"%filename1)
    if sys.platform == 'darwin':
        command = "'open -a TextEdit "+filename1+" &'"
    elif sys.platform == 'linux':
        command = "'gedit "+filename1+" &'"

    os.system(command)

class XoppyPhysics:
    @classmethod
    def getMaterialDensity(cls, material_formula):
        if material_formula is None: return 0.0
        if str(material_formula.strip()) == "": return 0.0

        try:
            compoundData = xraylib.CompoundParser(material_formula)

            if compoundData["nElements"] == 1:
                return xraylib.ElementDensity(compoundData["Elements"][0])
            else:
                return 0.0
        except:
            return 0.0
class XoppyGui:

    @classmethod
    def combobox_text(cls, widget, master, value, box=None, label=None, labelWidth=None,
             orientation='vertical', items=(), callback=None,
             sendSelectedValue=False, valueType=str,
             control2attributeDict=None, emptyString=None, editable=False, selectedValue = None,
             **misc):

        combo = gui.comboBox(widget, master, value, box=box, label=label, labelWidth=labelWidth, orientation=orientation,
                             items=items, callback=callback, sendSelectedValue=sendSelectedValue, valueType=valueType,
                             control2attributeDict=control2attributeDict, emptyString=emptyString,editable=editable, **misc)
        try:
            combo.setCurrentIndex(items.index(selectedValue))
        except:
            pass

        return combo

class XoppyPlot:

    @classmethod
    def plot_histo(cls, plot_window, x, y, title, xtitle, ytitle, color='blue', replace=True):
        matplotlib.rcParams['axes.formatter.useoffset']='False'

        plot_window.addCurve(x, y, title, symbol='', color=color, xlabel=xtitle, ylabel=ytitle, replace=replace) #'+', '^', ','

        if not xtitle is None: plot_window.setGraphXLabel(xtitle)
        if not ytitle is None: plot_window.setGraphYLabel(ytitle)
        if not title is None: plot_window.setGraphTitle(title)

        plot_window.setDrawModeEnabled(True, 'rectangle')
        plot_window.setInteractiveMode(True)
        plot_window.resetZoom()
        plot_window.replot()

        plot_window.setActiveCurve(title)
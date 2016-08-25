__author__ = 'labx'

import sys, os, numpy
import orangecanvas.resources as resources
from orangewidget import gui
import xraylib
from PyQt4 import QtGui, QtCore

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib import figure as matfig
    import pylab
except ImportError:
    print(sys.exc_info()[1])
    pass

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

class ShowTextDialog(QtGui.QDialog):

    def __init__(self, title, text, width=650, height=400, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(title)
        layout = QtGui.QVBoxLayout(self)

        text_edit = QtGui.QTextEdit(text, self)
        text_edit.setReadOnly(True)

        text_area = QtGui.QScrollArea(self)
        text_area.setWidget(text_edit)
        text_area.setWidgetResizable(True)
        text_area.setFixedHeight(height)
        text_area.setFixedWidth(width)

        bbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)

        bbox.accepted.connect(self.accept)
        layout.addWidget(text_area)
        layout.addWidget(bbox)

    @classmethod
    def show_text(cls, title, text, width=650, height=400, parent=None):
        dialog = ShowTextDialog(title, text, width, height, parent)
        dialog.show()

def xoppy_doc(app):
    home_doc = locations.home_doc()

    filename1 = os.path.join(home_doc,app+'.txt')
    filename2 = os.path.join(home_doc,app+'_par.txt')

    if sys.platform == 'darwin':
        command = "open -a TextEdit "+filename1+" "+filename2+" &"
    elif sys.platform == 'linux':
        command = "gedit "+filename1+" "+filename2+" &"

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
    def plot_histo(cls, plot_window, x, y, title, xtitle, ytitle):
        matplotlib.rcParams['axes.formatter.useoffset']='False'

        plot_window.addCurve(x, y, title, symbol='', color='blue', replace=True) #'+', '^', ','
        if not xtitle is None: plot_window.setGraphXLabel(xtitle)
        if not ytitle is None: plot_window.setGraphYLabel(ytitle)
        if not title is None: plot_window.setGraphTitle(title)
        plot_window.setDrawModeEnabled(True, 'rectangle')
        plot_window.setZoomModeEnabled(True)
        plot_window.resetZoom()
        plot_window.replot()

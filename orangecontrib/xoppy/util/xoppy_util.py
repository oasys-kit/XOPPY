__author__ = 'labx'

import sys, os
import orangecanvas.resources as resources
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

import traceback
import xraylib

from oasys.widgets import gui

from PyMca5.PyMcaGui import PyMcaQt as qt
from PyMca5.PyMcaCore import PyMcaDirs
from PyMca5.PyMcaIO import ArraySave
from PyMca5.PyMcaGui.plotting.PyMca_Icons import IconDict
from PyMca5.PyMcaGui.plotting.ImageView import ImageView


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
    def plot_histo(cls, plot_window, x, y, title, xtitle, ytitle, color='blue', replace=True):
        matplotlib.rcParams['axes.formatter.useoffset']='False'

        plot_window.addCurve(x, y, title, symbol='', color=color, xlabel=xtitle, ylabel=ytitle, replace=replace) #'+', '^', ','
        if title  is not None: plot_window.setGraphTitle(title)
        plot_window.setDrawModeEnabled(True, 'rectangle')
        plot_window.setZoomModeEnabled(True)
        plot_window.resetZoom()
        plot_window.replot()


    class XoppyImageView(ImageView):
        """Subclass ImageView to add save 2D dataset.

        Image origin and scale are not taken into account while saving the image.
        """
        def __init__(self, *args, **kwargs):
            super(XoppyPlot.XoppyImageView, self).__init__(*args, **kwargs)

            # Disable default save behavior and
            # connect to icon signal to get save icon events
            self._imagePlot.enableOwnSave(False)
            self.sigIconSignal.connect(self._handleSaveIcon)

            # Used in getOutputFileName
            self.outputDir = None
            self._saveFilter = None

        def getOutputFileName(self):
            """Open a FileDialog to get the image filename to save to."""
            # Copied from PyMca5.PyMcaGui.plotting.MaskImageWidget
            initdir = PyMcaDirs.outputDir
            if self.outputDir is not None:
                if os.path.exists(self.outputDir):
                    initdir = self.outputDir
            filedialog = qt.QFileDialog(self)
            filedialog.setFileMode(filedialog.AnyFile)
            filedialog.setAcceptMode(qt.QFileDialog.AcceptSave)
            filedialog.setWindowIcon(qt.QIcon(qt.QPixmap(IconDict["gioconda16"])))
            formatlist = ["ASCII Files *.dat",
                          "EDF Files *.edf",
                          'CSV(, separated) Files *.csv',
                          'CSV(; separated) Files *.csv',
                          'CSV(tab separated) Files *.csv',
                          # Added from PlotWindow._getOutputFileName for snapshot
                          'Widget PNG *.png',
                          'Widget JPG *.jpg']
            if hasattr(qt, "QStringList"):
                strlist = qt.QStringList()
            else:
                strlist = []
            for f in formatlist:
                    strlist.append(f)
            if self._saveFilter is None:
                self._saveFilter = formatlist[0]
            filedialog.setFilters(strlist)
            filedialog.selectFilter(self._saveFilter)
            filedialog.setDirectory(initdir)
            ret = filedialog.exec_()
            if not ret:
                return ""
            filename = filedialog.selectedFiles()[0]
            if len(filename):
                filename = qt.safe_str(filename)
                self.outputDir = os.path.dirname(filename)
                self._saveFilter = qt.safe_str(filedialog.selectedFilter())
                filterused = "." + self._saveFilter[-3:]
                PyMcaDirs.outputDir = os.path.dirname(filename)
                if len(filename) < 4:
                    filename = filename + filterused
                elif filename[-4:] != filterused:
                    filename = filename + filterused
            else:
                filename = ""
            return filename

        def _handleSaveIcon(self, event):
            """Handle save icon events.

            Get current active image and save it as a file.
            """
            if event['event'] == 'iconClicked' and event['key'] == 'save':
                imageData = self.getActiveImage()
                if imageData is None:
                    qt.QMessageBox.information(self, "No Data",
                                               "No image to be saved")
                    return
                data, legend, info, pixmap = imageData
                imageList = [data]
                labels = ['value']

                # Copied from MaskImageWidget.saveImageList
                filename = self.getOutputFileName()
                if not len(filename):
                    return

                # Add PNG and JPG adapted from PlotWindow.defaultSaveAction
                if 'WIDGET' in self._saveFilter.upper():
                    fformat = self._saveFilter[-3:].upper()
                    pixmap = qt.QPixmap.grabWidget(self._imagePlot)
                    # Use the following instead to grab the image + histograms
                    # pixmap = qt.QPixmap.grabWidget(self)
                    if not pixmap.save(filename, fformat):
                        msg = qt.QMessageBox(self)
                        msg.setIcon(qt.QMessageBox.Critical)
                        msg.setInformativeText(str(sys.exc_info()[1]))
                        msg.setDetailedText(traceback.format_exc())
                        msg.exec_()
                    return

                if filename.lower().endswith(".edf"):
                    ArraySave.save2DArrayListAsEDF(imageList, filename, labels)
                elif filename.lower().endswith(".csv"):
                    if "," in self._saveFilter:
                        csvseparator = ","
                    elif ";" in self._saveFilter:
                        csvseparator = ";"
                    else:
                        csvseparator = "\t"
                    ArraySave.save2DArrayListAsASCII(imageList, filename, labels,
                                                     csv=True,
                                                     csvseparator=csvseparator)
                else:
                    ArraySave.save2DArrayListAsASCII(imageList, filename, labels,
                                                     csv=False)
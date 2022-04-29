import sys, os, numpy, platform
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

from oasys.widgets import gui
from orangecontrib.xoppy.widgets.gui.text_window import TextWindow
from xoppylib.xoppy_util import locations

from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

def xoppy_doc(app):
    home_doc = locations.home_doc()

    filename1 = os.path.join(home_doc,app+'.txt')

    o = TextWindow()
    o.set_file(filename1)

class XoppyGui:

    @classmethod
    def combobox_text(cls, widget, master, value, box=None, label=None, labelWidth=None,
             orientation='vertical', items=(), callback=None,
             sendSelectedValue=False, valueType=str,
             control2attributeDict=None, emptyString=None, editable=False, selectedValue = None,
             **misc):

        combo = gui.comboBox(widget, master, value, box=box, label=label, labelWidth=labelWidth, orientation=orientation,
                                  items=items, callback=callback, sendSelectedValue=sendSelectedValue, valueType=valueType,
                                  control2attributeDict=control2attributeDict, emptyString=emptyString, editable=editable, **misc)
        try:
            combo.setCurrentIndex(items.index(selectedValue))
        except:
            pass

        return combo

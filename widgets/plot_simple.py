from PyQt4 import QtGui
from PyQt4.QtGui import QDoubleValidator
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import numpy as np
import Orange
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class OWPlotSimple(widget.OWWidget):
    name = "Plot Simple"
    id = "orange.widgets.data.widget_name"
    description = ""
    icon = "icons/Unknown.svg"
    author = ""
    maintainer_email = ""
    priority = 10
    category = ""
    keywords = ["list", "of", "keywords"]
    inputs = [{"name": "xoppy_data",
                "type": np.ndarray,
                "doc": "",
                "handler": "do_plot" }]


    def __init__(self):
        super().__init__()
        self.figure_canvas = None

    def do_plot(self,xoppy_data):
        x = xoppy_data[:, 0]
        y = xoppy_data[:, 1]
        x.shape = -1
        y.shape = -1
        fig = plt.figure()
        plt.plot(x,y,linewidth=1.0, figure=fig)
        plt.grid(True)
        if self.figure_canvas is not None:
            self.mainArea.layout().removeWidget(self.figure_canvas)
        self.figure_canvas = FigureCanvas(fig) #plt.figure())
        self.mainArea.layout().addWidget(self.figure_canvas)
        
        

#import os        
#name = os.path.split(__file__)[0] + "foo.json"
#json = open(name).read()
#data = eval(json)
#print(data)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ow = OWPlotSimple()
    a = np.array([
        [  8.47091837e+04,   1.16210756e+12],
        [  8.57285714e+04,   1.10833975e+12],
        [  8.67479592e+04,   1.05700892e+12],
        [  8.77673469e+04,   1.00800805e+12] ])
    ow.do_plot(a)
    ow.show()
    app.exec_()
    ow.saveSettings()

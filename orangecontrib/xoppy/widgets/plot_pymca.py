from PyQt4 import QtGui
from PyQt4.QtGui import QDoubleValidator
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import numpy as np
import Orange
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyMca5.PyMcaGui.plotting.PlotWindow import PlotWindow


class OWPlotPymca(widget.OWWidget):
    name = "plot using PyMca"
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


    # def replaceObject(self, index, object):
    #     if self.plot_canvas[index] is not None:
    #         self.tab[index].layout().removeWidget(self.plot_canvas[index])
    #     return_object = self.plot_canvas[index]
    #     self.plot_canvas[index] = object
    #     self.tab[index].layout().addWidget(self.plot_canvas[index])


    # def replace_fig(self, figure_canvas_index, figure):
    #     old_figure = self.replaceObject(figure_canvas_index, FigureCanvas(figure))
    #
    #     if not old_figure is None:
    #         old_figure.figure.clf()
    #         old_figure = None
    #         ST.plt.close("all")
    #         gc.collect()
    #
    #
    # def replace_plot(self, plot_canvas_index, plot):
    #     old_figure = self.replaceObject(plot_canvas_index, plot)
    #
    #     if not old_figure is None:
    #         old_figure = None
    #         ST.plt.close("all")
    #         gc.collect()

    def do_plot(self,xoppy_data):
        x = xoppy_data[:, 0]
        y = xoppy_data[:, 1]
        x.shape = -1
        y.shape = -1
        #fig = plt.figure()
        #plt.plot(x,y,linewidth=1.0, figure=fig)
        #plt.grid(True)
        #if self.figure_canvas is not None:
        #    self.mainArea.layout().removeWidget(self.figure_canvas)
        #self.figure_canvas = FigureCanvas(fig) #plt.figure())
        #self.mainArea.layout().addWidget(self.figure_canvas)
        title = "top"
        xtitle = "X"
        ytitle = "Y"
        print (x,y)

        plot = PlotWindow(roi=True, control=True, position=True)
        plot.setDefaultPlotLines(False)
        plot.setActiveCurveColor(color='darkblue')
        plot.addCurve(x, y, title, symbol='o', color='blue') #'+', '^',
        plot.setGraphXLabel(xtitle)
        plot.setGraphYLabel(ytitle)
        plot.setDrawModeEnabled(True, 'rectangle')
        plot.setZoomModeEnabled(True)
        if self.figure_canvas is not None:
            self.mainArea.layout().removeWidget(self.figure_canvas)

        self.figure_canvas = plot #plt.figure())
        self.mainArea.layout().addWidget(self.figure_canvas)

        #self.replace_plot(plot_canvas_index, plot)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ow = OWPlotPymca()
    a = np.array([
        [  8.47091837e+04,   1.16210756e+12],
        [  8.57285714e+04,   1.10833975e+12],
        [  8.67479592e+04,   1.05700892e+12],
        [  8.77673469e+04,   1.00800805e+12] ])
    ow.do_plot(a)
    ow.show()
    app.exec_()
    ow.saveSettings()


    #self.replace_plot(plot_canvas_index, plot)
    #self.progressBarSet(progressBarValue)

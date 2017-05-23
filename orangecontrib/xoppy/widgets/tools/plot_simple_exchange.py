from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QDoubleValidator
from orangewidget import widget, gui
from orangewidget.settings import Setting
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from oasys.widgets.exchange import DataExchangeObject

class OWPlotSimpleExchange(widget.OWWidget):
    name = "Xoppy-Data Plot"
    id = "orange.widgets.data.widget_name"
    description = ""
    icon = "icons/histogram.png"
    author = ""
    maintainer_email = ""
    priority = 10
    category = ""
    keywords = ["list", "of", "keywords"]
    inputs = [{"name": "xoppy_data",
                "type": DataExchangeObject,
                "doc": "",
                "handler": "do_plot" }, ]


    def __init__(self):
        super().__init__()
        self.figure_canvas = None

    '''
    def do_plot(self, exchange_data):
        print(">>plot_data_exchange: data received")
        plot_type = None
        try:
            data = exchange_data.get_content("data")
            plot_type = "1D"
        except:
            pass
        try:
            data = exchange_data.get_content("data2D")
            plot_type = "2D"
        except:
            pass

        if plot_type == None:
            print(">>plot_data_exchange: Nothing to plot")
            return

        if plot_type == "1D":
            print(">>plot_data_exchange: plotting 1D")
            try:
                xcol = exchange_data.get_content("plot_x_col")
            except:
                xcol = 0
            try:
                ycol = exchange_data.get_content("plot_y_col")
            except:
                ycol = 0

            x = data[xcol,:]
            y = data[ycol,:]
            x.shape = -1
            y.shape = -1
            fig = plt.figure()
            plt.plot(x,y,linewidth=1.0, figure=fig)
            try:
                plt.title(exchange_data.get_content("name"))
            except:
                pass
            try:
                plt.xlabel(exchange_data.get_content("labels")[xcol])
            except:
                pass
            try:
                plt.ylabel(exchange_data.get_content("labels")[ycol])
            except:
                pass
            plt.grid(True)
    '''

    def do_plot(self, exchange_data):
        print(">>plot_data_exchange: data received")
        plot_type = None
        try:
            data = exchange_data.get_content("xoppy_data").T
            plot_type = "1D"
        except:
            pass

        try:

            data = exchange_data.get_content("data2D")
            plot_type = "2D"
        except:
            pass

        if plot_type == None:
            print(">>plot_data_exchange: Nothing to plot")
            return

        if plot_type == "1D":
            print(">>plot_data_exchange: plotting 1D")
            try:
                xcol = exchange_data.get_content("plot_x_col")
            except:
                xcol = 0
            try:
                ycol = exchange_data.get_content("plot_y_col")
            except:
                ycol = 1

            x = data[xcol,:]
            y = data[ycol,:]
            x.shape = -1
            y.shape = -1
            fig = plt.figure()
            plt.plot(x,y,linewidth=1.0, figure=fig)
            try:
                plt.title(exchange_data.get_content("name"))
            except:
                pass
            try:
                plt.xlabel(exchange_data.get_content("labels")[xcol])
            except:
                pass
            try:
                plt.ylabel(exchange_data.get_content("labels")[ycol])
            except:
                pass
            plt.grid(True)

        if plot_type == "2D":
            print(">>plot_data_exchange: plotting 2D")
            try:
                x = exchange_data.get_content("dataX")
            except:
                x = numpy.arange(data.shape[0])
            try:
                y = exchange_data.get_content("dataY")
            except:
                y = numpy.arange(data.shape[0])

            from srxraylib.plot.gol import plot_surface
            fig = plot_surface(data,x,y,show=0)




        if self.figure_canvas is not None:
            self.mainArea.layout().removeWidget(self.figure_canvas)
        self.figure_canvas = FigureCanvas(fig) #plt.figure())
        self.mainArea.layout().addWidget(self.figure_canvas)

def example_1d():
    app = QtWidgets.QApplication([])
    ow = OWPlotSimpleExchange()
    a = DataExchangeObject("TEXT","TEST")
    a.add_content("data",numpy.array([
        [  8.47091837e+04,   1.16210756e+12],
        [  8.57285714e+04,   1.10833975e+12],
        [  8.67479592e+04,   1.05700892e+12],
        [  8.77673469e+04,   1.00800805e+12] ]))
    ow.do_plot(a)

    ow.show()
    app.exec_()
    ow.saveSettings()

def example_2d():
    app = QtWidgets.QApplication([])
    ow = OWPlotSimpleExchange()
    a = DataExchangeObject("TEXT","TEST")

    x = numpy.linspace(-4, 4, 20)
    y = numpy.linspace(-4, 4, 20)
    z = numpy.sqrt(x[numpy.newaxis, :]**2 + y[:, numpy.newaxis]**2)

    a.add_content("data2D",z)
    a.add_content("dataX",x)
    a.add_content("dataY",y)

    ow.do_plot(a)

    ow.show()
    app.exec_()
    ow.saveSettings()

if __name__ == '__main__':

    example_1d()
    example_2d()


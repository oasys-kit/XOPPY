import sys
import numpy
import matplotlib

from silx.gui.plot import Plot2D
from silx.io.specfile import SpecFile

from silx.gui.plot.StackView import StackViewMainWindow

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from srxraylib.plot import gol

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import OWAction
from oasys.widgets import widget
from oasys.widgets import gui as oasysgui
from oasys.widgets.exchange import DataExchangeObject
from oasys.util.oasys_util import EmittingStream

from orangecontrib.xoppy.util.python_script import PythonScript

class XoppyWidget(widget.OWWidget):
    author = "Manuel Sanchez del Rio, Luca Rebuffi"
    maintainer_email = "srio@esrf.eu"
    outputs = [{"name": "xoppy_data",
                "type": DataExchangeObject,
                "doc": ""}]

    IMAGE_WIDTH = 760
    IMAGE_HEIGHT = 545
    MAX_WIDTH = 1320
    MAX_HEIGHT = 700
    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT = 560

    view_type=Setting(1)

    calculated_data = None

    want_main_area = 1

    def __init__(self,show_script_tab=False):
        super().__init__()

        self.runaction = OWAction("Compute", self)
        self.runaction.triggered.connect(self.compute)
        self.addAction(self.runaction)

        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())

        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        box0 = gui.widgetBox(self.controlArea, "", orientation="horizontal")
        #widget buttons: compute, set defaults, help
        gui.button(box0, self, "Compute", callback=self.compute)
        gui.button(box0, self, "Defaults", callback=self.defaults)
        gui.button(box0, self, "Help", callback=self.help1)

        gui.separator(self.controlArea, height=10)

        self.build_gui()

        self.process_showers()

        gui.rubber(self.controlArea)

        self.main_tabs = oasysgui.tabWidget(self.mainArea)
        plot_tab = oasysgui.createTabPage(self.main_tabs, "Results")


        #results tab
        view_box = oasysgui.widgetBox(plot_tab, "Results Options", addSpace=False, orientation="horizontal")
        view_box_1 = oasysgui.widgetBox(view_box, "", addSpace=False, orientation="vertical", width=350)

        self.view_type_combo = gui.comboBox(view_box_1, self, "view_type", label="View Results",
                                            labelWidth=220,
                                            items=["No", "Yes"],
                                            callback=self.set_ViewType, sendSelectedValue=False, orientation="horizontal")

        self.tabs = oasysgui.tabWidget(plot_tab)

        self.tab = []
        self.initializeTabs()

        #output tab
        out_tab = oasysgui.createTabPage(self.main_tabs, "Output")
        self.xoppy_output = QtWidgets.QTextEdit()
        self.xoppy_output.setReadOnly(True)

        out_box = gui.widgetBox(out_tab, "System Output", addSpace=True, orientation="horizontal")
        out_box.layout().addWidget(self.xoppy_output)

        # self.xoppy_output.setFixedHeight(600)
        # self.xoppy_output.setFixedWidth(600)

        if show_script_tab:

            # script tab
            script_tab = oasysgui.createTabPage(self.main_tabs, "Script")
            self.xoppy_script = PythonScript()
            self.xoppy_script.code_area.setFixedHeight(400)

            script_box = gui.widgetBox(script_tab, "Python script", addSpace=True, orientation="horizontal")
            script_box.layout().addWidget(self.xoppy_script)

            # self.xoppy_script.setFixedHeight(600)
            # self.xoppy_script.setFixedWidth(600)

        self.current_tab = -1

        gui.rubber(self.mainArea)

    def build_gui(self):
        pass

    def initializeTabs(self):
        size = len(self.tab)
        indexes = range(0, size)

        for index in indexes:
            self.tabs.removeTab(size-1-index)

        titles = self.getTitles()

        self.tab = []
        self.plot_canvas = []

        for index in range(0, len(titles)):
            self.tab.append(oasysgui.createTabPage(self.tabs, titles[index]))
            self.plot_canvas.append(None)

        for tab in self.tab:
            tab.setFixedHeight(self.IMAGE_HEIGHT)
            tab.setFixedWidth(self.IMAGE_WIDTH)

    def getDefaultPlotTabIndex(self):
        return -1

    def getTitles(self):
        return ["Calculation Result"]

    def getXTitles(self):
        return ["Energy [eV]"]

    def getYTitles(self):
        return ["X [$\mu$m]"]

    def getVariablesToPlot(self):
        return [(0, 1)]

    def getLogPlot(self):
        return [(False, False)]

    def set_ViewType(self):
        self.progressBarInit()

        if not self.calculated_data==None:
            try:
                self.initializeTabs()

                self.plot_results(self.calculated_data)
            except Exception as exception:
                QtWidgets.QMessageBox.critical(self, "Error",
                                            str(exception),
                                            QtWidgets.QMessageBox.Ok)

        self.progressBarFinished()

    def plot_results(self, calculated_data, progressBarValue=80):
        if not self.view_type == 0:
            if not calculated_data is None:
                current_index = self.tabs.currentIndex()

                self.view_type_combo.setEnabled(False)

                xoppy_data = calculated_data.get_content("xoppy_data")

                titles = self.getTitles()
                xtitles = self.getXTitles()
                ytitles = self.getYTitles()

                progress_bar_step = (100-progressBarValue)/len(titles)

                for index in range(0, len(titles)):
                    x_index, y_index = self.getVariablesToPlot()[index]
                    log_x, log_y = self.getLogPlot()[index]

                    try:
                        self.plot_histo(xoppy_data[:, x_index],
                                        xoppy_data[:, y_index],
                                        progressBarValue + ((index+1)*progress_bar_step),
                                        tabs_canvas_index=index,
                                        plot_canvas_index=index,
                                        title=titles[index],
                                        xtitle=xtitles[index],
                                        ytitle=ytitles[index],
                                        log_x=log_x,
                                        log_y=log_y)

                        # self.tabs.setCurrentIndex(index)
                    except Exception as e:
                        self.view_type_combo.setEnabled(True)

                        raise Exception("Data not plottable: bad content\n" + str(e))

                self.view_type_combo.setEnabled(True)

                try:
                    self.tabs.setCurrentIndex(current_index)
                except:
                    if self.getDefaultPlotTabIndex() == -1:
                        self.tabs.setCurrentIndex(len(titles) - 1)
                    else:
                        self.tabs.setCurrentIndex(self.getDefaultPlotTabIndex())


            else:
                raise Exception("Empty Data")

    def writeStdOut(self, text):
        cursor = self.xoppy_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.xoppy_output.setTextCursor(cursor)
        self.xoppy_output.ensureCursorVisible()

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="",
                   log_x=False, log_y=False, color='blue', replace=True, control=False):

        matplotlib.rcParams['axes.formatter.useoffset']='False'

        if self.plot_canvas[plot_canvas_index] is None:
            self.plot_canvas[plot_canvas_index] = oasysgui.plotWindow(parent=None,
                                                                      backend=None,
                                                                      resetzoom=True,
                                                                      autoScale=False,
                                                                      logScale=True,
                                                                      grid=True,
                                                                      curveStyle=True,
                                                                      colormap=False,
                                                                      aspectRatio=False,
                                                                      yInverted=False,
                                                                      copy=True,
                                                                      save=True,
                                                                      print_=True,
                                                                      control=control,
                                                                      position=True,
                                                                      roi=False,
                                                                      mask=False,
                                                                      fit=False)
            self.plot_canvas[plot_canvas_index].setDefaultPlotLines(True)
            self.plot_canvas[plot_canvas_index].setActiveCurveColor(color="#00008B")
            self.plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
            self.plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)

            self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])

        self.plot_canvas[plot_canvas_index].addCurve(x, y, title, symbol='', color=color, xlabel=xtitle, ylabel=ytitle, replace=replace) #'+', '^', ','

        if not xtitle is None: self.plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
        if not ytitle is None: self.plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
        if not title is None: self.plot_canvas[plot_canvas_index].setGraphTitle(title)

        self.plot_canvas[plot_canvas_index].setInteractiveMode('zoom',color='orange')
        self.plot_canvas[plot_canvas_index].resetZoom()
        self.plot_canvas[plot_canvas_index].replot()

        self.plot_canvas[plot_canvas_index].setActiveCurve(title)

        self.plot_canvas[plot_canvas_index].setXAxisLogarithmic(log_x)
        self.plot_canvas[plot_canvas_index].setYAxisLogarithmic(log_y)

        if min(y) < 0:
            if log_y:
                self.plot_canvas[plot_canvas_index].setGraphYLimits(min(y)*1.2, max(y)*1.2)
            else:
                self.plot_canvas[plot_canvas_index].setGraphYLimits(min(y)*1.01, max(y)*1.01)
        else:
            if log_y:
                self.plot_canvas[plot_canvas_index].setGraphYLimits(min(y), max(y)*1.2)
            else:
                self.plot_canvas[plot_canvas_index].setGraphYLimits(min(y), max(y)*1.01)


        self.progressBarSet(progressBarValue)

    def plot_data1D(self, dataX, dataY, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="",
                    control=False, xlog=False, ylog=False):

        self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(0))

        self.plot_canvas[plot_canvas_index] = oasysgui.plotWindow(parent=None,
                                                                      backend=None,
                                                                      resetzoom=True,
                                                                      autoScale=False,
                                                                      logScale=True,
                                                                      grid=True,
                                                                      curveStyle=True,
                                                                      colormap=False,
                                                                      aspectRatio=False,
                                                                      yInverted=False,
                                                                      copy=True,
                                                                      save=True,
                                                                      print_=True,
                                                                      control=control,
                                                                      position=True,
                                                                      roi=False,
                                                                      mask=False,
                                                                      fit=False)

        self.plot_canvas[plot_canvas_index].addCurve(dataX, dataY)

        self.plot_canvas[plot_canvas_index].resetZoom()
        self.plot_canvas[plot_canvas_index].setXAxisAutoScale(True)
        self.plot_canvas[plot_canvas_index].setYAxisAutoScale(True)
        self.plot_canvas[plot_canvas_index].setGraphGrid(False)

        self.plot_canvas[plot_canvas_index].setXAxisLogarithmic(xlog)
        self.plot_canvas[plot_canvas_index].setYAxisLogarithmic(ylog)
        self.plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
        self.plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
        self.plot_canvas[plot_canvas_index].setGraphTitle(title)

        self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])

    def plot_data2D(self, data2D, dataX, dataY, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", mode=2):

        for i in range(1+self.tab[tabs_canvas_index].layout().count()):
            self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(i))

        if mode == 0:
            figure = FigureCanvas(gol.plot_image(data2D,
                                                 dataX,
                                                 dataY,
                                                 xtitle=xtitle,
                                                 ytitle=ytitle,
                                                 title=title,
                                                 show=False,
                                                 aspect='auto'))


            self.plot_canvas[plot_canvas_index] = figure
        else:

            origin = (dataX[0],dataY[0])
            scale = (dataX[1]-dataX[0],dataY[1]-dataY[0])

            data_to_plot = data2D.T

            colormap = {"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256}


            if mode == 1:
                #TODO: delete: srio commented this part as it is never used
                raise Exception("Cannot use XoppyPlot.XoppyImageView()")
                # self.plot_canvas[plot_canvas_index] = XoppyPlot.XoppyImageView()
                # colormap = {"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256}
                #
                # self.plot_canvas[plot_canvas_index]._imagePlot.setDefaultColormap(colormap)
                # self.plot_canvas[plot_canvas_index].setImage(numpy.array(data_to_plot), origin=origin, scale=scale)
            elif mode == 2:

                self.plot_canvas[plot_canvas_index] = Plot2D()

                self.plot_canvas[plot_canvas_index].resetZoom()
                self.plot_canvas[plot_canvas_index].setXAxisAutoScale(True)
                self.plot_canvas[plot_canvas_index].setYAxisAutoScale(True)
                self.plot_canvas[plot_canvas_index].setGraphGrid(False)
                self.plot_canvas[plot_canvas_index].setKeepDataAspectRatio(True)
                self.plot_canvas[plot_canvas_index].yAxisInvertedAction.setVisible(False)

                self.plot_canvas[plot_canvas_index].setXAxisLogarithmic(False)
                self.plot_canvas[plot_canvas_index].setYAxisLogarithmic(False)
                #silx 0.4.0
                self.plot_canvas[plot_canvas_index].getMaskAction().setVisible(False)
                self.plot_canvas[plot_canvas_index].getRoiAction().setVisible(False)
                self.plot_canvas[plot_canvas_index].getColormapAction().setVisible(True)
                self.plot_canvas[plot_canvas_index].setKeepDataAspectRatio(False)



                self.plot_canvas[plot_canvas_index].addImage(numpy.array(data_to_plot),
                                                             legend="zio billy",
                                                             scale=scale,
                                                             origin=origin,
                                                             colormap=colormap,
                                                             replace=True)

                self.plot_canvas[plot_canvas_index].setActiveImage("zio billy")

            self.plot_canvas[plot_canvas_index].setGraphXLabel(xtitle)
            self.plot_canvas[plot_canvas_index].setGraphYLabel(ytitle)
            self.plot_canvas[plot_canvas_index].setGraphTitle(title)

        self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])


    def plot_data3D(self, data3D, dataE, dataX, dataY, tabs_canvas_index, plot_canvas_index,
                    title="", xtitle="", ytitle="", color_limits_uniform=False):

        for i in range(1+self.tab[tabs_canvas_index].layout().count()):
            self.tab[tabs_canvas_index].layout().removeItem(self.tab[tabs_canvas_index].layout().itemAt(i))

        xmin = numpy.min(dataX)
        xmax = numpy.max(dataX)
        ymin = numpy.min(dataY)
        ymax = numpy.max(dataY)


        stepX = dataX[1]-dataX[0]
        stepY = dataY[1]-dataY[0]
        if len(dataE) > 1: stepE = dataE[1]-dataE[0]
        else: stepE = 1.0

        if stepE == 0.0: stepE = 1.0
        if stepX == 0.0: stepX = 1.0
        if stepY == 0.0: stepY = 1.0

        dim0_calib = (dataE[0],stepE)
        dim1_calib = (ymin, stepY)
        dim2_calib = (xmin, stepX)


        data_to_plot = numpy.swapaxes(data3D,1,2)

        if color_limits_uniform:
            colormap = {"name":"temperature", "normalization":"linear", "autoscale":False, "vmin":data3D.min(), "vmax":data3D.max(), "colors":256}

        else:
            colormap = {"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256}

        self.plot_canvas[plot_canvas_index] = StackViewMainWindow()

        self.plot_canvas[plot_canvas_index].setGraphTitle(title)
        self.plot_canvas[plot_canvas_index].setLabels(["Photon Energy [eV]",ytitle,xtitle])
        self.plot_canvas[plot_canvas_index].setColormap(colormap=colormap)
        self.plot_canvas[plot_canvas_index].setTitleCallback(lambda idx: "Energy: %6.3f eV"%dataE[idx])

        self.plot_canvas[plot_canvas_index].setStack(numpy.array(data_to_plot),
                                                     calibrations=[dim0_calib, dim1_calib, dim2_calib] )
        self.tab[tabs_canvas_index].layout().addWidget(self.plot_canvas[plot_canvas_index])


    def compute(self):
        self.setStatusMessage("Running XOPPY")

        self.progressBarInit()

        try:
            self.xoppy_output.setText("")

            sys.stdout = EmittingStream(textWritten=self.writeStdOut)

            self.progressBarSet(20)

            self.check_fields()

            calculation_output = self.do_xoppy_calculation()

            self.progressBarSet(50)

            if calculation_output is None:
                raise Exception("Xoppy gave no result")
            else:
                self.calculated_data = self.extract_data_from_xoppy_output(calculation_output)

                self.add_specific_content_to_calculated_data(self.calculated_data)

                self.setStatusMessage("Plotting Results")

                self.plot_results(self.calculated_data, progressBarValue=60)

                self.setStatusMessage("")

                self.send("xoppy_data", self.calculated_data)

        except Exception as exception:
            QtWidgets.QMessageBox.critical(self, "Error",
                                       str(exception), QtWidgets.QMessageBox.Ok)
            self.setStatusMessage("Error!")

        self.progressBarFinished()


    def defaults(self):
         self.resetSettings()

    def help1(self):

        import os
        from orangecontrib.xoppy.widgets.gui.text_window import TextWindow
        from orangecontrib.xoppy.util.xoppy_util import locations

        home_doc = locations.home_doc()
        filename1 = os.path.join(home_doc, self.get_help_name() + '.txt')
        TextWindow(file=filename1,parent=self)




    def get_help_name(self):
        raise Exception("This method should be reimplementd in subclasses!")

    def check_fields(self):
        raise Exception("This method should be reimplementd in subclasses!")

    def do_xoppy_calculation(self):
        raise Exception("This method should be reimplementd in subclasses!")

    def extract_data_from_xoppy_output(self, calculation_output):
        spec_file_name = calculation_output

        sf = SpecFile(spec_file_name)

        if len(sf) == 1:
            #load spec file with one scan, # is comment
            print("Loading file:  ", spec_file_name)
            out = numpy.loadtxt(spec_file_name)
            if len(out) == 0 : raise Exception("Calculation gave no results (empty data)")

            #get labels
            # txt = open(spec_file_name).readlines()
            # tmp = [ line.find("#L") for line in txt]
            # itmp = numpy.where(numpy.array(tmp) != (-1))
            # labels = txt[int(itmp[0])].replace("#L ","").split("  ")
            # print("data labels: ", labels)

            calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())

            calculated_data.add_content("xoppy_specfile", spec_file_name)
            calculated_data.add_content("xoppy_data", out)

            return calculated_data
        else:
          raise Exception("File %s contains %d scans. Cannot send it as xoppy_table" % (spec_file_name, len(sf)))


    def get_data_exchange_widget_name(self):
        raise Exception("This method should be reimplementd in subclasses!")


    def add_specific_content_to_calculated_data(self, calculated_data):
        pass

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = XoppyWidget()
    ow.show()
    a.exec_()
    ow.saveSettings()

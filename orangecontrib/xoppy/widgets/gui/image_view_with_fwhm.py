# copied from oasys-wofry/orangecontrib/wofry/util/wofry_util.py
# TODO: centralize in OASYS?

import numpy, decimal
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QDialog, QVBoxLayout, QDialogButtonBox

from matplotlib.patches import FancyArrowPatch, ArrowStyle

from oasys.widgets import gui
from oasys.util.oasys_util import get_sigma, get_fwhm

from silx.gui.plot.ImageView import ImageView, PlotWindow

class InfoBoxWidget(QWidget):
    total_field = ""
    fwhm_h_field = ""
    fwhm_v_field = ""
    sigma_h_field = ""
    sigma_v_field = ""

    def __init__(self, x_scale_factor = 1.0, y_scale_factor = 1.0, is_2d=True):
        super(InfoBoxWidget, self).__init__()

        info_box_inner= gui.widgetBox(self, "Info")
        info_box_inner.setFixedHeight(515*y_scale_factor)
        info_box_inner.setFixedWidth(230*x_scale_factor)

        self.total = gui.lineEdit(info_box_inner, self, "total_field", "Total", tooltip="Total", labelWidth=115, valueType=str, orientation="horizontal")

        label_box_1 = gui.widgetBox(info_box_inner, "", addSpace=False, orientation="horizontal")

        self.label_h = QLabel("FWHM ")
        self.label_h.setFixedWidth(115)
        palette =  QPalette(self.label_h.palette())
        palette.setColor(QPalette.Foreground, QColor('blue'))
        self.label_h.setPalette(palette)
        label_box_1.layout().addWidget(self.label_h)
        self.fwhm_h = gui.lineEdit(label_box_1, self, "fwhm_h_field", "", tooltip="FWHM", labelWidth=115, valueType=str, orientation="horizontal")

        if is_2d:
            label_box_2 = gui.widgetBox(info_box_inner, "", addSpace=False, orientation="horizontal")

            self.label_v = QLabel("FWHM ")
            self.label_v.setFixedWidth(115)
            palette =  QPalette(self.label_h.palette())
            palette.setColor(QPalette.Foreground, QColor('red'))
            self.label_v.setPalette(palette)
            label_box_2.layout().addWidget(self.label_v)
            self.fwhm_v = gui.lineEdit(label_box_2, self, "fwhm_v_field", "", tooltip="FWHM", labelWidth=115, valueType=str, orientation="horizontal")

        label_box_1 = gui.widgetBox(info_box_inner, "", addSpace=False, orientation="horizontal")

        self.label_s_h = QLabel("\u03c3 ")
        self.label_s_h.setFixedWidth(115)
        palette =  QPalette(self.label_s_h.palette())
        palette.setColor(QPalette.Foreground, QColor('blue'))
        self.label_s_h.setPalette(palette)
        label_box_1.layout().addWidget(self.label_s_h)
        self.sigma_h = gui.lineEdit(label_box_1, self, "sigma_h_field", "", tooltip="Sigma", labelWidth=115, valueType=str, orientation="horizontal")

        if is_2d:
            label_box_2 = gui.widgetBox(info_box_inner, "", addSpace=False, orientation="horizontal")

            self.label_s_v = QLabel("\u03c3 ")
            self.label_s_v.setFixedWidth(115)
            palette =  QPalette(self.label_s_v.palette())
            palette.setColor(QPalette.Foreground, QColor('red'))
            self.label_s_v.setPalette(palette)
            label_box_2.layout().addWidget(self.label_s_v)
            self.sigma_v = gui.lineEdit(label_box_2, self, "sigma_v_field", "", tooltip="Sigma", labelWidth=115, valueType=str, orientation="horizontal")

        self.total.setReadOnly(True)
        font = QFont(self.total.font())
        font.setBold(True)
        self.total.setFont(font)
        palette = QPalette(self.total.palette())
        palette.setColor(QPalette.Text, QColor('dark blue'))
        palette.setColor(QPalette.Base, QColor(243, 240, 160))
        self.total.setPalette(palette)

        self.fwhm_h.setReadOnly(True)
        font = QFont(self.fwhm_h.font())
        font.setBold(True)
        self.fwhm_h.setFont(font)
        palette = QPalette(self.fwhm_h.palette())
        palette.setColor(QPalette.Text, QColor('dark blue'))
        palette.setColor(QPalette.Base, QColor(243, 240, 160))
        self.fwhm_h.setPalette(palette)

        self.sigma_h.setReadOnly(True)
        font = QFont(self.sigma_h.font())
        font.setBold(True)
        self.sigma_h.setFont(font)
        palette = QPalette(self.sigma_h.palette())
        palette.setColor(QPalette.Text, QColor('dark blue'))
        palette.setColor(QPalette.Base, QColor(243, 240, 160))
        self.sigma_h.setPalette(palette)

        if is_2d:
            self.fwhm_v.setReadOnly(True)
            font = QFont(self.fwhm_v.font())
            font.setBold(True)
            self.fwhm_v.setFont(font)
            palette = QPalette(self.fwhm_v.palette())
            palette.setColor(QPalette.Text, QColor('dark blue'))
            palette.setColor(QPalette.Base, QColor(243, 240, 160))
            self.fwhm_v.setPalette(palette)

            self.sigma_v.setReadOnly(True)
            font = QFont(self.sigma_v.font())
            font.setBold(True)
            self.sigma_v.setFont(font)
            palette = QPalette(self.sigma_v.palette())
            palette.setColor(QPalette.Text, QColor('dark blue'))
            palette.setColor(QPalette.Base, QColor(243, 240, 160))
            self.sigma_v.setPalette(palette)


    def clear(self):
        self.total.setText("0.0")
        self.fwhm_h.setText("0.0000")
        if hasattr(self, "fwhm_v"):  self.fwhm_v.setText("0.0000")
        self.sigma_h.setText("0.0000")
        if hasattr(self, "sigma_v"):  self.sigma_v.setText("0.0000")

class ImageViewWithFWHM(QWidget):
    def __init__(self, x_scale_factor = 1.0, y_scale_factor = 1.0):
        super(ImageViewWithFWHM, self).__init__()

        self.plot_canvas = ImageView(parent=self)
        self.set_plot_canvas_default_settings()

        self.info_box = InfoBoxWidget(x_scale_factor, y_scale_factor)

        layout = QGridLayout()

        layout.addWidget(self.info_box, 0, 1, 1, 1)
        layout.addWidget(self.plot_canvas, 0, 0, 1, 1)

        layout.setColumnMinimumWidth(0, 600*x_scale_factor)
        layout.setColumnMinimumWidth(1, 230*x_scale_factor)

        self.setLayout(layout)

    def get_ImageView(self):
        return self.plot_canvas

    def get_InfoBoxWidhet(self):
        return self.info_box

    def set_plot_canvas_default_settings(self):
        self.get_ImageView().resetZoom()
        self.get_ImageView().setXAxisAutoScale(True)
        self.get_ImageView().setYAxisAutoScale(True)
        self.get_ImageView().setGraphGrid(False)
        self.get_ImageView().setKeepDataAspectRatio(True)
        self.get_ImageView().yAxisInvertedAction.setVisible(False)
        self.get_ImageView().setXAxisLogarithmic(False)
        self.get_ImageView().setYAxisLogarithmic(False)
        self.get_ImageView().getMaskAction().setVisible(False)
        self.get_ImageView().getRoiAction().setVisible(False)
        self.get_ImageView().getColormapAction().setVisible(True)
        self.get_ImageView().setKeepDataAspectRatio(False)

    def plot_2D(self, histogram,xx=None,yy=None,
                title="", xtitle="", ytitle="", xum="[mm]", yum="[mm]",
                plotting_range=None,factor1=1.0,factor2=1.0,colormap=None):

        if xx is None:
            xx = numpy.arange(histogram.shape[0])

        if yy is None:
            yy = numpy.arange(histogram.shape[1])

        if plotting_range == None:
            nbins_h = xx.size
            nbins_v = yy.size
        else:
            range_x  = numpy.where(numpy.logical_and(xx>=plotting_range[0], xx<=plotting_range[1]))
            range_y  = numpy.where(numpy.logical_and(yy>=plotting_range[2], yy<=plotting_range[3]))

            xx = xx[range_x]
            yy = yy[range_y]

            nbins_h = xx.size
            nbins_v = yy.size

        if len(xx) == 0 or len(yy) == 0:
            raise Exception("Nothing to plot in the given range")

        xmin, xmax = xx.min(), xx.max()
        ymin, ymax = yy.min(), yy.max()

        origin = (xmin*factor1, ymin*factor2)
        scale = (abs((xmax-xmin)/nbins_h)*factor1, abs((ymax-ymin)/nbins_v)*factor2)

        # silx inverts axis!!!! histogram must be calculated reversed
        data_to_plot = []
        for y_index in range(0, nbins_v):
            x_values = []
            for x_index in range(0, nbins_h):
                x_values.append(histogram[x_index][y_index])

            data_to_plot.append(x_values)

        data_to_plot = numpy.array(data_to_plot)

        histogram_h = numpy.sum(data_to_plot, axis=0) # data to plot axis are inverted
        histogram_v = numpy.sum(data_to_plot, axis=1)

        ticket = {}
        ticket['total'] = numpy.sum(data_to_plot)

        ticket['fwhm_h'], ticket['fwhm_quote_h'], ticket['fwhm_coordinates_h'] = get_fwhm(histogram_h, xx)
        ticket['sigma_h'] = get_sigma(histogram_h, xx)

        ticket['fwhm_v'], ticket['fwhm_quote_v'], ticket['fwhm_coordinates_v'] = get_fwhm(histogram_v, yy)
        ticket['sigma_v'] = get_sigma(histogram_v, yy)

        self.plot_canvas.setColormap(colormap=colormap)
        self.plot_canvas.setImage(data_to_plot, origin=origin, scale=scale)


        self.plot_canvas.setGraphXLabel(xtitle)
        self.plot_canvas.setGraphYLabel(ytitle)
        self.plot_canvas.setGraphTitle(title)

        self.plot_canvas._histoHPlot.setGraphYLabel('Counts')

        self.plot_canvas._histoHPlot._backend.ax.xaxis.get_label().set_color('white')
        self.plot_canvas._histoHPlot._backend.ax.xaxis.get_label().set_fontsize(1)
        for label in self.plot_canvas._histoHPlot._backend.ax.xaxis.get_ticklabels():
            label.set_color('white')
            label.set_fontsize(1)

        self.plot_canvas._histoVPlot.setGraphXLabel('Counts')

        self.plot_canvas._histoVPlot._backend.ax.yaxis.get_label().set_color('white')
        self.plot_canvas._histoVPlot._backend.ax.yaxis.get_label().set_fontsize(1)
        for label in self.plot_canvas._histoVPlot._backend.ax.yaxis.get_ticklabels():
            label.set_color('white')
            label.set_fontsize(1)

        n_patches = len(self.plot_canvas._histoHPlot._backend.ax.patches)
        if (n_patches > 0): self.plot_canvas._histoHPlot._backend.ax.patches.remove(self.plot_canvas._histoHPlot._backend.ax.patches[n_patches-1])

        if not ticket['fwhm_h'] == 0.0:
            x_fwhm_i, x_fwhm_f = ticket['fwhm_coordinates_h']
            x_fwhm_i, x_fwhm_f = x_fwhm_i*factor1, x_fwhm_f*factor1
            y_fwhm = ticket['fwhm_quote_h']

            self.plot_canvas._histoHPlot._backend.ax.add_patch(FancyArrowPatch([x_fwhm_i, y_fwhm],
                                                                 [x_fwhm_f, y_fwhm],
                                                                 arrowstyle=ArrowStyle.CurveAB(head_width=2, head_length=4),
                                                                 color='b',
                                                                 linewidth=1.5))

        n_patches = len(self.plot_canvas._histoVPlot._backend.ax.patches)
        if (n_patches > 0): self.plot_canvas._histoVPlot._backend.ax.patches.remove(self.plot_canvas._histoVPlot._backend.ax.patches[n_patches-1])

        if not ticket['fwhm_v'] == 0.0:
            y_fwhm_i, y_fwhm_f = ticket['fwhm_coordinates_v']
            y_fwhm_i, y_fwhm_f = y_fwhm_i*factor2, y_fwhm_f*factor2
            x_fwhm = ticket['fwhm_quote_v']

            self.plot_canvas._histoVPlot._backend.ax.add_patch(FancyArrowPatch([x_fwhm, y_fwhm_i],
                                                                 [x_fwhm, y_fwhm_f],
                                                                 arrowstyle=ArrowStyle.CurveAB(head_width=2, head_length=4),
                                                                 color='r',
                                                                 linewidth=1.5))

        self.plot_canvas._histoHPlot.replot()
        self.plot_canvas._histoVPlot.replot()
        self.plot_canvas.replot()

        self.info_box.total.setText("{:.3e}".format(decimal.Decimal(ticket['total'])))
        self.info_box.fwhm_h.setText("{:5.4f}".format(ticket['fwhm_h'] * factor1))
        self.info_box.fwhm_v.setText("{:5.4f}".format(ticket['fwhm_v'] * factor2))
        self.info_box.label_h.setText("FWHM " + xum)
        self.info_box.label_v.setText("FWHM " + yum)
        self.info_box.sigma_h.setText("{:5.4f}".format(ticket['sigma_h']*factor1))
        self.info_box.sigma_v.setText("{:5.4f}".format(ticket['sigma_v']*factor2))
        self.info_box.label_s_h.setText("\u03c3 " + xum)
        self.info_box.label_s_v.setText("\u03c3 " + yum)


    def clear(self):
        self.plot_canvas.clear()

        self.plot_canvas._histoHPlot.clear()
        self.plot_canvas._histoVPlot.clear()

        self.plot_canvas._histoHPlot._backend.ax.xaxis.get_label().set_color('white')
        self.plot_canvas._histoHPlot._backend.ax.xaxis.get_label().set_fontsize(1)
        for label in self.plot_canvas._histoHPlot._backend.ax.xaxis.get_ticklabels():
            label.set_color('white')
            label.set_fontsize(1)

        self.plot_canvas._histoVPlot._backend.ax.yaxis.get_label().set_color('white')
        self.plot_canvas._histoVPlot._backend.ax.yaxis.get_label().set_fontsize(1)
        for label in self.plot_canvas._histoVPlot._backend.ax.yaxis.get_ticklabels():
            label.set_color('white')
            label.set_fontsize(1)

        self.plot_canvas._histoHPlot.setGraphYLabel('')
        self.plot_canvas._histoVPlot.setGraphXLabel('')

        self.plot_canvas._histoHPlot.replot()
        self.plot_canvas._histoVPlot.replot()

        self.info_box.clear()

if __name__=="__main__":


    from wofry.propagator.wavefront2D.generic_wavefront import GenericWavefront2D
    w =  GenericWavefront2D.initialize_wavefront_from_range(-0.002,0.002,-0.001,0.001,(200,200))
    w.set_gaussian(0.00055,0.0002)


    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    widget = QWidget()

    layout = QVBoxLayout()

    oo = ImageViewWithFWHM()
    oo.plot_2D(w.get_intensity(),w.get_coordinate_x(),w.get_coordinate_y(),factor1=1e6,factor2=1e6,
               title="Gaussian wavefront",xtitle="X / um", ytitle="Y / um",
               colormap={"name":"temperature", "normalization":"linear", "autoscale":True, "vmin":0, "vmax":0, "colors":256})

    layout.addWidget(oo)

    widget.setLayout(layout)

    widget.show()

    # oo.clear()

    app.exec_()

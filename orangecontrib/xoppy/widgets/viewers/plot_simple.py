from PyQt4 import QtGui
from PyQt4.QtGui import QDoubleValidator
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import numpy as np
import Orange
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyMca5.PyMcaIO import specfilewrapper as specfile


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
                "handler": "do_plot" },
              {"name": "xoppy_specfile",
                "type": str,
                "doc": "",
                "handler": "do_plot_spec" } ]


    def __init__(self):
        super().__init__()
        self.figure_canvas = None

    def do_plot(self,xoppy_data):
        x = xoppy_data[:, 0]
        y = xoppy_data[:, -1]
        x.shape = -1
        y.shape = -1
        fig = plt.figure()
        plt.plot(x,y,linewidth=1.0, figure=fig)
        plt.grid(True)
        if self.figure_canvas is not None:
            self.mainArea.layout().removeWidget(self.figure_canvas)
        self.figure_canvas = FigureCanvas(fig) #plt.figure())
        self.mainArea.layout().addWidget(self.figure_canvas)
        
    def do_plot_spec(self,file):


        sf = specfile.Specfile(file)
        sf_n = sf.scanno()
        print("plot_simple: SPEC file: %s.\n"%(file))
        print("plot_simple: Number of scans found %d\n"%(sf_n))
        s1 = sf[-1]
        tmp = s1.fileheader("UXOPPY_PLOT_SELECT_SCAN_INDEX")
        if len(tmp) > 0:
            idx = int( tmp[0].strip(" ")[-1] )
            print("plot_simple: Selected scan index: %d"%(idx))
            s1 = sf[idx]

        print("plot_simple: Columns found: " ,s1.alllabels())
        tmp = s1.header("UXOPPY_PLOT_H_COLUMN_INDEX")
        if len(tmp) == 1:
            idx = int( tmp[-1].strip(" ")[-1] )
            print("plot_simple: Selected H column index: %d"%(idx))
            hcol = [idx]
        elif len(tmp) == 2:
            idx1 = int( tmp[0].strip(" ")[-1] )
            idx2 = int( tmp[1].strip(" ")[-1] )
            print("plot_simple: Selected H column indices: %d,%d "%(idx1,idx2))
            hcol = [idx1,idx2]
        else:
            hcol = [0]

        tmp = s1.header("UXOPPY_PLOT_V_COLUMN_INDEX")
        if len(tmp) > 0:
            idx = int( tmp[-1].strip(" ")[-1] )
            print("plot_simple: Selected V column index: %d"%(idx))
            vcol = idx

        else:
            vcol = -1


        out =  s1.data().T
        labels = s1.alllabels()
        print("plot_simple: Shape(data): ",out.shape)
        title = s1.command()

        fig = plt.figure()

        plt.grid(True)


        plt.title(title)


        if len(hcol) == 1:
            x = out[:, hcol]
            y = out[:, vcol]
            # x.shape = -1
            # y.shape = -1
            plt.ylabel(labels[vcol])
            plt.xlabel(labels[hcol[0]])
            plt.plot(x,y,linewidth=1.0, figure=fig)
        else:
            pre_x1 = out[:, hcol[0]]
            pre_x2 = out[:, hcol[1]]
            pre_y = out[:, vcol]

            x1 = np.unique(pre_x1)
            x2 = np.unique(pre_x2)
            nx1 = len(x1)
            nx2 = len(x2)
            if (nx1*nx2 != len(pre_y)):
                raise RuntimeError("Posible error in arrays: n1=%d, n2=%d, npoints=%d!=n1*n2."%(nx1,nx2,len(pre_y)))

            y = np.zeros( (nx1,nx2) )
            ij = 0
            for i in range(nx1):
                for j in range(nx2):
                    x1[i] = pre_x1[ij]
                    x2[j] = pre_x2[ij]
                    y[i,j] = pre_y[ij]
                    ij += 1
            print("plot_simple: len x1,x2",len(x1),len(x2),len(x1)*len(x2))
            print("plot_simple: shape x1,x2,y",x1.shape,x2.shape,y.shape)
            plt4 = plt.contour(x1,x2,y.T,levels=np.linspace(0,y.max(),100))
            cbar = plt.colorbar(plt4 , format="%.2f")
            cbar.ax.set_ylabel(labels[vcol])
            plt.ylabel(labels[hcol[1]])
            plt.xlabel(labels[hcol[0]])


        if self.figure_canvas is not None:
            self.mainArea.layout().removeWidget(self.figure_canvas)
        self.figure_canvas = FigureCanvas(fig) #plt.figure())
        self.mainArea.layout().addWidget(self.figure_canvas)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ow = OWPlotSimple()
    # a = np.array([
    #     [  8.47091837e+04,   1.16210756e+12],
    #     [  8.57285714e+04,   1.10833975e+12],
    #     [  8.67479592e+04,   1.05700892e+12],
    #     [  8.77673469e+04,   1.00800805e+12] ])
    # ow.do_plot(a)

    fileName = "/users/srio/Oasys/OasysRun/undulator_power_density.spec"
    #fileName = "/users/srio/Oasys/OasysRun/undulator_flux.spec"
    ow.do_plot_spec(fileName)

    ow.show()
    app.exec_()
    ow.saveSettings()

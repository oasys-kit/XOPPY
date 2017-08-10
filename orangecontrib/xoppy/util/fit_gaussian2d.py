__author__ = 'srio'
# https://stackoverflow.com/questions/21566379/fitting-a-2d-gaussian-function-using-scipy-optimize-curve-fit-valueerror-and-m

import numpy as np
from srxraylib.plot.gol import plot_image
import scipy.optimize as opt

def fit_gaussian2d(data,x0,y0,p0=None):
    if p0 is None:
        p0 = moments(data.reshape(x0.size,y0.size),x0,y0)
    x, y = np.meshgrid(x0, y0)
    data1 = data.ravel()
    popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), data1, p0=p0)

    # print("initial guess: ",p0)
    # print("data fitted: ",popt)

    return popt


def twoD_Gaussian(xy, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x,y = xy
    xo = float(xo)
    yo = float(yo)    
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)))
    return g.T.ravel()

def moments(data,x0=None,y0=None):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = np.sqrt(abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(abs((np.arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    if x0 is None:
        return height, x, y, width_x, width_y, 0.0, 0.0
    else:
        xstep = x0[1] - x0[0]
        ystep = y0[1] - y0[0]
        return height, x*xstep+x0[0], y*ystep+y0[0], width_x*xstep, width_y*ystep, 0.0, 0.0


def info_params(mZ):
    txt = "\nFit 2D Gaussian function:\n\n"
    if abs(mZ[5] < 1e-3):
        txt += "  offset + A * exp( - (1/2)*((x-x0)/sigmax)**2 - (1/2)*((y-y0)/sigmay)**2 )\n"
        txt += "    Height A: %f\n"%mZ[0]
        txt += "    center x0:      %f\n"%mZ[1]
        txt += "    center y0:      %f\n"%mZ[2]
        txt += "    sigmax: %f\n"%mZ[3]
        txt += "    sigmay: %f\n"%mZ[4]
        txt += "    offset: %f\n"%mZ[6]
    else:
        txt += "  offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))\n"
        txt += "  with: \n"
        txt += "    a = (cos(theta)**2)/(2*sigma_x**2) + (sin(theta)**2)/(2*sigma_y**2)\n"
        txt += "    b = -(sin(2*theta))/(4*sigma_x**2) + (sin(2*theta))/(4*sigma_y**2)\n"
        txt += "    c = (sin(theta)**2)/(2*sigma_x**2) + (cos(theta)**2)/(2*sigma_y**2)\n\n"

        txt += "    Height A: %f\n"%mZ[0]
        txt += "    center x0:      %f\n"%mZ[1]
        txt += "    center y0:      %f\n"%mZ[2]
        txt += "    sigmax: %f\n"%mZ[3]
        txt += "    sigmay: %f\n"%mZ[4]
        txt += "    angle:  %f rad\n"%mZ[5]
        txt += "    offset: %f\n"%mZ[6]

    return txt

if __name__ == "__main__":
    nx = 200
    ny = 300
    x0 = np.linspace(-20,20,nx)
    y0 = np.linspace(-10,10,ny)
    x, y = np.meshgrid(x0, y0)
    data = twoD_Gaussian((x, y), 100, 0, 0, 10, 5, 0, 0)

    plot_image(data.reshape((nx,ny)),x0,y0,title="DATA")


    popt = fit_gaussian2d(data,x0,y0,p0=None)

    data_fitted = twoD_Gaussian((x, y), *popt)
        
    print(info_params(popt))

    plot_image(data_fitted.reshape((nx,ny)),x0,y0,title="FIT")



    






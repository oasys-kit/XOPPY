#
# tools for power3d app
#

import numpy
import scipy.constants as codata
import h5py
import xraylib
from orangecontrib.xoppy.util.xoppy_xraylib_util import reflectivity_fresnel
from orangecontrib.xoppy.util.xoppy_xraylib_util import nist_compound_list, density
from scipy.interpolate import interp2d, RectBivariateSpline
from srxraylib.util.h5_simple_writer import H5SimpleWriter

#
# calculation
#
def integral_2d(data2D,h=None,v=None, method=0):
    if h is None:
        h = numpy.arange(data2D.shape[0])
    if v is None:
        v = numpy.arange(data2D.shape[1])

    if method == 0:
        totPower2 = numpy.trapz(data2D, v, axis=1)
        totPower2 = numpy.trapz(totPower2, h, axis=0)
    else:
        totPower2 = data2D.sum() * (h[1] - h[0]) * (v[1] - v[0])

    return totPower2


def integral_3d(data3D, e=None, h=None, v=None, method=0):
    if e is None:
        e = numpy.arange(data3D.shape[0])
    if h is None:
        h = numpy.arange(data3D.shape[1])
    if v is None:
        v = numpy.arange(data3D.shape[2])

    if method == 0:

        totPower2 = numpy.trapz(data3D, v, axis=2)
        totPower2 = numpy.trapz(totPower2, h, axis=1)
        totPower2 = numpy.trapz(totPower2, e, axis=0)
    else:
        totPower2 = data3D.sum() * (e[1] - e[0]) * (h[1] - h[0]) * (v[1] - v[0])

    return totPower2


def calculate_component_absorbance_and_transmittance(
    # p0,
    e0, h0, v0, # todo: p0 not used
    substance="Si",
    thick=0.5,
    angle=3.5,
    defection=1, # deflection 0=H 1=V
    dens="?",
    roughness=0.0,
    flags=0,  # 0=Filter 1=Mirror 2 = Aperture 3 magnifier
    hgap=1000.0,
    vgap=1000.0,
    hgapcenter=0.0,
    vgapcenter=0.0,
    hmag=1.0,
    vmag=1.0,
    hrot=0.0,
    vrot=0.0,):

    #
    # important: the transmittance calculated here is referred on axes perp to the beam
    # therefore they do not include geometrical corrections for correct integral
    #

    e = e0.copy()
    h = h0.copy()
    v = v0.copy()

    transmittance = numpy.ones((e.size,h.size,v.size))
    E = e.copy()
    H = h.copy()
    V = v.copy()

    # initialize results

    #
    # get undefined densities
    #
    if flags <= 1:
        try:  # apply written value
            rho = float(dens)
        except:  # in case of ?
            rho = density(substance)
            print("Density for %s: %g g/cm3" % (substance, rho))
        dens = rho

    txt = ""

    if flags == 0:
        txt += '      *****   oe  [Filter] *************\n'
        txt += '      Material: %s\n' % (substance)
        txt += '      Density [g/cm^3]: %f \n' % (dens)
        txt += '      thickness [mm] : %f \n' % (thick)
        txt += '      H gap [mm]: %f \n' % (hgap)
        txt += '      V gap [mm]: %f \n' % (vgap)
        txt += '      H gap center [mm]: %f \n' % (hgapcenter)
        txt += '      V gap center [mm]: %f \n' % (vgapcenter)
        txt += '      H rotation angle [deg]: %f \n' % (hrot)
        txt += '      V rotation angle [deg]: %f \n' % (vrot)
    elif flags == 1:
        txt += '      *****   oe  [Mirror] *************\n'
        txt += '      Material: %s\n' % (substance)
        txt += '      Density [g/cm^3]: %f \n' % (dens)
        txt += '      grazing angle [mrad]: %f \n' % (angle)
        txt += '      roughness [A]: %f \n' % (roughness)
    elif flags == 2:
        txt += '      *****   oe  [Aperture] *************\n'
        txt += '      H gap [mm]: %f \n' % (hgap)
        txt += '      V gap [mm]: %f \n' % (vgap)
        txt += '      H gap center [mm]: %f \n' % (hgapcenter)
        txt += '      V gap center [mm]: %f \n' % (vgapcenter)
    elif flags == 3:
        txt += '      *****   oe  [Magnifier] *************\n'
        txt += '      H magnification: %f \n' % (hmag)
        txt += '      V magnification: %f \n' % (vmag)
    elif flags == 4:
        txt += '      *****   oe  [Screen rotated] *************\n'
        txt += '      H rotation angle [deg]: %f \n' % (hrot)
        txt += '      V rotation angle [deg]: %f \n' % (vrot)

    if flags == 0:  # filter
        for j, energy in enumerate(e):
            tmp = xraylib.CS_Total_CP(substance, energy / 1000.0)
            transmittance[j, :, :] = numpy.exp(-tmp * dens * (thick / 10.0))

        # rotation
        H = h / numpy.cos(hrot * numpy.pi / 180)
        V = v / numpy.cos(vrot * numpy.pi / 180)

        # aperture
        h_indices_bad = numpy.where(numpy.abs(H - hgapcenter) > (0.5 * hgap))
        if len(h_indices_bad) > 0:
            transmittance[:, h_indices_bad, :] = 0.0
        v_indices_bad = numpy.where(numpy.abs(V - vgapcenter) > (0.5 * vgap))
        if len(v_indices_bad) > 0:
            transmittance[:, :, v_indices_bad] = 0.0

        absorbance = 1.0 - transmittance

    elif flags == 1:  # mirror
        tmp = numpy.zeros(e.size)

        for j, energy in enumerate(e):
            tmp[j] = xraylib.Refractive_Index_Re(substance, energy / 1000.0, dens)

        if tmp[0] == 0.0:
            raise Exception("Probably the substrance %s is wrong" % substance)

        delta = 1.0 - tmp
        beta = numpy.zeros(e.size)

        for j, energy in enumerate(e):
            beta[j] = xraylib.Refractive_Index_Im(substance, energy / 1000.0, dens)

        try:
            (rs, rp, runp) = reflectivity_fresnel(refraction_index_beta=beta, refraction_index_delta=delta, \
                                                  grazing_angle_mrad=angle, roughness_rms_A=roughness, \
                                                  photon_energy_ev=e)
        except:
            raise Exception("Failed to run reflectivity_fresnel")

        for j, energy in enumerate(e):
            transmittance[j, :, :] = rs[j]

        # rotation
        if defection == 0:  # horizontally deflecting
            H = h / numpy.sin(angle * 1e-3)
        elif defection == 1:  # vertically deflecting
            V = v / numpy.sin(angle * 1e-3)

        # size
        absorbance = 1.0 - transmittance

        h_indices_bad = numpy.where(numpy.abs(H - hgapcenter) > (0.5 * hgap))
        if len(h_indices_bad) > 0:
            transmittance[:, h_indices_bad, :] = 0.0
            absorbance[:, h_indices_bad, :] = 0.0
        v_indices_bad = numpy.where(numpy.abs(V - vgapcenter) > (0.5 * vgap))
        if len(v_indices_bad) > 0:
            transmittance[:, :, v_indices_bad] = 0.0
            absorbance[:, :, v_indices_bad] = 0.0

    elif flags == 2:  # aperture
        h_indices_bad = numpy.where(numpy.abs(H - hgapcenter) > (0.5 * hgap))
        if len(h_indices_bad) > 0:
            transmittance[:, h_indices_bad, :] = 0.0
        v_indices_bad = numpy.where(numpy.abs(V - vgapcenter) > (0.5 * vgap))
        if len(v_indices_bad) > 0:
            transmittance[:, :, v_indices_bad] = 0.0

        absorbance = 1.0 - transmittance

    elif flags == 3:  # magnifier
        H = h * hmag
        V = v * vmag

        absorbance = 1.0 - transmittance

    elif flags == 4:  # rotation screen
        H = h / numpy.cos(hrot * numpy.pi / 180)
        V = v / numpy.cos(vrot * numpy.pi / 180)

        absorbance = 1.0 - transmittance

    return transmittance, absorbance, E, H, V, txt

def apply_transmittance_to_incident_beam(transmittance,p0,e0,h0,v0,
    flags=0,
    hgap=1000.0,
    vgap=1000.0,
    hgapcenter=0.0,
    vgapcenter=0.0,
    hmag=1.0,
    vmag=1.0,
    interpolation_flag=0,
    interpolation_factor_h=1.0,
    interpolation_factor_v=1.0,
    slit_crop=0,
    ):

    p = p0.copy()
    e = e0.copy()
    h = h0.copy()
    v = v0.copy()

    # coordinates to send: the same as incident beam (perpendicular to the optical axis)
    # except for the magnifier
    if flags == 3:  # magnifier  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        h *= hmag
        v *= vmag

    p_transmitted = p * transmittance / (h[0] / h0[0]) / (v[0] / v0[0])

    if (slit_crop == 1 and flags == 2):
        print("Cropping to %g mm x %g mm" % (hgap,vgap))
        h_d = numpy.where(numpy.abs(h - hgapcenter) <= (0.5 * hgap))[0]
        v_d = numpy.where(numpy.abs(v - vgapcenter) <= (0.5 * vgap))[0]

        p_transmitted = p_transmitted[:, h_d[0]:(h_d[-1]), v_d[0]:v_d[-1]].copy()
        e = e
        h = h[h_d[0]:h_d[-1]].copy()
        v = v[v_d[0]:v_d[-1]].copy()

    if interpolation_flag == 1:

        h_old = h
        v_old = v
        p_transmitted_old = p_transmitted

        nh = int(h_old.size * interpolation_factor_h)
        nv = int(v_old.size * interpolation_factor_v)
        p_transmitted = numpy.zeros((e.size, nh, nv))

        print("Interpolating from ",p_transmitted_old.shape, " to ", p_transmitted.shape)
        h = numpy.linspace(h_old[0], h_old[-1], nh)
        v = numpy.linspace(v_old[0], v_old[-1], nv)



        for i in range(e.size):
            f = RectBivariateSpline(h_old,
                                    v_old,
                                    p_transmitted_old[i, :, :])
            p_transmitted_i = f(h, v)
            p_transmitted[i, :, :] = p_transmitted_i

    return p_transmitted, e, h, v


#
# file io
#
def load_radiation_from_h5file(file_h5, subtitle="XOPPY_RADIATION"):

    hf = h5py.File(file_h5, 'r')

    if not subtitle in hf:
        raise Exception("XOPPY_RADIATION not found in h5 file %s"%file_h5)

    try:
        p = hf[subtitle + "/Radiation/stack_data"][:]
        e = hf[subtitle + "/Radiation/axis0"][:]
        h = hf[subtitle + "/Radiation/axis1"][:]
        v = hf[subtitle + "/Radiation/axis2"][:]
    except:
        raise Exception("Error reading h5 file %s \n"%file_h5 + "\n" + str(e))

    code = "unknown"

    try:
        if hf[subtitle + "/parameters/METHOD"].value == 0:
            code = 'US'
        elif hf[subtitle + "/parameters/METHOD"].value == 1:
            code = 'URGENT'
        elif hf[subtitle + "/parameters/METHOD"].value == 2:
            code = 'SRW'
        elif hf[subtitle + "/parameters/METHOD"].value == 3:
            code = 'pySRU'
    except:
        pass

    hf.close()

    return e, h, v, p, code


def write_radiation_to_h5file(e,h,v,p,
                       creator="xoppy",
                       h5_file="wiggler_radiation.h5",
                       h5_entry_name="XOPPY_RADIATION",
                       h5_initialize=True,
                       h5_parameters=None,
                       ):

    if h5_initialize:
        h5w = H5SimpleWriter.initialize_file(h5_file,creator=creator)
    else:
        h5w = H5SimpleWriter(h5_file,None)
    h5w.create_entry(h5_entry_name,nx_default=None)
    h5w.add_stack(e,h,v,p,stack_name="Radiation",entry_name=h5_entry_name,
        title_0="Photon energy [eV]",
        title_1="X gap [mm]",
        title_2="Y gap [mm]")
    h5w.create_entry("parameters",root_entry=h5_entry_name,nx_default=None)
    if h5_parameters is not None:
        for key in h5_parameters.keys():
            h5w.add_key(key,h5_parameters[key], entry_name=h5_entry_name+"/parameters")
    print("File written to disk: %s"%h5_file)


def write_txt_file(calculated_data, input_beam_content, filename="tmp.txt", method="3columns"):

    p0, e0, h0, v0 = input_beam_content # .get_content("xoppy_data")
    transmittance, absorbance, E, H, V = calculated_data

    #
    #
    #
    p = p0.copy()
    p_spectral_power = p * codata.e * 1e3

    absorbed3d = p_spectral_power * absorbance / (H[0] / h0[0]) / (V[0] / v0[0])
    absorbed2d = numpy.trapz(absorbed3d, E, axis=0)

    f = open(filename, 'w')
    if method == "3columns":
        for i in range(H.size):
            for j in range(V.size):
                f.write("%g  %g  %g\n" % (H[i]*1e-3, V[i]*1e-3, absorbed2d[i,j]*1e6))
    elif method == "matrix":
        f.write("%10.5g" % 0)
        for i in range(H.size):
            f.write(", %10.5g" % (H[i] * 1e-3))
        f.write("\n")

        for j in range(V.size):
                f.write("%10.5g" % (V[j] * 1e-3))
                for i in range(H.size):
                    f.write(", %10.5g" % (absorbed2d[i,j] * 1e6))
                f.write("\n")
    else:
        raise Exception("File type not understood.")
    f.close()

    print("File written to disk: %s" % filename)


def write_h5_file(calculated_data, input_beam_content, filename="tmp.txt",EL1_FLAG=1,EL1_HMAG=1.0,EL1_VMAG=1.0):

    p0, e0, h0, v0 = input_beam_content #.get_content("xoppy_data")
    transmittance, absorbance, E, H, V = calculated_data

    #
    #
    #
    p = p0.copy()
    e = e0.copy()
    h = h0.copy()
    v = v0.copy()
    p_spectral_power = p * codata.e * 1e3

    try:
        h5w = H5SimpleWriter.initialize_file(filename, creator="power3Dcomponent.py")
        txt = "\n\n\n"
        txt += info_total_power(p, e, v, h, transmittance, absorbance, EL1_FLAG=EL1_FLAG)
        h5w.add_key("info", txt, entry_name=None)
    except:
        print("ERROR writing h5 file (info)")


    try:
        #
        # source
        #
        entry_name = "source"

        h5w.create_entry(entry_name, nx_default=None)

        h5w.add_stack(e, h, v, p, stack_name="Radiation stack", entry_name=entry_name,
                      title_0="Photon energy [eV]",
                      title_1="X [mm] (normal to beam)",
                      title_2="Y [mm] (normal to beam)")

        h5w.add_image(numpy.trapz(p_spectral_power, E, axis=0) , H, V,
                      image_name="Power Density", entry_name=entry_name,
                      title_x="X [mm] (normal to beam)",
                      title_y="Y [mm] (normal to beam)")

        h5w.add_dataset(E, numpy.trapz(numpy.trapz(p_spectral_power, v, axis=2), h, axis=1),
                        entry_name=entry_name, dataset_name="Spectral power",
                        title_x="Photon Energy [eV]",
                        title_y="Spectral density [W/eV]")

    except:
        print("ERROR writing h5 file (source)")

    try:
        #
        # optical element
        #
        entry_name = "optical_element"

        h5w.create_entry(entry_name, nx_default=None)

        h5w.add_stack(E, H, V, transmittance, stack_name="Transmittance stack", entry_name=entry_name,
                      title_0="Photon energy [eV]",
                      title_1="X [mm] (o.e. coordinates)",
                      title_2="Y [mm] (o.e. coordinates)")

        absorbed = p_spectral_power * absorbance / (H[0] / h0[0]) / (V[0] / v0[0])
        h5w.add_image(numpy.trapz(absorbed, E, axis=0), H, V,
                      image_name="Absorbed Power Density on Element", entry_name=entry_name,
                      title_x="X [mm] (o.e. coordinates)",
                      title_y="Y [mm] (o.e. coordinates)")

        h5w.add_dataset(E, numpy.trapz(numpy.trapz(absorbed, v, axis=2), h, axis=1),
                        entry_name=entry_name, dataset_name="Absorbed Spectral Power",
                        title_x="Photon Energy [eV]",
                        title_y="Spectral density [W/eV]")

        #
        # transmitted
        #

        # coordinates to send: the same as incident beam (perpendicular to the optical axis)
        # except for the magnifier
        if EL1_FLAG == 3:  # magnifier <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            h *= EL1_HMAG
            v *= EL1_VMAG

        transmitted = p_spectral_power * transmittance / (h[0] / h0[0]) / (v[0] / v0[0])
        h5w.add_image(numpy.trapz(transmitted, E, axis=0), h, v,
                      image_name="Transmitted Power Density on Element", entry_name=entry_name,
                      title_x="X [mm] (normal to beam)",
                      title_y="Y [mm] (normal to beam)")

        h5w.add_dataset(E, numpy.trapz(numpy.trapz(transmitted, v, axis=2), h, axis=1),
                        entry_name=entry_name, dataset_name="Transmitted Spectral Power",
                        title_x="Photon Energy [eV]",
                        title_y="Spectral density [W/eV]")
    except:
        print("ERROR writing h5 file (optical element)")

    try:
        h5_entry_name = "XOPPY_RADIATION"

        h5w.create_entry(h5_entry_name,nx_default=None)
        h5w.add_stack(e, h, v, transmitted,stack_name="Radiation",entry_name=h5_entry_name,
            title_0="Photon energy [eV]",
            title_1="X gap [mm]",
            title_2="Y gap [mm]")
    except:
        print("ERROR writing h5 file (adding XOPPY_RADIATION)")

    print("File written to disk: %s" % filename)

#
# info
#
def info_total_power(p, e, v, h, transmittance, absorbance, EL1_FLAG=1):
    txt = ""
    txt += "\n\n\n"
    power_input = integral_3d(p, e, h, v, method=0) * codata.e * 1e3
    txt += '      Input beam power: %f W\n'%(power_input)

    power_transmitted = integral_3d(p * transmittance, e, h, v, method=0) * codata.e * 1e3
    power_absorbed = integral_3d(p * absorbance, e, h, v, method=0) * codata.e * 1e3

    power_lost = power_input - ( power_transmitted +  power_absorbed)
    if numpy.abs( power_lost ) > 1e-9:
        txt += '      Beam power not considered (removed by o.e. acceptance): %6.3f W (accepted: %6.3f W)\n' % \
               (power_lost, power_input - power_lost)

    txt += '      Beam power absorbed by optical element: %6.3f W\n' % power_absorbed

    if EL1_FLAG == 1:
        txt += '      Beam power reflected after optical element: %6.3f W\n' % power_transmitted
    else:
        txt += '      Beam power transmitted after optical element: %6.3f W\n' % power_transmitted

    return txt




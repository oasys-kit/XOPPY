#*********************************************************************************************************
#*********************************************************************************************************
#*********************************************************************************************************
#
# auxiliar functions for SRCALC
#
#*********************************************************************************************************
#*********************************************************************************************************

import numpy

def load_srcalc_output_file(filename="D_IDPower.TXT",skiprows=5,four_quadrants=True,
                            do_plot=False,verbose=True):
    """

    :param filename:
    :param skiprows:
    :param four_quadrants:
    :param do_plot:
    :param verbose:
    :return:
            out_dictionary:  Zlist 0 (63, 43)  <== source
            out_dictionary:  Zlist 1 (63, 43)  <== oe1
            out_dictionary:  Zlist 2 (63, 43)  <== oe2
            out_dictionary:  X (63,)
            out_dictionary:  Y (43,)
            out_dictionary:  RAWDATA (704, 3)
            out_dictionary: from D_IDPower.TXT:  NELEMENTS
    """

    a = numpy.loadtxt(filename,skiprows=skiprows)
    f = open(filename,'r')
    line = f.readlines()
    f.close()

    npx = int(line[0])
    xps = float(line[1])
    npy = int(line[2])
    yps = float(line[3])
    nMirr = int(line[4])

    if nMirr == 0:
        a.shape = (a.size,1)

    SOURCE = numpy.zeros((nMirr+1,npx,npy))

    ii = -1
    for ix in range(npx):
        for iy in range(npy):
            ii += 1
            for icol in range(nMirr+1):
                SOURCE[icol,ix,iy] = a[ii,icol]


    hh = numpy.linspace(0,0.5 * xps,npx)
    vv = numpy.linspace(0,0.5 * yps,npy)
    hhh = numpy.concatenate((-hh[::-1], hh[1:]))
    vvv = numpy.concatenate((-vv[::-1], vv[1:]))

    int_mesh1 = []
    int_mesh2 = []

    for i in range(nMirr+1):
        int_mesh = SOURCE[i,:,:].copy()
        # normalize every pixel to absolute power (W and not W/mm2)
        int_mesh *= (hh[1] - hh[0]) * (vv[1] - vv[0])

        int_mesh1.append(int_mesh)
        tmp = numpy.concatenate((int_mesh[::-1, :], int_mesh[1:, :]), axis=0)
        int_mesh2.append( numpy.concatenate((tmp[:, ::-1], tmp[:, 1:]), axis=1) )

        if do_plot:
            from srxraylib.plot.gol import plot_image
            if four_quadrants:
                # totPower = int_mesh2[i].sum() * (hhh[1] - hhh[0]) * (vvv[1] - vvv[0])
                totPower2 = trapezoidal_rule_2d_1darrays(int_mesh2[i],hhh,vvv)
                plot_image(int_mesh2[i],hhh,vvv,title=">>%d<< Source Tot Power %f, pow density: %f"%(i,totPower2,int_mesh2[i].max()),show=True)
            else:
                # totPower = int_mesh1[i].sum() * (hh[1] - hh[0]) * (vv[1] - vv[0])
                totPower2 = trapezoidal_rule_2d_1darrays(int_mesh1[i],hh,vv)
                plot_image(int_mesh1[i], hh, vv,
                           title=">>%d<< Source Tot Power %f, pow density: %f" % (i, totPower2, int_mesh2[i].max()),
                           show=True)

    if four_quadrants:
        out_dictionary = {"Zlist": int_mesh2, "X": hhh, "Y": vvv, "RAWDATA": a, "NELEMENTS": nMirr}
    else:
        out_dictionary = {"Zlist": int_mesh1, "X": hh, "Y": vv, "RAWDATA": a, "NELEMENTS": nMirr}

    if verbose:
        for key in out_dictionary.keys():
            if isinstance(out_dictionary[key],numpy.ndarray):
                print(">>1>> out_dictionary: from D_IDPower.TXT: ", key, out_dictionary[key].shape)
            elif isinstance(out_dictionary[key],list):
                for i in range(len(out_dictionary[key])):
                    print(">>1>> out_dictionary: from D_IDPower.TXT: ", key, i, out_dictionary[key][i].shape)
            else:
                print(">>1>> out_dictionary: from D_IDPower.TXT: ", key)
    return out_dictionary


def ray_tracing(
        out_dictionary,
        SOURCE_SCREEN_DISTANCE=13.73,
        number_of_elements=1,
        oe_parameters=  {
            "EL0_SHAPE":2,
            "EL0_P_POSITION":13.73,
            "EL0_Q_POSITION":0.0,
            "EL0_P_FOCUS":0.0,
            "EL0_Q_FOCUS":0.0,
            "EL0_ANG":88.75,
            "EL0_THICKNESS":1000,
            "EL0_RELATIVE_TO_PREVIOUS":2,
                        },
        real_space_shuffle=[0,0,0],
        dump_shadow_files=True,
        accumulate_results=True,
        store_footprint=True,
        store_image=True,
        verbose=False,
        run_index=None,
        undo_shadow_orientation_angle_rotation=False):
    """

    :param out_dictionary:
    :param SOURCE_SCREEN_DISTANCE:
    :param number_of_elements:
    :param oe_parameters:
    :param real_space_shuffle:
    :param dump_shadow_files:
    :param accumulate_results:
    :param verbose:
    :return:
            adds in the out_dictionary the keys:
            OE_FOOTPRINT: list[oe_index]  ndarray(3, 2709)   (shadow: col2,col1,col23)
            OE_IMAGE:     list[oe_index]  ndarray(3, 2709)   (shadow: col2,col1,col23)
    """

    from shadow4.beam.beam import Beam
    from shadow4.compatibility.beam3 import Beam3

    from shadow4.optical_surfaces.conic import Conic
    from shadow4.optical_surfaces.toroid import Toroid

    #
    # compute shadow beam from urgent results
    #
    vx = out_dictionary["X"] / ( 1e3 * SOURCE_SCREEN_DISTANCE )
    vz = out_dictionary["Y"] / ( 1e3 * SOURCE_SCREEN_DISTANCE )

    nrays = vx.size * vz.size

    VX = numpy.outer(vx, numpy.ones_like(vz)).flatten()
    VZ = numpy.outer(numpy.ones_like(vx), vz).flatten()
    VY = numpy.sqrt(1.0 - VX ** 2 + VZ ** 2).flatten()

    X = numpy.ones(nrays) * real_space_shuffle[0]
    Y = numpy.ones(nrays) * real_space_shuffle[1]
    Z = numpy.ones(nrays) * real_space_shuffle[2]


    # print(VY)

    beam = Beam.initialize_as_pencil(N=nrays)
    beam.set_column(1, X)
    beam.set_column(2, Y)
    beam.set_column(3, Z)
    beam.set_column(4, VX)
    beam.set_column(5, VY)
    beam.set_column(6, VZ)

    if dump_shadow_files:
        beam.set_column(7, (numpy.sqrt(out_dictionary["Zlist"][0]).flatten()))
        beam.set_column(8, 0.0)
        beam.set_column(9, 0.0)
        beam.set_column(16, 0.0)
        beam.set_column(17, 0.0)
        beam.set_column(18, 0.0)
        if run_index is None:
            filename = 'begin_srcalc.dat'
        else:
            filename = 'begin_srcalc_%03d.dat' % run_index
        Beam3.initialize_from_shadow4_beam(beam).write(filename)
        print("File written to disk: %s" % filename)

    OE_FOOTPRINT = []
    OE_IMAGE = []

    for oe_index in range(number_of_elements):

        p = oe_parameters["EL%d_P_POSITION" % oe_index]
        q = oe_parameters["EL%d_Q_POSITION" % oe_index]

        theta_grazing = (90.0 - oe_parameters["EL%d_ANG" % oe_index]) * numpy.pi / 180

        if oe_parameters["EL%d_RELATIVE_TO_PREVIOUS"%oe_index] == 0:
            alpha = 90.0 * numpy.pi / 180
        elif oe_parameters["EL%d_RELATIVE_TO_PREVIOUS"%oe_index] == 1:
            alpha = 270.0 * numpy.pi / 180
        elif oe_parameters["EL%d_RELATIVE_TO_PREVIOUS"%oe_index] == 2:
            alpha = 0.0
        elif oe_parameters["EL%d_RELATIVE_TO_PREVIOUS"%oe_index] == 3:
            alpha = 180.0 * numpy.pi / 180


        if oe_parameters["EL%d_SHAPE"%oe_index] == 0:     # "Toroidal mirror",
            is_conic = False
            toroid = Toroid()
            toroid.set_from_focal_distances(
                oe_parameters["EL%d_P_FOCUS" % oe_index],
                oe_parameters["EL%d_Q_FOCUS" % oe_index],
                theta_grazing)
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 1:     # "Spherical mirror",
            is_conic = True
            ccc = Conic.initialize_as_sphere_from_focal_distances(
                oe_parameters["EL%d_P_FOCUS" % oe_index],
                oe_parameters["EL%d_Q_FOCUS" % oe_index],
                theta_grazing,cylindrical=0,cylangle=0,switch_convexity=0)
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 2:     # "Plane mirror",
            is_conic = True
            ccc = Conic.initialize_as_plane()
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 3:     # "MerCyl mirror",
            is_conic = True
            ccc = Conic.initialize_as_sphere_from_focal_distances(
                oe_parameters["EL%d_P_FOCUS" % oe_index],
                oe_parameters["EL%d_Q_FOCUS" % oe_index],
                theta_grazing,cylindrical=1,cylangle=0,switch_convexity=0)
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 4:     # "SagCyl mirror",
            raise Exception("Not implemented")
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 5:     # "Ellipsoidal mirror",
            is_conic = True
            ccc = Conic.initialize_as_ellipsoid_from_focal_distances(
                oe_parameters["EL%d_P_FOCUS" % oe_index],
                oe_parameters["EL%d_Q_FOCUS" % oe_index],
                theta_grazing,cylindrical=0,cylangle=0,switch_convexity=0)
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 6:     # "MerEll mirror",
            is_conic = True
            ccc = Conic.initialize_as_ellipsoid_from_focal_distances(
                oe_parameters["EL%d_P_FOCUS" % oe_index],
                oe_parameters["EL%d_Q_FOCUS" % oe_index],
                theta_grazing,cylindrical=1,cylangle=0,switch_convexity=0)
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 7:     # "SagEllip mirror",
            raise Exception("Not implemented")
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 8:     # "Filter",
            is_conic = True
            ccc = Conic.initialize_as_plane()
        elif oe_parameters["EL%d_SHAPE"%oe_index] == 9:     # "Crystal"
            is_conic = True
            ccc = Conic.initialize_as_plane()

        if oe_index == 0:
            newbeam = beam.duplicate()

        #
        # put beam in mirror reference system
        #
        newbeam.rotate(alpha, axis=2)
        newbeam.rotate(theta_grazing, axis=1)
        newbeam.translation([0.0, -p * numpy.cos(theta_grazing), p * numpy.sin(theta_grazing)])
        #
        # reflect beam in the mirror surface and dump mirr.01
        #
        if is_conic:
            if verbose:
                print("\n\nElement %d is CONIC :\n" % (1 + oe_index), ccc.info())
            newbeam = ccc.apply_specular_reflection_on_beam(newbeam)
        else:
            if verbose:
                print("\n\nElement %d is TOROIDAL :\n" % (1 + oe_index), toroid.info())
            newbeam = toroid.apply_specular_reflection_on_beam(newbeam)
        print("\n     p: %f m" % p)
        print("      q: %f m" % q)
        print("      p (focal): %f m" % oe_parameters["EL%d_P_FOCUS" % oe_index] )
        print("      q (focal): %f m" % oe_parameters["EL%d_Q_FOCUS" % oe_index] )
        print("      alpha: %f rad = %f deg" % (alpha, alpha*180/numpy.pi) )
        print("      theta_grazing: %f rad = %f deg" %  (theta_grazing, theta_grazing*180/numpy.pi) )
        print("      theta_normal: %f rad = %f deg \n" % (numpy.pi/2 - theta_grazing, 90 - theta_grazing * 180 / numpy.pi))

        if dump_shadow_files:
            newbeam.set_column(7, (numpy.sqrt(out_dictionary["Zlist"][oe_index] - out_dictionary["Zlist"][oe_index + 1]).flatten()))
            newbeam.set_column(8, 0.0)
            newbeam.set_column(9, 0.0)
            newbeam.set_column(16, 0.0)
            newbeam.set_column(17, 0.0)
            newbeam.set_column(18, 0.0)
            if run_index is None:
                filename = 'mirr_srcalc.%02d' % (oe_index+1)
            else:
                filename = 'mirr_srcalc_%03d.%02d' % (run_index, oe_index+1)
            Beam3.initialize_from_shadow4_beam(newbeam).write(filename)
            print("File written to disk: %s" % filename)
        tmp = newbeam.get_columns((2, 1, 23))
        tmp[2,:] = (out_dictionary["Zlist"][oe_index+1]).flatten()
        OE_FOOTPRINT.append( tmp )
        #
        # put beam in lab frame and compute image
        #
        newbeam.rotate(theta_grazing, axis=1)
        # do not undo alpha rotation: newbeam.rotate(-alpha, axis=2)
        if undo_shadow_orientation_angle_rotation:
            newbeam.rotate(-alpha, axis=2)
        newbeam.retrace(q, resetY=True)
        if dump_shadow_files:
            newbeam.set_column(7, (numpy.sqrt(out_dictionary["Zlist"][oe_index + 1]).flatten()))
            newbeam.set_column(8, 0.0)
            newbeam.set_column(9, 0.0)
            newbeam.set_column(16, 0.0)
            newbeam.set_column(17, 0.0)
            newbeam.set_column(18, 0.0)
            if run_index is None:
                filename = 'star_srcalc.%02d' % (oe_index+1)
            else:
                filename = 'star_srcalc_%03d.%02d' % (run_index, oe_index+1)
            Beam3.initialize_from_shadow4_beam(newbeam).write(filename)
            print("File written to disk: %s" % filename)

        tmp = newbeam.get_columns((1, 3, 23))
        tmp[2,:] = (out_dictionary["Zlist"][oe_index+1]).flatten()
        OE_IMAGE.append(tmp)

    # add ray tracing results to in/out dictionary

    # footprint
    if store_footprint:
        out_dictionary["OE_FOOTPRINT"] = OE_FOOTPRINT

    if store_image:
        if accumulate_results:
            if "OE_IMAGE" in out_dictionary.keys():
                initialize_results = False
            else:
                initialize_results = True
        else:
            initialize_results = True

        if initialize_results:
            out_dictionary["OE_IMAGE"] = OE_IMAGE
        else:
            for oe_index in range(number_of_elements):
                out_dictionary["OE_IMAGE"][oe_index] = numpy.concatenate( \
                    (out_dictionary["OE_IMAGE"][oe_index], OE_IMAGE[oe_index]), axis=1)

    if True:
        if "OE_FOOTPRINT" in out_dictionary.keys():
            for i in range(len(out_dictionary["OE_FOOTPRINT"])):
                print(">>2>> out_dictionary: from raytracing OE_FOOTPRINT: ", i, out_dictionary["OE_FOOTPRINT"][i].shape)
        if "OE_IMAGE" in out_dictionary.keys():
            for i in range(len(out_dictionary["OE_IMAGE"])):
                print(">>2>> out_dictionary: from raytracing OE_IMAGE: ", i, out_dictionary["OE_IMAGE"][i].shape)
        print("\n")
    return out_dictionary

# def calculate_pixel_areas(X,Y,suppress_last_row_and_column=True):
#     u1 = numpy.roll(X, -1, axis=0) - X
#     u2 = numpy.roll(Y, -1, axis=0) - Y
#     v1 = numpy.roll(X, -1, axis=1) - X
#     v2 = numpy.roll(Y, -1, axis=1) - Y
#
#     if suppress_last_row_and_column:
#         u1 = u1[0:-1, 0:-1].copy()
#         u2 = u2[0:-1, 0:-1].copy()
#         v1 = v1[0:-1, 0:-1].copy()
#         v2 = v2[0:-1, 0:-1].copy()
#         XX = X[0:-1, 0:-1].copy()
#         YY = Y[0:-1, 0:-1].copy()
#     else:
#         XX = X.copy()
#         YY = Y.copy()
#     return u1 * v2 - u2 * v1, XX, YY

def interpolate_to_regular_grid(power_density_footprint, XX_FOOTPRINT, YY_FOOTPRINT,
                                nx=None, ny=None,
                                xrange=None, yrange=None,
                                renormalize_integrals=True,
                                interpolation_method=0):
    # debug_plot_3d(power_density_footprint.flatten(),
    #               XX_FOOTPRINT.flatten(), YY_FOOTPRINT.flatten(),
    #               title="before interpolation, oe: %d"%(element_index+1))
    if nx is None:
        nx = XX_FOOTPRINT.shape[0]
    if ny is None:
        ny = YY_FOOTPRINT.shape[1]

    if interpolation_method == 0:
        method = 'linear'
    elif interpolation_method == 1:
        method = 'nearest'
    elif interpolation_method == 2:
        method = 'cubic'
    else:
        raise Exception("Invalid interpolation method=%d"%interpolation_method)

    XX_FOOTPRINT_old = XX_FOOTPRINT.copy()
    YY_FOOTPRINT_old = YY_FOOTPRINT.copy()

    if xrange is None:
        XX_FOOTPRINT_MAX = numpy.max( (-XX_FOOTPRINT_old.min(), XX_FOOTPRINT_old.max()))
        xx_footprint = numpy.linspace(-XX_FOOTPRINT_MAX, XX_FOOTPRINT_MAX, nx)
    else:
        xx_footprint = numpy.linspace(xrange[0], xrange[1], nx)

    if yrange is None:
        YY_FOOTPRINT_MAX = numpy.max( (-YY_FOOTPRINT_old.min(), YY_FOOTPRINT_old.max()))
        yy_footprint = numpy.linspace(-YY_FOOTPRINT_MAX, YY_FOOTPRINT_MAX, ny)
    else:
        yy_footprint = numpy.linspace(yrange[0], yrange[1], ny)

    XX_FOOTPRINT = numpy.outer(xx_footprint,numpy.ones_like(yy_footprint))
    YY_FOOTPRINT = numpy.outer(numpy.ones_like(xx_footprint), yy_footprint)

    from scipy import interpolate
    tmptmp1 = trapezoidal_rule_2d(power_density_footprint)
    power_density_footprint = interpolate.griddata(
        (XX_FOOTPRINT_old.flatten(), YY_FOOTPRINT_old.flatten()),
        power_density_footprint.flatten(),
        (XX_FOOTPRINT, YY_FOOTPRINT), method=method, fill_value=0.0, rescale=True)

    if renormalize_integrals:
        tmptmp2 = trapezoidal_rule_2d(power_density_footprint)
        print(">> integral before interpolation: %f, integral after: %f" % (tmptmp1, tmptmp2))
        power_density_footprint *= tmptmp1 / tmptmp2
        print(">> Renormalized to match integral after with integral before interpolation")

    return power_density_footprint, XX_FOOTPRINT, YY_FOOTPRINT

def compute_power_density_footprint(dict1,
                                    verbose=True,
                                    interpolation_method=0,
                                    ratio_pixels_0=1.0,
                                    ratio_pixels_1=1.0,
                                    flip_pixels_number=[0,0,0,0,0,0]):

    shapeXY = (dict1["X"].size, dict1["Y"].size)

    # now build maps for optical elements

    if "OE_FOOTPRINT" in dict1.keys():
        OE_FOOTPRINT = dict1["OE_FOOTPRINT"]
        number_of_elements_traced = len(OE_FOOTPRINT)
    else:
        number_of_elements_traced = 0

    print(">> compute_power_density_footprint: Number of raytraced elements: %d"%number_of_elements_traced)

    POWER_DENSITY_FOOTPRINT = []
    POWER_DENSITY_FOOTPRINT_H = []
    POWER_DENSITY_FOOTPRINT_V = []

    for element_index in range(number_of_elements_traced):
        XX_FOOTPRINT = OE_FOOTPRINT[element_index][1, :].reshape(shapeXY)
        YY_FOOTPRINT = OE_FOOTPRINT[element_index][0, :].reshape(shapeXY)
        power_density_footprint = dict1["Zlist"][element_index] - dict1["Zlist"][element_index+1]

        if flip_pixels_number[element_index]:
            ny = int(shapeXY[0]*ratio_pixels_0)
            nx = int(shapeXY[1]*ratio_pixels_1)
        else:
            nx = int(shapeXY[0]*ratio_pixels_0)
            ny = int(shapeXY[1]*ratio_pixels_1)

        power_density_footprint, XX_FOOTPRINT, YY_FOOTPRINT = \
            interpolate_to_regular_grid(
            power_density_footprint, XX_FOOTPRINT, YY_FOOTPRINT,
            nx=nx,ny=ny,
            interpolation_method=interpolation_method)

        POWER_DENSITY_FOOTPRINT.append( power_density_footprint )
        POWER_DENSITY_FOOTPRINT_H.append(XX_FOOTPRINT)
        POWER_DENSITY_FOOTPRINT_V.append(YY_FOOTPRINT)

    dict1["POWER_DENSITY_FOOTPRINT"] = POWER_DENSITY_FOOTPRINT
    dict1["POWER_DENSITY_FOOTPRINT_H"] = POWER_DENSITY_FOOTPRINT_H
    dict1["POWER_DENSITY_FOOTPRINT_V"] = POWER_DENSITY_FOOTPRINT_V

    if verbose:
        for i in range(len(dict1["POWER_DENSITY_FOOTPRINT"])):
            print(">>3>> out_dictionary: POWER_DENSITY_FOOTPRINT  : ", i, dict1["POWER_DENSITY_FOOTPRINT"][i].shape)
            print(">>3>> out_dictionary: POWER_DENSITY_FOOTPRINT_H: ", i, dict1["POWER_DENSITY_FOOTPRINT_H"][i].shape)
            print(">>3>> out_dictionary: POWER_DENSITY_FOOTPRINT_V: ", i, dict1["POWER_DENSITY_FOOTPRINT_V"][i].shape)
            print("\n")

    return dict1

def compute_power_density_image(dict1,
                                verbose=True,
                                interpolation_or_histogramming=False,
                                interpolation_method=0,
                                ratio_pixels_0=1.0,
                                ratio_pixels_1=1.0,
                                flip_pixels_number=[0,0,0,0,0,0]):

    shapeXY = (dict1["X"].size, dict1["Y"].size)

    try:
        OE_IMAGE = dict1["OE_IMAGE"]
        number_of_elements_traced = len(OE_IMAGE)
    except:
        number_of_elements_traced = 0

    print(">> compute_power_density_image: Number of raytraced elements: %d"%number_of_elements_traced)

    POWER_DENSITY_IMAGE = []
    POWER_DENSITY_IMAGE_H = []
    POWER_DENSITY_IMAGE_V = []

    for element_index in range(number_of_elements_traced):

        tmptmp1 = trapezoidal_rule_2d(dict1["Zlist"][element_index+1])

        image_H = OE_IMAGE[element_index][0, :]
        image_V = OE_IMAGE[element_index][1, :]
        weights = OE_IMAGE[element_index][2, :]

        f = open("tmp.%02d" % (element_index + 1), 'w')
        for i in range(image_V.size):
            f.write("%g  %g  %g\n" % (image_H[i], image_V[i], weights[i]))
        f.close()
        print("File tmp.%02d written to disk" % (element_index + 1))

        # calculate limits
        image_H_max = numpy.max( (numpy.abs(image_H.min()), numpy.abs(image_H.max())) )
        image_V_max = numpy.max( (numpy.abs(image_V.min()), numpy.abs(image_V.max())) )

        if flip_pixels_number[element_index]:
            ny = int(shapeXY[0]*ratio_pixels_0)
            nx = int(shapeXY[1]*ratio_pixels_1)
        else:
            nx = int(shapeXY[0]*ratio_pixels_0)
            ny = int(shapeXY[1]*ratio_pixels_1)

        if interpolation_or_histogramming:
            # make histograms for image
            (hh,xx,yy) = numpy.histogram2d(image_H, image_V,
                            bins=[nx,ny], #[100,100], #2*nx0,2*ny0],
                            range=[[-image_H_max,image_H_max],[-image_V_max,image_V_max]],
                            normed=False,
                            weights=weights)
            bin_h_left = numpy.delete(xx,-1)
            bin_v_left = numpy.delete(yy,-1)
            bin_h_right = numpy.delete(xx,0)
            bin_v_right = numpy.delete(yy,0)
            bin_h_center = 0.5 * (bin_h_left + bin_h_right)
            bin_v_center = 0.5 * (bin_v_left + bin_v_right)
            xx_image = bin_h_center
            yy_image = bin_v_center
            power_density_image = hh
            # prepare outputs
            XX_IMAGE = numpy.outer(xx_image, numpy.ones_like(yy_image))
            YY_IMAGE = numpy.outer(numpy.ones_like(xx_image), yy_image)
        else:
            nruns = int(image_H.size / (shapeXY[0] * shapeXY[1]))
            weights_splitted = numpy.split(weights, nruns)
            image_H_splitted = numpy.split(image_H, nruns)
            image_V_splitted = numpy.split(image_V, nruns)

            power_density_image = numpy.zeros((nx, ny))

            for i in range(nruns):

                power_density_image_i, XX_IMAGE, YY_IMAGE = \
                    interpolate_to_regular_grid(
                        weights_splitted[i].reshape(shapeXY),
                        image_H_splitted[i].reshape(shapeXY),
                        image_V_splitted[i].reshape(shapeXY),
                        xrange=[-image_H_max,image_H_max],
                        yrange=[-image_V_max,image_V_max],
                        renormalize_integrals=False,
                        interpolation_method=interpolation_method,
                        nx=nx,
                        ny=ny,
                    )

                area_factor = image_H_max * image_V_max /\
                              (numpy.abs(image_H_splitted[i]).max() * \
                               numpy.abs(image_V_splitted[i]).max())
                power_density_image += power_density_image_i * area_factor


        tmptmp2 = trapezoidal_rule_2d(power_density_image)
        power_density_image *= tmptmp1 / tmptmp2

        print(">> oe %d: integral before interpolation/histograming %f and after: %f" % (element_index+1,tmptmp1, tmptmp2))
        print(">> Renormalized to match integral after with integral before interpolation/histogramming")

        POWER_DENSITY_IMAGE.append(power_density_image)
        POWER_DENSITY_IMAGE_H.append(XX_IMAGE)
        POWER_DENSITY_IMAGE_V.append(YY_IMAGE)

    dict1["POWER_DENSITY_IMAGE"] = POWER_DENSITY_IMAGE
    dict1["POWER_DENSITY_IMAGE_H"] = POWER_DENSITY_IMAGE_H
    dict1["POWER_DENSITY_IMAGE_V"] = POWER_DENSITY_IMAGE_V

    if verbose:
        for i in range(len(dict1["POWER_DENSITY_FOOTPRINT"])):
            print(">>3>> out_dictionary: POWER_DENSITY_IMAGE: ",       i, dict1["POWER_DENSITY_IMAGE"][i].shape)
            print(">>3>> out_dictionary: POWER_DENSITY_IMAGE_H: ",     i, dict1["POWER_DENSITY_IMAGE_H"][i].shape)
            print(">>3>> out_dictionary: POWER_DENSITY_IMAGE_V: ",     i, dict1["POWER_DENSITY_IMAGE_V"][i].shape)
            print("\n")

    return dict1

def trapezoidal_rule_2d(data2D,H=None,V=None):
    if H is None:
        HH = numpy.arange(data2D.shape[0])
    else:
        HH = H[:, 0]

    if V is None:
        VV = numpy.arange(data2D.shape[1])
    else:
        VV = V[0, :]

    totPower2 = numpy.trapz(data2D, VV, axis=1)
    totPower2 = numpy.trapz(totPower2, HH, axis=0)
    return totPower2

def trapezoidal_rule_2d_1darrays(data2D,h=None,v=None):
    if h is None:
        h = numpy.arange(data2D.shape[0])
    if v is None:
        v = numpy.arange(data2D.shape[1])
    totPower2 = numpy.trapz(data2D, v, axis=1)
    totPower2 = numpy.trapz(totPower2, h, axis=0)
    return totPower2

def debug_plot_3d(zs,xs,ys,title=""):
    import matplotlib.pylab as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    self_axis = fig.add_subplot(111, projection='3d')

    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    # for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
    for m, zlow, zhigh in [('o', zs.min(), zs.max())]:
        self_axis.scatter(xs, ys, zs, marker=m)

    self_axis.set_xlabel('X [mm]')
    self_axis.set_ylabel('Y [mm]')
    self_axis.set_zlabel('Z [um]')
    self_axis.set_title(title)
    plt.show()

def write_ansys_files(absorbed2d, H, V, oe_number=1):

    filename="idpower_fea_3columns_element%d.txt" % oe_number
    f = open(filename, 'w')
    for i in range(H.size):
        for j in range(V.size):
            f.write("%g  %g  %g\n" % (H[i]*1e-3, V[j]*1e-3, absorbed2d[i,j]*1e6))
    f.close()
    print("File written to disk: %s" % filename)

    #

    filename="idpower_fea_matrix_element%d.txt" % oe_number
    f = open(filename, 'w')

    f.write("%10.5g" % 0)
    for i in range(H.size):
        f.write(", %10.5g" % (H[i] * 1e-3))
    f.write("\n")

    for j in range(V.size):
            f.write("%10.5g" % (V[j] * 1e-3))
            for i in range(H.size):
                f.write(", %10.5g" % (absorbed2d[i,j] * 1e6))
            f.write("\n")
    f.close()
    print("File written to disk: %s" % filename)

if __name__ == "__main__":
    path = "C:/Users/Manuel/OASYS1.2/OASYS1-ALS-ShadowOui/orangecontrib/xoppy/als/widgets/srcalc/"

    test = 3  # 0= widget, 1=load D_IDPower.TXT, 2 =ray tracing, 3 integral
    if test == 0:
        pass
    elif test == 1:
        dict1 = load_srcalc_output_file(filename=path+"D_IDPower.TXT", skiprows=5, do_plot=0)
        dict2 = ray_tracing(dict1)
        dict3 = compute_power_density_footprint(dict2)
    elif test == 2:
        dict1 = load_srcalc_output_file(filename=path+"D_IDPower.TXT", skiprows=5, do_plot=0)
        dict2 = ray_tracing(dict1)
        OE_FOOTPRINT = dict2["OE_FOOTPRINT"]
        OE_IMAGE = dict2["OE_IMAGE"]
        print(OE_FOOTPRINT[0].shape)
        from srxraylib.plot.gol import plot_scatter
        plot_scatter(OE_FOOTPRINT[0][0,:],OE_FOOTPRINT[0][1,:],plot_histograms=False,title="Footprint",show=False)
        plot_scatter(OE_IMAGE[0][0, :], OE_IMAGE[0][1, :], plot_histograms=False,title="Image")

    elif test == 3:
        a = numpy.loadtxt(path+"D_IDPower.TXT",skiprows=5)
        nX = 31 # intervals - URGENT input
        nY = 21 # intervals - URGENT input
        npointsX = nX + 1
        npointsY = nY + 1

        print("Dimensions ", a.shape, npointsX * npointsY)

        stepX = 30.0 / 2 / nX
        stepY = 15.0 / 2 / nY

        X = numpy.linspace(0, 30.0 / 2, nX + 1)
        Y = numpy.linspace(0, 15.0 / 2, nY + 1)

        print("X, Y: ",X.shape,Y.shape)
        totPower1 = 4 * trapezoidal_rule_2d_1darrays((a[:, 0]).copy().reshape((npointsX, npointsY)), X, Y)
        totPower2 = 4 * trapezoidal_rule_2d_1darrays((a[:, 1]).copy().reshape((npointsX, npointsY)), X, Y)
        totPower3 = 4 * trapezoidal_rule_2d_1darrays((a[:, 2]).copy().reshape((npointsX, npointsY)), X, Y)

        print("Sum for column 1: ", totPower1)
        print("Sum for column 2: ", totPower2)
        print("Sum for column 3: ", totPower3)

        dict1 = load_srcalc_output_file(filename=path+"D_IDPower.TXT", skiprows=5,
                                four_quadrants=True,
                                do_plot=False,
                                verbose=True)

        totPower11 = trapezoidal_rule_2d_1darrays(dict1["Zlist"][0])
        totPower22 = trapezoidal_rule_2d_1darrays(dict1["Zlist"][1])
        totPower33 = trapezoidal_rule_2d_1darrays(dict1["Zlist"][2])

        print("Sum for element 1: ", totPower11)
        print("Sum for element 2: ", totPower22)
        print("Sum for element 3: ", totPower33)
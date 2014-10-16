import Shadow
import numpy

def calc_xsh_und_gauss(UND_LENGTH=4.0,UND_E0=15000.0,UND_DE=1500.0,USERUNIT=1,SIGMAX=0.0001,SIGMAZ=0.0001,SIGDIX=1e-06,SIGDIZ=1e-06,NPOINT=15000,ISTAR1=0):
    print("Inside calc_xsh_und_gauss. ")

    print("before:",(SIGMAX,SIGMAZ,SIGDIX,SIGDIZ))

    (SIGMAX,SIGMAZ,SIGDX,SIGDIZ) = getPhotonSizes(SIGMAX=SIGMAX,SIGMAZ=SIGMAZ,SIGDIX=SIGDIX,SIGDIZ=SIGDIZ,UND_E0=UND_E0,UND_LENGTH=UND_LENGTH,USERUNIT=1)

    print("after:",(SIGMAX,SIGMAZ,SIGDIX,SIGDIZ))

    #
    # define Shadow Geometrical Gaussian Source in the
    # energy interval UND_E0 +- UND_DE/2
    # Note that this energy interval is not correlated with the geometry,
    # thus is a constant spectrum.
    #
    s1 = Shadow.Source()

    # these are the variables that change from the defult values
    s1.FDISTR =  3
    s1.FSOUR =  3
    s1.F_PHOT =  0
    s1.F_POLAR =  1
    s1.ISTAR1 =  ISTAR1
    s1.NPOINT =  NPOINT
    s1.F_COLOR =  3
    s1.PH1 =        UND_E0-UND_DE/2.0
    s1.PH2 =        UND_E0+UND_DE/2.0
    s1.SIGDIX = SIGDIX
    s1.SIGDIZ = SIGDIZ
    s1.SIGMAX = SIGMAX
    s1.SIGMAZ = SIGMAZ
    s1.HDIV1 =    0.0
    s1.HDIV2 =    0.0
    s1.VDIV1 =    0.0
    s1.VDIV2 =    0.0

    # write shadow file (not needed)
    s1.write('start.00')
    print("File written to disk: start.00")

    # create source
    beam = Shadow.Beam()
    beam.genSource(s1)
    beam.write("beginG.dat")
    print("File written to disk: beginG.dat")


    print("after FWHM:",(SIGMAX*2.35,SIGMAZ*2.35,SIGDIX*2.35,SIGDIZ*2.35))

    return(None)


def getPhotonSizes(SIGMAX=1e-4,SIGMAZ=1e-4,SIGDIX=1e-6,SIGDIZ=1e-6,UND_E0=15000.0,UND_LENGTH=4.0,USERUNIT=1):
#USERUNIT: 0=mm, 1=cm, 2=mm

    user_unit_to_m = 1.0
    if USERUNIT == 0:
        userunit_to_m = 1e-3
    if USERUNIT == 1:
        userunit_to_m = 1e-2

    codata_c = numpy.array(299792458.0)
    codata_h = numpy.array(6.62606957e-34)
    codata_ec = numpy.array(1.602176565e-19)
    m2ev = codata_c*codata_h/codata_ec


    lambda1 = m2ev/UND_E0
    print ("   photon energy [eV]: %f \n"%(UND_E0))
    print ("   photon wavelength [A]: %f \n"%(lambda1*1e10))

    # calculate sizes of the photon undulator beam
    # see formulas 25 & 30 in Elleaume (Onaki & Elleaume)
    s_phot = 2.740/(4e0*numpy.pi)*numpy.sqrt(UND_LENGTH*lambda1)
    sp_phot = 0.69*numpy.sqrt(lambda1/UND_LENGTH)

    print('\n')
    print('   RMS electon size H/V [um]: '+
                 repr(SIGMAX*1e6*userunit_to_m)+ ' /  '+
                 repr(SIGMAZ*1e6*userunit_to_m) )
    print('   RMS electon divergence H/V[urad]: '+
                 repr(SIGDIX*1e6)+ ' /  '+
                 repr(SIGDIZ*1e6)  )
    print('\n')
    print('   RMS radiation size [um]: '+repr(s_phot*1e6))
    print('   RMS radiation divergence [urad]: '+repr(sp_phot*1e6))
    print('\n')
    print('   Photon beam (convolution): ')

    photon_h = numpy.sqrt(numpy.power(SIGMAX*userunit_to_m,2) + numpy.power(s_phot,2) )
    photon_v = numpy.sqrt(numpy.power(SIGMAZ*userunit_to_m,2) + numpy.power(s_phot,2) )
    photon_hp = numpy.sqrt(numpy.power(SIGDIX,2) + numpy.power(sp_phot,2) )
    photon_vp = numpy.sqrt(numpy.power(SIGDIZ,2) + numpy.power(sp_phot,2) )

    print('   RMS size H/V [um]: '+ repr(photon_h*1e6) + '  /  '+repr(photon_v*1e6))
    print('   RMS divergence H/V [um]: '+ repr(photon_hp*1e6) + '  /  '+repr(photon_vp*1e6))
    return (photon_h/userunit_to_m,photon_v/userunit_to_m,photon_hp,photon_vp)

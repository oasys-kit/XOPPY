
r"""

srundplug: Undulator spectra calculations. An easy (or not too difficult) 
           interface to make these calculations using Srw, Urgent, and Us.


     functions (summary): 

        calc1d<code>   returns (e,f) 
                           f=flux (phot/s/0.1%bw) versus e=photon energy in eV

        calc2d<code>   returns (h,v,p) 
                           p=power density (W/mm^2) versus h and v slit 
                           directions in mm

        calc3d<code>   returns (e,h,v,f) 
                           f = flux (phot/s/0.1%bw/mm^2) versus e=energy in eV,
                           h and v slit directions in mm 





 
"""

__author__    = "Manuel Sanchez del Rio"
__contact__   = "srio@esrf.eu"
__copyright__ = "ESRF, 2014-2016"

#
#----------------------------  IMPORT ------------------------------------------
#

import os
import sys
import time
import array

import numpy
import shutil # to copy files


#SRW

USE_URGENT= True
USE_US = True
USE_SRWLIB = True
USE_PYSRU = False

if USE_SRWLIB:
    try:
        import srwlib
    except:
        try:
            import wpg.srwlib as srwlib
        except:
            USE_SRWLIB = False
            print("SRW is not available")


#catch standard optput
try:
    from io import StringIO  # Python3
except ImportError:
    from StringIO import StringIO  # Python2

try:
    import matplotlib.pylab as plt
except ImportError:
    print("failed to import matplotlib. Do not try to do on-line plots.")

from srxraylib.plot.gol import plot, plot_contour, plot_surface, plot_image, plot_show

########################################################################################################################
#
# GLOBAL NAMES
#
########################################################################################################################

# #Physical constants (global, by now)
import scipy.constants as codata
codata_mee = numpy.array(codata.physical_constants["electron mass energy equivalent in MeV"][0])
m2ev = codata.c * codata.h / codata.e      # lambda(m)  = m2eV / energy(eV)

# counter for output files
scanCounter = 0

# try:
#     from orangecontrib.xoppy.util.xoppy_util import locations
# except:
#     raise Exception("IMPORT")

# directory  where to find urgent and us binaries
try:
    from orangecontrib.xoppy.util.xoppy_util import locations
    home_bin = locations.home_bin()
except:
    import platform
    if platform.system() == 'Linux':
        home_bin='/scisoft/xop2.4/bin.linux/'
        print("srundplug: undefined home_bin. It has been set to ", home_bin)
    elif platform.system() == 'Darwin':
        home_bin = "/scisoft/xop2.4/bin.darwin/"
        print("srundplug: undefined home_bin. It has been set to ", home_bin)
    else:
        raise FileNotFoundError("srundplug: undefined home_bin")

#check
if os.path.isfile(home_bin + 'us') == False:
    raise FileNotFoundError("srundplug: File not found: "+home_bin+'us')
if os.path.isfile(home_bin + 'urgent') == False:
    raise FileNotFoundError("srundplug: File not found: " + home_bin + 'urgent')




# directory  where to find urgent and us binaries
try:
    home_bin
except NameError:
    #home_bin='/users/srio/Oasys/Orange-XOPPY/orangecontrib/xoppy/bin.linux/'
    home_bin='/scisoft/xop2.4/bin.linux/'
    print("srundplug: undefined home_bin. It has been set to ",home_bin)

#check
if os.path.isfile(home_bin+'us') == False:
    print("srundplug: File not found: "+home_bin+'us')
if os.path.isfile(home_bin+'urgent') == False:
    sys.exit("srundplug: File not found: "+home_bin+'urgent')




########################################################################################################################
#
# 1D: calc1d<code> Flux calculations
#
########################################################################################################################
def calc1d_pysru(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=5,
                npoints_grid=51,zero_emittance=False,fileName=None,fileAppend=False):

    r"""
        run pySRU for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """

    global scanCounter

    t0 = time.time()
    print("Inside calc1d_pysru")

    from pySRU.Simulation import create_simulation
    from pySRU.ElectronBeam import ElectronBeam
    from pySRU.MagneticStructureUndulatorPlane import MagneticStructureUndulatorPlane
    from pySRU.TrajectoryFactory import TrajectoryFactory, TRAJECTORY_METHOD_ANALYTIC,TRAJECTORY_METHOD_ODE

    from pySRU.RadiationFactory import RadiationFactory,RADIATION_METHOD_NEAR_FIELD, \
                                     RADIATION_METHOD_APPROX_FARFIELD


    myBeam = ElectronBeam(Electron_energy=bl['ElectronEnergy'], I_current=bl['ElectronCurrent'])
    myUndulator = MagneticStructureUndulatorPlane(K=bl['Kv'], period_length=bl['PeriodID'], length=bl['PeriodID']*bl['NPeriods'])


    is_quadrant = 1

    if is_quadrant:
        X = numpy.linspace(0,0.5*bl['gapH'],npoints_grid)
        Y = numpy.linspace(0,0.5*bl['gapV'],npoints_grid)
    else:
        X = numpy.linspace(-0.5*bl['gapH'],0.5*bl['gapH'],npoints_grid)
        Y = numpy.linspace(-0.5*bl['gapH'],0.5*bl['gapH'],npoints_grid)


    #
    # Warning: The automatic calculation of Nb_pts_trajectory dependens on the energy at this setup and it
    #           will kept constant over the full spectrum. Therefore, the setup here is done for the most
    #           "difficult" case, i.e., the highest energy.
    #           Setting photon_energy=None will do it at the first harmonic, and it was found that the flux
    #           diverges at high energies in some cases (energy_radiated_approximation_and_farfield)
    #
    simulation_test = create_simulation(magnetic_structure=myUndulator,electron_beam=myBeam,
                        magnetic_field=None, photon_energy=photonEnergyMax,
                        traj_method=TRAJECTORY_METHOD_ODE,Nb_pts_trajectory=None,
                        rad_method=RADIATION_METHOD_NEAR_FIELD, Nb_pts_radiation=None,
                        initial_condition=None, distance=bl['distance'],XY_are_list=False,X=X,Y=Y)

    # simulation_test.trajectory.plot()


    simulation_test.print_parameters()
    # simulation_test.radiation.plot(title=("radiation in a screen for first harmonic"))
    print("Integrated flux at resonance: %g photons/s/0.1bw"%(simulation_test.radiation.integration(is_quadrant=is_quadrant)))

    energies = numpy.linspace(photonEnergyMin,photonEnergyMax,photonEnergyPoints)

    eArray,intensArray = simulation_test.calculate_spectrum_on_slit(abscissas_array=energies,use_eV=1,is_quadrant=is_quadrant,do_plot=0)

    #**********************Saving results

    if fileName is not None:
        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        f.write("\n")
        scanCounter +=1
        f.write("#S %d Undulator spectrum calculation using pySRU\n"%(scanCounter))

        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
        f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
        f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))

        #
        # write flux to file
        #
        header="#N 4 \n#L PhotonEnergy[eV]  PhotonWavelength[A]  Flux[phot/sec/0.1%bw]  Spectral Power[W/eV]\n"
        f.write(header)

        for i in range(eArray.size):
            f.write(' ' + repr(eArray[i]) + '   ' + repr(m2ev/eArray[i]*1e10) + '    ' +
                    repr(intensArray[i]) + '    ' +
                    repr(intensArray[i]*codata.e*1e3) + '\n')
        f.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    return (eArray,intensArray)



def calc1d_srw(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,zero_emittance=False,
              srw_max_harmonic_number=None,fileName=None,fileAppend=False):

    r"""
        run SRW for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """

    global scanCounter

    t0 = time.time()
    print("Inside calc1d_srw")

    #derived
    #TODO calculate the numerical factor using codata
    #B0 = bl['Kv']/0.934/(bl['PeriodID']*1e2)

    cte = codata.e/(2*numpy.pi*codata.electron_mass*codata.c)
    B0 = bl['Kv']/bl['PeriodID']/cte


    if srw_max_harmonic_number == None:
        gamma = bl['ElectronEnergy'] / (codata_mee * 1e-3)

        resonance_wavelength = (1 + bl['Kv']**2 / 2.0) / 2 / gamma**2 * bl["PeriodID"]
        resonance_energy = m2ev / resonance_wavelength

        srw_max_harmonic_number = int(photonEnergyMax / resonance_energy * 1.1)
        print ("Max harmonic considered:%d ; Resonance energy: %g eV\n"%(srw_max_harmonic_number,resonance_energy))


    Nmax = srw_max_harmonic_number # 21,61

    print('Running SRW (SRWLIB Python)')

    #***********Undulator
    harmB = srwlib.SRWLMagFldH() #magnetic field harmonic
    harmB.n = 1 #harmonic number
    harmB.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB.B = B0 #magnetic field amplitude [T]

    und = srwlib.SRWLMagFldU([harmB])
    und.per = bl['PeriodID'] #period length [m]
    und.nPer = bl['NPeriods'] #number of periods (will be rounded to integer)

    #Container of all magnetic field elements
    magFldCnt = srwlib.SRWLMagFldC([und], srwlib.array('d', [0]), srwlib.array('d', [0]), srwlib.array('d', [0]))

    #***********Electron Beam
    eBeam = srwlib.SRWLPartBeam()
    eBeam.Iavg = bl['ElectronCurrent'] #average current [A]
    eBeam.partStatMom1.x = 0. #initial transverse positions [m]
    eBeam.partStatMom1.y = 0.
    eBeam.partStatMom1.z = 0. #initial longitudinal positions (set in the middle of undulator)
    eBeam.partStatMom1.xp = 0 #initial relative transverse velocities
    eBeam.partStatMom1.yp = 0
    eBeam.partStatMom1.gamma = bl['ElectronEnergy']*1e3/codata_mee #relative energy

    if zero_emittance:
        sigX     = 1e-25
        sigXp    = 1e-25
        sigY     = 1e-25
        sigYp    = 1e-25
        sigEperE = 1e-25
    else:
        sigX =  bl['ElectronBeamSizeH'] #horizontal RMS size of e-beam [m]
        sigXp = bl['ElectronBeamDivergenceH'] #horizontal RMS angular divergence [rad]
        sigY =  bl['ElectronBeamSizeV'] #vertical RMS size of e-beam [m]
        sigYp = bl['ElectronBeamDivergenceV'] #vertical RMS angular divergence [rad]
        sigEperE = bl['ElectronEnergySpread']

    print("calc1dSrw: starting calculation using ElectronEnergySpead=%e \n"%((sigEperE)))

    #2nd order stat. moments:
    eBeam.arStatMom2[0] = sigX*sigX #<(x-<x>)^2>
    eBeam.arStatMom2[1] = 0 #<(x-<x>)(x'-<x'>)>
    eBeam.arStatMom2[2] = sigXp*sigXp #<(x'-<x'>)^2>
    eBeam.arStatMom2[3] = sigY*sigY #<(y-<y>)^2>
    eBeam.arStatMom2[4] = 0 #<(y-<y>)(y'-<y'>)>
    eBeam.arStatMom2[5] = sigYp*sigYp #<(y'-<y'>)^2>
    eBeam.arStatMom2[10] = sigEperE*sigEperE #<(E-<E>)^2>/<E>^2

    #***********Precision Parameters
    arPrecF = [0]*5 #for spectral flux vs photon energy
    arPrecF[0] = 1 #initial UR harmonic to take into account
    arPrecF[1] = Nmax #final UR harmonic to take into account
    arPrecF[2] = 1.5 #longitudinal integration precision parameter
    arPrecF[3] = 1.5 #azimuthal integration precision parameter
    arPrecF[4] = 1 #calculate flux (1) or flux per unit surface (2)

    #***********UR Stokes Parameters (mesh) for Spectral Flux
    stkF = srwlib.SRWLStokes() #for spectral flux vs photon energy
    #srio stkF.allocate(10000, 1, 1) #numbers of points vs photon energy, horizontal and vertical positions
    stkF.allocate(photonEnergyPoints, 1, 1) #numbers of points vs photon energy, horizontal and vertical positions
    stkF.mesh.zStart = bl['distance'] #longitudinal position [m] at which UR has to be calculated
    stkF.mesh.eStart = photonEnergyMin #initial photon energy [eV]
    stkF.mesh.eFin =   photonEnergyMax #final photon energy [eV]
    stkF.mesh.xStart = -bl['gapH']/2 #initial horizontal position [m]
    stkF.mesh.xFin =    bl['gapH']/2 #final horizontal position [m]
    stkF.mesh.yStart = -bl['gapV']/2 #initial vertical position [m]
    stkF.mesh.yFin =    bl['gapV']/2 #final vertical position [m]

    #**********************Calculation (SRWLIB function calls)
    print('Performing Spectral Flux (Stokes parameters) calculation ... ') # , end='')

    srwlib.srwl.CalcStokesUR(stkF, eBeam, und, arPrecF)

    print('Done calc1dSrw calculation in %10.3f s'%(time.time()-t0))
    #**********************Saving results

    if fileName is not None:
        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        f.write("\n")
        scanCounter +=1
        f.write("#S %d Undulator spectrum calculation using SRW\n"%(scanCounter))

        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
        f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
        f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))
        f.write("#UD B0 =  %f\n"%(B0))

        #
        # write flux to file
        #
        header="#N 4 \n#L PhotonEnergy[eV]  PhotonWavelength[A]  Flux[phot/sec/0.1%bw]  Spectral Power[W/eV]\n"
        f.write(header)

    eArray = numpy.zeros(photonEnergyPoints)
    intensArray = numpy.zeros(photonEnergyPoints)
    for i in range(stkF.mesh.ne):
        ener = stkF.mesh.eStart+i*(stkF.mesh.eFin-stkF.mesh.eStart)/numpy.array((stkF.mesh.ne-1)).clip(min=1)
        if fileName is not None: f.write(' ' + repr(ener) + '   ' + repr(m2ev/ener*1e10) + '    ' +
                repr(stkF.arS[i]) + '    ' +
                repr(stkF.arS[i]*codata.e*1e3) + '\n')
        eArray[i] = ener
        intensArray[i] = stkF.arS[i]

    if fileName is not None:
        f.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))


    return (eArray,intensArray)

def calc1d_urgent(bl,photonEnergyMin=1000.0,photonEnergyMax=100000.0,photonEnergyPoints=500,zero_emittance=False,fileName=None,fileAppend=False):

    r"""
        run Urgent for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin

    print("Inside calc1d_urgent")

    t0 = time.time()
    for file in ["urgent.inp","urgent.out"]:
        try:
            os.remove(os.path.join(locations.home_bin_run(),file))
        except:
            pass

    with open("urgent.inp","wt") as f:
        f.write("%d\n"%(1))               # ITYPE
        f.write("%f\n"%(bl['PeriodID']))  # PERIOD
        f.write("%f\n"%(0.00000))         #KX
        f.write("%f\n"%(bl['Kv']))        #KY
        f.write("%f\n"%(0.00000))         #PHASE
        f.write("%d\n"%(bl['NPeriods']))         #N

        f.write("%f\n"%(photonEnergyMin))            #EMIN
        f.write("%f\n"%(photonEnergyMax))            #EMAX
        f.write("%d\n"%(photonEnergyPoints))         #NENERGY

        f.write("%f\n"%(bl['ElectronEnergy']))                #ENERGY
        f.write("%f\n"%(bl['ElectronCurrent']))               #CUR
        f.write("%f\n"%(bl['ElectronBeamSizeH']*1e3))         #SIGX
        f.write("%f\n"%(bl['ElectronBeamSizeV']*1e3))         #SIGY
        f.write("%f\n"%(bl['ElectronBeamDivergenceH']*1e3))   #SIGX1
        f.write("%f\n"%(bl['ElectronBeamDivergenceV']*1e3))   #SIGY1

        f.write("%f\n"%(bl['distance']))         #D
        f.write("%f\n"%(0.00000))         #XPC
        f.write("%f\n"%(0.00000))         #YPC
        f.write("%f\n"%(bl['gapH']*1e3))  #XPS
        f.write("%f\n"%(bl['gapV']*1e3))  #YPS
        f.write("%d\n"%(50))              #NXP
        f.write("%d\n"%(50))              #NYP

        f.write("%d\n"%(4))               #MODE
        if zero_emittance:                #ICALC
            f.write("%d\n"%(3))
        else:
            f.write("%d\n"%(1))
        f.write("%d\n"%(-1))              #IHARM

        f.write("%d\n"%(0))               #NPHI
        f.write("%d\n"%(0))               #NSIG
        f.write("%d\n"%(0))               #NALPHA
        f.write("%f\n"%(0.00000))         #DALPHA
        f.write("%d\n"%(0))               #NOMEGA
        f.write("%f\n"%(0.00000))         #DOMEGA

    command = "'" + os.path.join(home_bin,"urgent' < urgent.inp")
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    os.system(command)
    print('Done calc1dUrgent calculation in %10.3f s'%(time.time()-t0))
    # write spec file
    txt = open("urgent.out").readlines()
    if fileName is not None:

        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        f.write("\n")
        scanCounter +=1
        f.write("#S %d Undulator spectrum calculation using Urgent\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
        f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
        f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))

        f.write("#N 10\n")
        f.write("#L  Energy(eV)  Wavelength(A)  Flux(ph/s/0.1%bw)  Spectral Power(W/eV)  imin  imax  p1  p2  p3  p4\n")

    nArray = 0
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           nArray += 1
           tmp = tmp.replace('D','e')
           if fileName is not None: f.write(tmp)
        else:
           if fileName is not None: f.write("#UD "+tmp)

    if fileName is not None:
        f.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    # stores results in numpy arrays for return
    eArray = numpy.zeros(nArray)
    intensArray = numpy.zeros(nArray)
    iArray = -1
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           iArray += 1
           tmp = tmp.replace('D','e')
           tmpf = numpy.array( [float(j) for j in tmp.split()] )
           eArray[iArray] = tmpf[0]
           intensArray[iArray] = tmpf[2]



    return (eArray,intensArray)

def calc1d_us(bl,photonEnergyMin=1000.0,photonEnergyMax=100000.0,photonEnergyPoints=500,zero_emittance=False,fileName=None,fileAppend=False):

    r"""
        run US for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin


    t0 = time.time()
    for file in ["us.inp","us.out"]:
        try:
            os.remove(os.path.join(locations.home_bin_run(),file))
        except:
            pass


    print("Inside calc1d_us")
    with open("us.inp","wt") as f:

        f.write("US run\n")
        f.write("    %f  %f   %f                         Ring-Energy Current\n"%
               (bl['ElectronEnergy'],bl['ElectronCurrent']*1e3,bl['ElectronEnergySpread']))
        f.write("  %f  %f  %f  %f               Sx Sy Sxp Syp\n"%
               (bl['ElectronBeamSizeH']*1e3,bl['ElectronBeamSizeV']*1e3,
                bl['ElectronBeamDivergenceH']*1e3,bl['ElectronBeamDivergenceV']*1e3) )
        f.write("    %f      %d   0.000   %f               Period N Kx Ky\n"%
                (bl['PeriodID']*1e2,bl['NPeriods'],bl['Kv']) )
        f.write("    %f      %f     %d                   Emin Emax Ne\n"%
               (photonEnergyMin,photonEnergyMax,photonEnergyPoints) )
        f.write("  %f   0.000   0.000   %f   %f    50    50   D Xpc Ypc Xps Yps Nxp Nyp\n"%
               (bl['distance'],bl['gapH']*1e3,bl['gapV']*1e3) )
        # f.write("       4       4       0                       Mode Method Iharm\n")
        if zero_emittance:
            f.write("       4       3       0                       Mode Method Iharm\n")
        else:
            f.write("       4       4       0                       Mode Method Iharm\n")
        f.write("       0       0     0.0      64     8.0     0 Nphi Nalpha Dalpha2 Nomega Domega Nsigma\n")
        f.write("foreground\n")

    command = "'" + os.path.join(home_bin,'us') + "'"
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    os.system(command)
    print('Done calc1dUs calculation in %10.3f s'%(time.time()-t0))

    txt = open("us.out").readlines()
    # write spec file
    if fileName is not None:

        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        f.write("\n")
        scanCounter +=1
        f.write("#S %d Undulator spectrum calculation using US\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
        f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
        f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))

        f.write("#N 8\n")
        f.write("#L  Energy(eV)  Wavelength(A)  Flux(ph/s/0.1%bw)  SpectralPower(W/ev)  p1  p2  p3  p4\n")

    nArray = 0
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           tmp = tmp.replace('D','e')
           tmp = numpy.fromstring(tmp,dtype=float,sep=' ')
           if fileName is not None:
               f.write(("%g "*8+"\n")%(tmp[0],1e10*m2ev/tmp[0],tmp[1],tmp[1]*1e3*codata.e,tmp[2],tmp[3],tmp[4],tmp[5]))
           nArray  += 1
        else:
           if fileName is not None: f.write("#UD "+tmp)

    if fileName is not None:
        f.close()
        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    # stores results in numpy arrays for return
    eArray = numpy.zeros(nArray)
    intensArray = numpy.zeros(nArray)
    iArray = -1
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           iArray += 1
           tmp = tmp.replace('D','e')
           tmpf = numpy.array( [float(j) for j in tmp.split()] )
           eArray[iArray] = tmpf[0]
           intensArray[iArray] = tmpf[1]

    return (eArray,intensArray)





########################################################################################################################
#
# 2D: calc2d<code> Power density calculations
#
########################################################################################################################


def calc2d_pysru(bl,zero_emittance=False,hSlitPoints=51,vSlitPoints=51,
                photonEnergyMin=50.0,photonEnergyMax=2500.0,photonEnergyPoints=2451,
                fileName=None,fileAppend=False):

    e,h,v,i = calc3d_pysru(bl,zero_emittance=zero_emittance,
                photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                hSlitPoints=hSlitPoints,vSlitPoints=vSlitPoints,
                fileName=fileName,fileAppend=fileAppend)


    e_step = (photonEnergyMax - photonEnergyMin) / photonEnergyPoints
    plot(e,(i.sum(axis=2)).sum(axis=1)*(v[1]-v[0])*(h[1]-h[0]),show=0,title="Spectrum for %s"%bl)

    return (h,v,i.sum(axis=0)*e_step*codata.e*1e3)





def calc2d_srw(bl,zero_emittance=False,hSlitPoints=101,vSlitPoints=51,srw_max_harmonic_number=21,
              fileName=None,fileAppend=False,):

    r"""
        run SRW for calculating power density

        input: a dictionary with beamline
        output: file name with results
    """

    global scanCounter
    print("Inside calc2d_srw")
    #Maximum number of harmonics considered. This is critical for speed.
    #TODO: set it automatically to a reasonable value (see how is done by Urgent).
    Nmax = srw_max_harmonic_number # 21,61
    #derived
    #TODO calculate the numerical factor using codata
    # B0 = bl['Kv']/0.934/(bl['PeriodID']*1e2)
    cte = codata.e/(2*numpy.pi*codata.electron_mass*codata.c)
    B0 = bl['Kv']/bl['PeriodID']/cte

    print('Running SRW (SRWLIB Python)')

    #***********Undulator
    harmB = srwlib.SRWLMagFldH() #magnetic field harmonic
    harmB.n = 1 #harmonic number
    harmB.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB.B = B0 #magnetic field amplitude [T]

    und = srwlib.SRWLMagFldU([harmB])
    und.per = bl['PeriodID'] #period length [m]
    und.nPer = bl['NPeriods'] #number of periods (will be rounded to integer)

    #Container of all magnetic field elements
    magFldCnt = srwlib.SRWLMagFldC([und], array.array('d', [0]), array.array('d', [0]), array.array('d', [0]))

    #***********Electron Beam
    eBeam = srwlib.SRWLPartBeam()
    eBeam.Iavg = bl['ElectronCurrent'] #average current [A]
    eBeam.partStatMom1.x = 0. #initial transverse positions [m]
    eBeam.partStatMom1.y = 0.
    eBeam.partStatMom1.z = 0. #initial longitudinal positions (set in the middle of undulator)
    eBeam.partStatMom1.xp = 0 #initial relative transverse velocities
    eBeam.partStatMom1.yp = 0
    eBeam.partStatMom1.gamma = bl['ElectronEnergy']*1e3/codata_mee #relative energy

    if zero_emittance:
        sigEperE = 1e-25
        sigX     = 1e-25
        sigXp    = 1e-25
        sigY     = 1e-25
        sigYp    = 1e-25
    else:
        sigEperE = bl['ElectronEnergySpread'] #relative RMS energy spread
        sigX =  bl['ElectronBeamSizeH'] #horizontal RMS size of e-beam [m]
        sigXp = bl['ElectronBeamDivergenceH'] #horizontal RMS angular divergence [rad]
        sigY =  bl['ElectronBeamSizeV'] #vertical RMS size of e-beam [m]
        sigYp = bl['ElectronBeamDivergenceV'] #vertical RMS angular divergence [rad]

    #2nd order stat. moments:
    eBeam.arStatMom2[0] = sigX*sigX #<(x-<x>)^2>
    eBeam.arStatMom2[1] = 0 #<(x-<x>)(x'-<x'>)>
    eBeam.arStatMom2[2] = sigXp*sigXp #<(x'-<x'>)^2>
    eBeam.arStatMom2[3] = sigY*sigY #<(y-<y>)^2>
    eBeam.arStatMom2[4] = 0 #<(y-<y>)(y'-<y'>)>
    eBeam.arStatMom2[5] = sigYp*sigYp #<(y'-<y'>)^2>
    eBeam.arStatMom2[10] = sigEperE*sigEperE #<(E-<E>)^2>/<E>^2

    #***********Precision Parameters
    arPrecP = [0]*5 #for power density
    arPrecP[0] = 1.5 #precision factor
    arPrecP[1] = 1 #power density computation method (1- "near field", 2- "far field")
    arPrecP[2] = 0 #initial longitudinal position (effective if arPrecP[2] < arPrecP[3])
    arPrecP[3] = 0 #final longitudinal position (effective if arPrecP[2] < arPrecP[3])
    arPrecP[4] = 20000 #number of points for (intermediate) trajectory calculation

    #***********UR Stokes Parameters (mesh) for power densiyu
    stkP = srwlib.SRWLStokes() #for power density
    stkP.allocate(1, hSlitPoints, vSlitPoints) #numbers of points vs horizontal and vertical positions (photon energy is not taken into account)
    stkP.mesh.zStart = bl['distance'] #longitudinal position [m] at which power density has to be calculated
    stkP.mesh.xStart = -bl['gapH']/2 #initial horizontal position [m]
    stkP.mesh.xFin =    bl['gapH']/2 #final horizontal position [m]
    stkP.mesh.yStart = -bl['gapV']/2 #initial vertical position [m]
    stkP.mesh.yFin =    bl['gapV']/2 #final vertical position [m]

    #**********************Calculation (SRWLIB function calls)
    print('Performing Power Density calculation (from field) ... ')
    t0 = time.time()
    srwlib.srwl.CalcPowDenSR(stkP, eBeam, 0, magFldCnt, arPrecP)
    print('Done Performing Power Density calculation (from field).')

    #**********************Saving results

    if fileName is not None:
        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        #
        # write power density to file as mesh scan
        #
        scanCounter +=1
        f.write("\n#S %d Undulator power density calculation using SRW\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write('\n#U B0 = ' + repr(B0 ) + '\n' )
        f.write('\n#U hSlitPoints = ' + repr(hSlitPoints) + '\n' )
        f.write('\n#U vSlitPoints = ' + repr(vSlitPoints) + '\n' )
        f.write("#N 3 \n#L H[mm]  V[mm]  PowerDensity[W/mm^2] \n" )

    hArray = numpy.zeros(stkP.mesh.nx)
    vArray = numpy.zeros(stkP.mesh.ny)
    totPower = numpy.array(0.0)

    hProfile = numpy.zeros(stkP.mesh.nx)
    vProfile = numpy.zeros(stkP.mesh.ny)
    powerArray = numpy.zeros((stkP.mesh.nx,stkP.mesh.ny))

    # fill arrays
    ij = -1
    for j in range(stkP.mesh.ny):
        for i in range(stkP.mesh.nx):
            ij += 1
            xx = stkP.mesh.xStart + i*(stkP.mesh.xFin-stkP.mesh.xStart)/(stkP.mesh.nx-1)
            yy = stkP.mesh.yStart + j*(stkP.mesh.yFin-stkP.mesh.yStart)/(stkP.mesh.ny-1)
            #ij = i*stkP.mesh.nx + j
            totPower += stkP.arS[ij]
            powerArray[i,j] = stkP.arS[ij]
            hArray[i] = xx*1e3 # mm
            vArray[j] = yy*1e3 # mm

    # dump
    if fileName is not None:
        for i in range(stkP.mesh.nx):
            for j in range(stkP.mesh.ny):
                f.write(repr(hArray[i]) + ' ' + repr(vArray[j]) + ' ' + repr(powerArray[i,j]) + '\n')


    totPower = totPower * \
               (stkP.mesh.xFin-stkP.mesh.xStart)/(stkP.mesh.nx-1)*1e3 * \
               (stkP.mesh.yFin-stkP.mesh.yStart)/(stkP.mesh.ny-1)*1e3
    hStep = (stkP.mesh.xFin-stkP.mesh.xStart)/(stkP.mesh.nx-1)

    # dump profiles
    if fileName is not None:


        scanCounter +=1
        f.write("\n#S %d Undulator power density calculation using SRW: H profile\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write( "#UD Total power [W]: "+repr(totPower)+"\n")
        f.write( "#UD FWHM [mm] : "+repr(calc_fwhm(hProfile,hStep)[0]*1e3)+"\n")
        f.write( "#N 2 \n")
        f.write( "#L H[mm]  PowerDensityCentralProfile[W/mm2] \n" )
        for i in range(stkP.mesh.nx):
            #xx = stkP.mesh.xStart + i*hStep
            #f.write(repr(xx*1e3) + ' ' + repr(hProfile[i]) + '\n')
            f.write(repr(hArray[i]) + ' ' + \
                    repr(powerArray[i,int(len(vArray)/2)]) + '\n')

        scanCounter +=1
        vStep = (stkP.mesh.yFin-stkP.mesh.yStart)/(stkP.mesh.ny-1)
        f.write("\n#S %d Undulator power density calculation using SRW: V profile\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write( "#UD Total power [W]: "+repr(totPower)+"\n")
        f.write( "#UD FWHM [mm] : "+repr(calc_fwhm(vProfile,vStep)[0]*1e3)+"\n")
        f.write( "#N 2 \n")
        f.write( "#L V[mm]  PowerDensityCentralProfile[W/mm2] \n" )
        for j in range(stkP.mesh.ny):
            f.write(repr(vArray[j]) + ' ' +  \
                    repr(powerArray[int(len(hArray)/2),j]) + '\n')

        f.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    print( "Total power SRW [W]: "+repr(totPower))

    return (hArray, vArray, powerArray)


def calc2d_us(bl,zero_emittance=False,hSlitPoints=51,vSlitPoints=51,fileName=None,fileAppend=False):

    r"""
        run US for calculating power density

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc2d_us")

    for file in ["us.inp","us.out"]:
        try:
            os.remove(os.path.join(locations.home_bin_run(),file))
        except:
            pass

    with open("us.inp","wt") as f:
        #f.write("%d\n"%(1))               # ITYPE
        #f.write("%f\n"%(bl['PeriodID']))  # PERIOD

        f.write("US run\n")
        f.write("    %f  %f  %f                           Ring-Energy Current\n"%
               (bl['ElectronEnergy'],bl['ElectronCurrent']*1e3,bl['ElectronEnergySpread']))
        f.write("  %f  %f  %f  %f               Sx Sy Sxp Syp\n"%
               (bl['ElectronBeamSizeH']*1e3,bl['ElectronBeamSizeV']*1e3,
                bl['ElectronBeamDivergenceH']*1e3,bl['ElectronBeamDivergenceV']*1e3) )





        f.write("    %f      %d   0.000   %f               Period N Kx Ky\n"%
                (bl['PeriodID']*1e2,bl['NPeriods'],bl['Kv']) )
        f.write("    9972.1   55000.0     500                   Emin Emax Ne\n")
        f.write("  %f   0.000   0.000   %f   %f    %d    %d   D Xpc Ypc Xps Yps Nxp Nyp\n"%
               (bl['distance'],bl['gapH']*1e3,bl['gapV']*1e3,hSlitPoints-1,vSlitPoints-1) )
        if zero_emittance:
            f.write("       6       3       0                       Mode Method Iharm\n")
        else:
            f.write("       6       1       0                       Mode Method Iharm\n")
        f.write("       0       0     0.0      64     8.0     0 Nphi Nalpha Dalpha2 Nomega Domega Nsigma\n")
        f.write("foreground\n")

    command = "'" + os.path.join(home_bin,'us') + "'"
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("Done.")
    print("\n--------------------------------------------------------\n")

    txt = open("us.out").readlines()
    # write spec file

    if fileName is not None:



        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        f.write("\n")
        scanCounter +=1
        f.write("#S %d Undulator power density calculation using US\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#N 7\n")
        f.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]  p1  p2  p3  p4\n")

    mesh = numpy.zeros((7,(hSlitPoints)*(vSlitPoints)))
    hh = numpy.zeros((hSlitPoints))
    vv = numpy.zeros((vSlitPoints))
    int_mesh = numpy.zeros( ((hSlitPoints),(vSlitPoints)) )
    imesh = -1
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           if fileName is not None: f.write(tmp)
           tmpf = numpy.array( [float(j) for j in tmp.split()] )
           imesh = imesh + 1
           mesh[:,imesh] = tmpf
        else:
           if fileName is not None: f.write("#UD "+tmp)

    imesh = -1
    for i in range(hSlitPoints):
        for j in range(vSlitPoints):
            imesh = imesh + 1
            hh[i] = mesh[0,imesh]
            vv[j] = mesh[1,imesh]
            int_mesh[i,j] = mesh[2,imesh]

    hhh = numpy.concatenate((-hh[::-1],hh[1:]))
    vvv = numpy.concatenate((-vv[::-1],vv[1:]))

    tmp = numpy.concatenate( (int_mesh[::-1,:],int_mesh[1:,:]), axis=0)
    int_mesh2 = numpy.concatenate( (tmp[:,::-1],tmp[:,1:]),axis=1)

    if fileName is not None:
        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using US (whole slit)\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#N 3\n")
        f.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]\n")
        for i in range(len(hhh)):
            for j in range(len(vvv)):
               f.write("%f  %f  %f\n"%(hhh[i],vvv[j],int_mesh2[i,j]) )


    totPower = int_mesh2.sum() * (hh[1]-hh[0]) * (vv[1]-vv[0])

    if fileName is not None:
        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using US: H profile\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#UD Total power [W]: "+repr(totPower)+"\n")
        f.write("#N 2\n")
        f.write("#L  H[mm]  PowerDensity[W/mm2]\n")
        for i in range(len(hhh)):
           f.write("%f  %f\n"%(hhh[i],int_mesh2[i,int(len(vvv)/2)]) )

        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using US: V profile\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#UD Total power [W]: "+repr(totPower)+"\n")
        f.write("#N 2\n")
        f.write("#L  V[mm]  PowerDensity[W/mm2]\n")
        for i in range(len(vvv)):
           f.write("%f  %f\n"%(vvv[i],int_mesh2[int(len(hhh)/2),i]) )

        f.close()


        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    print( "Total power US [W]: "+repr(totPower))
    return (hhh, vvv, int_mesh2)


def calc2d_urgent(bl,zero_emittance=False,fileName=None,fileAppend=False,hSlitPoints=21,vSlitPoints=51):

    r"""
        run Urgent for calculating power density

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc2d_urgent")

    for file in ["urgent.inp","urgent.out"]:
        try:
            os.remove(os.path.join(locations.home_bin_run(),file))
        except:
            pass

    with open("urgent.inp","wt") as f:
        f.write("%d\n"%(1))               # ITYPE
        f.write("%f\n"%(bl['PeriodID']))  # PERIOD
        f.write("%f\n"%(0.00000))         #KX
        f.write("%f\n"%(bl['Kv']))        #KY
        f.write("%f\n"%(0.00000))         #PHASE
        f.write("%d\n"%(bl['NPeriods']))         #N

        f.write("1000.0\n")                #EMIN
        f.write("100000.0\n")              #EMAX
        f.write("1\n")                     #NENERGY

        f.write("%f\n"%(bl['ElectronEnergy']))                #ENERGY
        f.write("%f\n"%(bl['ElectronCurrent']))               #CUR
        f.write("%f\n"%(bl['ElectronBeamSizeH']*1e3))         #SIGX
        f.write("%f\n"%(bl['ElectronBeamSizeV']*1e3))         #SIGY
        f.write("%f\n"%(bl['ElectronBeamDivergenceH']*1e3))   #SIGX1
        f.write("%f\n"%(bl['ElectronBeamDivergenceV']*1e3))   #SIGY1

        f.write("%f\n"%(bl['distance']))         #D
        f.write("%f\n"%(0.00000))         #XPC
        f.write("%f\n"%(0.00000))         #YPC
        f.write("%f\n"%(bl['gapH']*1e3))  #XPS
        f.write("%f\n"%(bl['gapV']*1e3))  #YPS
        f.write("%d\n"%(hSlitPoints-1))             #NXP
        f.write("%d\n"%(vSlitPoints-1))             #NYP

        f.write("%d\n"%(6))               #MODE
        if zero_emittance:                #ICALC
            f.write("%d\n"%(2))
        else:
            f.write("%d\n"%(1))
        f.write("%d\n"%(-200))             #IHARM   TODO: check max harmonic number

        f.write("%d\n"%(0))               #NPHI
        f.write("%d\n"%(0))               #NSIG
        f.write("%d\n"%(0))               #NALPHA
        f.write("%f\n"%(0.00000))         #DALPHA
        f.write("%d\n"%(0))               #NOMEGA
        f.write("%f\n"%(0.00000))         #DOMEGA

    command = "'" + os.path.join(home_bin,"urgent' < urgent.inp")
    print("\n\n--------------------------------------------------------\n")
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    os.system(command)
    print("Done.")

    # write spec file
    txt = open("urgent.out").readlines()

    if fileName is not None:
        if fileAppend:
            f = open(fileName,"a")
        else:
            scanCounter = 0
            f = open(fileName,"w")
            f.write("#F "+fileName+"\n")

        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using Urgent (a slit quadrant)\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#N 4\n")
        f.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]  Flux[Phot/s/0.1%bw]\n")

    mesh = numpy.zeros((4,(hSlitPoints)*(vSlitPoints)))
    hh = numpy.zeros((hSlitPoints))
    vv = numpy.zeros((vSlitPoints))
    int_mesh = numpy.zeros( ((hSlitPoints),(vSlitPoints)) )
    imesh = -1
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           if fileName is not None: f.write(tmp)
           tmp = tmp.replace('D','e')
           tmpf = numpy.array( [float(j) for j in tmp.split()] )
           imesh = imesh + 1
           mesh[:,imesh] = tmpf
        else:
           if len(tmp) > 0:  # remove the last block
               if tmp.split(" ")[0] == 'HARMONIC':
                   break
           if fileName is not None: f.write("#UD "+tmp)

    imesh = -1
    for i in range(hSlitPoints):
        for j in range(vSlitPoints):
            imesh = imesh + 1
            hh[i] = mesh[0,imesh]
            vv[j] = mesh[1,imesh]
            int_mesh[i,j] = mesh[2,imesh]

    hhh = numpy.concatenate((-hh[::-1],hh[1:]))
    vvv = numpy.concatenate((-vv[::-1],vv[1:]))

    tmp = numpy.concatenate( (int_mesh[::-1,:],int_mesh[1:,:]), axis=0)
    int_mesh2 = numpy.concatenate( (tmp[:,::-1],tmp[:,1:]),axis=1)
    totPower = int_mesh2.sum() * (hh[1]-hh[0]) * (vv[1]-vv[0])

    if fileName is not None:
        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using Urgent (whole slit)\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#N 3\n")
        f.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]\n")
        for i in range(len(hhh)):
            for j in range(len(vvv)):
               f.write("%f  %f  %f\n"%(hhh[i],vvv[j],int_mesh2[i,j]) )




        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using Urgent: H profile\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#UD Total power [W]: "+repr(totPower)+"\n")
        f.write("#N 2\n")
        f.write("#L  H[mm]  PowerDensity[W/mm2]\n")
        for i in range(len(hhh)):
           f.write("%f  %f\n"%(hhh[i],int_mesh2[i,int(len(vvv)/2)]) )

        scanCounter += 1
        f.write("\n#S %d Undulator power density calculation using Urgent: V profile\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#UD Total power [W]: "+repr(totPower)+"\n")
        f.write("#N 2\n")
        f.write("#L  V[mm]  PowerDensity[W/mm2]\n")
        for i in range(len(vvv)):
           f.write("%f  %f\n"%(vvv[i],int_mesh2[int(len(hhh)/2),i]) )


        f.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    print( "Total power URGENT [W]: "+repr(totPower))
    print("\n--------------------------------------------------------\n\n")

    return (hhh, vvv, int_mesh2)



########################################################################################################################
#
# 3D: calc3d<code> Emission calculations
#
########################################################################################################################
def calc3d_srw(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,
               zero_emittance=False,hSlitPoints=51,vSlitPoints=51,
               fileName=None,fileAppend=False):

    r"""
        run SRW for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """

    global scanCounter

    print("Inside calc3d_srw")

    if fileName is not None:
        if fileAppend:
            fout = open(fileName,"a")
        else:
            scanCounter = 0
            fout = open(fileName,"w")
            fout.write("#F "+fileName+"\n")


    #TODO calculate the numerical factor using codata
    # B0 = bl['Kv']/0.934/(bl['PeriodID']*1e2)
    cte = codata.e/(2*numpy.pi*codata.electron_mass*codata.c)
    B0 = bl['Kv']/bl['PeriodID']/cte

    print('Running SRW (SRWLIB Python)')


    if zero_emittance:
        eBeam = _srw_electron_beam(E=bl['ElectronEnergy'],Iavg=bl['ElectronCurrent'],) # no emmitance now
    else:
        eBeam = _srw_electron_beam(E=bl['ElectronEnergy'], sigE = bl['ElectronEnergySpread'], Iavg=bl['ElectronCurrent'],
                     sigX=bl['ElectronBeamSizeH'], sigY=bl['ElectronBeamSizeV'],
                     sigXp=bl['ElectronBeamDivergenceH'], sigYp=bl['ElectronBeamDivergenceV'])



    #***********Precision Parameters

    mesh = srwlib.SRWLRadMesh(photonEnergyMin,photonEnergyMax,photonEnergyPoints,
                              -bl['gapH']/2,bl['gapH']/2,hSlitPoints,
                              -bl['gapV']/2,bl['gapV']/2,vSlitPoints,bl['distance'])


    #
    # #***********UR Stokes Parameters (mesh) for Spectral Flux
    # stkF = srwlib.SRWLStokes() #for spectral flux vs photon energy
    # stkF.allocate(photonEnergyPoints, hSlitPoints, vSlitPoints) #numbers of points vs photon energy, horizontal and vertical positions
    # stkF.mesh.zStart = bl['distance'] #longitudinal position [m] at which UR has to be calculated
    # stkF.mesh.eStart = photonEnergyMin #initial photon energy [eV]
    # stkF.mesh.eFin =   photonEnergyMax #final photon energy [eV]
    # stkF.mesh.xStart = -bl['gapH']/2 #initial horizontal position [m]
    # stkF.mesh.xFin =    bl['gapH']/2 #final horizontal position [m]
    # stkF.mesh.yStart = -bl['gapV']/2 #initial vertical position [m]
    # stkF.mesh.yFin =    bl['gapV']/2 #final vertical position [m]

    #**********************Calculation (SRWLIB function calls)
    print('Performing Spectral Flux 3d calculation ... ') # , end='')
    t0 = time.time()


    if zero_emittance:
        #
        # single electron
        #
        und0 = srwlib.SRWLMagFldU([srwlib.SRWLMagFldH(1, 'v', B0)],bl['PeriodID'],bl['NPeriods'])
        und = srwlib.SRWLMagFldC([und0],array.array('d', [0]), array.array('d', [0]), array.array('d', [0]))

        # arPrecS = [0]*7 #for electric field and single-electron intensity
        # arPrecS[0] = 1 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
        # arPrecS[1] = 0.01 #relative precision
        # arPrecS[2] = 0 #longitudinal position to start integration (effective if < zEndInteg)
        # arPrecS[3] = 0 #longitudinal position to finish integration (effective if > zStartInteg)
        # arPrecS[4] = 20000 #Number of points for intermediate trajectory calculation
        # arPrecS[5] = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        # arPrecS[6] = -1 #0.1 #sampling factor for adjusting nx, ny (effective if > 0)

        paramSE = [1, 0.01, 0, 0, 50000, 1, 0]

        wfr = srwlib.SRWLWfr()
        wfr.mesh = mesh
        wfr.partBeam = eBeam
        wfr.allocate(mesh.ne, mesh.nx, mesh.ny)
        # eBeam = SrwDriftElectronBeam(eBeam, und)
        srwlib.srwl.CalcElecFieldSR(wfr, 0, und, paramSE)
        stk = srwlib.SRWLStokes()
        stk.mesh = mesh
        stk.allocate(mesh.ne, mesh.nx, mesh.ny)
        # eBeam = SrwDriftElectronBeam(eBeam, -eBeam.moved)
        wfr.calc_stokes(stk)

        # Stokes0ToSpec(stk,fname=fileName)
        #
        # intensArray,eArray,hArray,vArray = Stokes0ToArrays(stk)



        Shape = (4,stk.mesh.ny,stk.mesh.nx,stk.mesh.ne)
        data = numpy.ndarray(buffer=stk.arS, shape=Shape,dtype=stk.arS.typecode)
        data0 = data #[0]
        hArray = numpy.linspace(stk.mesh.xStart,stk.mesh.xFin,stk.mesh.nx)
        vArray = numpy.linspace(stk.mesh.yStart,stk.mesh.yFin,stk.mesh.ny)
        eArray = numpy.linspace(stk.mesh.eStart,stk.mesh.eFin,stk.mesh.ne)
        # intensArray = numpy.zeros((eArray.size,hArray.size,vArray.size))
        intensArray = numpy.zeros((eArray.size,hArray.size,vArray.size))
        for ie in range(eArray.size):
          for ix in range(hArray.size):
              for iy in range(vArray.size):
                # intensArray[ie,ix,iy] = data0[iy,ix,ie]
                intensArray[ie,ix,iy,] = data[0,iy,ix,ie]

    else:
        #
        # convolution
        #
        und0 = srwlib.SRWLMagFldU([srwlib.SRWLMagFldH(1, 'v', B0)],bl['PeriodID'],bl['NPeriods'])
        und = srwlib.SRWLMagFldC([und0],array.array('d', [0]), array.array('d', [0]), array.array('d', [0]))

        # arPrecS = [0]*7 #for electric field and single-electron intensity
        # arPrecS[0] = 1 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
        # arPrecS[1] = 0.01 #relative precision
        # arPrecS[2] = 0 #longitudinal position to start integration (effective if < zEndInteg)
        # arPrecS[3] = 0 #longitudinal position to finish integration (effective if > zStartInteg)
        # arPrecS[4] = 20000 #Number of points for intermediate trajectory calculation
        # arPrecS[5] = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        # arPrecS[6] = -1 #0.1 #sampling factor for adjusting nx, ny (effective if > 0)

        paramME = [1, 0.01, 0, 0, 50000, 1, 0]

        wfr = srwlib.SRWLWfr()
        wfr.mesh = mesh
        wfr.partBeam = eBeam
        wfr.allocate(mesh.ne, mesh.nx, mesh.ny)
        # eBeam = _srw_drift_electron_beam(eBeam, und)
        srwlib.srwl.CalcElecFieldSR(wfr, 0, und, paramME)



        #
        # Extract intensity
        #

        mesh0 = wfr.mesh
        # arI0 = array.array('f', [0]*mesh0.nx*mesh0.ny) #"flat" array to take 2D intensity data
        # arI0 = array.array('f', [0]*mesh0.nx*mesh0.ny*mesh.ne) #"flat" array to take 2D intensity data

        INTENSITY_TYPE_SINGLE_ELECTRON=0
        INTENSITY_TYPE_MULTI_ELECTRON=1

        hArray=numpy.linspace(wfr.mesh.xStart,wfr.mesh.xFin, wfr.mesh.nx)
        vArray=numpy.linspace(wfr.mesh.yStart,wfr.mesh.yFin, wfr.mesh.ny)
        eArray=numpy.linspace(wfr.mesh.eStart,wfr.mesh.eFin, wfr.mesh.ne)

        intensArray = numpy.zeros((eArray.size,hArray.size,vArray.size,))
        for ie in range(eArray.size):
            arI0 = array.array('f', [0]*mesh0.nx*mesh0.ny) #"flat" array to take 2D intensity data
            # 6 is for total polarizarion; 0=H, 1=V
            srwlib.srwl.CalcIntFromElecField(arI0, wfr, 6, INTENSITY_TYPE_MULTI_ELECTRON, 3, eArray[ie], 0, 0)

            Shape = (mesh0.ny,mesh0.nx)
            data = numpy.ndarray(buffer=arI0, shape=Shape,dtype=arI0.typecode)

            for ix in range(hArray.size):
                for iy in range(vArray.size):
                    intensArray[ie,ix,iy,] = data[iy,ix]



    print('  done\n')
    print('  saving SE Stokes...')
    print('Done Performing Spectral Flux 3d calculation in sec '+str(time.time()-t0))


    if fileName is not None:
        for ie in range(eArray.size):
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using SRW at E=%6.3f eV (whole slit )\n"%(scanCounter,eArray[ie]))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hArray.size))
            fout.write("#UD vSlitPoints =  %f\n"%(vArray.size))
            fout.write("#N 3\n")
            fout.write("#L  H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]\n")
            for i in range(len(hArray)):
                for j in range(len(vArray)):
                   fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],intensArray[ie,i,j]) )

        fout.close()
        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    # grid in mm
    return (eArray, 1e3*hArray, 1e3*vArray, intensArray)



def calc3d_urgent(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,
                  zero_emittance=False,hSlitPoints=50,vSlitPoints=50,
                  fileName=None,fileAppend=False,):

    r"""
        run Urgent for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc3d_urgent")


    if fileName is not None:
        if fileAppend:
            fout = open(fileName,"a")
        else:
            scanCounter = 0
            fout = open(fileName,"w")
            fout.write("#F "+fileName+"\n")

    if photonEnergyPoints == 1:
        eStep = 0.0
    else:
        eStep = (photonEnergyMax-photonEnergyMin)/(photonEnergyPoints-1)
    eArray = numpy.zeros( photonEnergyPoints )
    intensArray = numpy.zeros( photonEnergyPoints )
    hArray = numpy.zeros( (hSlitPoints*2-1) )
    vArray = numpy.zeros( (vSlitPoints*2-1) )
    int_mesh2integrated = numpy.zeros( (hSlitPoints*2-1,vSlitPoints*2-1) )
    int_mesh3 = numpy.zeros( (photonEnergyPoints,hSlitPoints*2-1,vSlitPoints*2-1) )

    for iEner in range(photonEnergyPoints):
        ener = photonEnergyMin + iEner*eStep
        eArray[iEner] = ener

        for file in ["urgent.inp","urgent.out"]:
            try:
                os.remove(os.path.join(locations.home_bin_run(),file))
            except:
                pass

        with open("urgent.inp","wt") as f:
            f.write("%d\n"%(1))               # ITYPE
            f.write("%f\n"%(bl['PeriodID']))  # PERIOD
            f.write("%f\n"%(0.00000))         #KX
            f.write("%f\n"%(bl['Kv']))        #KY
            f.write("%f\n"%(0.00000))         #PHASE
            f.write("%d\n"%(bl['NPeriods']))         #N

            f.write("%f\n"%(ener))       #EMIN
            f.write("100000.0\n")              #EMAX
            f.write("1\n")                     #NENERGY

            f.write("%f\n"%(bl['ElectronEnergy']))                #ENERGY
            f.write("%f\n"%(bl['ElectronCurrent']))               #CUR
            f.write("%f\n"%(bl['ElectronBeamSizeH']*1e3))         #SIGX
            f.write("%f\n"%(bl['ElectronBeamSizeV']*1e3))         #SIGY
            f.write("%f\n"%(bl['ElectronBeamDivergenceH']*1e3))   #SIGX1
            f.write("%f\n"%(bl['ElectronBeamDivergenceV']*1e3))   #SIGY1

            f.write("%f\n"%(bl['distance']))         #D
            f.write("%f\n"%(0.00000))         #XPC
            f.write("%f\n"%(0.00000))         #YPC
            f.write("%f\n"%(bl['gapH']*1e3))  #XPS
            f.write("%f\n"%(bl['gapV']*1e3))  #YPS
            f.write("%d\n"%(hSlitPoints-1))     #NXP
            f.write("%d\n"%(vSlitPoints-1))     #NYP

            f.write("%d\n"%(1))               #MODE
            if zero_emittance:                #ICALC
                f.write("%d\n"%(3))
            else:
                f.write("%d\n"%(1))
            f.write("%d\n"%(-81))             #IHARM   TODO: check max harmonic number

            f.write("%d\n"%(0))               #NPHI
            f.write("%d\n"%(0))               #NSIG
            f.write("%d\n"%(0))               #NALPHA
            f.write("%f\n"%(0.00000))         #DALPHA
            f.write("%d\n"%(0))               #NOMEGA
            f.write("%f\n"%(0.00000))         #DOMEGA

        command = "'" + os.path.join(home_bin,"urgent' < urgent.inp")
        print("\n\n--------------------------------------------------------\n")
        print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
        os.system(command)
        print("Done.")

        shutil.copy2("urgent.inp","urgent_energy_index%d.inp"%iEner)
        shutil.copy2("urgent.out","urgent_energy_index%d.out"%iEner)
        # write spec file
        txt = open("urgent.out").readlines()



        if fileName is not None:
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Urgent at E=%0.3f keV (a slit quadrant)\n"%(scanCounter,ener*1e-3))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
            fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
            fout.write("#N 7\n")
            fout.write("#L  H[mm]  V[mm]  Flux[Phot/s/mm^2/0.1%bw]  l1  l2  l3  l4\n")

        if zero_emittance:
            mesh = numpy.zeros((8,(hSlitPoints)*(vSlitPoints)))
        else:
            mesh = numpy.zeros((7,(hSlitPoints)*(vSlitPoints)))
        hh = numpy.zeros((hSlitPoints))
        vv = numpy.zeros((vSlitPoints))
        int_mesh = numpy.zeros( ((hSlitPoints),(vSlitPoints)) )
        imesh = -1
        for i in txt:
            tmp = i.strip(" ")
            if tmp[0].isdigit():
               if fileName is not None:
                   fout.write(tmp)
               tmp = tmp.replace('D','e')
               tmpf = numpy.array( [float(j) for j in tmp.split()] )
               imesh = imesh + 1
               mesh[:,imesh] = tmpf
            else:
               if fileName is not None:
                   fout.write("#UD "+tmp)

        imesh = -1
        for i in range(hSlitPoints):
            for j in range(vSlitPoints):
                imesh = imesh + 1
                hh[i] = mesh[0,imesh]
                vv[j] = mesh[1,imesh]
                int_mesh[i,j] = mesh[2,imesh]

        hArray = numpy.concatenate((-hh[::-1],hh[1:]))
        vArray = numpy.concatenate((-vv[::-1],vv[1:]))
        #hArray = hhh*0.0
        #vArray = vvv*0.0
        totIntens = 0.0

        tmp = numpy.concatenate( (int_mesh[::-1,:],int_mesh[1:,:]), axis=0)
        int_mesh2 = numpy.concatenate( (tmp[:,::-1],tmp[:,1:]),axis=1)

        if fileName is not None:
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Urgent at E=%6.3f eV (whole slit )\n"%(scanCounter,ener))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
            fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
            fout.write("#N 3\n")
            fout.write("#L  H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]\n")
        for i in range(len(hArray)):
            for j in range(len(vArray)):
               if fileName is not None: fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],int_mesh2[i,j]) )
               int_mesh3[iEner,i,j] = int_mesh2[i,j]
               int_mesh2integrated[i,j] += int_mesh2[i,j]
               totIntens += int_mesh2[i,j]

        totIntens = totIntens * (hh[1]-hh[0]) * (vv[1]-vv[0])
        intensArray[iEner] = totIntens


    # now dump the integrated power
    # convert from phot/s/0,1%bw/mm2 to W/mm^2
    int_mesh2integrated = int_mesh2integrated *codata.e*1e3 * eStep

    if fileName is not None:
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density vs H,E (integrated in energy) calculation using Urgent\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        fout.write("#UD IntegratedPower[W] =  %f\n"%( int_mesh2integrated.sum()*(hArray[1]-hArray[0])*(vArray[1]-vArray[0])))
        fout.write("#N 3\n")
        fout.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]\n")
        for i in range(len(hArray)):
            for j in range(len(vArray)):
                fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],int_mesh2integrated[i,j]) )
        #print(">>>>>>>>>>>>>>>power1",int_mesh2integrated.sum()*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))
        #print(">>>>>>>>>>>>>>>power2",intensArray.sum()*codata.e*1e3*(eArray[1]-eArray[0]))
        #print(">>>>>>>>>>>>>>>power3",int_mesh3.sum()*codata.e*1e3*(eArray[1]-eArray[0])*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))

        # now dump the spectrum as the sum
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density vs energy (integrated in H,V) calculation using Urgent\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        if photonEnergyPoints > 1:
            fout.write("#UD IntegratedPower[W] =  %f\n"%(intensArray.sum()*codata.e*1e3*(eArray[1]-eArray[0])))
        fout.write("#N 3\n")
        fout.write("#L  photonEnergy[eV]  Flux[phot/s/0.1%bw]  PowerDensity[W/eV]\n")
        for i in range(photonEnergyPoints):
           fout.write("%f  %f  %f\n"%(eArray[i],intensArray[i],intensArray[i]*codata.e*1e3) )

        fout.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    print("\n--------------------------------------------------------\n\n")
    # append direct calculation for comparison
    tmp = calc1d_urgent(bl,photonEnergyMin=photonEnergyMin,
                  photonEnergyMax=photonEnergyMax,
                  photonEnergyPoints=photonEnergyPoints,
                  fileName=fileName,fileAppend=True)
    # return abscissas in mm
    return  (eArray, hArray, vArray, int_mesh3)



def calc3d_us(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,
              zero_emittance=False,hSlitPoints=50,vSlitPoints=50,
              fileName=None,fileAppend=True,):

    r"""
        run Us for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc3d_us")



    if fileName is not None:
        if fileAppend:
            fout = open(fileName,"a")
        else:
            scanCounter = 0
            fout = open(fileName,"w")
            fout.write("#F "+fileName+"\n")

    if photonEnergyPoints == 1:
        eStep = 0.0
    else:
        eStep = (photonEnergyMax-photonEnergyMin)/(photonEnergyPoints-1)
    eArray = numpy.zeros( photonEnergyPoints )
    intensArray = numpy.zeros( photonEnergyPoints )
    hArray = numpy.zeros( (hSlitPoints*2-1) )
    vArray = numpy.zeros( (vSlitPoints*2-1) )
    int_mesh2integrated = numpy.zeros( (hSlitPoints*2-1,vSlitPoints*2-1) )
    int_mesh3 = numpy.zeros( (photonEnergyPoints,hSlitPoints*2-1,vSlitPoints*2-1) )

    for iEner in range(photonEnergyPoints):
        ener = photonEnergyMin + iEner*eStep
        eArray[iEner] = ener

        for file in ["us.inp","us.out"]:
            try:
                os.remove(os.path.join(locations.home_bin_run(),file))
            except:
                pass

        with open("us.inp","wt") as f:
            #f.write("%d\n"%(1))               # ITYPE
            #f.write("%f\n"%(bl['PeriodID']))  # PERIOD

            f.write("US run\n")
            f.write("    %f  %f  %f                           Ring-Energy Current\n"%
                   (bl['ElectronEnergy'],bl['ElectronCurrent']*1e3,bl['ElectronEnergySpread']))
            f.write("  %f  %f  %f  %f               Sx Sy Sxp Syp\n"%
                   (bl['ElectronBeamSizeH']*1e3,bl['ElectronBeamSizeV']*1e3,
                    bl['ElectronBeamDivergenceH']*1e3,bl['ElectronBeamDivergenceV']*1e3) )
            f.write("    %f      %d   0.000   %f               Period N Kx Ky\n"%
                    (bl['PeriodID']*1e2,bl['NPeriods'],bl['Kv']) )
            f.write("    %f   55000.0       1                   Emin Emax Ne\n"%(ener))
            f.write("  %f   0.000   0.000   %f   %f    %d    %d   D Xpc Ypc Xps Yps Nxp Nyp\n"%
                   (bl['distance'],bl['gapH']*1e3,bl['gapV']*1e3,hSlitPoints-1,vSlitPoints-1) )
            if zero_emittance:
                f.write("       1       3       0                       Mode Method Iharm\n")
            else:
                f.write("       1       1       0                       Mode Method Iharm\n")
            f.write("       0       0     0.0      64     8.0     0 Nphi Nalpha Dalpha2 Nomega Domega Nsigma\n")
            f.write("foreground\n")

        command = "'" + os.path.join(home_bin,'us') + "'"
        print("\n\n--------------------------------------------------------\n")
        print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
        os.system(command)
        print("Done.")

        shutil.copy2("us.inp","us_energy_index%d.inp"%iEner)
        shutil.copy2("us.out","us_energy_index%d.out"%iEner)
        # shutil.copy2("us.log","us%d.log"%iEner)

        # write spec file
        txt = open("us.out").readlines()


        if fileName is not None:
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Us at E=%6.3f eV (a slit quadrant)\n"%(scanCounter,ener))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
            fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
            fout.write("#N 7\n")
            fout.write("#L  H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]  p1  p2  p3  p4\n")

        mesh = numpy.zeros((7,(hSlitPoints)*(vSlitPoints)))
        hh = numpy.zeros((hSlitPoints))
        vv = numpy.zeros((vSlitPoints))
        int_mesh = numpy.zeros( ((hSlitPoints),(vSlitPoints)) )
        imesh = -1
        for i in txt:
            tmp = i.strip(" ")
            if tmp[0].isdigit():
               if fileName is not None:
                   fout.write(tmp)
               #tmp = tmp.replace('D','e')
               tmpf = numpy.array( [float(j) for j in tmp.split()] )
               imesh = imesh + 1
               mesh[:,imesh] = tmpf
            else:
               if fileName is not None:
                   fout.write("#UD "+tmp)

        imesh = -1
        for i in range(hSlitPoints):
            for j in range(vSlitPoints):
                imesh = imesh + 1
                hh[i] = mesh[0,imesh]
                vv[j] = mesh[1,imesh]
                int_mesh[i,j] = mesh[2,imesh]

        hArray = numpy.concatenate((-hh[::-1],hh[1:]))
        vArray = numpy.concatenate((-vv[::-1],vv[1:]))
        totIntens = 0.0

        tmp = numpy.concatenate( (int_mesh[::-1,:],int_mesh[1:,:]), axis=0)
        int_mesh2 = numpy.concatenate( (tmp[:,::-1],tmp[:,1:]),axis=1)

        if fileName is not None:
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Us at E=%6.3f eV (whole slit )\n"%(scanCounter,ener))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
            fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
            fout.write("#N 3\n")
            fout.write("#L  H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]\n")

        for i in range(len(hArray)):
            for j in range(len(vArray)):
               if fileName is not None:
                   fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],int_mesh2[i,j]) )
               int_mesh3[iEner,i,j] = int_mesh2[i,j]
               int_mesh2integrated[i,j] += int_mesh2[i,j]
               totIntens += int_mesh2[i,j]

        totIntens = totIntens * (hh[1]-hh[0]) * (vv[1]-vv[0])
        intensArray[iEner] = totIntens


    # now dump the integrated power
    # convert from phot/s/0,1%bw/mm2 to W/mm^2
    int_mesh2integrated = int_mesh2integrated *codata.e*1e3 * eStep

    # print(">>>>>>>>>>>>>>>power1",int_mesh2integrated.sum()*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))
    # if photonEnergyPoints > 1:
    #     print(">>>>>>>>>>>>>>>power2",intensArray.sum()*codata.e*1e3*(eArray[1]-eArray[0]))
    #     print(">>>>>>>>>>>>>>>power3",int_mesh3.sum()*codata.e*1e3*(eArray[1]-eArray[0])*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))

    if fileName is not None:
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density vs H,E (integrated in energy) calculation using Us\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        fout.write("#UD IntegratedPower[W] =  %f\n"%( int_mesh2integrated.sum()*(hArray[1]-hArray[0])*(vArray[1]-vArray[0])))
        fout.write("#N 3\n")
        fout.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]\n")
        for i in range(len(hArray)):
            for j in range(len(vArray)):
                fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],int_mesh2integrated[i,j]) )



        # now dump the spectrum as the sum
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density vs energy (integrated in H,V) calculation using Us\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        if photonEnergyPoints > 1:
            fout.write("#UD IntegratedPower[W] =  %f\n"%(intensArray.sum()*codata.e*1e3*(eArray[1]-eArray[0])))
        fout.write("#N 3\n")
        fout.write("#L  photonEnergy[eV]  Flux[phot/s/0.1%bw]  PowerDensity[W/eV]\n")
        for i in range(photonEnergyPoints):
           fout.write("%f   %f  %f\n"%(eArray[i],intensArray[i],intensArray[i]*codata.e*1e3) )

        fout.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    # append direct calculation for comparison
    tmp = calc1d_us(bl,photonEnergyMin=photonEnergyMin,
                  photonEnergyMax=photonEnergyMax,
                  photonEnergyPoints=photonEnergyPoints,
                  fileName=fileName,fileAppend=True)
    print("\n--------------------------------------------------------\n\n")

    # grid in mn
    return  (eArray, hArray, vArray, int_mesh3)


def calc3d_pysru(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,
                 zero_emittance=False,hSlitPoints=51,vSlitPoints=51,
                 fileName=None,fileAppend=True):

    r"""
        run pySRU for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """

    from pySRU.Simulation import create_simulation
    from pySRU.ElectronBeam import ElectronBeam
    from pySRU.MagneticStructureUndulatorPlane import MagneticStructureUndulatorPlane
    from pySRU.TrajectoryFactory import TrajectoryFactory, TRAJECTORY_METHOD_ANALYTIC,TRAJECTORY_METHOD_ODE

    from pySRU.RadiationFactory import RadiationFactory,RADIATION_METHOD_NEAR_FIELD, \
                                     RADIATION_METHOD_APPROX_FARFIELD

    global scanCounter

    print("Inside calc3d_pysru")

    if fileName is not None:
        if fileAppend:
            fout = open(fileName,"a")
        else:
            scanCounter = 0
            fout = open(fileName,"w")
            fout.write("#F "+fileName+"\n")


    print('Running pySRU')

    # Example_spectrum_on_central_cone()

    hArray = numpy.linspace(-0.5*bl['gapH'], 0.5*bl['gapH'],hSlitPoints)
    vArray = numpy.linspace(-0.5*bl['gapV'], 0.5*bl['gapV'],vSlitPoints)
    H = numpy.outer(hArray,numpy.ones_like(vArray))
    V = numpy.outer(numpy.ones_like(hArray),vArray)
    eArray = numpy.linspace(photonEnergyMin,photonEnergyMax,photonEnergyPoints)

    myBeam = ElectronBeam(Electron_energy=bl['ElectronEnergy'], I_current=bl['ElectronCurrent'])
    myUndulator = MagneticStructureUndulatorPlane(K=bl['Kv'], period_length=bl['PeriodID'], length=bl['PeriodID']*bl['NPeriods'])



    intensArray = numpy.zeros((photonEnergyPoints,hArray.size,vArray.size))

    method = 0
    if method == 0:   # recreate simulation object at each step
        for ie in range(eArray.size):
            print(">> pySRU running energy point %d of %d..."%(ie+1,eArray.size))
            simulation_test = create_simulation(magnetic_structure=myUndulator,electron_beam=myBeam,
                                magnetic_field=None, photon_energy=eArray[ie],
                                traj_method=TRAJECTORY_METHOD_ODE,Nb_pts_trajectory=None,
                                rad_method=RADIATION_METHOD_NEAR_FIELD, Nb_pts_radiation=None,
                                initial_condition=None, distance=bl['distance'],XY_are_list=False,
                                X=hArray,Y=vArray)

            # simulation_test.radiation.plot("title=photon energy = %f"%eArray[ie])
            tmp = simulation_test.radiation.intensity.copy()
            intensArray[ie] = tmp
    elif method == 1:
        #create simulation object for the highest energy
        simulation_test = create_simulation(magnetic_structure=myUndulator,electron_beam=myBeam,
                            magnetic_field=None, photon_energy=eArray[-1],
                            traj_method=TRAJECTORY_METHOD_ODE,Nb_pts_trajectory=None,
                            rad_method=RADIATION_METHOD_NEAR_FIELD, Nb_pts_radiation=None,
                            initial_condition=None, distance=bl['distance'],XY_are_list=False,
                            X=hArray,Y=vArray)
        for ie in range(eArray.size):
            print(">> pySRU setting new energy point %d of %d..."%(ie+1,eArray.size))
            simulation_test.change_energy_eV(eArray[ie],update_radiation=1)
            # simulation_test.radiation.plot("title=photon energy = %f"%eArray[ie])
            tmp = simulation_test.radiation.intensity.copy()
            intensArray[ie] = tmp
    else:
        raise Exception("Not implemented method.")



    #
    # testing convolution for non zero emittance
    #
    if not zero_emittance:
        from scipy.ndimage.filters import convolve as convolve
        from scipy.ndimage.filters import gaussian_filter1d as gaussian_filter1d
        SigmaH = numpy.sqrt( bl['ElectronBeamSizeH']**2 + (bl['distance']*bl['ElectronBeamDivergenceH'])**2 )
        SigmaV = numpy.sqrt( bl['ElectronBeamSizeV']**2 + (bl['distance']*bl['ElectronBeamDivergenceV'])**2 )
        tmp1 = numpy.exp(-H*H/2/SigmaH/SigmaH) * numpy.exp(-V*V/2/SigmaV/SigmaV)
        for ie in range(eArray.size):
            # pass
            #OK  intensArray[ie] = convolve(intensArray[ie],tmp1)/tmp1.sum()
            intensArray[ie] = gaussian_filter1d(intensArray[ie],SigmaH/(hArray[1]-hArray[0]),axis=0)
            intensArray[ie] = gaussian_filter1d(intensArray[ie],SigmaV/(vArray[1]-vArray[0]),axis=1)
            # intensArray[ie] = gaussian_filter1d(tmp1,SigmaV,axis=1)

    if fileName is not None:
        for ie in range(eArray.size):
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density vs H,E (integrated in energy) calculation using pySRU et E=%f eV\n"%
                       (scanCounter,eArray[ie]))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
            fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
            # fout.write("#UD IntegratedPower[W] =  %f\n"%( int_mesh2integrated.sum()*(hArray[1]-hArray[0])*(vArray[1]-vArray[0])))
            fout.write("#N 3\n")
            fout.write("#L  H[mm]  V[mm]  PowerDensity[W/mm^2]\n")
            for i in range(len(hArray)):
                for j in range(len(vArray)):
                    fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],intensArray[ie,i,j]) )


        # now dump the spectrum as the sum
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density vs energy (integrated in H,V) calculation using pySRU\n"%(scanCounter))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        if photonEnergyPoints > 1:
            fout.write("#UD IntegratedPower[W] =  %f\n"%(intensArray.sum()*codata.e*1e3*(eArray[1]-eArray[0])))
        fout.write("#N 3\n")
        fout.write("#L  photonEnergy[eV]  Flux[phot/s/0.1%bw]  PowerDensity[W/eV]\n")
        for i in range(photonEnergyPoints):
           fout.write("%f   %f  %f\n"%(eArray[i],intensArray[i].sum(),intensArray[i].sum()*codata.e*1e3) )

        fout.close()

        if fileAppend:
            print("Data appended to file: %s"%(os.path.join(os.getcwd(),fileName)))
        else:
            print("File written to disk: %s"%(os.path.join(os.getcwd(),fileName)))

    # append direct calculation for comparison
    # tmp = calc1d_us(bl,photonEnergyMin=photonEnergyMin,
    #               photonEnergyMax=photonEnergyMax,
    #               photonEnergyPoints=photonEnergyPoints,
    #               fileName=fileName,fileAppend=True)
    print("\n--------------------------------------------------------\n\n")

    # grid in mm
    return (eArray, 1e3*hArray, 1e3*vArray, intensArray)

########################################################################################################################
#
# Do 3d calculations and obtain power density and spectrum by integration
#
########################################################################################################################

def calc_from_3d(code,bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=5,
                npoints_grid=101,zero_emittance=False,fileName=None,fileAppend=False):

    if code == "pySRU":
        e,h,v,i = calc3d_pysru(bl,zero_emittance=zero_emittance,fileName=fileName,
                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                    hSlitPoints=npoints_grid,vSlitPoints=npoints_grid)
    elif code == "SRW":
        e,h,v,i = calc3d_srw(bl,zero_emittance=zero_emittance,fileName=fileName,
                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                    hSlitPoints=npoints_grid,vSlitPoints=npoints_grid)
    elif code == "US":
        e,h,v,i = calc3d_us(bl,zero_emittance=zero_emittance,fileName=fileName,
                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                    hSlitPoints=npoints_grid,vSlitPoints=npoints_grid)
    elif code == "URGENT":
        e,h,v,i = calc3d_urgent(bl,zero_emittance=zero_emittance,fileName=fileName,
                    photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                    hSlitPoints=npoints_grid,vSlitPoints=npoints_grid)
    else:
        raise Exception("Undefined code")

    e_step = (photonEnergyMax - photonEnergyMin) / photonEnergyPoints
    # plot(e,(i.sum(axis=2)).sum(axis=1)*(v[1]-v[0])*(h[1]-h[0]),show=0,title="Spectrum for %s"%bl)
    # plot_contour(i.sum(axis=0)*e_step*codata.e*1e3,h,v,title="PySRU Power density",show=0)

    out = {"e":e,"h":h,"v":v,"radiance":i,
           "power_density":i.sum(axis=0)*e_step*codata.e*1e3,
           "spectrum":(i.sum(axis=2)).sum(axis=1)*(v[1]-v[0])*(h[1]-h[0])}
    return out

########################################################################################################################
#
# Tuning curves on a slit
#
########################################################################################################################

def tuning_curves_on_slit(bl,Kmin=0.2,Kmax=2.2,Kpoints=10,harmonics=[1],zero_emittance=False,
                          do_plot_peaks=False,code='srw'):

    if do_plot_peaks:
        from srxraylib.plot.gol import plot
    #

    #
    # calculations
    #

    gamma = bl["ElectronEnergy"]* 1e9 / (codata.m_e *  codata.c**2 / codata.e)
    Kvalues = numpy.linspace(Kmin,Kmax,Kpoints)

    # B0 = 93.6 * bl['PeriodID'] / kvalues
    lambda1 = bl['PeriodID'] * (1+0.5*Kvalues**2) / 2 / gamma**2
    lambda1shifted = lambda1 + 0.5 * bl['PeriodID'] * (bl["gapV"] / bl["distance"])**2
    energy1 = codata.h * codata.c / codata.e / lambda1
    energy1shifted = codata.h * codata.c / codata.e / lambda1shifted
    energy1delta = energy1 - energy1shifted

    flux_values = numpy.zeros((Kpoints,len(harmonics)))
    evalues = numpy.zeros((Kpoints,len(harmonics)))
    evalues_at_flux_peak = numpy.zeros((Kpoints,len(harmonics)))
    #
    #
    for ik,k in enumerate(Kvalues):
        bl['Kv'] = k
        print("\n-------- tuning_curves_on_slit: calculating flux for Kv: %f4.3"%k)
        for ih,harmonic in enumerate(harmonics):

            if code == "srw":
                e_s,f_s = calc1d_srw(bl,
                                photonEnergyMin=(harmonic*energy1[ik]-(1.0/harmonic)*energy1delta[ik]),
                                photonEnergyMax=harmonic*energy1[ik],
                                photonEnergyPoints=100,zero_emittance=zero_emittance,fileName=None,fileAppend=False)
            elif code == "us":
                e_s,f_s = calc1d_us(bl,
                                photonEnergyMin=(harmonic*energy1[ik]-(1.0/harmonic)*energy1delta[ik]),
                                photonEnergyMax=harmonic*energy1[ik],
                                photonEnergyPoints=100,zero_emittance=zero_emittance,fileName=None,fileAppend=False)
            elif code == "urgent":
                e_s,f_s = calc1d_urgent(bl,
                                photonEnergyMin=(harmonic*energy1[ik]-(1.0/harmonic)*energy1delta[ik]),
                                photonEnergyMax=harmonic*energy1[ik],
                                photonEnergyPoints=100,zero_emittance=zero_emittance,fileName=None,fileAppend=False)
            else:
                raise Exception("Not implemented code %s"%code)


            max_at = numpy.argmax(f_s)
            flux_values[ik,ih] = f_s[max_at]
            evalues[ik,ih] = harmonic*energy1[ik]
            evalues_at_flux_peak[ik,ih] = e_s[max_at]

            if do_plot_peaks:
                plot(e_s,f_s,ylog=False,title="K=%4.2f, n=%d"%(k,harmonic))


    #
    # calculate power
    #
    Pvalues = numpy.zeros_like(Kvalues)

    for ik,k in enumerate(Kvalues):
        bl['Kv'] = k
        print("\n-------- tuning_curves_on_slit: calculating power for Kv: %4.3f"%k)

        if code == "srw":
            h,v,p = calc2d_srw(bl,zero_emittance=zero_emittance,hSlitPoints=51,vSlitPoints=51,
                       srw_max_harmonic_number=51,fileName=None,fileAppend=False,)
            tot_power = p.sum()*(h[1]-h[0])*(v[1]-v[0])
        elif code == "us":
            h,v,p = calc2d_us(bl,zero_emittance=zero_emittance,hSlitPoints=51,vSlitPoints=51,
                       fileName=None,fileAppend=False,)
            tot_power = p.sum()*(h[1]-h[0])*(v[1]-v[0])
        elif code == "urgent":
            h,v,p = calc2d_urgent(bl,zero_emittance=zero_emittance,hSlitPoints=51,vSlitPoints=51,
                       fileName=None,fileAppend=False,)
            tot_power = p.sum()*(h[1]-h[0])*(v[1]-v[0])
        else:
            raise Exception("Not implemented code %s"%code)

        Pvalues[ik] = tot_power


    print("\n\nHarmonic     Kv     Resonance [eV]    Flux peak [eV]   Total Power on slit [eV]")
    for ih in range(len(harmonics)):
        for i in range(Kvalues.size):
            print("%10d%17.3f%17.3f%17.3f%17.3f"%
                  (harmonics[ih],Kvalues[i],evalues[i,ih],evalues_at_flux_peak[i,ih],Pvalues[i]))

    return Kvalues,harmonics,Pvalues,evalues_at_flux_peak,flux_values,

########################################################################################################################
#
# Tools
#
########################################################################################################################

def calc_fwhm(h,binSize):
  t = numpy.where(h>=max(h)*0.5)
  return binSize*(t[0][-1]-t[0][0]+1), t[0][-1], t[0][0]




def _srw_electron_beam(E=6.0, sigE = 1.e-30, Iavg=0.2,sigX=1.e-30, sigY=1.e-30, sigXp=1.e-30, sigYp=1.e-30):

    # #2nd order stat. moments:
    # eBeam.arStatMom2[0] = sigX*sigX #<(x-<x>)^2>
    # eBeam.arStatMom2[1] = 0 #<(x-<x>)(x'-<x'>)>
    # eBeam.arStatMom2[2] = sigXp*sigXp #<(x'-<x'>)^2>
    # eBeam.arStatMom2[3] = sigY*sigY #<(y-<y>)^2>
    # eBeam.arStatMom2[4] = 0 #<(y-<y>)(y'-<y'>)>
    # eBeam.arStatMom2[5] = sigYp*sigYp #<(y'-<y'>)^2>
    # eBeam.arStatMom2[10] = sigEperE*sigEperE #<(E-<E>)^2>/<E>^2

    el_rest = codata_mee * 1e-3 # 0.51099890221e-03
    eBeam = srwlib.SRWLPartBeam()
    eBeam.Iavg = Iavg
    eBeam.partStatMom1.gamma =  E / el_rest


    # always fixed here
    eBeam.partStatMom1.relE0 =  1.0
    eBeam.partStatMom1.nq    = -1
    eBeam.arStatMom2[1]   = 0.0
    eBeam.arStatMom2[4]   = 0.0
    eBeam.partStatMom1.x  = 0.0
    eBeam.partStatMom1.y  = 0.0
    eBeam.partStatMom1.z  = 0.0
    eBeam.partStatMom1.xp = 0.0
    eBeam.partStatMom1.yp = 0.0

    #from inputs
    eBeam.arStatMom2[ 0] = sigX**2
    eBeam.arStatMom2[ 2] = sigXp**2
    eBeam.arStatMom2[ 3] = sigY**2
    eBeam.arStatMom2[ 5] = sigYp**2
    eBeam.arStatMom2[10] = sigE**2

    return eBeam

def _srw_drift_electron_beam(eBeam, und ):
    if isinstance(und, float):
        length = und
    elif isinstance(und, srwlib.SRWLMagFldU):    # Always defined in (0., 0., 0.) move the electron beam before the magnetic field.
        length = 0.0-0.55*und.nPer*und.per-eBeam.partStatMom1.z
    elif isinstance(und, srwlib.SRWLMagFldC):
        if isinstance(und.arMagFld[0], srwlib.SRWLMagFldU):
            length = und.arZc[0]-0.55*und.arMagFld[0].nPer*und.arMagFld[0].per-eBeam.partStatMom1.z
        else: raise NameError
    else: raise NameError
    eBeam.partStatMom1.z += length
    eBeam.arStatMom2[0]  += 2*length*eBeam.arStatMom2[1]+length**2*eBeam.arStatMom2[2]
    eBeam.arStatMom2[1]  += length*eBeam.arStatMom2[2]
    eBeam.arStatMom2[3]  += 2*length*eBeam.arStatMom2[4]+length**2*eBeam.arStatMom2[5]
    eBeam.arStatMom2[4]  += length*eBeam.arStatMom2[5]
    eBeam.moved = length
    return eBeam


########################################################################################################################
#
# Comparison scripts
#
########################################################################################################################
def compare_flux(beamline,emin=3000.0,emax=50000.0,npoints=200,
                 zero_emittance=False,fileName=None,):


    gamma = beamline['ElectronEnergy'] / (codata_mee * 1e-3)
    print ("Gamma: %f \n"%(gamma))

    resonance_wavelength = (1 + beamline['Kv']**2 / 2.0) / 2 / gamma**2 * beamline["PeriodID"]
    resonance_energy = m2ev / resonance_wavelength

    print ("Resonance wavelength [A]: %g \n"%(1e10*resonance_wavelength))
    print ("Resonance energy [eV]: %g \n"%(resonance_energy))

    if emin == None:
        emin = resonance_energy - 5000
        emax = resonance_energy + 5000

    print("Calculating %d spectrum points in [%f,%f] eV"%(npoints,emin,emax))

    data = []
    legend = []

    if USE_SRWLIB:
        e_s,f_s = calc1d_srw(beamline,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True,
                             srw_max_harmonic_number=None)
        print("Power from integral of SRW spectrum: %f W"%(f_s.sum()*1e3*codata.e*(e_s[1]-e_s[0])))
        beamline["calc1d_srw"] = {"energy":e_s,"flux":f_s}


    if USE_URGENT:
        e_ur,f_ur = calc1d_urgent(beamline,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        print("Power from integral of URGENT spectrum: %f W"%(f_ur.sum()*1e3*codata.e*(e_ur[1]-e_ur[0])))
        beamline["calc1d_urgent"] = {"energy":e_ur,"flux":f_ur}


    if USE_US:
        e_us,f_us = calc1d_us(beamline,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        print("Power from integral of US spectrum: %f W"%(f_us.sum()*1e3*codata.e*(e_us[1]-e_us[0])))
        beamline["calc1d_us"] = {"energy":e_us,"flux":f_us}


    if USE_PYSRU:
        e_py,f_py = calc1d_pysru(beamline,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        print("Power from integral of pySRU spectrum: %f W"%(f_py.sum()*1e3*codata.e*(e_py[1]-e_py[0])))
        beamline["calc1d_pysru"] = {"energy":e_py,"flux":f_py}


    return beamline

def plot_flux(beamline_dict,plot_lin=True,plot_log=True,show=True):
    data = []
    legend = []
    for key in ["calc1d_us","calc1d_urgent","calc1d_pysru","calc1d_srw"]:
        if key in beamline_dict.keys():
            data.append(beamline_dict[key]["energy"])
            data.append(beamline_dict[key]["flux"])
            legend.append(key)

    if plot_lin: plot(data,title=beamline_dict['name'],show=False,legend=legend,ylog=True)
    if plot_log: plot(data,title=beamline_dict['name'],show=False,legend=legend,ylog=False)
    if show: plot_show()


def compare_flux_from_3d(beamline,emin=3000.0,emax=50000.0,npoints=10,
                 zero_emittance=False,fileName=None,iplot=False,show=True):

    gamma = beamline['ElectronEnergy'] / (codata_mee * 1e-3)
    print ("Gamma: %f \n"%(gamma))

    resonance_wavelength = (1 + beamline['Kv']**2 / 2.0) / 2 / gamma**2 * beamline["PeriodID"]
    resonance_energy = m2ev / resonance_wavelength

    print ("Resonance wavelength [A]: %g \n"%(1e10*resonance_wavelength))
    print ("Resonance energy [eV]: %g \n"%(resonance_energy))

    if emin == None:
        emin = resonance_energy - 5000
        emax = resonance_energy + 5000

    print("Calculating %d spectrum points in [%f,%f] eV"%(npoints,emin,emax))

    npoints_grid = 51

    if USE_PYSRU:
        r_pysru = calc_from_3d("pySRU",  beamline,photonEnergyMin=emin,photonEnergyMax=emax,photonEnergyPoints=npoints,
                             npoints_grid=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
    if USE_SRWLIB:
        r_srw = calc_from_3d("SRW",      beamline,photonEnergyMin=emin,photonEnergyMax=emax,photonEnergyPoints=npoints,
                                 npoints_grid=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
    r_us = calc_from_3d("US",        beamline,photonEnergyMin=emin,photonEnergyMax=emax,photonEnergyPoints=npoints,
                             npoints_grid=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
    r_urgent = calc_from_3d("URGENT",beamline,photonEnergyMin=emin,photonEnergyMax=emax,photonEnergyPoints=npoints,
                             npoints_grid=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)



    if iplot:
        if USE_PYSRU and USE_SRWLIB:
            plot(r_pysru["e"],r_pysru["spectrum"],
                 r_srw["e"],r_srw["spectrum"],
                 r_us["e"],r_us["spectrum"],
                 r_urgent["e"],r_urgent["spectrum"],
                 title=beamline,show=0,legend=["pySRU","SRW","US","URGENT"],ylog=True)
            plot(r_pysru["e"],r_pysru["spectrum"],
                 r_srw["e"],r_srw["spectrum"],
                 r_us["e"],r_us["spectrum"],
                 r_urgent["e"],r_urgent["spectrum"],
                 title=beamline,show=0,legend=["pySRU","SRW","US","URGENT"],ylog=False)
        else:
            if USE_PYSRU:
                plot(r_pysru["e"],r_pysru["spectrum"],
                     r_us["e"],r_us["spectrum"],
                     r_urgent["e"],r_urgent["spectrum"],
                     title=beamline,show=0,legend=["pySRU","US","URGENT"],ylog=True)
                plot(r_pysru["e"],r_pysru["spectrum"],
                     r_us["e"],r_us["spectrum"],
                     r_urgent["e"],r_urgent["spectrum"],
                     title=beamline,show=0,legend=["pySRU","US","URGENT"],ylog=False)
            elif USE_SRWLIB:
                plot(r_srw["e"],r_srw["spectrum"],
                     r_us["e"],r_us["spectrum"],
                     r_urgent["e"],r_urgent["spectrum"],
                     title=beamline,show=0,legend=["SRW","US","URGENT"],ylog=True)
                plot(r_srw["e"],r_srw["spectrum"],
                     r_us["e"],r_us["spectrum"],
                     r_urgent["e"],r_urgent["spectrum"],
                     title=beamline,show=0,legend=["SRW","US","URGENT"],ylog=False)
            else:
                plot(r_us["e"],r_us["spectrum"],
                     r_urgent["e"],r_urgent["spectrum"],
                     title=beamline,show=0,legend=["US","URGENT"],ylog=True)
                plot(r_us["e"],r_us["spectrum"],
                     r_urgent["e"],r_urgent["spectrum"],
                     title=beamline,show=0,legend=["US","URGENT"],ylog=False)


        if show:
            plot_show()


def compare_power_density(beamline,npoints_grid=40,zero_emittance=False,fileName=None,post_convolution=False):

    if post_convolution:
        zero_emittance = True
        from scipy.ndimage.filters import convolve as convolve
        from scipy.ndimage.filters import gaussian_filter1d as gaussian_filter1d
        SigmaH = numpy.sqrt( beamline['ElectronBeamSizeH']**2 + (beamline['distance']*beamline['ElectronBeamDivergenceH'])**2 )
        SigmaV = numpy.sqrt( beamline['ElectronBeamSizeV']**2 + (beamline['distance']*beamline['ElectronBeamDivergenceV'])**2 )

        # H = numpy.outer(h,numpy.ones_like(v))
        # V = numpy.outer(numpy.ones_like(h),v)
        # tmp1 = numpy.exp(-H*H/2/SigmaH/SigmaH) * numpy.exp(-V*V/2/SigmaV/SigmaV)
        # p = convolve(p,tmp1)/tmp1.sum()




    if USE_US:
        h, v, p =     calc2d_us(beamline,hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        if post_convolution:
            p1 = gaussian_filter1d(p ,SigmaH/(h[1]-h[0]),axis=0)
            p  = gaussian_filter1d(p1,SigmaV/(v[1]-v[0]),axis=1)

            # H = numpy.outer(h,numpy.ones_like(v))
            # V = numpy.outer(numpy.ones_like(h),v)
            # tmp1 = numpy.exp(-H*H/2/SigmaH/SigmaH) * numpy.exp(-V*V/2/SigmaV/SigmaV)
            # p = convolve(p,tmp1)/tmp1.sum()

        print("Total power US: ",p.sum()*(h[1]-h[0])*(v[1]-v[0]))
        beamline["calc2d_us"] = {"h":h,"v":v,"p":p}

    if USE_URGENT:
        h, v, p = calc2d_urgent(beamline,hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        if post_convolution:
            p1 = gaussian_filter1d(p ,SigmaH/(h[1]-h[0]),axis=0,mode='mirror')
            p  = gaussian_filter1d(p1,SigmaV/(v[1]-v[0]),axis=1,mode='mirror')

            # H = numpy.outer(h,numpy.ones_like(v))
            # V = numpy.outer(numpy.ones_like(h),v)
            # tmp1 = numpy.exp(-H*H/2/SigmaH/SigmaH) * numpy.exp(-V*V/2/SigmaV/SigmaV)
            # p = convolve(p,tmp1)/tmp1.sum()
        print("Total power URGENT: ",p.sum()*(h[1]-h[0])*(v[1]-v[0]))
        beamline["calc2d_urgent"] = {"h":h,"v":v,"p":p}

    if USE_SRWLIB:
        h, v, p = calc2d_srw(beamline,hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        if post_convolution:
            p1 = gaussian_filter1d(p ,SigmaH/(h[1]-h[0]),axis=0)
            p  = gaussian_filter1d(p1,SigmaV/(v[1]-v[0]),axis=1)


            # H = numpy.outer(h,numpy.ones_like(v))
            # V = numpy.outer(numpy.ones_like(h),v)
            # tmp1 = numpy.exp(-H*H/2/SigmaH/SigmaH) * numpy.exp(-V*V/2/SigmaV/SigmaV)
            # p = convolve(p,tmp1)/tmp1.sum()
        print("Total power SRW: ",p.sum()*(h[1]-h[0])*(v[1]-v[0]))
        beamline["calc2d_srw"] = {"h":h,"v":v,"p":p}

    if USE_PYSRU:
        h, v, p = calc2d_pysru(beamline,hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        if post_convolution:
            p1 = gaussian_filter1d(p ,SigmaH/(h[1]-h[0]),axis=0)
            p  = gaussian_filter1d(p1,SigmaV/(v[1]-v[0]),axis=1)

            # H = numpy.outer(h,numpy.ones_like(v))
            # V = numpy.outer(numpy.ones_like(h),v)
            # tmp1 = numpy.exp(-H*H/2/SigmaH/SigmaH) * numpy.exp(-V*V/2/SigmaV/SigmaV)
            # p = convolve(p,tmp1)/tmp1.sum()

        print("Total power pySRU: ",p.sum()*(h[1]-h[0])*(v[1]-v[0]))
        beamline["calc2d_pysru"] = {"h":h,"v":v,"p":p}

    if post_convolution:
        print("Post-convolution with sigmaH: %f mm, sigmaV: %f mm"%(1e3*SigmaH,1e3*SigmaV))
    return beamline

def plot_power_density(beamline_dict,show=True,contour=True,surface=True):


    cmax = -100000.0
    for key in ["calc2d_us","calc2d_urgent","calc2d_pysru","calc2d_srw"]:
        if key in beamline_dict.keys():
            h = beamline_dict[key]["h"]
            v = beamline_dict[key]["v"]
            p = beamline_dict[key]["p"]
            cmax = numpy.max([cmax,p.max()])

    contour_levels = numpy.linspace(0,cmax,100)

    for key in ["calc2d_us","calc2d_urgent","calc2d_pysru","calc2d_srw"]:
        if key in beamline_dict.keys():
            h = beamline_dict[key]["h"]
            v = beamline_dict[key]["v"]
            p = beamline_dict[key]["p"]

            if contour: plot_contour(p,h,v,title="%s %s"%(beamline_dict['name'],key),
                         xtitle="H [mm]",ytitle="V [mm]",plot_points=0,
                         contour_levels=contour_levels,cmap=None,cbar=1,cbar_title="Power density [$W/mm^2$]",show=0)
            if surface: plot_surface(p,h,v,title="%s %s"%(beamline_dict['name'],key),xtitle="H [mm]",ytitle="V [mm]",show=0)

    if show:
        plot_show()

def compare_radiation(beamline,
                      photonEnergyMin=None,photonEnergyMax=100000.0,photonEnergyPoints=1,
                      npoints_grid=51,
                      zero_emittance=False,fileName=None):



    gamma = beamline['ElectronEnergy'] / (codata_mee * 1e-3)
    print ("Gamma: %f \n"%(gamma))

    resonance_wavelength = (1 + beamline['Kv']**2 / 2.0) / 2 / gamma**2 * beamline["PeriodID"]
    resonance_energy = m2ev / resonance_wavelength

    print ("Resonance wavelength [A]: %g \n"%(1e10*resonance_wavelength))
    print ("Resonance energy [eV]: %g \n"%(resonance_energy))

    if photonEnergyMin == None:
        photonEnergyMin = resonance_energy
        photonEnergyMax = resonance_energy
        photonEnergyPoints = 1



    if USE_SRWLIB:
        e,h,v,f = calc3d_srw(beamline,
                            photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                            hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,
                            zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        beamline["calc3d_srw"] = {"e":e,"h":h,"v":v,"f":f}
        print("Shapes for SRW:",e.shape,h.shape,v.shape,f.shape)
        print("Integral for SRW   :",f.sum()*(h[1]-h[0])*(v[1]-v[0]) )

    if USE_PYSRU:
        e,h,v,f = calc3d_pysru(beamline,
                            photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                            hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,
                            zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        beamline["calc3d_pysru"] = {"e":e,"h":h,"v":v,"f":f}
        print("Shapes for pySRU:",e.shape,h.shape,v.shape,f.shape,"MAX: ",f.max())
        print("Integral for pySRU :",f.sum()*(h[1]-h[0])*(v[1]-v[0]) )

    if USE_URGENT:
        e,h,v,f = calc3d_urgent(beamline,
                            photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                            hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,
                            zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        beamline["calc3d_urgent"] = {"e":e,"h":h,"v":v,"f":f}
        print("Shapes for URGENT:",e.shape,h.shape,v.shape,f.shape,"MAX: ",f.max())
        print("Integral for URGENT :",f.sum()*(h[1]-h[0])*(v[1]-v[0]) )

    if USE_US:
        e,h,v,f = calc3d_us(beamline,
                            photonEnergyMin=photonEnergyMin,photonEnergyMax=photonEnergyMax,photonEnergyPoints=photonEnergyPoints,
                            hSlitPoints=npoints_grid,vSlitPoints=npoints_grid,
                            zero_emittance=zero_emittance,fileName=fileName,fileAppend=True)
        beamline["calc3d_us"] = {"e":e,"h":h,"v":v,"f":f}
        print("Shapes for US:",e.shape,h.shape,v.shape,f.shape,"MAX: ",f.max())
        print("Integral for US :",f.sum()*(h[1]-h[0])*(v[1]-v[0]) )



    return beamline

def plot_radiation(beamline_dict,stack=True,show=True):

    cmax = -100000.0
    data_found = False
    for key in ["calc3d_us","calc3d_urgent","calc3d_pysru","calc3d_srw"]:
        if key in beamline_dict.keys():
            f = beamline_dict[key]["f"]
            cmax = numpy.max([cmax,f.max()])
            data_found = True

    if not data_found: return

    contour_levels = numpy.linspace(0,cmax,20)

    # silx stackView
    if stack == True:
        from silx.gui import qt
        from silx.gui.plot.StackView import StackViewMainWindow
        app = qt.QApplication(sys.argv[1:])

        SV = []
    for key in ["calc3d_us","calc3d_urgent","calc3d_pysru","calc3d_srw"]:
        if key in beamline_dict.keys():
            h = beamline_dict[key]["h"]
            v = beamline_dict[key]["v"]
            e = beamline_dict[key]["e"]
            f = beamline_dict[key]["f"]

            if stack:
                sv = StackViewMainWindow()
                SV.append(sv)
                sv.setColormap("jet", autoscale=True)
                sv.setStack(f)
                sv.setGraphTitle(key)
                sv.setKeepDataAspectRatio(True)
                sv.setLabels(["E: %10.3f to %10.3f eV (%d points)"%(e.min(),e.max(),e.size),
                              "H: %5.1f to %5.1f mm (%d points)"%(h.min(),h.max(),h.size),
                              "V: %5.1f to %5.1f mm (%d points)"%(v.min(),v.max(),v.size)])
                sv.show()
            else:
                plot_contour(f[int(e.size/2),:,:],h,v,title="%s %s; E=%g eV"%(beamline_dict['name'],key,e[int(e.size/2)]),
                             xtitle="H [mm]",ytitle="V [mm]",plot_points=0,contour_levels=contour_levels,
                             cmap=None,cbar=1,cbar_title="Flux ",show=False)

                plot_surface(f[int(e.size/2),:,:],h,v,title="%s %s; E=%g eV"%(beamline_dict['name'],key,e[int(e.size/2)]),
                             xtitle="H [mm]",ytitle="V [mm]",show=False)

    if stack: app.exec_()

    if show: plot_show()


def calculate_power(bl):
    for key in ["calc1d_us","calc1d_urgent","calc1d_pysru","calc1d_srw"]:
        if key in bl.keys():
            e = bl[key]["energy"]
            f = bl[key]["flux"]
            print(">>>>    Power from integral of spectrum (%s): %f W"%(key,f.sum()*1e3*codata.e*(e[1]-e[0])))

    for key in ["calc2d_us","calc2d_urgent","calc2d_pysru","calc2d_srw"]:
        if key in bl.keys():
            h = bl[key]["h"]
            v = bl[key]["v"]
            p = bl[key]["p"]
            print(">>>>    Power from power density calculations (%s): %f W"%(key,p.sum()*(h[1]-h[0])*(v[1]-v[0])))

    for key in ["calc3d_us","calc3d_urgent","calc3d_pysru","calc3d_srw"]:
        if key in bl.keys():
            h = bl[key]["h"]
            v = bl[key]["v"]
            e = bl[key]["e"]
            f = bl[key]["f"]
            if e.size == 1:
                e_step = 1.0
                txt = "/eV"
            else:
                e_step = e[1] - e[0]
                txt = ""
            print(">>>>    Power from integral of 3D-volume (energy,h,v) (%s): %f W%s"%
                  (key,f.sum()*1e3*codata.e*e_step*(h[1]-h[0])*(v[1]-v[0]),txt))



def main(radiance=True,flux=True,flux_from_3d=True,power_density=True):

    #
    # example fig 2-5 in X-ray Data Booklet
    #

    beamline = {}
    beamline['name'] = "XRAY_BOOKLET"
    beamline['ElectronBeamDivergenceH'] = 1e-20
    beamline['ElectronBeamDivergenceV'] = 1e-20
    beamline['ElectronBeamSizeH'] = 1e-20
    beamline['ElectronBeamSizeV'] = 1e-20
    beamline['ElectronEnergySpread'] = 1e-20
    beamline['ElectronCurrent'] = 1.0
    beamline['ElectronEnergy'] = 1.3
    beamline['Kv'] = 1.87
    beamline['NPeriods'] = 14
    beamline['PeriodID'] = 0.035
    beamline['distance'] =   1.0*1e2
    beamline['gapH']      = 0.002*1e2 #0.001
    beamline['gapV']      = 0.002*1e2 #0.001


    zero_emittance = True



    #
    # Radiance
    #

    if radiance:
        out = compare_radiation(beamline,zero_emittance=zero_emittance,npoints_grid=101,energy=None)
        plot_radiation(out)



    #
    # Flux
    #

    if flux:
        out = compare_flux(beamline,emin=100,emax=900,npoints=200, zero_emittance=zero_emittance)
        plot_flux(out)
    if flux_from_3d:
        out = compare_flux_from_3d(beamline,emin=100,emax=900,npoints=10,zero_emittance=zero_emittance)
        plot_flux(out)

    #
    # Power density
    #

    if power_density:
        out = compare_power_density(beamline,npoints_grid=51,zero_emittance=zero_emittance)
        plot_power_density(out)

if __name__ == '__main__':
    main(radiance=True,flux=False,flux_from_3d=False,power_density=False)

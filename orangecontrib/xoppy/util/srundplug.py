
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

        <code>=Srw,urgent,Us


     functions(list): 

         auxiliary:
            getGlossaryElement()
            getFWHM()
            getBeamline()
    
         main parameters:
            calcUndulator()
    
         flux spectrum versus energy:
            calc1dSrw()
            calc1dUrgent()
            calc1dUs
    
         power density versus (h,v):
            calc2dSrw()
            calc2dUrgent()
            calc2dUs()
    
         flux in a slit vs (energy,h,v)
            calc3dSrw
            calc3dUrgent
            calc3dUs

TODO: 
     -rename the package
     -documentation write and adapt to sphynx? 
     -think in structuring the Glossary
     -restructure the code to OO (class/methods)
     -think on plots
     -check timing routines (delete?)
     -manage globals
 
"""

__author__    = "Manuel Sanchez del Rio"
__contact__   = "srio@esrf.eu"
__copyright__ = "ESRF, 2014"

#
#----------------------------  IMPORT ------------------------------------------
#

import os
import sys
from collections import OrderedDict
import time

import numpy

#SRW
try:
    import srwlib
except ImportError:
    print("Failed to import srwlib. Do not try to use it!")

#catch standard optput
try:
    from io import StringIO  # Python3
except ImportError:
    from StringIO import StringIO  # Python2

#
#----------------------------  GLOBAL NAMES ------------------------------------
#

#Physical constants (global, by now)
try:
    import scipy.constants.codata
    codata = scipy.constants.codata.physical_constants
    
    codata_c, tmp1, tmp2 = codata["speed of light in vacuum"]
    codata_c = numpy.array(codata_c)
    
    codata_mee, tmp1, tmp2 = codata["electron mass energy equivalent in MeV"]
    codata_mee = numpy.array(codata_mee)
    
    codata_h, tmp1, tmp2 = codata["Planck constant"]
    codata_h = numpy.array(codata_h)
    
    codata_ec, tmp1, tmp2 = codata["elementary charge"]
    codata_ec = numpy.array(codata_ec)
except ImportError:
    print("Failed to import scipy. Finding alternative ways.")
    codata_c = numpy.array(299792458.0)
    codata_mee = numpy.array(9.10938356e-31)
    codata_h = numpy.array(6.626070040e-34)
    codata_ec = numpy.array(1.6021766208e-19)

m2ev = codata_c*codata_h/codata_ec      # lambda(m)  = m2eV / energy(eV)

# counter for output files
scanCounter = 0

# directory  where to find urgent and us binaries
try:
    home_bin
except NameError:
    home_bin='/users/srio/Oasys/Orange-XOPPY/orangecontrib/xoppy/bin.linux/'
    #home_bin='/scisoft/xop2.4/bin.linux/'
    print("srundplug: undefined home_bin. It has been set to ",home_bin)

#check
if os.path.isfile(home_bin+'us') == False:
    print("srundplug: File not found: "+home_bin+'us')
if os.path.isfile(home_bin+'urgent') == False:
    sys.exit("srundplug: File not found: "+home_bin+'urgent')

#
#----------------------------  FUNCTIONS -------------------------------------
#

def calcFWHM(h,binSize):
  t = numpy.where(h>=max(h)*0.5)
  return binSize*(t[0][-1]-t[0][0]+1), t[0][-1], t[0][0]

def getGlossaryElement(str1=""):
    r"""
     Gets a dictionary for a given element in the Glossary

     MODIFICATION HISTORY: 
            Written by:     M. Sanchez del Rio, srio@esrf.eu, 2004-09-16
      
    """ 
    dict1 = None
    dict1 = OrderedDict()
    if (str1 == "BC_ElectronBeamGaussian"):
        dict1.update(  {
            "ElectronEnergy" : 6.04, 
            "ElectronCurrent" : 0.2,
            "ElectronBeamSizeH" : 413e-6,
            "ElectronBeamSizeV" : 3e-6,
            "ElectronBeamDivergenceH" : 10.0e-6,
            "ElectronBeamDivergenceV" : 1.2e-6 } )
        return dict1

    if (str1 == "BC_InsertionDevice"):
        dict1.update(  {
            "PeriodID" : 26.0e-3,
            "NPeriods" : 96,
            "Kv" : 0.82} )

    if (str1 == "IC_DriftSpace"):
        dict1.update(  {
            "d" : 20.0} )

    if (str1 == "BC_Slit"):
        dict1.update(  {
            "gapH" : 1.0e-3,
            "gapV" : 1.0e-3 } )

    return dict1

def getBeamline(nameBeamline,silent=False):
    #
    # get the elements
    #
    ebeam = getGlossaryElement("BC_ElectronBeamGaussian")
    idv = getGlossaryElement("BC_InsertionDevice")
    drift = getGlossaryElement("IC_DriftSpace")
    slit = getGlossaryElement("BC_Slit")
    
    #
    # modify elements
    #
    if nameBeamline == "ID16_NA":
        if silent == False:
            print("Setting inputs for ESRF-ID16_NA")
        ebeam['ElectronBeamDivergenceH'] = 10.3e-06
        ebeam['ElectronBeamDivergenceV'] = 1.2e-06
        ebeam['ElectronBeamSizeH'] = 0.0004131
        ebeam['ElectronBeamSizeV'] = 3.4e-06
        ebeam['ElectronCurrent'] = 0.2
        ebeam['ElectronEnergy'] = 6.04
        idv['Kv'] = 4.0 # 0.82
        idv['NPeriods'] = 77
        idv['PeriodID'] = 0.026
        drift['distance'] = 20.0
        slit['gapH'] = 0.001 #0.001
        slit['gapV'] = 0.001 #0.001
    
    if nameBeamline == "ESRF_LB":
        if silent == False:
            print("Setting inputs for ESRF Low Beta")
        ebeam['ElectronBeamDivergenceH'] = 88.3e-6
        ebeam['ElectronBeamDivergenceV'] = 3.8e-6
        ebeam['ElectronBeamSizeH'] = 57e-6
        ebeam['ElectronBeamSizeV'] = 10.3e-6
        ebeam['ElectronCurrent'] = 0.2
        ebeam['ElectronEnergy'] = 6.04
        idv['Kv'] = 1.68
        idv['NPeriods'] = int(4.0/0.018)
        idv['PeriodID'] = 0.018
        drift['distance'] = 30.0
        slit['gapH'] = 0.001
        slit['gapV'] = 0.001

    if nameBeamline == "ESRF_LB_OB":
        if silent == False:
            print("Setting inputs for ESRF Low Beta after OB")
        ebeam['ElectronBeamDivergenceH'] = 106.9e-6
        ebeam['ElectronBeamDivergenceV'] = 1.2e-6
        ebeam['ElectronBeamSizeH'] = 37.4e-6
        ebeam['ElectronBeamSizeV'] = 3.5e-6
        ebeam['ElectronCurrent'] = 0.2
        ebeam['ElectronEnergy'] = 6.04
        idv['Kv'] = 1.68
        idv['NPeriods'] = int(4.0/0.018)
        idv['PeriodID'] = 0.018
        drift['distance'] = 30.0
        slit['gapH'] = 0.001
        slit['gapV'] = 0.001


    if nameBeamline == "ESRF_HB":
        if silent == False:
            print("Setting inputs for ESRF High Beta")
        ebeam['ElectronBeamDivergenceH'] = 10.5e-6
        ebeam['ElectronBeamDivergenceV'] = 3.9e-6
        ebeam['ElectronBeamSizeH'] = 395e-6
        ebeam['ElectronBeamSizeV'] = 9.9e-6
        ebeam['ElectronCurrent'] = 0.2
        ebeam['ElectronEnergy'] = 6.04
        idv['Kv'] = 1.68
        idv['NPeriods'] = int(4.0/0.018)
        idv['PeriodID'] = 0.018
        drift['distance'] = 30.0

    if nameBeamline == "ESRF_HB_OB":
        if silent == False:
            print("Setting inputs for ESRF High Beta after OB")
        ebeam['ElectronBeamDivergenceH'] = 10.3e-6
        ebeam['ElectronBeamDivergenceV'] = 1.2e-6
        ebeam['ElectronBeamSizeH'] = 387.8e-6
        ebeam['ElectronBeamSizeV'] = 3.5e-6
        ebeam['ElectronCurrent'] = 0.2
        ebeam['ElectronEnergy'] = 6.04
        idv['Kv'] = 1.68
        idv['NPeriods'] = int(4.0/0.018)
        idv['PeriodID'] = 0.018
        drift['distance'] = 30.0
        slit['gapH'] = 0.001 
        slit['gapV'] = 0.001 



    if nameBeamline == "ESRF_NEW_OB":
        if silent == False:
            print("Setting inputs for ESRF Low Beta")
        ebeam['ElectronBeamDivergenceH'] = 5.2e-6
        ebeam['ElectronBeamDivergenceV'] = 1.4e-6
        ebeam['ElectronBeamSizeH'] = 27.2e-6
        ebeam['ElectronBeamSizeV'] = 3.4e-6
        ebeam['ElectronCurrent'] = 0.2
        ebeam['ElectronEnergy'] = 6.0
        idv['Kv'] = 1.68
        idv['NPeriods'] = int(4.0/0.018)
        idv['PeriodID'] = 0.018
        drift['distance'] = 30.0
        slit['gapH'] = 0.001 
        slit['gapV'] = 0.001 

    #
    # build the beamline as a list
    # 
    #    bl = [ebeam,idv,drift,slit]
    #
    #    print ("-----------------------------------------------------")
    #    print ("-----------------------------------------------------")
    #    for oe in bl: #range(len(bl)):
    #        for i,j in oe.items():
    #            print ("%s = %s" % (i,j) )
    #        print ("-----------------------------------------------------")
    #    print ("-----------------------------------------------------")
    
    #
    # build the beamline as a merged dictionary
    # TODO: merge elements is dangerous (possible key duplication) and 
    #       does not allow multiple identical elements. Find a better solution...
    # 
    bl = OrderedDict()
    bl.update(ebeam)
    bl.update(idv)
    bl.update(drift)
    bl.update(slit)
    #if silent == False:
    #    print ("\n\n-----------------------------------------------------")
    #    for i,j in bl.items(): 
    #        print ("%s = %s" % (i,j) )
    #    print ("-----------------------------------------------------\n\n")
    return bl


def calcUndulator(bl,photonEnergy=None,distance=None,silent=False):

    #init capture standard output 
    # see http://wrongsideofmemphis.com/2010/03/01/store-standard-output-on-a-variable-in-python/
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result

    print("=============  Undulator parameters =============================\n")
    print("Inputs: \n")
    for i,j in bl.items(): 
        print ("%s = %s" % (i,j) )
    print("\n\nOutputs (supposing at waist): \n")
    print ("Electron beam Emittance H [m.rad]: %e \n"%(bl['ElectronBeamSizeH']*bl['ElectronBeamDivergenceH']))
    print ("Electron beam Emittance V [m.rad]: %e \n"%(bl['ElectronBeamSizeV']*bl['ElectronBeamDivergenceV']))
    print ("Electron Beta H [m]: %e \n"%(bl['ElectronBeamSizeH']/bl['ElectronBeamDivergenceH']))
    print ("Electron Beta V [m]: %e \n"%(bl['ElectronBeamSizeV']/bl['ElectronBeamDivergenceV']))
    l1 = bl['PeriodID']*bl['NPeriods']
    print ("Undulator length [m]: %f \n"%(l1))

    # 
    # energy-dependent parameters
    #
    if photonEnergy != None:
        phE = numpy.array(photonEnergy)
        phE.shape = -1
        for phEi in phE:
            print ("\n\n----------------------  photon energy [eV]: %0.2f \n"%(phEi))
            print('\n')
            lambda1 = m2ev/phEi
            print ("   photon wavelength [A]: %f \n"%(lambda1*1e10))
        
            # calculate sizes of the photon undulator beam
            # see formulas 25 & 30 in Elleaume (Onaki & Elleaume)
            s_phot = 2.740/(4e0*numpy.pi)*numpy.sqrt(l1*lambda1)
            sp_phot = 0.69*numpy.sqrt(lambda1/l1)
            print('\n')
            print('   RMS electon size H/V [um]: '+
                 repr(bl['ElectronBeamSizeH']*1e6)+ ' /  '+
                 repr(bl['ElectronBeamSizeV']*1e6) )
            print('   RMS electon divergence H/V[urad]: '+
                 repr(bl['ElectronBeamDivergenceH']*1e6)+ ' /  '+
                 repr(bl['ElectronBeamDivergenceV']*1e6)  )
            print('\n')
            print('   RMS radiation size [um]: '+repr(s_phot*1e6))
            print('   RMS radiation divergence [urad]: '+repr(sp_phot*1e6))
            print('\n')
            print('   Photon beam (convolution): ')
            photon_h = numpy.sqrt(numpy.power(bl['ElectronBeamSizeH'],2) + numpy.power(s_phot,2) )
            photon_v = numpy.sqrt(numpy.power(bl['ElectronBeamSizeV'],2) + numpy.power(s_phot,2) )
            photon_hp = numpy.sqrt(numpy.power(bl['ElectronBeamDivergenceH'],2) + numpy.power(sp_phot,2) )
            photon_vp = numpy.sqrt(numpy.power(bl['ElectronBeamDivergenceV'],2) + numpy.power(sp_phot,2) )
            print('   RMS size H/V [um]: '+ repr(photon_h*1e6) + '  /  '+repr(photon_v*1e6))
            print('   RMS divergence H/V [um]: '+ repr(photon_hp*1e6) + '  /  '+repr(photon_vp*1e6))
         
            print('\n')
            cohH = lambda1/4/numpy.pi / photon_h / photon_hp
            cohV = lambda1/4/numpy.pi / photon_v / photon_vp
            print('   Coherent volume in H phase space: '+ repr(cohH) )
            print('   Coherent volume in V phase space: '+ repr(cohV) )
            print('\n')
            dls = numpy.sqrt(2*l1*lambda1)/4/numpy.pi
            print('   RMS diffraction limit source size [um]: '+ repr(dls*1e6) )
            print('   FWHM diffraction limit source size [um]: '+ repr(dls*2.35*1e6) )
            #
            # values that depen on screen distance
            #
            if distance != None:
                print('\n')
                hRMS = numpy.sqrt( numpy.power(photon_hp*distance,2) + numpy.power(photon_h,2))
                vRMS = numpy.sqrt( numpy.power(photon_vp*distance,2) + numpy.power(photon_v,2))
            
                print('   At a screen placed at :%f m from the source:\n'%(distance))
                print('   RMS size H/V [mm]: '+ repr(hRMS*1e3) + '  /  '+repr(vRMS*1e3))
                print('   FWHM size H/V [mm]: '+ repr(hRMS*2.35*1e3) + '  /  '+repr(vRMS*2.35*1e3))
                print('\n')
                print('   FWHM coherence length H [um] : '+ repr(hRMS*cohH*2.35*1e6) )
                print('   FWHM coherence length V [um] : '+ repr(vRMS*cohV*2.35*1e6) )

        
    print("=================================================================\n")

    sys.stdout = old_stdout
    result_string = result.getvalue()

    if silent == False:
        print(result_string)

    return  result_string


def calc1dSrw(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,fileName="/dev/null",fileAppend=True):

    r"""
        run SRW for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """
    
    global scanCounter

    t0 = time.time()
    print("Inside calc1dSrw")
    outFile = 'flux.spec'
    #Maximum number of harmonics considered. This is critical for speed. 
    #TODO: set it automatically to a reasonable value (see how is done by Urgent).
    Nmax = 21
    #derived
    #TODO calculate the numerical factor using codata
    B0 = bl['Kv']/0.934/(bl['PeriodID']*1e2)
    
    
    
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
    magFldCnt = srwlib.SRWLMagFldC([und], srwlib.array('distance', [0]), srwlib.array('distance', [0]), srwlib.array('distance', [0]))
    
    #***********Electron Beam
    eBeam = srwlib.SRWLPartBeam()
    eBeam.Iavg = bl['ElectronCurrent'] #average current [A]
    eBeam.partStatMom1.x = 0. #initial transverse positions [m]
    eBeam.partStatMom1.y = 0.
    eBeam.partStatMom1.z = 0. #initial longitudinal positions (set in the middle of undulator)
    eBeam.partStatMom1.xp = 0 #initial relative transverse velocities
    eBeam.partStatMom1.yp = 0
    eBeam.partStatMom1.gamma = bl['ElectronEnergy']/0.51099890221e-03 #relative energy

    sigX =  bl['ElectronBeamSizeH'] #horizontal RMS size of e-beam [m]
    sigXp = bl['ElectronBeamDivergenceH'] #horizontal RMS angular divergence [rad]
    sigY =  bl['ElectronBeamSizeV'] #vertical RMS size of e-beam [m]
    sigYp = bl['ElectronBeamDivergenceV'] #vertical RMS angular divergence [rad]

    if 'ElectronEnergySpread' in bl.keys():
        sigEperE = bl['ElectronEnergySpread']
    else:
        sigEperE = 0.001 #relative RMS energy spread

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

    #**********************Saving results
    
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
        f.write(' ' + repr(ener) + '   ' + repr(m2ev/ener*1e10) + '    ' +
                repr(stkF.arS[i]) + '    ' +
                repr(stkF.arS[i]*codata_ec*1e3) + '\n')
        eArray[i] = ener
        intensArray[i] = stkF.arS[i]
    
    f.close()

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    print('Done calc1dSrw calculation in sec '+str(time.time()-t0))

    return (eArray,intensArray) 

def calc1dUrgent(bl,photonEnergyMin=1000.0,photonEnergyMax=100000.0,photonEnergyPoints=500,fileName="/dev/null",fileAppend=False):

    r"""
        run Urgent for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin


    t0 = time.time()
    print("Inside calc1dUrgent")
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
        f.write("%d\n"%(1))               #ICALC
        f.write("%d\n"%(-1))              #IHARM

        f.write("%d\n"%(0))               #NPHI
        f.write("%d\n"%(0))               #NSIG
        f.write("%d\n"%(0))               #NALPHA
        f.write("%f\n"%(0.00000))         #DALPHA
        f.write("%d\n"%(0))               #NOMEGA
        f.write("%f\n"%(0.00000))         #DOMEGA

    command = os.path.join(home_bin,'urgent < urgent.inp')
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("Done.")
    print("\n--------------------------------------------------------\n")

    # write spec file
    
    txt = open("urgent.out").readlines()

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
           f.write(tmp)
        else:
           f.write("#UD "+tmp)

    f.close()


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

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    print('Done calc1dUrgent calculation in sec '+str(time.time()-t0))

    return (eArray,intensArray)

def calc1dUs(bl,photonEnergyMin=1000.0,photonEnergyMax=100000.0,photonEnergyPoints=500,fileName="/tmp/null",fileAppend=False):

    r"""
        run US for calculating flux

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin


    t0 = time.time()

    print("Inside calc1dUs")
    with open("us.inp","wt") as f:
        #f.write("%d\n"%(1))               # ITYPE
        #f.write("%f\n"%(bl['PeriodID']))  # PERIOD

        f.write("US run\n")
        f.write("    %f  %f                               Ring-Energy Current\n"%
               (bl['ElectronEnergy'],bl['ElectronCurrent']*1e3))
        f.write("  %f  %f  %f  %f               Sx Sy Sxp Syp\n"%
               (bl['ElectronBeamSizeH']*1e3,bl['ElectronBeamSizeV']*1e3,
                bl['ElectronBeamDivergenceH']*1e3,bl['ElectronBeamDivergenceV']*1e3) )
        f.write("    %f      %d   0.000   %f               Period N Kx Ky\n"%
                (bl['PeriodID']*1e2,bl['NPeriods'],bl['Kv']) )
        f.write("    %f      %f     %d                   Emin Emax Ne\n"%
               (photonEnergyMin,photonEnergyMax,photonEnergyPoints) )
        f.write("  %f   0.000   0.000   %f   %f    50    50   D Xpc Ypc Xps Yps Nxp Nyp\n"%
               (bl['distance'],bl['gapH']*1e3,bl['gapV']*1e3) )
        f.write("       4       4       0                       Mode Method Iharm\n")
        f.write("       0       0     0.0      64     8.0     0 Nphi Nalpha Dalpha2 Nomega Domega Nsigma\n")
        f.write("foreground\n")

    command = os.path.join(home_bin,'us')
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("Done.")
    print("\n--------------------------------------------------------\n")

    # write spec file
    txt = open("us.out").readlines()

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

    f.write("#N 6\n")
    f.write("#L  Energy(eV)  Flux(ph/s/0.1%bw)  p1  p2  p3  p4\n")

    nArray = 0
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           tmp = tmp.replace('D','e')
           f.write(tmp)
           nArray  += 1
        else:
           f.write("#UD "+tmp)

    f.close()

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

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    print('Done calc1dUs calculation in sec '+str(time.time()-t0))

    return (eArray,intensArray)


def calc2dSrw(bl,fileName="/dev/null",fileAppend=True,hSlitPoints=101,vSlitPoints=51):

    r"""
        run SRW for calculating power density

        input: a dictionary with beamline
        output: file name with results
    """
    
    global scanCounter
    print("Inside calc2dSrw")
    #Maximum number of harmonics considered. This is critical for speed. 
    #TODO: set it automatically to a reasonable value (see how is done by Urgent).
    Nmax = 21
    #derived
    #TODO calculate the numerical factor using codata
    B0 = bl['Kv']/0.934/(bl['PeriodID']*1e2)
    
    
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
    magFldCnt = srwlib.SRWLMagFldC([und], srwlib.array('distance', [0]), srwlib.array('distance', [0]), srwlib.array('distance', [0]))
    
    #***********Electron Beam
    eBeam = srwlib.SRWLPartBeam()
    eBeam.Iavg = bl['ElectronCurrent'] #average current [A]
    eBeam.partStatMom1.x = 0. #initial transverse positions [m]
    eBeam.partStatMom1.y = 0.
    eBeam.partStatMom1.z = 0. #initial longitudinal positions (set in the middle of undulator)
    eBeam.partStatMom1.xp = 0 #initial relative transverse velocities
    eBeam.partStatMom1.yp = 0
    eBeam.partStatMom1.gamma = bl['ElectronEnergy']/0.51099890221e-03 #relative energy

    sigEperE = 0.00089 #relative RMS energy spread
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
    for i in range(stkP.mesh.nx):  
        for j in range(stkP.mesh.ny): 
            f.write(repr(hArray[i]) + ' ' + repr(vArray[j]) + ' ' + repr(powerArray[i,j]) + '\n')


    totPower = totPower * \
               (stkP.mesh.xFin-stkP.mesh.xStart)/(stkP.mesh.nx-1)*1e3 * \
               (stkP.mesh.yFin-stkP.mesh.yStart)/(stkP.mesh.ny-1)*1e3

    # dump profiles

    hStep = (stkP.mesh.xFin-stkP.mesh.xStart)/(stkP.mesh.nx-1)
    scanCounter +=1 
    f.write("\n#S %d Undulator power density calculation using SRW: H profile\n"%(scanCounter))
    for i,j in bl.items(): # write bl values
        f.write ("#UD %s = %s\n" % (i,j) )
    f.write( "#UD Total power [W]: "+repr(totPower)+"\n")
    f.write( "#UD FWHM [mm] : "+repr(calcFWHM(hProfile,hStep)[0]*1e3)+"\n")
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
    f.write( "#UD FWHM [mm] : "+repr(calcFWHM(vProfile,vStep)[0]*1e3)+"\n")
    f.write( "#N 2 \n")
    f.write( "#L V[mm]  PowerDensityCentralProfile[W/mm2] \n" )
    for j in range(stkP.mesh.ny):  
        f.write(repr(vArray[j]) + ' ' +  \
                repr(powerArray[int(len(hArray)/2),j]) + '\n')
    
    f.close()

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    return (hArray, vArray, powerArray)


def calc2dUs(bl,fileName="/dev/null",fileAppend=False,hSlitPoints=21,vSlitPoints=51):

    r"""
        run US for calculating power density

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc2dUs")
    with open("us.inp","wt") as f:
        #f.write("%d\n"%(1))               # ITYPE
        #f.write("%f\n"%(bl['PeriodID']))  # PERIOD

        f.write("US run\n")
        f.write("    %f  %f                               Ring-Energy Current\n"%
               (bl['ElectronEnergy'],bl['ElectronCurrent']*1e3))
        f.write("  %f  %f  %f  %f               Sx Sy Sxp Syp\n"%
               (bl['ElectronBeamSizeH']*1e3,bl['ElectronBeamSizeV']*1e3,
                bl['ElectronBeamDivergenceH']*1e3,bl['ElectronBeamDivergenceV']*1e3) )
        f.write("    %f      %d   0.000   %f               Period N Kx Ky\n"%
                (bl['PeriodID']*1e2,bl['NPeriods'],bl['Kv']) )
        f.write("    9972.1   55000.0     500                   Emin Emax Ne\n")
        f.write("  %f   0.000   0.000   %f   %f    %d    %d   D Xpc Ypc Xps Yps Nxp Nyp\n"%
               (bl['distance'],bl['gapH']*1e3,bl['gapV']*1e3,hSlitPoints-1,vSlitPoints-1) )
        f.write("       6       1       0                       Mode Method Iharm\n")
        f.write("       0       0     0.0      64     8.0     0 Nphi Nalpha Dalpha2 Nomega Domega Nsigma\n")
        f.write("foreground\n")

    command = os.path.join(home_bin,'us')
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("Done.")
    print("\n--------------------------------------------------------\n")

    # write spec file
    txt = open("us.out").readlines()

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
           f.write(tmp)
           tmpf = numpy.array( [float(j) for j in tmp.split()] )
           imesh = imesh + 1
           mesh[:,imesh] = tmpf
        else:
           f.write("#UD "+tmp)

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

    #os.chdir(pwd)
    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    return (hhh, vvv, int_mesh2)


def calc2dUrgent(bl,fileName="/dev/null",fileAppend=False,hSlitPoints=21,vSlitPoints=51):

    r"""
        run Urgent for calculating power density

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc2dUrgent")

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
        f.write("%d\n"%(1))               #ICALC
        f.write("%d\n"%(-200))             #IHARM   TODO: check max harmonic number

        f.write("%d\n"%(0))               #NPHI
        f.write("%d\n"%(0))               #NSIG
        f.write("%d\n"%(0))               #NALPHA
        f.write("%f\n"%(0.00000))         #DALPHA
        f.write("%d\n"%(0))               #NOMEGA
        f.write("%f\n"%(0.00000))         #DOMEGA

    command = os.path.join(home_bin,'urgent < urgent.inp')
    print("\n\n--------------------------------------------------------\n")
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    os.system(command)
    print("Done.")

    # write spec file
    txt = open("urgent.out").readlines()

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
           f.write(tmp)
           tmp = tmp.replace('D','e')
           tmpf = numpy.array( [float(j) for j in tmp.split()] )
           imesh = imesh + 1
           mesh[:,imesh] = tmpf
        else:
           if len(tmp) > 0:  # remove the last block
               if tmp.split(" ")[0] == 'HARMONIC':
                   break
           f.write("#UD "+tmp)

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

            
    totPower = int_mesh2.sum() * (hh[1]-hh[0]) * (vv[1]-vv[0]) 

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

    #os.chdir(pwd)
    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    print("\n--------------------------------------------------------\n\n")

    return (hhh, vvv, int_mesh2)


def calc3dSrw(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,fileName="/dev/null",fileAppend=True,hSlitPoints=11,vSlitPoints=11):

    r"""
        run SRW for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """
    
    global scanCounter
    print("Inside calc3dSrw")
    outFile = 'flux3d.spec'
    #Maximum number of harmonics considered. This is critical for speed. 
    #TODO: set it automatically to a reasonable value (see how is done by Urgent).
    Nmax = 8 # 21
    #derived
    #TODO calculate the numerical factor using codata
    B0 = bl['Kv']/0.934/(bl['PeriodID']*1e2)
    
    
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
    magFldCnt = srwlib.SRWLMagFldC([und], srwlib.array('distance', [0]), srwlib.array('distance', [0]), srwlib.array('distance', [0]))
    
    #***********Electron Beam
    eBeam = srwlib.SRWLPartBeam()
    eBeam.Iavg = bl['ElectronCurrent'] #average current [A]
    eBeam.partStatMom1.x = 0. #initial transverse positions [m]
    eBeam.partStatMom1.y = 0.
    eBeam.partStatMom1.z = 0. #initial longitudinal positions (set in the middle of undulator)
    eBeam.partStatMom1.xp = 0 #initial relative transverse velocities
    eBeam.partStatMom1.yp = 0
    eBeam.partStatMom1.gamma = bl['ElectronEnergy']/0.51099890221e-03 #relative energy

    sigEperE = 0.00089 #relative RMS energy spread
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
    arPrecF = [0]*5 #for spectral flux vs photon energy
    arPrecF[0] = 1 #initial UR harmonic to take into account
    arPrecF[1] = Nmax #final UR harmonic to take into account
    arPrecF[2] = 1.5 #longitudinal integration precision parameter
    arPrecF[3] = 1.5 #azimuthal integration precision parameter
    arPrecF[4] = 1 #calculate flux (1) or flux per unit surface (2)
    
    #***********UR Stokes Parameters (mesh) for Spectral Flux
    stkF = srwlib.SRWLStokes() #for spectral flux vs photon energy
    stkF.allocate(photonEnergyPoints, hSlitPoints, vSlitPoints) #numbers of points vs photon energy, horizontal and vertical positions
    stkF.mesh.zStart = bl['distance'] #longitudinal position [m] at which UR has to be calculated
    stkF.mesh.eStart = photonEnergyMin #initial photon energy [eV]
    stkF.mesh.eFin =   photonEnergyMax #final photon energy [eV]
    stkF.mesh.xStart = -bl['gapH']/2 #initial horizontal position [m]
    stkF.mesh.xFin =    bl['gapH']/2 #final horizontal position [m]
    stkF.mesh.yStart = -bl['gapV']/2 #initial vertical position [m]
    stkF.mesh.yFin =    bl['gapV']/2 #final vertical position [m]
    
    #**********************Calculation (SRWLIB function calls)
    print('Performing Spectral Flux 3d (Stokes parameters) calculation ... ') # , end='')
    t0 = time.time()
    srwlib.srwl.CalcStokesUR(stkF, eBeam, und, arPrecF)
    print('Done Performing Spectral Flux 3d (Stokes parameters) calculation in sec '+str(time.time()-t0))

    #reshape array
    aaaa = numpy.array(stkF.arS)
    aaaa.shape = (4,stkF.mesh.ny,stkF.mesh.nx,stkF.mesh.ne)
    #**********************Saving results
    
    if fileAppend:
        f = open(fileName,"a")
    else:
        scanCounter = 0
        f = open(fileName,"w")
        f.write("#F "+fileName+"\n")

   

    #
    # brute force loop to verify that reshape works correctly
    #
    #bruteforce = False
    #if bruteforce:
    #    kijs=-1
    #    print(aaaa.shape)
    #    for s in range(4):
    #        for j in range(stkF.mesh.ny): 
    #            for i in range(hSlitPoints):  
    #                for k in range(vSlitPoints): 
    #                         kijs = kijs + 1
    #                         ener = stkF.mesh.eStart+k*(stkF.mesh.eFin-stkF.mesh.eStart)/numpy.array((stkF.mesh.ne-1)).clip(min=1)
    #                         xx = stkF.mesh.xStart + i*(stkF.mesh.xFin-stkF.mesh.xStart)/numpy.array((stkF.mesh.nx-1)).clip(min=1)
    #                         yy = stkF.mesh.yStart + j*(stkF.mesh.yFin-stkF.mesh.yStart)/numpy.array((stkF.mesh.ny-1)).clip(min=1)
    #                         if s == 0:
    #                             print(ener,xx,yy,k,i,j,s,stkF.arS[kijs],
    #                                   aaaa[s,j,i,k])

    #
    # write flux to file
    #
    flux2 = numpy.zeros(photonEnergyPoints)
    mesh2 = numpy.zeros((vSlitPoints,hSlitPoints))

    # for output
    intensArray = numpy.zeros((photonEnergyPoints,hSlitPoints,vSlitPoints))
    eArray = numpy.zeros(photonEnergyPoints)
    hArray = numpy.zeros(hSlitPoints)
    vArray = numpy.zeros(vSlitPoints)

    for k in range(stkF.mesh.ne): 
        ener = stkF.mesh.eStart+k*(stkF.mesh.eFin-stkF.mesh.eStart)/numpy.array((stkF.mesh.ne-1)).clip(min=1)
        eArray[k] = ener
        scanCounter += 1
        f.write("\n#S %d Undulator 3d flux distribition using SRW at E= %0.3f eV\n"%(k+1,ener*1e-3))
        for i,j in bl.items(): # write bl values
            f.write ("#UD %s = %s\n" % (i,j) )
        f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
        f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
        f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))
        f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        f.write("#UD B0 =  %f\n"%(B0))
    
        f.write("#N 3 \n#L H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]\n")
        for i in range(hSlitPoints):  
            xx = stkF.mesh.xStart + i*(stkF.mesh.xFin-stkF.mesh.xStart)/numpy.array((stkF.mesh.nx-1)).clip(min=1)
            hArray[i] = xx
            for j in range(vSlitPoints): 
                yy = stkF.mesh.yStart + j*(stkF.mesh.yFin-stkF.mesh.yStart)/numpy.array((stkF.mesh.ny-1)).clip(min=1)
                f.write(' ' + repr(xx*1e3) + '   ' + repr(yy*1e3) + '    ' +
                repr(aaaa[0,j,i,k]) + '\n')
                flux2[k] = flux2[k] + aaaa[0,j,i,k]
                mesh2[j,i] = mesh2[j,i] + aaaa[0,j,i,k]

                vArray[j] = yy
                intensArray[k,i,j] = aaaa[0,j,i,k]

    #
    # write flux integrated over all energies
    #
    #scanCounter += 1
    #f.write("\n#S %d Undulator flux 3d distribution using SRW at E=[%0.3f,%0.3f] keV\n"%(k+10,photonEnergyMin*1e-3,photonEnergyMax*1e-3))
    #for i,j in bl.items(): # write bl values
    #    f.write ("#UD %s = %s\n" % (i,j) )
    #f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
    #f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
    #f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))
    #f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
    #f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
    #f.write("#UD B0 =  %f\n"%(B0))

    #f.write("#N 3 \n#L H[mm]  V[mm]  Flux[Phot/s/0.1%bw] \n")
    #for i in range(hSlitPoints):  
    #    xx = stkF.mesh.xStart + i*(stkF.mesh.xFin-stkF.mesh.xStart)/numpy.array((stkF.mesh.nx-1)).clip(min=1)
    #    for j in range(vSlitPoints): 
    #        yy = stkF.mesh.yStart + j*(stkF.mesh.yFin-stkF.mesh.yStart)/numpy.array((stkF.mesh.ny-1)).clip(min=1)
    #        f.write(' ' + repr(xx*1e3) + '   ' + repr(yy*1e3) + '    ' +
    #        repr(mesh2[j,i]) + '\n')
    

    #
    # write flux to file
    #
    scanCounter += 1
    f.write("\n#S %d  Integrated flux comparison (recalculated and sum)\n"%(scanCounter))
    for i,j in bl.items(): # write bl values
        f.write ("#UD %s = %s\n" % (i,j) )
    f.write("#UD photonEnergyMin =  %f\n"%(photonEnergyMin))
    f.write("#UD photonEnergyMax =  %f\n"%(photonEnergyMax))
    f.write("#UD photonEnergyPoints =  %d\n"%(photonEnergyPoints))
    f.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
    f.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
    f.write("#UD B0 =  %f\n"%(B0))
    f.write("#N 3 \n#L PhotonEnergy[eV]  Flux[Photo/s/0.1%bw](sum)  Spectral Power[W/eV](sum)\n")
    for k in range(stkF.mesh.ne): 
        ener = stkF.mesh.eStart+k*(stkF.mesh.eFin-stkF.mesh.eStart)/numpy.array((stkF.mesh.ne-1)).clip(min=1)
        f.write(' ' + repr(ener) + '   ' + 
                repr(flux2[k]) + '    ' +
                repr(flux2[k]*codata_ec*1e3) + '    '+
                '\n')

    f.close()

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    # append direct calculation for comparison
    tmp = calc1dSrw(bl,photonEnergyMin=photonEnergyMin,
                  photonEnergyMax=photonEnergyMax,
                  photonEnergyPoints=photonEnergyPoints,
                  fileName=fileName,fileAppend=True)

    return (eArray, hArray, vArray, intensArray)



def calc3dUrgent(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,fileName="/dev/null",fileAppend=False,hSlitPoints=50,vSlitPoints=50):

    r"""
        run Urgent for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc3dUrgent")

    
    if fileAppend:
        fout = open(fileName,"a")
    else:
        scanCounter = 0
        fout = open(fileName,"w")
        fout.write("#F "+fileName+"\n")

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
            f.write("%d\n"%(1))               #ICALC
            f.write("%d\n"%(-61))             #IHARM   TODO: check max harmonic number
    
            f.write("%d\n"%(0))               #NPHI
            f.write("%d\n"%(0))               #NSIG
            f.write("%d\n"%(0))               #NALPHA
            f.write("%f\n"%(0.00000))         #DALPHA
            f.write("%d\n"%(0))               #NOMEGA
            f.write("%f\n"%(0.00000))         #DOMEGA
    
        command = os.path.join(home_bin,'urgent < urgent.inp')
        print("\n\n--------------------------------------------------------\n")
        print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
        os.system(command)
        print("Done.")
    
        # write spec file
        txt = open("urgent.out").readlines()
    
    
        iWrite = 0
        if iWrite:
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Urgent at E=%0.3f keV (a slit quadrant)\n"%(scanCounter,ener*1e-3))
            for i,j in bl.items(): # write bl values
                fout.write ("#UD %s = %s\n" % (i,j) )
            fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
            fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
            fout.write("#N 7\n")
            fout.write("#L  H[mm]  V[mm]  Flux[Phot/s/mm^2/0.1%bw]  l1  l2  l3  l4\n")
    
        mesh = numpy.zeros((7,(hSlitPoints)*(vSlitPoints)))
        hh = numpy.zeros((hSlitPoints))
        vv = numpy.zeros((vSlitPoints))
        int_mesh = numpy.zeros( ((hSlitPoints),(vSlitPoints)) )
        imesh = -1
        for i in txt:
            tmp = i.strip(" ")
            if tmp[0].isdigit():
               if iWrite:
                   fout.write(tmp)
               tmp = tmp.replace('D','e')
               tmpf = numpy.array( [float(j) for j in tmp.split()] )
               imesh = imesh + 1
               mesh[:,imesh] = tmpf
            else:
               if iWrite:
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
    
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Urgent at E=%0.3f eV (whole slit )\n"%(scanCounter,ener*1e-3))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        fout.write("#N 3\n")
        fout.write("#L  H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]\n")
        for i in range(len(hArray)):
            for j in range(len(vArray)):
               fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],int_mesh2[i,j]) )
               int_mesh3[iEner,i,j] = int_mesh2[i,j]
               int_mesh2integrated[i,j] += int_mesh2[i,j]
               totIntens += int_mesh2[i,j]

        totIntens = totIntens * (hh[1]-hh[0]) * (vv[1]-vv[0]) 
        intensArray[iEner] = totIntens


    # now dump the integrated power
    # convert from phot/s/0,1%bw/mm2 to W/mm^2
    int_mesh2integrated = int_mesh2integrated *codata_ec*1e3 * eStep

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
    #print(">>>>>>>>>>>>>>>power2",intensArray.sum()*codata_ec*1e3*(eArray[1]-eArray[0]))
    #print(">>>>>>>>>>>>>>>power3",int_mesh3.sum()*codata_ec*1e3*(eArray[1]-eArray[0])*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))

    # now dump the spectrum as the sum
    scanCounter += 1
    fout.write("\n#S %d Undulator 3d flux density vs energy (integrated in H,V) calculation using Urgent\n"%(scanCounter))
    for i,j in bl.items(): # write bl values
        fout.write ("#UD %s = %s\n" % (i,j) )
    fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
    fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
    fout.write("#UD IntegratedPower[W] =  %f\n"%(intensArray.sum()*codata_ec*1e3*(eArray[1]-eArray[0])))
    fout.write("#N 3\n")
    fout.write("#L  photonEnergy[eV]  Flux[phot/s/0.1%bw]  PowerDensity[W/eV]\n")
    for i in range(photonEnergyPoints):
       fout.write("%f  %f  %f\n"%(eArray[i],intensArray[i],intensArray[i]*codata_ec*1e3) )

    fout.close()

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    print("\n--------------------------------------------------------\n\n")
    # append direct calculation for comparison
    tmp = calc1dUrgent(bl,photonEnergyMin=photonEnergyMin,
                  photonEnergyMax=photonEnergyMax,
                  photonEnergyPoints=photonEnergyPoints,
                  fileName=fileName,fileAppend=True)

    return  (eArray, hArray, vArray, int_mesh3)



def calc3dUs(bl,photonEnergyMin=3000.0,photonEnergyMax=55000.0,photonEnergyPoints=500,fileName="/dev/null",fileAppend=False,hSlitPoints=50,vSlitPoints=50):

    r"""
        run Us for calculating intensity vs H,V,energy

        input: a dictionary with beamline
        output: file name with results
    """
    global scanCounter
    global home_bin
    print("Inside calc3dUs")

    
    if fileAppend:
        fout = open(fileName,"a")
    else:
        scanCounter = 0
        fout = open(fileName,"w")
        fout.write("#F "+fileName+"\n")

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

        with open("us.inp","wt") as f:
            #f.write("%d\n"%(1))               # ITYPE
            #f.write("%f\n"%(bl['PeriodID']))  # PERIOD
    
            f.write("US run\n")
            f.write("    %f  %f                               Ring-Energy Current\n"%
                   (bl['ElectronEnergy'],bl['ElectronCurrent']*1e3))
            f.write("  %f  %f  %f  %f               Sx Sy Sxp Syp\n"%
                   (bl['ElectronBeamSizeH']*1e3,bl['ElectronBeamSizeV']*1e3,
                    bl['ElectronBeamDivergenceH']*1e3,bl['ElectronBeamDivergenceV']*1e3) )
            f.write("    %f      %d   0.000   %f               Period N Kx Ky\n"%
                    (bl['PeriodID']*1e2,bl['NPeriods'],bl['Kv']) )
            f.write("    %f   55000.0       1                   Emin Emax Ne\n"%(ener))
            f.write("  %f   0.000   0.000   %f   %f    %d    %d   D Xpc Ypc Xps Yps Nxp Nyp\n"%
                   (bl['distance'],bl['gapH']*1e3,bl['gapV']*1e3,hSlitPoints-1,vSlitPoints-1) )
            f.write("       1       1       0                       Mode Method Iharm\n")
            f.write("       0       0     0.0      64     8.0     0 Nphi Nalpha Dalpha2 Nomega Domega Nsigma\n")
            f.write("foreground\n")
    
        command = os.path.join(home_bin,'us')
        print("\n\n--------------------------------------------------------\n")
        print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
        os.system(command)
        print("Done.")
    
        # write spec file
        txt = open("us.out").readlines()
    
    
        iWrite = False
        if iWrite:
            scanCounter += 1
            fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Us at E=%0.3f keV (a slit quadrant)\n"%(scanCounter,ener*1e-3))
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
               if iWrite:
                   fout.write(tmp)
               #tmp = tmp.replace('D','e')
               tmpf = numpy.array( [float(j) for j in tmp.split()] )
               imesh = imesh + 1
               mesh[:,imesh] = tmpf
            else:
               if iWrite:
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
    
        scanCounter += 1
        fout.write("\n#S %d Undulator 3d flux density (irradiance) calculation using Us at E=%0.3f eV (whole slit )\n"%(scanCounter,ener*1e-3))
        for i,j in bl.items(): # write bl values
            fout.write ("#UD %s = %s\n" % (i,j) )
        fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
        fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
        fout.write("#N 3\n")
        fout.write("#L  H[mm]  V[mm]  Flux[phot/s/0.1%bw/mm^2]\n")
        for i in range(len(hArray)):
            for j in range(len(vArray)):
               fout.write("%f  %f  %f\n"%(hArray[i],vArray[j],int_mesh2[i,j]) )
               int_mesh3[iEner,i,j] = int_mesh2[i,j]
               int_mesh2integrated[i,j] += int_mesh2[i,j]
               totIntens += int_mesh2[i,j]
               #hArray[i] += int_mesh2[i,j]
               #vArray[j] += int_mesh2[i,j]
               #totIntens += int_mesh2[i,j]

            
        #hArray = hArray * (hh[1]-hh[0]) 
        #vArray = vArray * (vv[1]-vv[0]) 
        #totIntens += (hh[1]-hh[0]) * (vv[1]-vv[0]) 
        totIntens = totIntens * (hh[1]-hh[0]) * (vv[1]-vv[0]) 
        intensArray[iEner] = totIntens


    # now dump the integrated power
    # convert from phot/s/0,1%bw/mm2 to W/mm^2
    int_mesh2integrated = int_mesh2integrated *codata_ec*1e3 * eStep

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
    print(">>>>>>>>>>>>>>>power1",int_mesh2integrated.sum()*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))
    print(">>>>>>>>>>>>>>>power2",intensArray.sum()*codata_ec*1e3*(eArray[1]-eArray[0]))
    print(">>>>>>>>>>>>>>>power3",int_mesh3.sum()*codata_ec*1e3*(eArray[1]-eArray[0])*(hArray[1]-hArray[0])*(vArray[1]-vArray[0]))

    # now dump the spectrum as the sum
    scanCounter += 1
    fout.write("\n#S %d Undulator 3d flux density vs energy (integrated in H,V) calculation using Us\n"%(scanCounter))
    for i,j in bl.items(): # write bl values
        fout.write ("#UD %s = %s\n" % (i,j) )
    fout.write("#UD hSlitPoints =  %f\n"%(hSlitPoints))
    fout.write("#UD vSlitPoints =  %f\n"%(vSlitPoints))
    fout.write("#UD IntegratedPower[W] =  %f\n"%(intensArray.sum()*codata_ec*1e3*(eArray[1]-eArray[0])))
    fout.write("#N 3\n")
    fout.write("#L  photonEnergy[eV]  Flux[phot/s/0.1%bw]  PowerDensity[W/eV]\n")
    for i in range(photonEnergyPoints):
       fout.write("%f   %f  %f\n"%(eArray[i],intensArray[i],intensArray[i]*codata_ec*1e3) )

    fout.close()

    if fileAppend:
        print("Data appended to file: "+fileName)
    else:
        print("File written to disk: "+fileName)

    # append direct calculation for comparison
    tmp = calc1dUs(bl,photonEnergyMin=photonEnergyMin,
                  photonEnergyMax=photonEnergyMax,
                  photonEnergyPoints=photonEnergyPoints,
                  fileName=fileName,fileAppend=True)
    print("\n--------------------------------------------------------\n\n")

    return  (eArray, hArray, vArray, int_mesh3)


#
#----------------------------  MAIN CODE -------------------------------------
#

if __name__ == '__main__':

    pltOk = True
    try:
        import matplotlib.pylab as plt
    except ImportError:
        pltOk = False
        print("failed to import matplotlib. No on-line plots.")

#
# type of calculation and output file
#
    fileName = "srundplug.spec"

    #bl = getBeamline("ID16_NA")
    bl = getBeamline("ESRF_HB")

    icalc = 1  # 0=generalities
               # 1=flux spectrum
               # 2=power density
               # 3=3d matrix (Hor,Ver,Ener,Intens)


#
# calculate info
#
    if icalc == 0:
        tmp = calcUndulator(bl,photonEnergy=[5e3,10e3,20e3],distance=20.0)

#
# calculate flux
#
    if icalc == 1:
        emin = 3000.0
        emax = 55000.0
        npoints = 500

        e,f = calc1dSrw(bl,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,fileName=fileName,fileAppend=False)
        if pltOk:
            plt.figure(1)
            plt0 = plt.plot(e,f,'blue',label='Srw')

        e,f = calc1dUrgent(bl,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,fileName=fileName,fileAppend=True)
        if pltOk:
            plt1 = plt.plot(e,f,'green',label='Urgent')

        e,f = calc1dUs(bl,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,fileName=fileName,fileAppend=True)
        if pltOk:
            plt2 = plt.plot(e,f,'red',label='Us')
            #TODO: can be done simpler?
            ax = plt.subplot(111)
            ax.legend(bbox_to_anchor=(1.1, 1.05))
            ax.set_yscale('log')

#
# calculate power density
#
    if icalc == 2:
        h,v,p = calc2dSrw(bl,fileName=fileName,fileAppend=False)
        #
        if pltOk:
            plt.figure(2)
            h1,v1 = numpy.meshgrid(h,v) # not needed!
            plt3 = plt.contour(h1,v1,p.T,levels=numpy.linspace(0,p.max(),100))
            plt.title('Srw')
            plt.xlabel('H [mm]')
            plt.ylabel('V [mm]')
            cbar = plt.colorbar(plt3 , format="%.2f")
            cbar.ax.set_ylabel('Power density [$W/mm^2$]')

        h,v,p = calc2dUrgent(bl,fileName=fileName,fileAppend=True)
        #
        if pltOk:
            plt.figure(3)
            h1,v1 = numpy.meshgrid(h,v) # not needed!
            plt4 = plt.contour(h1,v1,p.T,levels=numpy.linspace(0,p.max(),100))
            plt.title('Urgent')
            plt.xlabel('H [mm]')
            plt.ylabel('V [mm]')
            cbar = plt.colorbar(plt4 , format="%.2f")
            cbar.ax.set_ylabel('Power density [$W/mm^2$]')


        h,v,p = calc2dUs(bl,fileName=fileName,fileAppend=True)
        #
        if pltOk:
            plt.figure(4)
            h1,v1 = numpy.meshgrid(h,v) # not needed!
            plt5 = plt.contour(h1,v1,p.T,levels=numpy.linspace(0,p.max(),100))
            plt.title('Us')
            plt.xlabel('H [mm]')
            plt.ylabel('V [mm]')
            cbar = plt.colorbar(plt5 , format="%.2f")
            cbar.ax.set_ylabel('Power density [$W/mm^2$]')

#
# calculate intensity vs H,V,E
#
    if icalc == 3:
        emin = 6000.0
        emax = 12000.0
        npoints = 11

        e,h,v,f = calc3dSrw(bl,photonEnergyMin=emin,photonEnergyMax=emax,
              photonEnergyPoints=npoints,fileName=fileName,fileAppend=False)

        e,h,v,f = calc3dUrgent(bl,photonEnergyMin=emin,photonEnergyMax=emax, \
              photonEnergyPoints=npoints,fileName=fileName,fileAppend=True)

        e,h,v,f = calc3dUs(bl,photonEnergyMin=emin,photonEnergyMax=emax, \
              photonEnergyPoints=npoints,fileName=fileName,fileAppend=True)



    if pltOk:
        plt.show()

import os
import numpy
from collections import OrderedDict

from Orange import __file__ as orange_init

from orangecontrib.xoppy import *
from orangecontrib.xoppy.util import srfunc
from orangecontrib.xoppy.util import srundplug

import xraylib
import PyMca5.PyMcaPhysics.xrf.Elements as Elements



def reflectivity_fresnel(refraction_index_delta=1e-5,refraction_index_beta=0.0,\
                 grazing_angle_mrad=3.0,roughness_rms_A=0.0,photon_energy_ev=10000.0):
    """
    Calculates the reflectivity of an interface using Fresnel formulas.

    Code adapted from XOP and SHADOW

    :param refraction_index_delta: scalar or array with delta (n=1-delta+i beta)
    :param refraction_index_beta: scalar or array with beta (n=1-delta+i beta)
    :param grazing_angle_mrad: scalar with grazing angle in mrad
    :param roughness_rms_A: scalar with roughness rms in Angstroms
    :param photon_energy_ev: scalar or array with photon energies in eV
    :return: (rs,rp,runp) the s-polarized, p-pol and unpolarized reflectivities
    """
    # ;
    # ; calculation of reflectivity (piece of code adapted from shadow/abrefc)
    # ;
    #
    theta1 = grazing_angle_mrad*1e-3     # in rad
    rough1 = roughness_rms_A*1e-8 # in cm

    # ; epsi = 1 - alpha - i gamma
    # alpha = 2.0D0*k*f1
    # gamma = 2.0D0*k*f2
    alpha = 2*refraction_index_delta
    gamma = 2*refraction_index_beta

    rho = (numpy.sin(theta1))**2 - alpha
    rho += numpy.sqrt((numpy.sin(theta1)**2 - alpha)**2 + gamma**2)
    rho = numpy.sqrt(rho/2)

    rs1 = 4*(rho**2)*(numpy.sin(theta1) - rho)**2 + gamma**2
    rs2 = 4*(rho**2)*(numpy.sin(theta1) + rho)**2 + gamma**2
    rs = rs1/rs2

    ratio1 = 4*rho**2 * (rho*numpy.sin(theta1)-numpy.cos(theta1)**2)**2 + gamma**2*numpy.sin(theta1)**2
    ratio2 = 4*rho**2 * (rho*numpy.sin(theta1)+numpy.cos(theta1)**2)**2 + gamma**2*numpy.sin(theta1)**2
    ratio = ratio1/ratio2

    rp = rs*ratio
    runp = 0.5 * (rs + rp)
    wavelength_m = srfunc.m2ev/photon_energy_ev
    debyewaller = numpy.exp( -(4.0*numpy.pi*numpy.sin(theta1)*rough1/(wavelength_m*1e10))**2 )

    return(rs*debyewaller,rp*debyewaller,runp*debyewaller)



def xoppy_calc_black_body(TITLE="Thermal source: Planck distribution",TEMPERATURE=1200000.0,E_MIN=10.0,E_MAX=1000.0,NPOINTS=500):
    print("Inside xoppy_calc_black_body. ")
    return(None)


def xoppy_calc_bm(MACHINE_NAME="ESRF bending magnet",RB_CHOICE=0,MACHINE_R_M=25.0,BFIELD_T=0.8,\
                  BEAM_ENERGY_GEV=6.04,CURRENT_A=0.1,HOR_DIV_MRAD=1.0,VER_DIV=0,\
                  PHOT_ENERGY_MIN=100.0,PHOT_ENERGY_MAX=100000.0,NPOINTS=500,LOG_CHOICE=1,\
                  PSI_MRAD_PLOT=1.0,PSI_MIN=-1.0,PSI_MAX=1.0,PSI_NPOINTS=500,TYPE_CALC=0):
    print("Inside xoppy_calc_bm. ")

    outFile = "bm.spec"

    # electron energy in GeV
    gamma = BEAM_ENERGY_GEV*1e3/srfunc.codata_mee

    r_m = MACHINE_R_M      # magnetic radius in m
    if RB_CHOICE == 1:
        r_m = srfunc.codata_me * srfunc.codata_c / srfunc.codata_ec / BFIELD_T * numpy.sqrt( gamma*gamma - 1)

    # calculate critical energy in eV
    ec_m = 4.0*numpy.pi*r_m/3.0/numpy.power(gamma,3) # wavelength in m
    ec_ev = srfunc.m2ev/ec_m


    if TYPE_CALC == 0:


        if LOG_CHOICE == 0:
            energy_ev = numpy.linspace(PHOT_ENERGY_MIN,PHOT_ENERGY_MAX,NPOINTS) # photon energy grid
        else:
            energy_ev = numpy.logspace(numpy.log10(PHOT_ENERGY_MIN),numpy.log10(PHOT_ENERGY_MAX),NPOINTS) # photon energy grid

        a5 = srfunc.sync_ene(VER_DIV,energy_ev,ec_ev=ec_ev,polarization=0,  \
               e_gev=BEAM_ENERGY_GEV,i_a=CURRENT_A,hdiv_mrad=HOR_DIV_MRAD, \
               psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a5par = srfunc.sync_ene(VER_DIV,energy_ev,ec_ev=ec_ev,polarization=1,  \
               e_gev=BEAM_ENERGY_GEV,i_a=CURRENT_A,hdiv_mrad=HOR_DIV_MRAD, \
               psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a5per = srfunc.sync_ene(VER_DIV,energy_ev,ec_ev=ec_ev,polarization=2,  \
               e_gev=BEAM_ENERGY_GEV,i_a=CURRENT_A,hdiv_mrad=HOR_DIV_MRAD, \
               psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        if VER_DIV == 0:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw]','Power[Watts/eV]']
            title='integrated in Psi,'
        if VER_DIV == 1:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw/mradPsi]','Power[Watts/eV/mradPsi]']
            title='at Psi=0,'
        if VER_DIV == 2:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw]','Power[Watts/eV]']
            title='in Psi=[%e,%e]'%(PSI_MIN,PSI_MAX)

        if VER_DIV == 3:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw/mradPsi]','Power[Watts/eV/mradPsi]']
            title='at Psi=%e mrad'%(PSI_MIN)

        a6=numpy.zeros((7,len(energy_ev)))
        a1 = energy_ev
        a6[0,:] = (a1)
        a6[1,:] = srfunc.m2ev*1e10/(a1)
        a6[2,:] = (a1)/ec_ev # E/Ec
        a6[3,:] = (a5par)/(a5)
        a6[4,:] = (a5per)/(a5)
        a6[5,:] = (a5)
        a6[6,:] = (a5)*1e3*srfunc.codata_ec




    if TYPE_CALC == 1:  # angular distributions over over all energies
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        a6 = numpy.zeros((6,NPOINTS))
        a6[0,:] = angle_mrad # angle in mrad
        a6[1,:] = angle_mrad*gamma/1e3 # Psi[rad]*Gamma
        a6[2,:] = srfunc.sync_f(angle_mrad*gamma/1e3)
        a6[3,:] = srfunc.sync_f(angle_mrad*gamma/1e3,polarization=1)
        a6[4,:] = srfunc.sync_f(angle_mrad*gamma/1e3,polarization=2)
        a6[5,:] = srfunc.sync_ang(0,angle_mrad,i_a=CURRENT_A,hdiv_mrad=HOR_DIV_MRAD,e_gev=BEAM_ENERGY_GEV, r_m=r_m)

        coltitles=['Psi[mrad]','Psi[rad]*Gamma','F','F s-pol','F p-pol','Power[Watts/mrad(Psi)]']

    if TYPE_CALC == 2:  # angular distributions at a single energy
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        a6 = numpy.zeros((7,NPOINTS))
        a6[0,:] = angle_mrad # angle in mrad
        a6[1,:] = angle_mrad*gamma/1e3 # Psi[rad]*Gamma
        a6[2,:] = srfunc.sync_f(angle_mrad*gamma/1e3)
        a6[3,:] = srfunc.sync_f(angle_mrad*gamma/1e3,polarization=1)
        a6[4,:] = srfunc.sync_f(angle_mrad*gamma/1e3,polarization=2)
        tmp = srfunc.sync_ang(1,angle_mrad,energy=PHOT_ENERGY_MIN,i_a=CURRENT_A,hdiv_mrad=HOR_DIV_MRAD,e_gev=BEAM_ENERGY_GEV, ec_ev=ec_ev)
        tmp.shape = -1
        a6[5,:] = tmp
        a6[6,:] = a6[5,:]*srfunc.codata_ec*1e3

        coltitles=['Psi[mrad]','Psi[rad]*Gamma','F','F s-pol','F p-pol','Flux[Ph/sec/0.1%bw/mradPsi]','Power[Watts/eV/mradPsi]']


    if TYPE_CALC == 3:  # angular,energy distributions flux
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        if LOG_CHOICE == 0:
            energy_ev = numpy.linspace(PHOT_ENERGY_MIN,PHOT_ENERGY_MAX,NPOINTS) # photon energy grid
        else:
            energy_ev = numpy.logspace(numpy.log10(PHOT_ENERGY_MIN),numpy.log10(PHOT_ENERGY_MAX),NPOINTS) # photon energy grid

        tmp1, fm, a = srfunc.sync_ene(2,energy_ev,ec_ev=ec_ev,e_gev=BEAM_ENERGY_GEV,i_a=CURRENT_A,\
                                      hdiv_mrad=HOR_DIV_MRAD,psi_min=PSI_MIN,psi_max=PSI_MAX,psi_npoints=PSI_NPOINTS)

        a6 = numpy.zeros((4,len(a)*len(energy_ev)))
        ij = -1
        for i in range(len(a)):
            for j in range(len(energy_ev)):
                ij += 1
                a6[0,ij] = a[i]
                a6[1,ij] = energy_ev[j]
                a6[2,ij] = fm[i,j]*srfunc.codata_ec*1e3
                a6[3,ij] = fm[i,j]

        coltitles=['Psi [mrad]','Photon Energy [eV]','Power [Watts/eV/mradPsi]','Flux [Ph/sec/0.1%bw/mradPsi]']



        import matplotlib.pylab as plt
        from mpl_toolkits.mplot3d import Axes3D  # need for example 6

        toptitle='Flux vs vertical angle and photon energy'
        xtitle  ='angle [mrad]'
        ytitle  ='energy [eV]'
        ztitle = "Photon flux [Ph/s/mrad/0.1%bw]"
        pltN = 0
        fig = plt.figure(pltN)
        ax = fig.add_subplot(111, projection='3d')
        fa, fe = numpy.meshgrid(a, energy_ev)
        surf = ax.plot_surface(fa, fe, fm.T, \
            rstride=1, cstride=1, \
            linewidth=0, antialiased=False)

        plt.title(toptitle)
        ax.set_xlabel(xtitle)
        ax.set_ylabel(ytitle)
        ax.set_zlabel(ztitle)
        plt.show()



    # write spec file
    ncol = len(coltitles)
    npoints = len(a6[0,:])

    f = open(outFile,"w")
    f.write("#F "+outFile+"\n")
    f.write("\n")
    f.write("#S 1 bm results\n")
    f.write("#N %d\n"%(ncol))
    f.write("#L")
    for i in range(ncol):
        f.write("  "+coltitles[i])
    f.write("\n")

    for i in range(npoints):
            f.write((" %e "*ncol+"\n")%(tuple(a6[:,i].tolist())))
    f.close()
    print("File written to disk: "+outFile)


    return(outFile)






def xoppy_calc_mlayer(MODE=0,SCAN=0,F12_FLAG=0,SUBSTRATE="Si",ODD_MATERIAL="Si",EVEN_MATERIAL="W",ENERGY=8050.0,\
                      THETA=0.0,SCAN_STEP=0.009999999776483,NPOINTS=600,ODD_THICKNESS=25.0,EVEN_THICKNESS=25.0,\
                      NLAYERS=50,FILE="layers.dat"):
    print("Inside xoppy_calc_mlayer. ")
    return(None)



def xoppy_calc_nsources(TEMPERATURE=300.0,ZONE=0,MAXFLUX_F=200000000000000.0,MAXFLUX_EPI=20000000000000.0,\
                        MAXFLUX_TH=200000000000000.0,NPOINTS=500):
    print("Inside xoppy_calc_nsources. ")
    return(None)



def xoppy_calc_ws(TITLE="Wiggler A at APS",ENERGY=7.0,CUR=100.0,PERIOD=8.5,N=28.0,KX=0.0,KY=8.739999771118164,\
                  EMIN=1000.0,EMAX=100000.0,NEE=2000,D=30.0,XPC=0.0,YPC=0.0,XPS=2.0,YPS=2.0,NXP=10,NYP=10):
    print("Inside xoppy_calc_ws. ")
    pwd = os.getcwd()
    # os.chdir(home_wd)
    with open("ws.inp","wt") as f:
        f.write("%s\n"%(TITLE))
        f.write("%f     %f\n"%(ENERGY,CUR))
        f.write("%f  %d  %f  %f\n"%(PERIOD,N,KX,KY))
        f.write("%f  %f   %f\n"%(EMIN,EMAX,NEE))
        f.write("%f  %f  %f  %f  %f  %f  %f\n"%(D,XPC,YPC,XPS,YPS,NXP,NYP))
        f.write("%d  \n"%(4))
    command = os.path.join(home_bin,'ws')
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")

    # write spec file
    txt = open("ws.out").readlines()
    f = open("ws.spec","w")

    f.write("#F ws.spec\n")
    f.write("\n")
    f.write("#S 1 ws results\n")
    f.write("#N 6\n")
    f.write("#L  Energy(eV)  Flux(ph/s/0.1%bw)  p1  p2  p3  p4")
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           f.write(tmp)
        else:
           f.write("#UD "+tmp)
    f.close()
    print("File written to disk: ws.spec")

    #os.chdir(pwd)
    outFile = "ws.spec"
    return(outFile)






    return(None)



def xoppy_calc_xtubes(ITUBE=0,VOLTAGE=30.0):
    print("Inside xoppy_calc_xtubes. ")
    pwd = os.getcwd()
    #os.chdir(home_wd)
    with open("xoppy.inp","wt") as f:
        f.write("%d\n%f\n"%(ITUBE+1,VOLTAGE))
    command = os.path.join(home_bin,'xtubes') + " < xoppy.inp"
    print("Running command '%s' in directory: %s "%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")
    os.chdir(pwd)
    outFile = "xtubes_tmp.dat"
    return(outFile)


def xoppy_calc_xtube_w(VOLTAGE=100.0,RIPPLE=0.0,AL_FILTER=0.0):
    print("Inside xoppy_calc_xtube_w. ")
    pwd = os.getcwd()
    #os.chdir(home_wd)
    with open("xoppy.inp","wt") as f:
        f.write("%f\n%f\n%f\n"%(VOLTAGE,RIPPLE,AL_FILTER))
    command = os.path.join(home_bin,'tasmip') + " < xoppy.inp"
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")
    os.chdir(pwd)
    outFile = "tasmip_tmp.dat"
    return(outFile)



def xoppy_calc_xinpro(CRYSTAL_MATERIAL=0,MODE=0,ENERGY=8000.0,MILLER_INDEX_H=1,MILLER_INDEX_K=1,MILLER_INDEX_L=1,\
                      ASYMMETRY_ANGLE=0.0,THICKNESS=500.0,TEMPERATURE=300.0,NPOINTS=100,SCALE=0,XFROM=-50.0,XTO=50.0):
    print("Inside xoppy_calc_xinpro. ")
    pwd = os.getcwd()
    #os.chdir(home_wd)
    with open("xoppy.inp","wt") as f:
        f.write("%s\n"% (os.path.join(home_data,"inpro"+os.sep)))
        if MODE == 0:
            f.write("+1\n")
        elif MODE == 1:
            f.write("-1\n")
        elif MODE == 2:
            f.write("+2\n")
        elif MODE == 3:
            f.write("-1\n")
        else:
            f.write("ERROR!!\n")

        f.write("%f\n%d\n"%(THICKNESS,CRYSTAL_MATERIAL+1))
        f.write("%s\n%f\n"%("EV",ENERGY))
        f.write("%d\n%d\n%d\n"%(MILLER_INDEX_H,MILLER_INDEX_K,MILLER_INDEX_L))
        f.write("%f\n%f\n%s\n"%(ASYMMETRY_ANGLE,TEMPERATURE,"inpro.dat"))
        if SCALE == 0:
            f.write("1\n")
        else:
            f.write("%d\n%f\n%f\n"%(2,XFROM,XTO))
        f.write("%d\n"%(NPOINTS))
            
    command = os.path.join(home_bin,'inpro') + " < xoppy.inp"
    print("Running command '%s' in directory: %s "%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")
    #add SPEC header
    txt = open("inpro.dat").read()
    f = open("inpro.spec","w")
    f.write("#F inpro.spec\n")
    f.write("\n")
    f.write("#S 1 inpro results\n")
    f.write("#N 3\n")
    f.write("#L Theta-TetaB  s-polarized reflectivity  p-polarized reflectivity\n")
    f.write(txt)
    f.close()
    print("File written to disk: inpro.dat, inpro.par, inpro.spec")

     #exit
    #os.chdir(pwd)
    outFile = "inpro.spec"

    return(outFile)



def xoppy_calc_xcrystal(FILEF0=0,FILEF1F2=0,FILECROSSSEC=0,CRYSTAL_MATERIAL=0,\
                        MILLER_INDEX_H=1,MILLER_INDEX_K=1,MILLER_INDEX_L=1,\
                        I_ABSORP=2,TEMPER="1.0",MOSAIC=0,GEOMETRY=0,SCAN=2,UNIT=1,\
                        SCANFROM=-100.0,SCANTO=100.0,SCANPOINTS=200,ENERGY=8000.0,\
                        ASYMMETRY_ANGLE=0.0,THICKNESS=0.7,MOSAIC_FWHM=0.1,RSAG=125.0,RMER=1290.0,\
                        ANISOTROPY=0,POISSON=0.22,CUT="2 -1 -1 ; 1 1 1 ; 0 0 0",FILECOMPLIANCE="mycompliance.dat"):
    print("Inside xoppy_calc_xcrystal. ")
    return(None)



def xoppy_calc_xwiggler(FIELD=0,NPERIODS=12,ULAMBDA=0.125,K=14.0,ENERGY=6.04,PHOT_ENERGY_MIN=100.0,\
                        PHOT_ENERGY_MAX=100100.0,NPOINTS=100,LOGPLOT=1,NTRAJPOINTS=101,CURRENT=200.0,FILE="?"):

    print("Inside xoppy_calc_xwiggler. ")

    outFileTraj = "xwiggler_traj.spec"
    outFile = "xwiggler.spec"

    if FIELD == 0:
        t0,p = srfunc.wiggler_trajectory(b_from=0, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS,  \
                                 ener_gev=ENERGY, per=ULAMBDA, kValue=K, \
                                 trajFile=outFileTraj)
    if FIELD == 1:
        # magnetic field from B(s) map
        t0,p = srfunc.wiggler_trajectory(b_from=1, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS,  \
                       ener_gev=ENERGY4, inData=FILE,trajFile=outFileTraj)
    if FIELD == 2:
        # magnetic field from harmonics
        # hh = srfunc.wiggler_harmonics(b_t,Nh=41,fileOutH="tmp.h")
        t0,p = srfunc.wiggler_trajectory(b_from=2, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS,  \
                       ener_gev=ENERGY, per=ULAMBDA, inData="",trajFile=outFileTraj)
    print(p)
    #
    # now spectra
    #
    e, f0 = srfunc.wiggler_spectrum(t0,enerMin=PHOT_ENERGY_MIN,enerMax=PHOT_ENERGY_MAX,nPoints=NPOINTS, \
                 electronCurrent=CURRENT*1e-3, outFile=outFile, elliptical=False)

    return(outFile)



def xoppy_calc_xxcom(NAME="Pyrex Glass",SUBSTANCE=3,DESCRIPTION="SiO2:B2O3:Na2O:Al2O3:K2O",\
                     FRACTION="0.807:0.129:0.038:0.022:0.004",GRID=1,GRIDINPUT=0,\
                     GRIDDATA="0.0804:0.2790:0.6616:1.3685:2.7541",ELEMENTOUTPUT=0):
    print("Inside xoppy_calc_xxcom. ")

    pwd = os.getcwd()
    #os.chdir(home_wd)
    with open("xoppy.inp","wt") as f:
        f.write( os.path.join(home_data,'xcom')+os.sep+"\n" )
        f.write( NAME+"\n" )
        f.write("%d\n"%(1+SUBSTANCE))
        if (1+SUBSTANCE) != 4:
            f.write( DESCRIPTION+"\n")
            if (1+SUBSTANCE) <= 2:
                f.write("%d\n"%(1+ELEMENTOUTPUT))
        else:
            nn = DESCRIPTION.split(":")
            mm = FRACTION.split(":")
            f.write("%d\n"%( len(nn)))
            print(">>>>>>>",nn,len(nn))
            for i in range(len(nn)):
                print("<><><><>",i,nn[i],mm[i])
                f.write(nn[i]+"\n")
                f.write(mm[i]+"\n")
            f.write("1\n")
        f.write("%d\n"%(1+GRID))
        if (1+GRID) != 1:
            f.write("%d\n"%(1+GRIDINPUT))
            if (1+GRIDINPUT) == 1:
                nn = GRIDDATA.split(":")
                f.write("%d\n"%( len(nn)))
                for i in nn:
                    f.write(i+"\n")
                if (1+GRID) != 1:
                    f.write("N\n")
        f.write("xcom.out\n")
        f.write("1\n")
        f.close()

    command = os.path.join(home_bin,'xcom') + " < xoppy.inp"
    print("Running command '%s' in directory: %s "%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")
    # write spec file

    if (1+SUBSTANCE) <= 2:
        if (1+ELEMENTOUTPUT) == 1:
            titles = "Photon Energy [Mev]  Coherent scat [b/atom]  " \
                     "Incoherent scat [b/atom]  Photoel abs [b/atom]  " \
                     "Pair prod in nucl field [b/atom]  Pair prod in elec field [b/atom]  " \
                     "Tot atten with coh scat [b/atom]  Tot atten w/o coh scat [b/atom]"
        elif (1+ELEMENTOUTPUT) == 2:
            titles = "Photon Energy [Mev]  Coherent scat [b/atom]  " \
                     "Incoherent scat [b/atom]  Photoel abs [b/atom]  " \
                     "Pair prod in nucl field [b/atom]  Pair prod in elec field [b/atom]  " \
                     "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"
        elif (1+ELEMENTOUTPUT) == 3:
            titles = "Photon Energy [Mev]  Coherent scat [cm2/g]  " \
                     "Incoherent scat [cm2/g]  Photoel abs [cm2/g]  " \
                     "Pair prod in nucl field [cm2/g]  Pair prod in elec field [cm2/g]  " \
                     "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"
        else:
            titles = "Photon Energy [Mev]  Coherent scat [cm2/g]  " \
                     "Incoherent scat [cm2/g]  Photoel abs [cm2/g]  " \
                     "Pair prod in nucl field [cm2/g]  Pair prod in elec field [cm2/g]  " \
                     "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"
    else:
       titles = "Photon Energy [Mev]  Coherent scat [cm2/g]  " \
                "Incoherent scat [cm2/g]  Photoel abs [cm2/g]  " \
                "Pair prod in nucl field [cm2/g]  Pair prod in elec field [cm2/g]  " \
                "Tot atten with coh scat [cm2/g]  Tot atten w/o coh scat [cm2/g]"


    txt = open("xcom.out").readlines()
    f = open("xcom.spec","w")

    f.write("#F xcom.spec\n")
    f.write("\n")
    f.write("#S 1 xcom results\n")
    f.write("#N 8\n")
    f.write("#L  "+titles+"\n")
    for i in txt:
        tmp = i.strip(" ")
        if tmp[0].isdigit():
           f.write(tmp)
        else:
           f.write("#UD "+tmp)
    f.close()
    print("File written to disk: xcom.spec")


    #os.chdir(pwd)
    outFile = "xcom.spec"
    return(outFile)




    return(None)



def xoppy_calc_xbfield(PERIOD=4.0,NPER=42,NPTS=40,IMAGNET=0,ITYPE=0,K=1.379999995231628,GAP=2.0,GAPTAP=10.0,FILE="undul.bf"):
    print("Inside xoppy_calc_xbfield. ")
    return(None)



def xoppy_calc_xfilter(EMPTY1="              ",EMPTY2="              ",NELEMENTS=1,SOURCE=0,ENER_MIN=1000.0,ENER_MAX=50000.0,ENER_N=100,SOURCE_FILE="SRCOMPW",EL1_SYM="Be",EL1_THI=500.0,EL2_SYM="Al",EL2_THI=50.0,EL3_SYM="Pt",EL3_THI=10.0,EL4_SYM="Au",EL4_THI=10.0,EL5_SYM="Cu",EL5_THI=10.0):
    print("Inside xoppy_calc_xfilter. ")
    return(None)


#
# undulators
#

def xoppy_calc_undulator_flux(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                              ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                              ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                              PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                              PHOTONENERGYMIN=3000.0,PHOTONENERGYMAX=55000.0,PHOTONENERGYPOINTS=500,METHOD=0):
    print("Inside xoppy_calc_undulator_flux. ")

    bl = OrderedDict()
    bl['ElectronBeamDivergenceH'] = ELECTRONBEAMDIVERGENCEH
    bl['ElectronBeamDivergenceV'] = ELECTRONBEAMDIVERGENCEV
    bl['ElectronBeamSizeH'] = ELECTRONBEAMSIZEH
    bl['ElectronBeamSizeV'] = ELECTRONBEAMSIZEV
    bl['ElectronCurrent'] = ELECTRONCURRENT
    bl['ElectronEnergy'] = ELECTRONENERGY
    bl['ElectronEnergySpread'] = ELECTRONENERGYSPREAD
    bl['Kv'] = KV
    bl['NPeriods'] = NPERIODS
    bl['PeriodID'] = PERIODID
    bl['distance'] = DISTANCE
    bl['gapH'] = GAPH
    bl['gapV'] = GAPV


    # tmp = srundplug.calcUndulator(bl,distance=DISTANCE,\
    #                               photonEnergy=[PHOTONENERGYMIN,0.5*(PHOTONENERGYMIN+PHOTONENERGYMAX),PHOTONENERGYMAX])

    outFile = "undulator_flux.spec"
    if METHOD == 0:
        print("Undulator flux calculation using US. Please wait...")
        e,f = srundplug.calc1dUs(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")
    if METHOD == 1:
        print("Undulator flux calculation using URGENT. Please wait...")
        e,f = srundplug.calc1dUrgent(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")
    if METHOD == 2:
        print("Undulator flux calculation using SRW. Please wait...")
        e,f = srundplug.calc1dSrw(bl,photonEnergyMin=PHOTONENERGYMIN,photonEnergyMax=PHOTONENERGYMAX,
              photonEnergyPoints=PHOTONENERGYPOINTS,fileName=outFile,fileAppend=False)
        print("Done")

    return(outFile)



def xoppy_calc_undulator_power_density(ELECTRONENERGY=6.04,ELECTRONENERGYSPREAD=0.001,ELECTRONCURRENT=0.2,\
                                       ELECTRONBEAMSIZEH=0.000395,ELECTRONBEAMSIZEV=9.9e-06,\
                                       ELECTRONBEAMDIVERGENCEH=1.05e-05,ELECTRONBEAMDIVERGENCEV=3.9e-06,\
                                       PERIODID=0.018,NPERIODS=222,KV=1.68,DISTANCE=30.0,GAPH=0.001,GAPV=0.001,\
                                       HSLITPOINTS=101,VSLITPOINTS=51,METHOD=0):
    print("Inside xoppy_calc_undulator_power_density. ")

    bl = OrderedDict()
    bl['ElectronBeamDivergenceH'] = ELECTRONBEAMDIVERGENCEH
    bl['ElectronBeamDivergenceV'] = ELECTRONBEAMDIVERGENCEV
    bl['ElectronBeamSizeH'] = ELECTRONBEAMSIZEH
    bl['ElectronBeamSizeV'] = ELECTRONBEAMSIZEV
    bl['ElectronCurrent'] = ELECTRONCURRENT
    bl['ElectronEnergy'] = ELECTRONENERGY
    bl['ElectronEnergySpread'] = ELECTRONENERGYSPREAD
    bl['Kv'] = KV
    bl['NPeriods'] = NPERIODS
    bl['PeriodID'] = PERIODID
    bl['distance'] = DISTANCE
    bl['gapH'] = GAPH
    bl['gapV'] = GAPV


    # tmp = srundplug.calcUndulator(bl,distance=DISTANCE,\
    #                               photonEnergy=[PHOTONENERGYMIN,0.5*(PHOTONENERGYMIN+PHOTONENERGYMAX),PHOTONENERGYMAX])

    outFile = "undulator_power_density.spec"
    if METHOD == 0:
        print("Undulator power_density calculation using US. Please wait...")
        h,v,p = srundplug.calc2dUs(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS)
        print("Done")
    if METHOD == 1:
        print("Undulator power_density calculation using URGENT. Please wait...")
        h,v,p = srundplug.calc2dUrgent(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS)
        print("Done")
    if METHOD == 2:
        print("Undulator power_density calculation using SRW. Please wait...")
        h,v,p = srundplug.calc2dSrw(bl,fileName=outFile,fileAppend=False,hSlitPoints=HSLITPOINTS,vSlitPoints=VSLITPOINTS)
        print("Done")

    return(outFile)

def xoppy_calc_xpower(F1F2=0,MU=0,SOURCE=1,DUMMY1="",DUMMY2="",DUMMY3="",ENER_MIN=1000.0,ENER_MAX=50000.0,ENER_N=100,\
                      SOURCE_FILE="?",NELEMENTS=1,\
                      EL1_FOR="Be",EL1_FLAG=0,EL1_THI=0.5,EL1_ANG=3.0,EL1_ROU=0.0,EL1_DEN="?",\
                      EL2_FOR="Rh",EL2_FLAG=1,EL2_THI=0.5,EL2_ANG=3.0,EL2_ROU=0.0,EL2_DEN="?",\
                      EL3_FOR="Al",EL3_FLAG=0,EL3_THI=0.5,EL3_ANG=3.0,EL3_ROU=0.0,EL3_DEN="?",\
                      EL4_FOR= "B",EL4_FLAG=0,EL4_THI=0.5,EL4_ANG=3.0,EL4_ROU=0.0,EL4_DEN="?",\
                      EL5_FOR="Pt",EL5_FLAG=1,EL5_THI=0.5,EL5_ANG=3.0,EL5_ROU=0.0,EL5_DEN="?"):
    print("Inside xoppy_calc_xpower. ")

    # if ENER_N < 1:
    #     print("Error: Number of energy points (%d) not allowed. If you wish to calculate a single energy point, then use the same energy values for the minimum and maximum and use a number of points greater that 1 (e.g. 2)"%(ENER_N))
    #     return None

    if ENER_MAX == ENER_MIN:
        ENER_N = 2

    #xpower_inp

    nelem = 1+NELEMENTS
    substance = [EL1_FOR,EL2_FOR,EL3_FOR,EL4_FOR,EL5_FOR]
    thick     = numpy.array( (EL1_THI,EL2_THI,EL3_THI,EL4_THI,EL5_THI))
    angle     = numpy.array( (EL1_ANG,EL2_ANG,EL3_ANG,EL4_ANG,EL5_ANG))
    dens      = [EL1_DEN,EL2_DEN,EL3_DEN,EL4_DEN,EL5_DEN]
    roughness = numpy.array( (EL1_ROU,EL2_ROU,EL3_ROU,EL4_ROU,EL5_ROU))
    flags     = numpy.array( (EL1_FLAG,EL2_FLAG,EL3_FLAG,EL4_FLAG,EL5_FLAG))

    for i in range(nelem):
        try:
            rho = float(dens[i])
        except:
            # rho = 1.0
            #is element? take density from PyMca
            rho = 0.0
            for item in Elements.ElementsInfo:
                if item[0] == substance[i]: rho = item[6]*1e-3
            if rho != 0:
                print("Found density for %s: %d g/cm3"%(substance[i],rho))
            else:
                print("Undefined density for %s => taking density = 1.0"%(substance[i]))
                rho = 1.0

        dens[i] = rho


    if SOURCE == 0:
        energies = numpy.linspace(1,100,495)
        source = numpy.ones(energies.size)
        tmp = numpy.vstack( (energies,source))
    if SOURCE == 1:
        energies = numpy.linspace(ENER_MIN,ENER_MAX,ENER_N)
        source = numpy.ones(energies.size)
        tmp = numpy.vstack( (energies,source))

    if SOURCE >= 2:
        if SOURCE == 2: source_file = SOURCE_FILE
        if SOURCE == 3: source_file = "SRCOMPE"
        if SOURCE == 4: source_file = "SRCOMPF"
        try:
            tmp = numpy.loadtxt(source_file)
            energies = tmp[:,0]
            source = tmp[:,1]
        except:
            print("Error loading file %s "%(source_file))
            raise

    # if ENER_MIN == ENER_MAX:
    #     energies = energies[0:2]
    #     source = source[0:2]


    outArray = numpy.hstack( energies )
    outColTitles = ["Photon Energy [eV]"]
    outArray = numpy.vstack((outArray,source))
    outColTitles.append("Source")

    txt = ""
    txt += "*************************** Xpower Results ******************\n"
    if energies[0] != energies[-1]:
        txt += "  Source energy: start=%f keV, end=%f keV, points=%d \n"%(energies[0],energies[-1],energies.size)
    else:
        txt += "  Source energy: %f keV\n"%(energies[0])
    txt += "  Number of optical elements: %d\n"%(nelem)

    if energies[0] != energies[-1]:
        # I0 = source[0:-1].sum()*(energies[1]-energies[0])
        I0 = numpy.trapz(source, x=energies, axis=-1)
        txt += "  Incoming power (integral of spectrum): %f \n"%(I0)

        I1 = I0
    else:
        txt += "  Incoming power: %f \n"%(source[0])
        I0  = source[0]
        I1 = I0

    outFile = "xpower.spec"

    cumulated = source

    for i in range(nelem):
        #info oe
        if flags[i] == 0:
            txt += '      *****   oe '+str(i+1)+'  [Filter] *************\n'
            txt += '      Material: %s\n'%(substance[i])
            txt += '      Density [g/cm^3]: %f \n'%(dens[i])
            txt += '      thickness [mm] : %f \n'%(thick[i])
        else:
            txt += '      *****   oe '+str(i+1)+'  [Mirror] *************\n'
            txt += '      Material: %s\n'%(substance[i])
            txt += '      Density [g/cm^3]: %f \n'%(dens[i])
            txt += '      grazing angle [mrad]: %f \n'%(angle[i])
            txt += '      roughness [A]: %f \n'%(roughness[i])


        if flags[i] == 0: # filter
            tmp = numpy.zeros(energies.size)
            for j,energy in enumerate(energies):

                tmp[j] = xraylib.CS_Total_CP(substance[i],energy/1000.0)

            trans = numpy.exp(-tmp*dens[i]*(thick[i]/10.0))
            outArray = numpy.vstack((outArray,tmp))
            outColTitles.append("[oe %i] Total CS cm2/g"%(1+i))
            print(outArray)

            outArray = numpy.vstack((outArray,tmp*dens[i]))
            outColTitles.append("[oe %i] Mu cm^-1"%(1+i))


            outArray = numpy.vstack((outArray,trans))
            outColTitles.append("[oe %i] Transmitivity "% (1+i))
            outArray = numpy.vstack((outArray,1.0-trans))
            outColTitles.append("[oe %i] Absorption "% (1+i))

            cumulated *= trans

        if flags[i] == 1: # mirror
            tmp = numpy.zeros(energies.size)
            for j,energy in enumerate(energies):
                tmp[j] = xraylib.Refractive_Index_Re(substance[i],energy/1000.0,dens[i])
            delta = 1.0 - tmp
            outArray = numpy.vstack((outArray,delta))
            outColTitles.append("[oe %i] 1-Re[n]=delta"%(1+i))

            beta = numpy.zeros(energies.size)
            for j,energy in enumerate(energies):
                beta[j] = xraylib.Refractive_Index_Im(substance[i],energy/1000.0,dens[i])
            outArray = numpy.vstack((outArray,beta))
            outColTitles.append("[oe %i] Im[n]=beta"%(1+i))

            outArray = numpy.vstack((outArray,delta/beta))
            outColTitles.append("[oe %i] delta/beta"%(1+i))

            (rs,rp,runp) = reflectivity_fresnel(refraction_index_beta=beta,refraction_index_delta=delta,\
                                        grazing_angle_mrad=angle[i],roughness_rms_A=roughness[i],\
                                        photon_energy_ev=energies)
            outArray = numpy.vstack((outArray,rs))
            outColTitles.append("[oe %i] Reflectivity-s"%(1+i))
            outArray = numpy.vstack((outArray,1.0-rs))
            outColTitles.append("[oe %i] Transmitivity"%(1+i))

            cumulated *= rs

        if energies[0] != energies[-1]:
            # I2 = cumulated[0:-1].sum()*(energies[1]-energies[0])
            #txt += "      Outcoming power [Sum]: %f\n"%(I2)
            #txt += "      Outcoming power [Trapez]: %f\n"%(I2b)
            I2 = numpy.trapz( cumulated, x=energies, axis=-1)
            txt += "      Outcoming power: %f\n"%(I2)
            txt += "      Absorbed power: %f\n"%(I1-I2)
            txt += "      Normalized Outcoming Power: %f\n"%(I2/I0)
            if flags[i] == 0:
                pass
                txt += "      Absorbed dose Gy.(mm^2 beam cross section)/s %f\n: "%((I1-I2)/(dens[i]*thick[i]*1e-6))
            I1 = I2
        else:
            I2 = cumulated[0]
            txt += "      Outcoming power: %f\n"%(cumulated[0])
            txt += "      Absorbed power: %f\n"%(I1-I2)
            txt += "      Normalized Outcoming Power: %f\n"%(I2/I0)
            I1 = I2

        outArray = numpy.vstack((outArray,cumulated))
        outColTitles.append("Intensity after oe #%i"%(1+i))



        #

    ncol = len(outColTitles)
    npoints = energies.size

    f = open(outFile,"w")
    f.write("#F "+outFile+"\n")
    f.write("\n")
    f.write("#S 1 xpower: properties of optical elements\n")

    txt2 = txt.splitlines()
    for i in range(len(txt2)):
        f.write("#UINFO %s\n"%(txt2[i]))

    f.write("#N %d\n"%(ncol))
    f.write("#L")
    for i in range(ncol):
        f.write("  "+outColTitles[i])
    f.write("\n")

    for i in range(npoints):
            f.write((" %e "*ncol+"\n")%(tuple(outArray[:,i].tolist())))

    f.close()
    print("File written to disk: "+outFile)

    print(txt)


    return(outFile)

def xoppy_calc_xtc(TITLE="APS Undulator A, Beam Parameters for regular lattice nux36nuy39.twi, 1.5% cpl.",ENERGY=7.0,CUR=100.0,SIGE=0.000959999975748,TEXT_MACHINE="",SIGX=0.273999989032745,SIGY=0.010999999940395,SIGX1=0.011300000362098,SIGY1=0.00359999993816,TEXT_BEAM="",PERIOD=3.299999952316284,NP=70,TEXT_UNDULATOR="",EMIN=2950.0,EMAX=13500.0,N=20,TEXT_ENERGY="",IHMIN=1,IHMAX=15,IHSTEP=2,TEXT_HARM="",IHEL=0,METHOD=1,IK=1,NEKS=100,TEXT_PARM="",RUN_MODE_NAME="foreground"):
    print("Inside xoppy_calc_xtc. ")
    return(None)



def xoppy_calc_xus(TITLE="APS Undulator A, Beam Parameters for regular lattice nux36nuy39.twi, 1.5% cpl.",ENERGY=7.0,CUR=100.0,TEXT_MACHINE="",SIGX=0.273999989032745,SIGY=0.010999999940395,SIGX1=0.011300000362098,SIGY1=0.00359999993816,TEXT_BEAM="",PERIOD=3.299999952316284,NP=70,KX=0.0,KY=2.75,TEXT_UNDULATOR="",EMIN=1000.0,EMAX=50000.0,N=5000,TEXT_ENERGY="",D=30.0,XPC=0.0,YPC=0.0,XPS=2.5,YPS=1.0,NXP=25,NYP=10,TEXT_PINHOLE="",MODE=2,METHOD=4,IHARM=0,TEXT_MODE="",NPHI=0,NALPHA=0,CALPHA2=0.0,NOMEGA=64,COMEGA=8.0,NSIGMA=0,TEXT_CALC="",RUN_MODE_NAME="foreground"):
    print("Inside xoppy_calc_xus. ")
    return(None)



def xoppy_calc_xurgent(TITLE="ESRF HIGH BETA UNDULATOR",ENERGY=6.039999961853027,CUR=0.100000001490116,SIGX=0.400000005960464,SIGY=0.079999998211861,SIGX1=0.016000000759959,SIGY1=0.00899999961257,ITYPE=1,PERIOD=0.046000000089407,N=32,KX=0.0,KY=1.700000047683716,PHASE=0.0,EMIN=10000.0,EMAX=50000.0,NENERGY=100,D=27.0,XPC=0.0,YPC=0.0,XPS=3.0,YPS=3.0,NXP=25,NYP=25,MODE=4,ICALC=2,IHARM=-1,NPHI=0,NSIG=0,NALPHA=0,DALPHA=0.0,NOMEGA=0,DOMEGA=0.0):
    print("Inside xoppy_calc_xurgent. ")
    return(None)



def xoppy_calc_xyaup(TITLE="YAUP EXAMPLE (ESRF BL-8)",PERIOD=4.0,NPER=42,NPTS=40,EMIN=3000.0,EMAX=30000.0,NENERGY=100,ENERGY=6.039999961853027,CUR=0.100000001490116,SIGX=0.425999999046326,SIGY=0.08500000089407,SIGX1=0.017000000923872,SIGY1=0.008500000461936,D=30.0,XPC=0.0,YPC=0.0,XPS=2.0,YPS=2.0,NXP=0,NYP=0,MODE=4,NSIG=2,TRAJECTORY="new+keep",XSYM="yes",HANNING=0,BFILE="undul.bf",TFILE="undul.traj"):
    print("Inside xoppy_calc_xyaup. ")
    return(None)



def xoppy_calc_xf0(DATASETS=0,MAT_FLAG=0,MAT_LIST=0,DESCRIPTOR="Si",GRID=0,GRIDSTART=0.0,GRIDEND=4.0,GRIDN=100):
    print("Inside xoppy_calc_xf0. ")
    return(None)



def xoppy_calc_xcrosssec(DATASETS=1,MAT_FLAG=0,MAT_LIST=0,DESCRIPTOR="Si",DENSITY=1.0,CALCULATE="all",GRID=0,GRIDSTART=100.0,GRIDEND=10000.0,GRIDN=200,UNIT=0):
    print("Inside xoppy_calc_xcrosssec. ")
    return(None)



def xoppy_calc_xf1f2(DATASETS=1,MAT_FLAG=0,MAT_LIST=0,DESCRIPTOR="Si",DENSITY=1.0,CALCULATE=1,GRID=0,GRIDSTART=5000.0,GRIDEND=25000.0,GRIDN=100,THETAGRID=0,ROUGH=0.0,THETA1=2.0,THETA2=5.0,THETAN=50):
    print("Inside xoppy_calc_xf1f2. ")
    return(None)



def xoppy_calc_xfh(FILEF0=0,FILEF1F2=0,FILECROSSSEC=0,ILATTICE=0,HMILLER=1,KMILLER=1,LMILLER=1,I_ABSORP=2,TEMPER="1.0",ENERGY=8000.0,ENERGY_END=18000.0,NPOINTS=20):
    print("Inside xoppy_calc_xfh. ")
    return(None)



def xoppy_calc_mare(CRYSTAL=2,H=2,K=2,L=2,HMAX=3,KMAX=3,LMAX=3,FHEDGE=1e-08,DISPLAY=0,LAMBDA=1.54,DELTALAMBDA=0.009999999776483,PHI=-20.0,DELTAPHI=0.1):
    print("Inside xoppy_calc_mare. ")
    return(None)

def xoppy_calc_xsh_bragg(STRUCTURE=0,LATTICE_CTE_A=5.4309401512146,LATTICE_CTE_C=1.0,H_MILLER_INDEX=1,K_MILLER_INDEX=1,L_MILLER_INDEX=1,SYMBOL_1ST="Si",SYMBOL_2ND="Si",ABSORPTION=1,TEMPERATURE_FACTOR=1.0,E_MIN=5000.0,E_MAX=15000.0,E_STEP=100.0,SHADOW_FILE="reflec.dat",RC=1,MOSAIC=0,RC_MODE=1,RC_ENERGY=8000.0,MOSAIC_FWHM=0.100000001490116,THICKNESS=0.009999999776483,ASYMMETRIC_ANGLE=0.0,ANGULAR_RANGE=100.0,NUMBER_OF_POINTS=200,SEC_OF_ARC=0,CENTERED_CURVE=0,IONIC_ASK=0):
    print("Inside xoppy_calc_xsh_bragg. ")
    return(None)



def xoppy_calc_xsh_pre_mlayer(FILE="mlayer.dat",E_MIN=5000.0,E_MAX=20000.0,S_DENSITY="2.33",S_MATERIAL="Si",E_DENSITY="2.40",E_MATERIAL="B4C",O_DENSITY="9.40",O_MATERIAL="Ru",GRADE_DEPTH=0,N_PAIRS=70,THICKNESS=33.1,GAMMA=0.483,ROUGHNESS_EVEN=3.3,ROUGHNESS_ODD=3.1,FILE_DEPTH="myfile_depth.dat",GRADE_SURFACE=0,FILE_SHADOW="mlayer1.sha",FILE_THICKNESS="mythick.dat",FILE_GAMMA="mygamma.dat",AA0=1.0,AA1=0.0,AA2=0.0):
    print("Inside xoppy_calc_xsh_pre_mlayer. ")
    return(None)



def xoppy_calc_xsh_prerefl(SYMBOL="SiC",DENSITY="3.217",FILE="reflec.dat",E_MIN=100.0,E_MAX=20000.0,E_STEP=100.0):
    print("Inside xoppy_calc_xsh_prerefl. ")
    return(None)



def xoppy_calc_xsh_conic(P=3000.0,Q=1000.0,THETA=3.0,TYPE=2,CONVEX=0,CYL=0,CYLANGLE=0.0,WIDTH=6.0,LENGTH=300.0,NX=10,NY=200,SAG=0,FILE="presurface.dat"):
    print("Inside xoppy_calc_xsh_conic. ")
    return(None)



def xoppy_calc_xraylib_widget(FUNCTION=0,ELEMENT=26,ELEMENTORCOMPOUND="FeSO4",COMPOUND="Ca5(PO4)3",TRANSITION_IUPAC_OR_SIEGBAHN=1,\
                              TRANSITION_IUPAC_TO=0,TRANSITION_IUPAC_FROM=0,TRANSITION_SIEGBAHN=0,SHELL=0,ENERGY=10.0):
    print("Inside xoppy_calc_xraylib with FUNCTION=%d. "%(FUNCTION))

    if FUNCTION == 0:
        if TRANSITION_IUPAC_OR_SIEGBAHN == 0:
            lines = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
            line = lines[TRANSITION_IUPAC_TO]+lines[TRANSITION_IUPAC_FROM]+"_LINE"
            command = "result = xraylib.LineEnergy(%d,xraylib.%s)"%(ELEMENT,line)
            print("executing command: ",command)
            line = getattr(xraylib,line)
            result = xraylib.LineEnergy(ELEMENT,line)
            print("result: %f keV"%(result))
        if TRANSITION_IUPAC_OR_SIEGBAHN == 1:
            lines = ['KA1_LINE', 'KA2_LINE', 'KB1_LINE', 'KB2_LINE', 'KB3_LINE', 'KB4_LINE', 'KB5_LINE', 'LA1_LINE', 'LA2_LINE', 'LB1_LINE', 'LB2_LINE', 'LB3_LINE', 'LB4_LINE', 'LB5_LINE', 'LB6_LINE', 'LB7_LINE', 'LB9_LINE', 'LB10_LINE', 'LB15_LINE', 'LB17_LINE', 'LG1_LINE', 'LG2_LINE', 'LG3_LINE', 'LG4_LINE', 'LG5_LINE', 'LG6_LINE', 'LG8_LINE', 'LE_LINE', 'LL_LINE', 'LS_LINE', 'LT_LINE', 'LU_LINE', 'LV_LINE']
            line = lines[TRANSITION_SIEGBAHN]
            command = "result = xraylib.LineEnergy(%d,xraylib.%s)"%(ELEMENT,line)
            print("executing command: ",command)
            line = getattr(xraylib,line)
            result = xraylib.LineEnergy(ELEMENT,line)
            print("result: %f keV"%(result))
        if TRANSITION_IUPAC_OR_SIEGBAHN == 2:
            lines = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
            for i1,l1 in enumerate(lines):
                for i2,l2 in enumerate(lines):
                    if i1 != i2:
                        line = l1+l2+"_LINE"

                        try:
                            line = getattr(xraylib,line)
                            result = xraylib.LineEnergy(ELEMENT,line)
                        except:
                            pass
                        else:
                            if result != 0.0: print("%s%s  %f   keV"%(l1, l2, result))
    if FUNCTION == 1:
        shells = ['All shells', 'K_SHELL', 'L1_SHELL', 'L2_SHELL', 'L3_SHELL', 'M1_SHELL', 'M2_SHELL', 'M3_SHELL', 'M4_SHELL', 'M5_SHELL', 'N1_SHELL', 'N2_SHELL', 'N3_SHELL', 'N4_SHELL', 'N5_SHELL', 'N6_SHELL', 'N7_SHELL', 'O1_SHELL', 'O2_SHELL', 'O3_SHELL', 'O4_SHELL', 'O5_SHELL', 'O6_SHELL', 'O7_SHELL', 'P1_SHELL', 'P2_SHELL', 'P3_SHELL', 'P4_SHELL', 'P5_SHELL', 'Q1_SHELL', 'Q2_SHELL', 'Q3_SHELL']
        if SHELL == 0: #"all"
            for i,myshell in enumerate(shells):
                if i >= 1:
                    # command = "result = xraylib.EdgeEnergy(%d,xraylib.%s)"%(ELEMENT,myshell)
                    # print("executing command: ",command)
                    shell_index = getattr(xraylib,myshell)
                    try:
                        result = xraylib.EdgeEnergy(ELEMENT,shell_index)
                    except:
                        pass
                    else:
                        if result != 0.0: print("%s  %f   keV"%(myshell, result))
        else:
            shell_index = getattr(xraylib,shells[SHELL])
            try:
                command = "result = xraylib.EdgeEnergy(%d,xraylib.%s)"%(ELEMENT,shells[SHELL])
                print("executing command: ",command)
                result = xraylib.EdgeEnergy(ELEMENT,shell_index)
            except:
                pass
            else:
                if result != 0.0: print("Z=%d %s : %f   keV"%(ELEMENT, shells[SHELL], result))

    if FUNCTION == 2:
        result = xraylib.AtomicWeight(ELEMENT)
        if result != 0.0: print("Atomic weight for Z=%d : %f  g/mol"%(ELEMENT,result))
    if FUNCTION == 3:
        result = xraylib.ElementDensity(ELEMENT)
        if result != 0.0: print("Element density for Z=%d : %f  g/cm3"%(ELEMENT,result))

    if FUNCTION == 4:
        command = "result = xraylib.CS_Total_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Total_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Total absorption cross section: %f  g/cm3"%(result))

    if FUNCTION == 5:
        command = "result = xraylib.CS_Photo_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Photo_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Photoionization cross section: %f  g/cm3"%(result))

    if FUNCTION == 6:
        shells = ['All shells', 'K_SHELL', 'L1_SHELL', 'L2_SHELL', 'L3_SHELL', 'M1_SHELL', 'M2_SHELL', 'M3_SHELL', 'M4_SHELL', 'M5_SHELL', 'N1_SHELL', 'N2_SHELL', 'N3_SHELL', 'N4_SHELL', 'N5_SHELL', 'N6_SHELL', 'N7_SHELL', 'O1_SHELL', 'O2_SHELL', 'O3_SHELL', 'O4_SHELL', 'O5_SHELL', 'O6_SHELL', 'O7_SHELL', 'P1_SHELL', 'P2_SHELL', 'P3_SHELL', 'P4_SHELL', 'P5_SHELL', 'Q1_SHELL', 'Q2_SHELL', 'Q3_SHELL']
        if SHELL == 0: #"all"
            for i,myshell in enumerate(shells):
                if i >= 1:
                    command = "result = xraylib.CS_Photo_Partial(%d,xraylib.%s, ENERGY)"%(ELEMENT,myshell,ENERGY)
                    shell_index = getattr(xraylib,myshell)
                    try:
                        result = xraylib.CS_Photo_Partial(ELEMENT,shell_index,ENERGY)
                    except:
                        pass
                    else:
                        if result != 0.0: print("%s  %f   cm2/g"%(myshell, result))
        else:
            shell_index = getattr(xraylib,shells[SHELL])
            try:
                command = "result = xraylib.xraylib.CS_Photo_Partial('%d',xraylib.%s,%f)"%(ELEMENT,shells[SHELL],ENERGY)
                print("executing command: ",command)
                result = xraylib.CS_Photo_Partial(ELEMENT,shell_index,ENERGY)
            except:
                pass
            else:
                if result != 0.0: print("Z=%d, %s at E=%f keV: %f   cm2/g"%(ELEMENT,shells[SHELL], ENERGY, result))

    if FUNCTION == 7:
        command = "result = xraylib.CS_Rayl_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Rayl_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Rayleigh cross section: %f  cm2/g"%(result))

    if FUNCTION == 8:
        command = "result = xraylib.CS_Compt_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Compt_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Compton cross section: %f  cm2/g"%(result))

    if FUNCTION == 9:
        command = "result = xraylib.CS_KN(%f)"%(ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_KN(ENERGY)
        if result != 0.0: print("Klein Nishina cross section: %f  cm2/g"%(result))

    if FUNCTION == 10:
        command = "result = xraylib.CS_Energy_CP('%s',%f)"%(ELEMENTORCOMPOUND,ENERGY)
        print("executing command: ",command)
        result = xraylib.CS_Energy_CP(ELEMENTORCOMPOUND,ENERGY)
        if result != 0.0: print("Mass-energy absorption cross section: %f  cm2/g"%(result))
    return(None)


def xoppy_doc(app):
    filename1 = os.path.join(home_doc,app+'.txt')
    filename2 = os.path.join(home_doc,app+'_par.txt')
    command = "gedit "+filename1+" "+filename2+" &"
    print("Running command '%s' "%(command))
    os.system(command)

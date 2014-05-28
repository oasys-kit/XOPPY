import os
import numpy
from Orange import __file__ as orange_init

from Orange.XOPPY import *


def xoppy_calc_black_body(TITLE="Thermal source: Planck distribution",TEMPERATURE=1200000.0,E_MIN=10.0,E_MAX=1000.0,NPOINTS=500):
    print("Inside xoppy_calc_black_body. ")
    return(None)



def xoppy_calc_bm(MACHINE_NAME="ESRF bending magnet",RB_CHOICE=0,MACHINE_R_M=25.0,BFIELD_T=0.800000011920929,BEAM_ENERGY_GEV=6.039999961853027,CURRENT_A=0.100000001490116,HOR_DIV_MRAD=1.0,VER_DIV=0,PHOT_ENERGY_MIN=100.0,PHOT_ENERGY_MAX=100000.0,NPOINTS=500,LOG_CHOICE=1,PSI_MRAD_PLOT=1.0,PSI_MIN=-1.0,PSI_MAX=1.0,PSI_NPOINTS=500):
    print("Inside xoppy_calc_bm. ")
    return(None)



def xoppy_calc_mlayer(MODE=0,SCAN=0,F12_FLAG=0,SUBSTRATE="Si",ODD_MATERIAL="Si",EVEN_MATERIAL="W",ENERGY=8050.0,THETA=0.0,SCAN_STEP=0.009999999776483,NPOINTS=600,ODD_THICKNESS=25.0,EVEN_THICKNESS=25.0,NLAYERS=50,FILE="layers.dat"):
    print("Inside xoppy_calc_mlayer. ")
    return(None)



def xoppy_calc_nsources(TEMPERATURE=300.0,ZONE=0,MAXFLUX_F=200000000000000.0,MAXFLUX_EPI=20000000000000.0,MAXFLUX_TH=200000000000000.0,NPOINTS=500):
    print("Inside xoppy_calc_nsources. ")
    return(None)



def xoppy_calc_ws(TITLE="Wiggler A at APS",ENERGY=7.0,CUR=100.0,PERIOD=8.5,N=28.0,KX=0.0,KY=8.739999771118164,EMIN=1000.0,EMAX=100000.0,NEE=2000,D=30.0,XPC=0.0,YPC=0.0,XPS=2.0,YPS=2.0,NXP=10,NYP=10):
    print("Inside xoppy_calc_ws. ")
    pwd = os.getcwd()
    os.chdir(home_wd)
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

    os.chdir(pwd)
    outFile = os.path.join(home_wd,"ws.spec")
    return(outFile)






    return(None)



def xoppy_calc_xtubes(ITUBE=0,VOLTAGE=30.0):
    print("Inside xoppy_calc_xtubes. ")
    pwd = os.getcwd()
    os.chdir(home_wd)
    with open("xoppy.inp","wt") as f:
        f.write("%d\n%f\n"%(ITUBE+1,VOLTAGE))
    command = os.path.join(home_bin,'xtubes') + " < xoppy.inp"
    print("Running command '%s' in directory: %s "%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")
    os.chdir(pwd)
    outFile = os.path.join(home_wd,"xtubes_tmp.dat")
    return(outFile)


def xoppy_calc_xtube_w(VOLTAGE=100.0,RIPPLE=0.0,AL_FILTER=0.0):
    print("Inside xoppy_calc_xtube_w. ")
    pwd = os.getcwd()
    os.chdir(home_wd)
    with open("xoppy.inp","wt") as f:
        f.write("%f\n%f\n%f\n"%(VOLTAGE,RIPPLE,AL_FILTER))
    command = os.path.join(home_bin,'tasmip') + " < xoppy.inp"
    print("Running command '%s' in directory: %s \n"%(command,os.getcwd()))
    print("\n--------------------------------------------------------\n")
    os.system(command)
    print("\n--------------------------------------------------------\n")
    os.chdir(pwd)
    outFile = os.path.join(home_wd,"tasmip_tmp.dat")
    return(outFile)



def xoppy_calc_xinpro(CRYSTAL_MATERIAL=0,MODE=0,ENERGY=8000.0,MILLER_INDEX_H=1,MILLER_INDEX_K=1,MILLER_INDEX_L=1,ASYMMETRY_ANGLE=0.0,THICKNESS=500.0,TEMPERATURE=300.0,NPOINTS=100,SCALE=0,XFROM=-50.0,XTO=50.0):
    print("Inside xoppy_calc_xinpro. ")
    pwd = os.getcwd()
    os.chdir(home_wd)
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
    os.chdir(pwd)
    outFile = os.path.join(home_wd,"inpro.spec")

    return(outFile)



def xoppy_calc_xcrystal(FILEF0=0,FILEF1F2=0,FILECROSSSEC=0,CRYSTAL_MATERIAL=0,MILLER_INDEX_H=1,MILLER_INDEX_K=1,MILLER_INDEX_L=1,I_ABSORP=2,TEMPER="1.0",MOSAIC=0,GEOMETRY=0,SCAN=2,UNIT=1,SCANFROM=-100.0,SCANTO=100.0,SCANPOINTS=200,ENERGY=8000.0,ASYMMETRY_ANGLE=0.0,THICKNESS=0.7,MOSAIC_FWHM=0.1,RSAG=125.0,RMER=1290.0,ANISOTROPY=0,POISSON=0.22,CUT="2 -1 -1 ; 1 1 1 ; 0 0 0",FILECOMPLIANCE="mycompliance.dat"):
    print("Inside xoppy_calc_xcrystal. ")
    return(None)



def xoppy_calc_xwiggler(FIELD=0,NPERIODS=12,ULAMBDA=0.125,K=14.0,ENERGY=6.04,PHOT_ENERGY_MIN=100.0,PHOT_ENERGY_MAX=100100.0,NPOINTS=100,LOGPLOT=1,NTRAJPOINTS=101,CURRENT=200.0,FILE="?"):
    print("Inside xoppy_calc_xwiggler. ")
    return(None)



def xoppy_calc_xxcom(NAME="Pyrex Glass",SUBSTANCE=3,DESCRIPTION="SiO2:B2O3:Na2O:Al2O3:K2O",FRACTION="0.807:0.129:0.038:0.022:0.004",GRID=1,GRIDINPUT=0,GRIDDATA="0.0804:0.2790:0.6616:1.3685:2.7541",ELEMENTOUTPUT=0):
    print("Inside xoppy_calc_xxcom. ")

    pwd = os.getcwd()
    os.chdir(home_wd)
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


    os.chdir(pwd)
    outFile = os.path.join(home_wd,"xcom.spec")
    return(outFile)




    return(None)



def xoppy_calc_xbfield(PERIOD=4.0,NPER=42,NPTS=40,IMAGNET=0,ITYPE=0,K=1.379999995231628,GAP=2.0,GAPTAP=10.0,FILE="undul.bf"):
    print("Inside xoppy_calc_xbfield. ")
    return(None)



def xoppy_calc_xfilter(EMPTY1="              ",EMPTY2="              ",NELEMENTS=1,SOURCE=0,ENER_MIN=1000.0,ENER_MAX=50000.0,ENER_N=100,SOURCE_FILE="SRCOMPW",EL1_SYM="Be",EL1_THI=500.0,EL2_SYM="Al",EL2_THI=50.0,EL3_SYM="Pt",EL3_THI=10.0,EL4_SYM="Au",EL4_THI=10.0,EL5_SYM="Cu",EL5_THI=10.0):
    print("Inside xoppy_calc_xfilter. ")
    return(None)



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


def xoppy_doc(app):
    filename1 = os.path.join(home_doc,app+'.txt')
    filename2 = os.path.join(home_doc,app+'_par.txt')
    command = "gedit "+filename1+" "+filename2+" &"
    print("Running command '%s' "%(command))
    os.system(command)

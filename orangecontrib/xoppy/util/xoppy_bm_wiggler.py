import numpy
from srxraylib.sources import srfunc


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


def xoppy_calc_bm(MACHINE_NAME="ESRF bending magnet",RB_CHOICE=0,MACHINE_R_M=25.0,BFIELD_T=0.8,\
                  BEAM_ENERGY_GEV=6.04,CURRENT_A=0.1,HOR_DIV_MRAD=1.0,VER_DIV=0,\
                  PHOT_ENERGY_MIN=100.0,PHOT_ENERGY_MAX=100000.0,NPOINTS=500,LOG_CHOICE=1,\
                  PSI_MRAD_PLOT=1.0,PSI_MIN=-1.0,PSI_MAX=1.0,PSI_NPOINTS=500,TYPE_CALC=0,FILE_DUMP=0):

    # electron energy in GeV
    gamma = BEAM_ENERGY_GEV*1e3 / srfunc.codata_mee

    r_m = MACHINE_R_M      # magnetic radius in m
    if RB_CHOICE == 1:
        r_m = srfunc.codata_me * srfunc.codata_c / srfunc.codata_ec / BFIELD_T * numpy.sqrt(gamma * gamma - 1)

    # calculate critical energy in eV
    ec_m = 4.0*numpy.pi*r_m/3.0/numpy.power(gamma,3) # wavelength in m
    ec_ev = srfunc.m2ev / ec_m

    fm = None
    a = None
    energy_ev = None

    if TYPE_CALC == 0:
        if LOG_CHOICE == 0:
            energy_ev = numpy.linspace(PHOT_ENERGY_MIN,PHOT_ENERGY_MAX,NPOINTS) # photon energy grid
        else:
            energy_ev = numpy.logspace(numpy.log10(PHOT_ENERGY_MIN),numpy.log10(PHOT_ENERGY_MAX),NPOINTS) # photon energy grid

        a5 = srfunc.sync_ene(VER_DIV, energy_ev, ec_ev=ec_ev, polarization=0, \
                             e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, \
                             psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a5par = srfunc.sync_ene(VER_DIV, energy_ev, ec_ev=ec_ev, polarization=1, \
                                e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, \
                                psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a5per = srfunc.sync_ene(VER_DIV, energy_ev, ec_ev=ec_ev, polarization=2, \
                                e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, \
                                psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        if VER_DIV == 0:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw]','Power[Watts/eV]']
            title='integrated in Psi,'
        if VER_DIV == 1:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw/mrad(Psi)]','Power[Watts/eV/mrad(Psi)]']
            title='at Psi=0,'
        if VER_DIV == 2:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw]','Power[Watts/eV]']
            title='in Psi=[%e,%e]'%(PSI_MIN,PSI_MAX)
        if VER_DIV == 3:
            coltitles=['Photon Energy [eV]','Photon Wavelength [A]','E/Ec','Flux_spol/Flux_total','Flux_ppol/Flux_total','Flux[Phot/sec/0.1%bw/mrad(Psi)]','Power[Watts/eV/mrad(Psi)]']
            title='at Psi=%e mrad'%(PSI_MIN)

        a6=numpy.zeros((7,len(energy_ev)))
        a1 = energy_ev
        a6[0,:] = (a1)
        a6[1,:] = srfunc.m2ev * 1e10 / (a1)
        a6[2,:] = (a1)/ec_ev # E/Ec
        a6[3,:] = numpy.array(a5par)/numpy.array(a5)
        a6[4,:] = numpy.array(a5per)/numpy.array(a5)
        a6[5,:] = numpy.array(a5)
        a6[6,:] = numpy.array(a5)*1e3 * srfunc.codata_ec

    if TYPE_CALC == 1:  # angular distributions over over all energies
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        a6 = numpy.zeros((6,NPOINTS))
        a6[0,:] = angle_mrad # angle in mrad
        a6[1,:] = angle_mrad*gamma/1e3 # Psi[rad]*Gamma
        a6[2,:] = srfunc.sync_f(angle_mrad * gamma / 1e3)
        a6[3,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=1)
        a6[4,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=2)
        a6[5,:] = srfunc.sync_ang(0, angle_mrad, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, e_gev=BEAM_ENERGY_GEV, r_m=r_m)

        coltitles=['Psi[mrad]','Psi[rad]*Gamma','F','F s-pol','F p-pol','Power[Watts/mrad(Psi)]']

    if TYPE_CALC == 2:  # angular distributions at a single energy
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        a6 = numpy.zeros((7,NPOINTS))
        a6[0,:] = angle_mrad # angle in mrad
        a6[1,:] = angle_mrad*gamma/1e3 # Psi[rad]*Gamma
        a6[2,:] = srfunc.sync_f(angle_mrad * gamma / 1e3)
        a6[3,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=1)
        a6[4,:] = srfunc.sync_f(angle_mrad * gamma / 1e3, polarization=2)
        tmp = srfunc.sync_ang(1, angle_mrad, energy=PHOT_ENERGY_MIN, i_a=CURRENT_A, hdiv_mrad=HOR_DIV_MRAD, e_gev=BEAM_ENERGY_GEV, ec_ev=ec_ev)
        tmp.shape = -1
        a6[5,:] = tmp
        a6[6,:] = a6[5,:] * srfunc.codata_ec * 1e3

        coltitles=['Psi[mrad]','Psi[rad]*Gamma','F','F s-pol','F p-pol','Flux[Ph/sec/0.1%bw/mrad(Psi)]','Power[Watts/eV/mrad(Psi)]']

    if TYPE_CALC == 3:  # angular,energy distributions flux
        angle_mrad = numpy.linspace(-PSI_MRAD_PLOT, +PSI_MRAD_PLOT,NPOINTS) # angle grid

        if LOG_CHOICE == 0:
            energy_ev = numpy.linspace(PHOT_ENERGY_MIN,PHOT_ENERGY_MAX,NPOINTS) # photon energy grid
        else:
            energy_ev = numpy.logspace(numpy.log10(PHOT_ENERGY_MIN),numpy.log10(PHOT_ENERGY_MAX),NPOINTS) # photon energy grid

        # fm[angle,energy]
        fm = srfunc.sync_ene(4, energy_ev, ec_ev=ec_ev, e_gev=BEAM_ENERGY_GEV, i_a=CURRENT_A, \
                                      hdiv_mrad=HOR_DIV_MRAD, psi_min=PSI_MIN, psi_max=PSI_MAX, psi_npoints=PSI_NPOINTS)

        a = numpy.linspace(PSI_MIN,PSI_MAX,PSI_NPOINTS)

        a6 = numpy.zeros((4,len(a)*len(energy_ev)))
        ij = -1
        for i in range(len(a)):
            for j in range(len(energy_ev)):
                ij += 1
                a6[0,ij] = a[i]
                a6[1,ij] = energy_ev[j]
                a6[2,ij] = fm[i,j] * srfunc.codata_ec * 1e3
                a6[3,ij] = fm[i,j]

        coltitles=['Psi [mrad]','Photon Energy [eV]','Power [Watts/eV/mrad(Psi)]','Flux [Ph/sec/0.1%bw/mrad(Psi)]']

    # write spec file
    ncol = len(coltitles)
    npoints = len(a6[0,:])

    if FILE_DUMP:
        outFile = "bm.spec"
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
        print("File written to disk: " + outFile)

    if TYPE_CALC == 0:
        if LOG_CHOICE == 0:
            print("\nPower from integral of spectrum: %15.3f W"%(a5.sum() * 1e3*srfunc.codata_ec * (energy_ev[1]-energy_ev[0])))

    return a6.T, fm, a, energy_ev


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def xoppy_calc_xwiggler(FIELD=0,NPERIODS=12,ULAMBDA=0.125,K=14.0,ENERGY=6.04,PHOT_ENERGY_MIN=100.0,\
                        PHOT_ENERGY_MAX=100100.0,NPOINTS=100,NTRAJPOINTS=101,CURRENT=200.0,FILE="?"):

    print("Inside xoppy_calc_xwiggler. ")

    outFileTraj = "xwiggler_traj.spec"
    outFile = "xwiggler.spec"

    if FIELD == 0:
        t0,p = srfunc.wiggler_trajectory(b_from=0, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS, \
                                         ener_gev=ENERGY, per=ULAMBDA, kValue=K, \
                                         trajFile=outFileTraj)
    if FIELD == 1:
        # magnetic field from B(s) map
        t0,p = srfunc.wiggler_trajectory(b_from=1, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS, \
                                         ener_gev=ENERGY, inData=FILE, trajFile=outFileTraj)
    if FIELD == 2:
        # magnetic field from harmonics
        # hh = srfunc.wiggler_harmonics(b_t,Nh=41,fileOutH="tmp.h")
        t0,p = srfunc.wiggler_trajectory(b_from=2, nPer=NPERIODS, nTrajPoints=NTRAJPOINTS, \
                                         ener_gev=ENERGY, per=ULAMBDA, inData="", trajFile=outFileTraj)
    print(p)
    #
    # now spectra
    #
    e, f0, p0 = srfunc.wiggler_spectrum(t0, enerMin=PHOT_ENERGY_MIN, enerMax=PHOT_ENERGY_MAX, nPoints=NPOINTS, \
                                    electronCurrent=CURRENT*1e-3, outFile=outFile, elliptical=False)

    try:
        cumulated_power = p0.cumsum() * numpy.abs(e[0] - e[1])
    except:
        cumulated_power = 0.0

    print("\nPower from integral of spectrum (sum rule): %8.3f W" % (cumulated_power[-1]))
    return e, f0, p0 , cumulated_power


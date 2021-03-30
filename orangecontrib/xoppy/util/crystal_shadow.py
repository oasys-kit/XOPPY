import numpy
import math
import scipy.constants as codata
def crystal_shadow(filename,str,phot_in):
    '''
    #+
    # Singapore Synchrotron Light Source (SSLS) 
    # :Author: X.J. Yu, slsyxj@nus.edu.sg
    # :Name:  crystal_shadow
    # :Purpose: create a shadow data file for a any crystal
    # :Input: 
    #     filename: file name to write
    #     str:  output from Bragg_Calc
    #     phot_in: photon neerg array
    #-
    '''

    RN = str["rn"]
    D_SPACING = str["dspacing"]
    nbatom = str["nbatom"]
    atnum = str["atnum"]
    TEMPER = str["temper"]
    G_0 = str["G_0"]
    G = str["G"]
    G_BAR = str["G_BAR"]
    f0coeff = numpy.array(str["f0coeff"])
    NPOINT = str["npoint"]
    energy = numpy.array(str["energy"])
    fp = numpy.array(str["f1"])
    fpp = numpy.array(str["f2"])
    zcol = numpy.array(str["zcol"])
    fcol = numpy.array(str["fraction"])
    UCOL = numpy.array(str["unique_AtomicName"])
    LCOL = numpy.array(str["list_AtomicName"])

    CI  = 0.0 + 1.0j
    TOANGS  =  codata.h * codata.c / codata.e * 1e10 
    TOCM    =  TOANGS*1e-8
    TWOPI = 2 * numpy.pi
    
    phot = phot_in[0]  #;first energy
    F1 = numpy.zeros((len(phot_in),nbatom),dtype=float)
    F2 = numpy.zeros((len(phot_in),nbatom),dtype=float)
    F000 =numpy.zeros(nbatom,dtype=float)
    
    for j in range(nbatom):
        icentral = int(f0coeff.shape[1]/2)
        F000[j] = f0coeff[j,icentral] #X.J. Yu, slsyxj@nus.edu.sg
        for i in range(icentral):
            F000[j] += f0coeff[j,i]  #actual number of electrons carried by each atom, X.J. Yu, slsyxj@nus.edu.sg
            
    BOOL_UCOL = UCOL[0]==''
    for i,phot in enumerate(phot_in):

        for j,ienergy in enumerate(energy):
            if ienergy > phot:
                break
        nener = j - 1

        for j in range(nbatom):
            F1[i,j] = fp[j,nener] + (fp[j,nener+1] - fp[j,nener]) * \
            (phot - energy[nener]) / (energy[nener+1] - energy[nener])
            F2[i,j] = fpp[j,nener] + (fpp[j,nener+1] - fpp[j,nener]) * \
            (phot - energy[nener]) / (energy[nener+1] - energy[nener])

        F_0 = 0.0 + 0.0j
        
        for j in range(nbatom):
#charged atom, the number of electrons not equal to atum anymore,while
# it is euqal to F000, and notably, fractial occupancy need consideration here
# occupancy till now, only consider in calculation of G, and G_BAR in bragg_calc
#comment out: X.J. Yu, slsyxj@nus.edu.sg
#
#            F_0 += G_0[j] * ( atnum[j] + F1[j] + 1j * F2[j] ) * 1.0
#
            FN = F000[j] + F1[i,j] + CI * F2[i,j]
            if BOOL_UCOL:   #normal crystal
                F_0 += FN*numpy.sum(numpy.where(zcol==atnum[j],fcol,0.0))
            else:
#complex compound crystals
#take care same element carrying with different charge, O2-, O1.5-
#so with different f0 coefficients
                F_0 += FN*numpy.sum(numpy.where(LCOL==UCOL[j],fcol,0.0))

        R_LAM0 = TOCM/phot          #;wavelength in cm
        SIN_GRA = R_LAM0/2/D_SPACING
        theta = math.asin(SIN_GRA) 

        REFRAC = (1.0+0.0j) - R_LAM0*R_LAM0*RN*F_0/TWOPI
        DELTA  = 1.0 -  REFRAC.real
        BETA   = -REFRAC.imag
        #;
        #; THETA_B is the Bragg angle corrected for refraction
        #;
        THETA_B = R_LAM0/(1.0 - (DELTA/(SIN_GRA*SIN_GRA)))/2.0/D_SPACING        #;sin(theta_b)

        C_TMP = numpy.zeros((nbatom,3),dtype=float)        #;C coeff for f0 interpolation
        
        if BOOL_UCOL:   #normal crystal
            for j in range(nbatom):
                zcol = numpy.where(zcol ==atnum[j],j+1,zcol)            #;index for fortran, start from 1 
        else:
            for j in range(nbatom):
                zcol = numpy.where(LCOL==UCOL[j],j+1,zcol)            #;index for fortran, start from 1 
        

        #;ratio   = [0.9D,1D,1.1D] * THETA_B/(TOANGS/PHOT)
        ratio   = numpy.array([0.9,1.0,1.1] ) * SIN_GRA/(TOANGS/phot)
        
        F0 = numpy.zeros((nbatom,3),dtype=float)
        A = numpy.zeros(3,dtype=float)
        for j in range(nbatom):
            icentral = len(f0coeff[0])
            icentral = int(icentral/2)
            F0[j,:] = f0coeff[j,icentral]
            for jj in range(icentral):
                F0[j,:] += f0coeff[j,jj] * \
                    numpy.exp(-1.0*f0coeff[j,jj+icentral+1]*ratio*ratio)
            
            IFLAG = -1
            Y = F0[j,:]
            A = numpy.polyfit(ratio,Y,2)[::-1]
            C_TMP[j,:] = A
        #;Test fitting working
        #;FOA = A[2]*ratio[1]^2 + A[1]*ratio[1] + A[0]

    with open(filename, "w") as file:
        try:
            file.write( ("-1  %g  %g\n")%(RN,D_SPACING) )
            file.write( ("%i  "*3 +"%.3lf\n")%(nbatom,len(zcol),len(phot_in),TEMPER[0]))
            for j in range(nbatom):
                file.write( ("%g  (%.6g, %.6g)  (%.6g, %.6g)\n")%(F000[j],G[j].real,G[j].imag,G_BAR[j].real,G_BAR[j].imag))
                file.write( ("%g  "*3 + "\n")%(C_TMP[j,0],C_TMP[j,1],C_TMP[j,2]))
            for j in range(len(zcol)):
                file.write( ("%i  %g\n")%(zcol[j],fcol[j]))
            for  iphot in range(len(phot_in)):
                file.write( "%g  \n"%(phot_in[iphot]))
                for j in range(nbatom):
                    file.write( ("%g  "*2+"\n")%(F1[iphot,j],F2[iphot,j]))
                    
            file.close()
            print("Shadow File written to disk: %s \n"%filename)
        except:
            file.close()
            raise Exception("crystal_shadow.py: Shadow file creation failure!\n")
            

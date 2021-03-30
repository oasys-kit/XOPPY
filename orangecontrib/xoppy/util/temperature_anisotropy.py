import numpy
import math
def TemperFactor(sinTheta_lambda,anisos,Miller={'h':1,'k':1,'l':1},cell={'a':23.44,'b':23.44,'c':23.44},n=1936):
    '''
    #+
    # Singapore Synchrotron Light Source (SSLS) 
    # :Author: X.J. Yu, slsyxj@nus.edu.sg
    # :Name:  TemperFactor
    # :Purpose: Calculation isotropic & anisotropic temerature factors
    # :Input: 
    #     Miller: Miller indice
    #     cell:  dictionary of lattice [a,b,c] in units of Aangstrom
    #     sinTheta_lambda: Sin(theta)/lambda, lambda in units of Aangstrom
    #     n: number of atomic sites
    #     anisos: array of dicionary contain anisotropic coefficients
    #     Out: output results, column 0: isotropic, column 1: anisotropic  
    #-
    '''
    #0: isotropic, 1: anisotropic temerature factors
    results = numpy.zeros([2,n])
    for i,aniso in enumerate(anisos):
        s = aniso['start']-1
        e = aniso['end']
        if aniso['beta11'] >= 1: 
            #if beta11>=1, then beta22 is Beq, the other fields are unused
            #if Beq specified, anisotropic temperature factor same as isotropic 
            Beq = aniso['beta22']     
            results[1,s:e] = math.exp(-sinTheta_lambda*sinTheta_lambda*Beq)        
        else: 
            Beq = 4.0/3.0*( aniso['beta11']*cell['a']*cell['a']+aniso['beta22']*cell['b']*cell['b']+ \
                aniso['beta33']*cell['c']*cell['c'] )
            results[1,s:e] = math.exp(-(aniso['beta11']*Miller['h']*Miller['h'] + \
                  aniso['beta22']*Miller['k']*Miller['k'] + aniso['beta33']*Miller['l']*Miller['l'] + \
                  2.0*Miller['h']*Miller['k']*aniso['beta12'] + 2.0*Miller['h']*Miller['l']*aniso['beta13'] + 2.0*Miller['k']*Miller['l']*aniso['beta23']))
        results[0,s:e] = math.exp(-sinTheta_lambda*sinTheta_lambda*Beq)

    return results
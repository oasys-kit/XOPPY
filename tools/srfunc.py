"""

srfunc: calculates synchrotron radiation emission (radiation and angle 
        distributions) 

        functions: 
             fintk53: integral of the Bessel function K5/3(x)
             sync_g1: energy spectrum integrated over the full vertical angle
             sync_f:  angular dependence of synchrotron radiation
             sync_hi: function Hi(x) = x^i * BeselK(x/2,2/3) 
             sync_ang: angular distributions
             sync_ene: energy distributions
 

"""

__author__ = "Manuel Sanchez del Rio"
__contact__ = "srio@esrf.eu"
__copyright = "ESRF, 2002-2012"


import numpy, math
import scipy.special
import scipy.constants.codata


def fintk53(xd):
    """
     Calculates the integral from x to infinity of the Bessel function K5/3(x) 

      NAME: 
            fintk53 
      
      PURPOSE: 
        Calculates the function consisting of the integral, from x to infinity,  
     	of the Bessel function K5/3(x).  
     	g_one=fintk53*x is the universal curve from which the energy spectrum  
     	of the synchrotron bending magnet is calculated. 
      
      CATEGORY: 
            Mathematics. 
      
      CALLING SEQUENCE: 
            Result = fintk53(x) 
      
      INPUTS: 
            x: the argument of the function. All calculations are done in doble 
                precision. 
      
      KEYWORD PARAMETERS: 
      
      OUTPUTS: 
            returns the value  of the fintk53 function 
      
      PROCEDURE: 
            Translated from a Fortran program, original from Umstatter.  
      	C 
      	C Routines taken from  
      	C 
      	C http://www.slac.stanford.edu/grp/arb/tn/arbvol2/ARDB162.pdf 
      	C The reference  1981 CERN/PS/SM/81-13  is cited in 
        C 'Synchrotron Radiation Spectra' by G.Brown and W. 
      	C Lavender pp.37-61 Handbook on Synchrotron Radiation, 
        C vol. 3 edited by G.S. Brown and D.E. Moncton (Elsevier 
      	C Science Publishers B.V. 1991 North-Holland, Amsterdam)  
      	C  
      
            I have performed a comparison of the result with Mathematica 
            with very good agreement (note that Mathematica values diverge 
            for x> 20. I do not know why): 
            (Mathematica evaluation N[g_one[0.001],20]) 
            (x = 620d0 & print,g_one(x),x*fintk53(x),format='(2G32.18)') 
      
          x      mathematica         idl (x*fintk53(x)) 
        0.001 0.2131390650914501     0.213139096577768417 
        0.01  0.4449725041142102     0.444972550630643671 
        0.1   0.818185534872854      0.818185588215680770 
        1.0   0.6514228153553639697  0.651422821506926542 
        5.0   0.021248129774982      0.0212481300729910755 
        10.0  0.00019223826428       0.000192238266987909711 
        20.0  5.960464477539063E-7   1.19686346217633044E-08 
        50.0  6.881280000000002E7    1.73478522828932108E-21 
        100.0 4.642275147320176E29   4.69759373162073832E-43 
        1000.0 -1.7E424              Floating underflow (<620 OK) 
      
      
      MODIFICATION HISTORY: 
            Written by:     M. Sanchez del Rio, srio@esrf.fr, 2002-04-22 
            20120208 srio@esrf.eu: python version
      
     -""" 
    #
    #C
    #C Computes Integral (from x to infinity) {K5/3(y) dy}
    #C
    xd = numpy.array(xd)
    oldshape=xd.shape
    xd.shape=-1
    a=1.0
    b=1.0
    p=1.0 
    q=1.0 
    x=1.0 
    y=1.0 
    z=1.0 
    
    xi = numpy.where(xd >= 5.0)
    xi = numpy.array(xi)
    count1 = xi.size
    
    fintk53=xd*0.0
    
    if (count1 > 0): 
        x = xd[xi]
        z=20./x-2.
        a= 0.0000000001
        b=z*a - 0.0000000004
        a=z*b-a + 0.0000000020
        b=z*a-b - 0.0000000110
        a=z*b-a + 0.0000000642
        b=z*a-b - 0.0000004076
        a=z*b-a + 0.0000028754
        b=z*a-b - 0.0000232125
        a=z*b-a + 0.0002250532
        b=z*a-b - 0.0028763680
        a=z*b-a + 0.0623959136
        p=0.5*z*a-b + 1.0655239080
        p=p* numpy.power(1.5707963268/x,0.5)/numpy.exp(x)
        fintk53[xi]=p
    
    xi = numpy.where(xd < 5.0)
    xi = numpy.array(xi)
    count2 = xi.size
    
    if ((count1+count2) != xd.size):
        print('Error: (count1+count2) NE N_Elements(xd)')
        print(count1)
        print(count2)
        raise ValueError("Error: (count1+count2) != size(xd)=%1" % xd.size)
    
    if (count2 > 0):
        x = xd[xi]
        z=numpy.power(x,2)/16.-2.
        a= 0.0000000001
        b=z*a + 0.0000000023
        a=z*b-a + 0.0000000813
        b=z*a-b + 0.0000024575
        a=z*b-a + 0.0000618126
        b=z*a-b + 0.0012706638
        a=z*b-a + 0.0209121680
        b=z*a-b + 0.2688034606
        a=z*b-a + 2.6190218379
        b=z*a-b + 18.6525089687
        a=z*b-a + 92.9523266592
        b=z*a-b + 308.1591941313
        a=z*b-a + 644.8697965824
        p=0.5*z*a-b + 414.5654364883
        a= 0.0000000012
        b=z*a + 0.0000000391
        a=z*b-a + 0.0000011060
        b=z*a-b + 0.0000258145
        a=z*b-a + 0.0004876869
        b=z*a-b + 0.0072845620
        a=z*b-a + 0.0835793546
        b=z*a-b + 0.7103136120
        a=z*b-a + 4.2678026127
        b=z*a-b + 17.0554078580
        a=z*b-a + 41.8390348678
        q=0.5*z*a-b + 28.4178737436
        y=numpy.power(x,0.666666667)
        p=(p/y-q*y-1.)*1.8137993642
        fintk53[xi]=p

        fintk53.shape=oldshape
        return fintk53


def sync_g1(x,polarization=0):
    """
    calculates the synchrotron radiation g1 function
    
      NAME:
            sync_g1
     
      PURPOSE:
            Calculates the functions used for calculating synchrotron
     	radiation energy spectrum integrated over the full vertical
     	angle.
     
      CATEGORY:
            Mathematics.
     
      CALLING SEQUENCE:
            Result = sync_g1(x)
     
      INPUTS:
            x:      the argument of the function. It is converted to double
     		precision for calculations. 
     
      KEYWORD PARAMETERS:
     	POLARIZATION: 0 Total 
     		      1 Parallel       (l2=1, l3=0, in Sokolov&Ternov notation)
     		      2 Perpendicular  (l2=0, l3=1)
      OUTPUTS:
            returns the value  of the sync_g1 function
     
      PROCEDURE:
            The number of emitted photons versus energy is:
     	N(E) = 2.4605e13 I[A] Ee[Gev] Theta[mrad] Sync_G1(E/Ec]
     	   Where: 
     		I is the storage ring intensity in A
     		Ee is the energy of the electrons in the storage ring 
     		E is the photon energy
     		Ec is the critical energy
     		The value Sync_G1 returned by this function is:
     	        sync_g1(x) (total polarization):
     		    x* Integrate[BeselK[x,5/3],{x,y,Infinity}]
     	        sync_g1(x,Pol=1) (parallel polarization):
     		    (1/2)* [x* Integrate[BesselK[x,5/3],{x,y,Infinity}] + 
     		    x*BesselK(x,2/3)]
     	        sync_g1(x,Pol=2) (perpendicular polarization):
     		    (1/2)* [x* Integrate[BesselK[x,5/3],{x,y,Infinity}] -
     		    x*BesselK(x,2/3)]
     
     	For calculating the Integrate[BeselK[x,5/3],{x,y,Infinity}]
     			function, the function fintk53 is used. 
     
     	Reference: A A Sokolov and I M Ternov, Synchrotron Radiation, 
     			Akademik-Verlag, Berlin, 1968, Formula 5.19, 
     			pag 32.
     
      MODIFICATION HISTORY:
            Written by:     M. Sanchez del Rio, srio@esrf.fr, 2002-05-24
            20120208 srio@esrf.eu: python version
      
    """
    y = fintk53(x)*x
    if polarization == 0:
        return y
    
    if polarization == 1:
        #return 0.5*(y+(x*BeselK(x,2.0/3.0)))
        return 0.5*(y+(x*scipy.special.kv(2.0/3.0,x)))
    
    if polarization == 2:
        #return 0.5*(y-(x*BeselK(x,2.0/3.0)))
        return 0.5*(y-(x*scipy.special.kv(2.0/3.0,x)))
    
    raise ValueError("invalid polarization=: %s" % polarization)


def sync_f(rAngle,rEnergy=None,polarization=0,gauss=0,l2=1,l1=0 ):
    """ angular dependency of synchrotron radiation emission

      NAME:
            sync_f
     
      PURPOSE:
            Calculates the function used for calculating the angular 
     	dependence of synchrotron radiation. 
     
      CATEGORY:
            Mathematics.
     
      CALLING SEQUENCE:
            Result = sync_f(rAngle [,rEnergy] )
     
      INPUTS:
            rAngle:  the reduced angle, i.e., angle[rads]*Gamma. It can be a
     		scalar or a vector.
      OPTIONAL INPUTS:
            rEnergy:  a value for the reduced photon energy, i.e., 
     		energy/critical_energy. It can be an scalar or a verctor. 
     		If this input is present, the calculation is done for this 
     		energy. Otherwise, the calculation results is the integration 
     		over all photon energies.
     
      KEYWORD PARAMETERS:
     	POLARIZATION: 0 Total 
     		      1 Parallel       (l2=1, l3=0, in Sokolov&Ternov notation)
     		      2 Perpendicular  (l2=0, l3=1)
     		      3 Any            (define l2 and l3)
     
     	l2: The polarization value of L2
     	l3: The polarization value of L3
     		Note: If using L2 and L3, both L2 and L3 must be defined.
     		      In this case, the Pol keyword is ignored.
     
     	GAUSS: When this keyword is set, the "Gaussian" approximaxion 
     		instead of the full calculation is used. 
     		Only valid for integrated flux aver all photon energies.
      OUTPUTS:
            returns the value  of the sync_f function
     		It is a scalar if both inputs are scalar. If one input
     		is an array, the result is an array of the same dimension. 
     		If both inputs are arrays, the resulting array has dimension
     		NxM, N=Dim(rAngle) and M=Dim(rEnergy)
     
      PROCEDURE:
            The number of emitted photons versus vertical angle Psi is
     	proportional to sync_f, which value is given by the formulas
     	in the references.
     
     	For angular distribution integrated over full photon energies (rEnergy 
     	optional input not present) we use the Formula 9, pag 4 in Green. 
     	For its gaussian approximation (in this case the polarization keyword 
     	has no effect) we use for 87 in pag 32 in Green.
     
     	For angular distribution at a given photon energy (rEnergy 
     	optional input not present) we use the Formula 11, pag 6 in Green. 
     
     
     	References: 
     		G K Green, "Spectra and optics of synchrotron radiation" 
     			BNL 50522 report (1976)
     		A A Sokolov and I M Ternov, Synchrotron Radiation, 
     			Akademik-Verlag, Berlin, 1968
     
      OUTPUTS:
            returns the value  of the sync_hi function
     
      PROCEDURE:
            Uses IDL's BeselK() function
     
      MODIFICATION HISTORY:
            Written by:     M. Sanchez del Rio, srio@esrf.fr, 2002-05-23
     	2002-07-12 srio@esrf.fr adds circular polarization term for 
     		wavelength integrated spectrum (S&T formula 5.25)
        20120208 srio@esrf.eu: python version
      
    """
    # auto-call for total polarization
    if polarization == 0:
        return sync_f(rAngle,rEnergy,polarization=1)+ \
               sync_f(rAngle,rEnergy,polarization=2)

    rAngle=numpy.array(rAngle)
    rAngle.shape=-1
    
    if polarization == 1:
        l2=1.0
        l3=0.0

    if polarization == 2:
        l2=0.0
        l3=1.0
    
    #;
    #; angle distribution integrated over full energies
    #;
    if rEnergy == None:
        if gauss == 1:
            #; Formula 87 in Pag 32 in Green 1975
            efe = 0.4375*numpy.exp(-0.5* numpy.power(rAngle/0.608,2) )
            return efe
    
        #if polarization == 0:
        #    return sync_f(rAngle,polarization=1)+sync_f(rAngle,polarization=2)
        #
        #; For 9 in Pag 4 in Green 1975
        #; The two summands correspond to the par and per polarizations, as 
        #; shown in Sokolov&Ternov formulas (3.31) and 5.26)
        #; However, for circular polarization a third term (S&T 5.25) 
        #; must also be used
        efe = (7.0/16.0)*l2*l2+ \
        (5.0/16.0)*(rAngle*rAngle/(1.0+rAngle*rAngle))*l3*l3 + \
        (64.0/16.0/numpy.pi/numpy.sqrt(3.0))* \
        (rAngle/numpy.power(1+rAngle*rAngle,0.5))*l2*l3
        efe = efe * ( numpy.power(1.0+rAngle*rAngle,-5.0/2.0) )
        return efe

    #;
    #; angle distribution for given energy/ies
    #;
    rEnergy=numpy.array(rEnergy)
    rEnergy.shape=-1
    #
    #; For 11 in Pag 6 in Green 1975
    #
    ji = numpy.sqrt( numpy.power(1.0+numpy.power(rAngle,2),3) )
    ji = numpy.outer(ji,rEnergy/2.0)
    rAngle2 = numpy.outer(rAngle,(rEnergy*0.0+1.0))
    efe = l2*scipy.special.kv(2.0/3.0,ji)+ \
          l3* rAngle2*scipy.special.kv(1.0/3.0,ji)/ \
    numpy.sqrt(1.0+numpy.power(rAngle2,2))
    efe = efe* (1.0+numpy.power(rAngle2,2))
    efe = efe*efe
    return efe


def sync_hi(x,i=2,polarization=0): 
    """ calculates the function Hi(x) used for Synchrotron radiation

      NAME:
            sync_hi
     
      PURPOSE:
            Calculates the function Hi(x) used for Synchrotron radiation 
     	Hi(x) = x^i * BesselK(x/2,2/3) (for total polarization)
     
     
      CATEGORY:
            Mathematics.
     
      CALLING SEQUENCE:
            Result = sync_hi(x [,i] )
     
      INPUTS:
            x:   the argument of the function. All calculations are done 
                 in doble precision.
     	    i:	the exponent. If this optional argument is not entered, it 
     		is set to 2.
     
      KEYWORD PARAMETERS:
     	POLARIZATION: 0 Total 
     		      1 Parallel       (l2=1, l3=0, in Sokolov&Ternov notation)
     		      2 Perpendicular  (l2=0, l3=1)
     
      OUTPUTS:
            returns the value  of the sync_hi function
     
      PROCEDURE:
            Uses the relation ship Hi(x) =  x^i * sync_f(0,x)
     
      MODIFICATION HISTORY:
            Written by:     M. Sanchez del Rio, srio@esrf.fr, 2002-05-23
            20120208 srio@esrf.eu: python version
      
    """
    x=numpy.array(x)
    x.shape=-1
    y1 = numpy.power(x,i) * sync_f(0,x,polarization=polarization)
    return y1


def sync_ang(flag,angle_mrad,polarization=0, \
    e_gev=1.0,i_a=0.001,hdiv_mrad=1.0,r_m=1.0,energy=1.0,ec_ev=1.0):
    """ Calculates the synchrotron radiation angular distribution

      NAME:
            sync_ang
     
      PURPOSE:
            Calculates the synchrotron radiation angular distribution
     
      CATEGORY:
            Mathematics.
     
      CALLING SEQUENCE:
            Result = sync_ang(flag, angle )
     
      INPUTS:
     	flag: 	0 Flux fully integrated in photon energy
     		1 Flux at a given photon energy
        angle:  the angle array [in mrad]
     
      KEYWORD PARAMETERS:
     	polarization: 0 Total 
     		      1 Parallel       (l2=1, l3=0, in Sokolov&Ternov notation)
     		      2 Perpendicular  (l2=0, l3=1)
     
     	IF flag=0 THE FOLLOWING KEYWORDS MUST BE ENTERED
     		e_geV= The electron energy [in GeV]  (default=1.0)
     		i_a= the electron beam intensity [in A] (default=1.0D-3)
     		hdiv_mrad= the horizontal divergence [in mrad] (default=1)
     		r_m= the bending magnet radius [in m] (default=1.0)
     
     	IF flag=1 THE FOLLOWING KEYWORDS MUST BE ENTERED
     		All keyworsd for FLAG=0 plus:
     		energy = the energy value [in eV] (default=1)
     		ec_ev= The critical energy [eV] (default=1)
     
      OUTPUTS:
            returns the array with the angular distribution 
             IF flag ==1 power density [Watts/mrad(Psi)]
     
      PROCEDURE:
     
     	References: 
     		G K Green, "Spectra and optics of synchrotron radiation" 
     			BNL 50522 report (1976)
     		A A Sokolov and I M Ternov, Synchrotron Radiation, 
     			Akademik-Verlag, Berlin, 1968
     
      MODIFICATION HISTORY:
            Written by:     M. Sanchez del Rio, srio@esrf.fr, 2002-06-03
            20120208 srio@esrf.eu: python version
      
    """
    # retrieve physical constants needed
    codata = scipy.constants.codata.physical_constants
    
    codata_c, tmp1, tmp2 = codata["speed of light in vacuum"]
    codata_c = numpy.array(codata_c)
    
    codata_mee, tmp1, tmp2 = codata["electron mass energy equivalent in MeV"]
    codata_mee = numpy.array(codata_mee)
    
    codata_h, tmp1, tmp2 = codata["Planck constant"]
    codata_h = numpy.array(codata_h)
    
    codata_ec, tmp1, tmp2 = codata["elementary charge"]
    codata_ec = numpy.array(codata_ec)

    angle_mrad = numpy.array(angle_mrad)
    angle_mrad.shape = -1
    
    if flag == 0:
        # fully integrated in photon energy
        a8 = 3e10*codata_c*codata_ec/numpy.power(codata_mee,5) # 41.357
        gamma = e_gev*1e3/codata_mee
        a5 = sync_f(angle_mrad*gamma/1e3,polarization=polarization)* \
             a8*i_a*hdiv_mrad/r_m*numpy.power(e_gev,5)
        return a5
    
    if flag == 1:
        #a8 = 1.3264d13
        a8 = codata_ec/numpy.power(codata_mee,2)/codata_h*(9e-2/2/numpy.pi) 
        energy = numpy.array(energy)
        energy.shape=-1
        eene = energy/ec_ev
        gamma = e_gev*1e3/codata_mee
        a5=sync_f(angle_mrad*gamma/1e3,eene,polarization=polarization)* \
        numpy.power(eene,2)* \
            a8*i_a*hdiv_mrad*numpy.power(e_gev,2)
        return a5


def sync_ene(f_psi,energy_ev,ec_ev=1.0,polarization=0,  \
             e_gev=1.0,i_a=0.001,hdiv_mrad=1.0, \
             psi_min=0.0, psi_max=0.0, psi_npoints=1): 
    """ Calculates the synchrotron radiation energy spectrum
      NAME:
            sync_ene
     
      PURPOSE:
            Calculates the synchrotron radiation energy spectrum
     
      CATEGORY:
            Mathematics.
     
      CALLING SEQUENCE:
            Result = sync_ene(flag, Energy )
     
      INPUTS:
     	flag: 	0 Flux fully integrated in angle (Psi)
     		1 Flux at Psi=0
     		2 Flux integrated in the angular interval [Psi_Min,Psi_Max]
     		3 Flux at Psi=Psi_Min
     
            energy:  the energy array [in eV]
     
      KEYWORD PARAMETERS:
     	polarization: 0 Total 
     		      1 Parallel       (l2=1, l3=0, in Sokolov&Ternov notation)
     		      2 Perpendicular  (l2=0, l3=1)
     
     	If flag=0 or flag=1 the following keywords MUST BE ENTERED
     
     		ec_ev= The critical energy [eV]
     		e_geV= The electron energy [in GeV] 
     		i_a= the electron beam intensity [in A]
     		hdiv_mrad= the horizontal divergence [in mrad]
     
     	If flag=2, in addition to the mentioned keywords, the following 
     		ones must be present:
     
     		Psi_Min the minimum integration angle [in mrad]
     		Psi_Max the maximum integration angle [in mrad]
     		Psi_NPoints the number of points in psi for integration
     
     	If flag=3, in addition to the mentioned keywords for flag=0 OR 
     		flag=1, the following kewford must be defined: 
     
     		psi_min the Psi angular value [in mrad]
     
      KEYWORD PARAMETERS (OUTPUT):
     
     	IF flag=2, the following keywords can be used to obtain additional info:
     
     		fmatrix=a two dimensional variable containing the matrix of 
     			flux as a function of angle [first index] and energy 
     			[second index]
     		angle_mrad= a: one-dim array with the angular points [in mrad]
     
      OUTPUTS:
            returns the array with the flux [photons/sec/0.1%bw] for FLAG=0,2
            and the flux [photons/sec/0.1%bw/mrad] for FLAG=1,3
     
      PROCEDURE:
     
     	References: 
     		G K Green, "Spectra and optics of synchrotron radiation" 
     			BNL 50522 report (1976)
     		A A Sokolov and I M Ternov, Synchrotron Radiation, 
     			Akademik-Verlag, Berlin, 1968
     
      EXAMPLE:
     	The following program was used for testing sync_ene
     	
     	
        #create 10-points energy array in [20,30] keV
        e=numpy.linspace(20000.0,30000.0,10)
     	
     	;
     	; test of spectra at Psi=0
     	;
     	; at psi=0 (i.e., flag=1)
        In [274]: srfunc.sync_ene(1,e,ec_ev=19166.0,e_gev=6,i_a=0.1,hdiv_mrad=1)
        Out[274]: 
              array([[  6.89307648e+13,   6.81126315e+13,   6.71581119e+13,
          6.60866137e+13,   6.49155481e+13,   6.36605395e+13,
          6.23356084e+13,   6.09533305e+13,   5.95249788e+13,
          5.80606485e+13]])


     	; at psi_min (FLAG=3)
        In [279]: srfunc.sync_ene(3,e,ec_ev=19166.0,e_gev=6,i_a=0.1, \
                  hdiv_mrad=1,psi_min=0.0)
        Out[279]: 
        array([[  6.89307648e+13,   6.81126315e+13,   6.71581119e+13,
          6.60866137e+13,   6.49155481e+13,   6.36605395e+13,
          6.23356084e+13,   6.09533305e+13,   5.95249788e+13,
          5.80606485e+13]])

     	;
     	; test of integrated spectra 
     	;
     	
     	; Integrating (by hand) using flag=3
        # a is large enough to cover the full radiation fan
     	a = numpy.linspace(-0.2,0.2,50) 
        #create 10-points energy array in [20,30] keV
        e=numpy.linspace(20000.0,30000.0,10)
     	
        y3=e*0.0
     	for i in range(a.size): 
     	    y2=srfunc.sync_ene(3,e,ec_ev=19166.0,e_gev=6,i_a=0.1,hdiv_mrad=1,psi_min=a[i])
     	    y3[i] = y3[i] + y2
     	y3=y3*(a[1]-a[0])
     	
     	; Integrating (automatically) using FLAG=2
     	y4 = srfunc.sync_ene(2,e,ec_ev=19166.0,e_gev=6,i_a=0.1,hdiv_mrad=1,\
        psi_min=-0.2,psi_max=0.2,psi_npoints=50)
     	
     	; Integrated (over all angles) using FLAG=0
     	y5 = srfunc.sync_ene(0,e,ec_ev=19166.0,e_gev=6,i_a=0.1,hdiv_mrad=1)
     	
        In [475]: for i in range(y3.size):
            print e[i],y3[i],y4[i],y5[i]
           .....:     
           .....:     

     	The results obtained are: 
        energy        int_by_hand       int_num           int
        20000.0       9.32554203564e+12 9.32554203564e+12 9.33199803948e+12
        21111.1111111 8.95286605221e+12 8.95286605221e+12 8.9590640148e+12
        22222.2222222 8.58856640727e+12 8.58856640727e+12 8.59451215453e+12
        23333.3333333 8.2334342483e+12 8.2334342483e+12 8.2391341364e+12
        24444.4444444 7.88805461639e+12 7.88805461639e+12 7.89351540031e+12
        25555.5555556 7.55284456882e+12 7.55284456882e+12 7.55807329003e+12
        26666.6666667 7.22808379127e+12 7.22808379127e+12 7.23308768405e+12
        27777.7777778 6.91393939677e+12 6.91393939677e+12 6.91872581084e+12
        28888.8888889 6.61048616971e+12 6.61048616971e+12 6.61506250643e+12
        30000.0       6.31772320182e+12 6.31772320182e+12 6.32209686189e+12

     	EXAMPLE 2
     		Surface plot of flux versus angle ane energy
     		e = numpy.linspace(20000,30000,20)
     		tmp1,fm,a = srfunc.sync_ene(2,e,ec_ev=19166.0,e_gev=6,i_a=0.1,\
                      hdiv_mrad=1,psi_min=-0.2,psi_max=0.2,psi_npoints=50)
     		surface,fm,a,e, ztitle='Flux[phot/sec/0.1%bw/mradPsi', $
     			xtitle='Angle [mrad]',ytitle='Energy [eV]'

      MODIFICATION HISTORY:
            Written by:     M. Sanchez del Rio, srio@esrf.fr, 2002-06-03
     	2007-05-14 srio@esrf.fr debug with FLAG=2. The bandwith in 
     		angle depends on the number of points. Now it is 1mrad
     		Bug reported by flori@n-nolz.de
     		Added default values. 
        2007-12-13  srio@esrf.eu fixes bug reported by Gernot.Buth@iss.fzk.de
                    concerning the normalization of the angular integral.
     
        20120208 srio@esrf.eu: python version
      
     -
    """
    # retrieve physical constants needed
    codata = scipy.constants.codata.physical_constants
    
    codata_c, tmp1, tmp2 = codata["speed of light in vacuum"]
    codata_c = numpy.array(codata_c)
    
    codata_mee, tmp1, tmp2 = codata["electron mass energy equivalent in MeV"]
    codata_mee = numpy.array(codata_mee)
    
    codata_h, tmp1, tmp2 = codata["Planck constant"]
    codata_h = numpy.array(codata_h)
    
    codata_ec, tmp1, tmp2 = codata["elementary charge"]
    codata_ec = numpy.array(codata_ec)

    energy_ev = numpy.array(energy_ev)
    oldshape = energy_ev.shape
    energy_ev.shape = -1
   
    

    if f_psi == 0: # fully integrated in Psi
    # numerical cte for integrated flux
        a8 = numpy.sqrt(3e0)*9e6*codata_ec/codata_h/codata_c/codata_mee 
        a5 = a8*e_gev*i_a*hdiv_mrad* \
             sync_g1(energy_ev/ec_ev,polarization=polarization)
        a5.shape = oldshape
        return a5

    if f_psi == 1: #at Psi = 0
        #a8 =  1.3264d13
        a8 = codata_ec/numpy.power(codata_mee,2)/codata_h*(9e-2/2/numpy.pi) 
        a5 = a8*numpy.power(e_gev,2)*i_a*hdiv_mrad* \
             sync_hi(energy_ev/ec_ev,polarization=polarization)
        a5.shape = oldshape
        return a5

    if f_psi == 2: #between PsiMin and PsiMax
        # a8 = 1.3264d13
        a8 = codata_ec/numpy.power(codata_mee,2)/codata_h*(9e-2/2/numpy.pi) 
        eene = energy_ev/ec_ev
        gamma = e_gev*1e3/codata_mee
        angle_mrad = numpy.linspace(psi_min,psi_max,psi_npoints)
        eene2 = numpy.outer(angle_mrad*0.0e0+1,eene)
        a5=sync_f(angle_mrad*gamma/1e3,eene,polarization=polarization) 
        
        a5 = a5*numpy.power(eene2,2)*a8*i_a*hdiv_mrad*numpy.power(e_gev,2)
        fMatrix = a5
        #a5 = Total(fMatrix,1) 
        # corrected srio@esrf.eu 2007/12/13 
        # bug reported by Gernot.Buth@iss.fzk.de
        angle_step = (float(psi_max)-psi_min)/(psi_npoints-1.0)
        a5 = fMatrix.sum(axis=0) * angle_step
        return a5,fMatrix,angle_mrad

    if f_psi == 3: #at PsiMin
        a8 = codata_ec/numpy.power(codata_mee,2)/codata_h*(9e-2/2/numpy.pi) 
        #a8 = 1.3264d13
        eene = energy_ev/ec_ev
        gamma = e_gev*1e3/codata_mee
        angle_mrad = psi_min
        a5=sync_f(angle_mrad*gamma/1e3,eene,polarization=polarization)
        a5 = a5*numpy.power(eene,2)*a8*i_a*hdiv_mrad*numpy.power(e_gev,2)
        a5.shape = oldshape
        return a5


if __name__ == '__main__':


    import sys
    plot_option = -1
    if len(sys.argv) >= 2: 
        plot_option = int(sys.argv[1])
    else:
        print("plot_option:    ")
        print("    -1 Cancel")
        print("     0 matplotlib  (imports: matplotlib,pylab)")
        print("     1 gnuplot     (imports: Gnuplot)")
        print("     2 R           (imports: rpy2)")
        print("     3 PyMca       (imports: PyQt4,PyMca)")
        print("     4 IDL         (imports: pidly)") 
        tmp = input("?>")
        plot_option = int(tmp)

    print("plot_option: ",plot_option)
    if plot_option == -1:
       exit()

    #plot_option = 2 # 0=matplotlib 1=gnuplot 2=R 3=PyMca 4=IDL

    # input for ESRF
    e_gev = 6.04    # electron energy in GeV
    r_m = 25.0      # magnetic radius in m
    i_a = 0.2       # electron current in A
    
    # calculate the critical energy
    
    # retrieve physical constants needed
    codata = scipy.constants.codata.physical_constants
    
    codata_c, tmp1, tmp2 = codata["speed of light in vacuum"]
    codata_c = numpy.array(codata_c)
    
    codata_mee, tmp1, tmp2 = codata["electron mass energy equivalent in MeV"]
    codata_mee = numpy.array(codata_mee)
    
    codata_h, tmp1, tmp2 = codata["Planck constant"]
    codata_h = numpy.array(codata_h)
    
    codata_ec, tmp1, tmp2 = codata["elementary charge"]
    codata_ec = numpy.array(codata_ec)
    
    # calculate critical energy in eV
    gamma = e_gev*1e3/codata_mee
    ec_m = 4.0*numpy.pi*r_m/3.0/numpy.power(gamma,3) # wavelength in m
    m2ev = codata_c*codata_h/codata_ec      # lamda(m)  = ec_ev/energy(eV)
    ec_ev = m2ev/ec_m
    

    # 
    # example 1
    #
    energy_ev = numpy.linspace(100.0,100000.0,99) # photon energy grid
    f_psi = 0    # flag: full angular integration
    flux = sync_ene(f_psi,energy_ev,ec_ev=ec_ev,polarization=0,  \
           e_gev=e_gev,i_a=i_a,hdiv_mrad=1.0, \
           psi_min=0.0, psi_max=0.0, psi_npoints=1)
    
    toptitle = "ESRF Bending Magnet emission"
    xtitle = "Photon energy [eV]"
    ytitle = "Photon flux [Ph/s/mrad/0.1%bw]"
    
    #plot 
    if plot_option == 0:
        import matplotlib
        matplotlib.use('qt4agg')
        from pylab import *

        print ("Kill the graphic to continue...") 
        loglog(energy_ev,flux)
        title(toptitle)
        xlabel(xtitle)
        ylabel(ytitle)
        show()

    if plot_option ==1:
        import Gnuplot, Gnuplot.funcutils
        g = Gnuplot.Gnuplot(debug=1)
        #d = Gnuplot.Data(energy_ev, flux,
        #             title='ESRF Bending Magnet emission',
        #             with_='points 3 3')
        dd=numpy.concatenate( (energy_ev.reshape(-1,1),
            flux.reshape(-1,1)),axis=1)
        g('set log xy')
        g.plot(dd,title=toptitle,
            xlabel=xtitle,
            ylabel=ytitle)
        input("Press ENTER to continue")

    if plot_option ==2:
        import rpy2.robjects  #.robjects.numpy2ri
        import rpy2.robjects.numpy2ri
        rpy2.robjects.r.plot(energy_ev,flux, main=toptitle,log="xy",\
            type="l",xlab=xtitle,ylab=ytitle)
        #raw_input("Press ENTER to continue")
        
    if plot_option ==3:
        import PyQt4.Qt as qt
        from PyMca import ScanWindow
        app = qt.QApplication([])
        w=ScanWindow.ScanWindow()
        w.addCurve(energy_ev, flux,legend=toptitle)
        w.resize(600,600)
        w.scanWindowInfoWidget.hide()
        w.show()        
        #app.exec_()

    if plot_option ==4:
        import pidly
        idl = pidly.IDL('/scisoft/xop2.3/xop -d none')
        idl.x = energy_ev
        idl.y = flux
        idl.toptitle = toptitle
        idl.xtitle = xtitle
        idl.ytitle = ytitle
        idl('help,x,y')
        idl('xplot,x,y,/xlog,/ylog,title=toptitle,xtitle=xtitle,ytitle=ytitle')
        #raw_input("Press ENTER to continue")
        #idl('exit')


    # 
    # example 2 
    #
    flag = 0 # full energy integration
    angle_mrad = numpy.linspace(-1.0,1.0,101) # angle grid
    flux = sync_ang(flag,angle_mrad,polarization=0, \
           e_gev=e_gev,i_a=i_a,hdiv_mrad=1.0,r_m=r_m,ec_ev=ec_ev)
    toptitle = "ESRF Bending Magnet angular emission (all energies)"
    xtitle   = "Psi[mrad]"
    ytitle   = "Photon Power [Watts/mrad(Psi)]"

    #for i in range(flux.size): 
    #    print angle_mrad[i],flux[i]
    
    #plot 
    if plot_option == 0:
        print ("Kill the graphic to continue...") 
        clf()
        plot(angle_mrad,flux)
        title(toptitle)
        xlabel(xtitle)
        ylabel(ytitle)
        show()

    if plot_option ==1:
        g.reset()
        g = Gnuplot.Gnuplot(debug=1)
        d = Gnuplot.Data(angle_mrad, flux,
        #title=toptitle,
            with_='linespoints')
        g.plot(d,title=toptitle,xlabel=xtitle, ylabel=ytitle)
        input("Press ENTER to continue")

    if plot_option ==2:
        rpy2.robjects.r.X11()
        rpy2.robjects.r.plot(angle_mrad,flux, main=toptitle,\
            type="l",xlab=xtitle,ylab=ytitle)

    if plot_option ==3:
        #import PyQt4.Qt as qt
        #from PyMca import ScanWindow
        #app = qt.QApplication([])
        w1=ScanWindow.ScanWindow()
        w1.addCurve(angle_mrad, flux,legend=toptitle)
        w1.resize(600,600)
        w1.scanWindowInfoWidget.hide()
        w1.show()        
        #app.exec_()

    if plot_option ==4:
        #import pidly
        #idl = pidly.IDL('/scisoft/xop2.3/xop -d none')
        idl.x = angle_mrad
        idl.y = flux
        idl.toptitle = toptitle
        idl.xtitle = xtitle
        idl.ytitle = ytitle
        idl('xplot,x,y,title=toptitle,xtitle=xtitle,ytitle=ytitle')
        #raw_input("Press ENTER to continue")
        #idl('exit')

    #
    # Example 3
    #
    e = numpy.linspace(20000,80000,80)
    tmp1,fm,a = sync_ene(2,e,ec_ev=ec_ev,e_gev=e_gev,i_a=i_a,\
        hdiv_mrad=1,psi_min=-0.2,psi_max=0.2,psi_npoints=50)
    toptitle='Flux vs vertical angle and photon energy'
    xtitle  ='angle [mrad]'
    ytitle  ='energy [eV]'
    ztitle = "Photon flux [Ph/s/mrad/0.1%bw]"
    if plot_option == 0:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        from matplotlib.ticker import LinearLocator
        #from matplotlib import pyplot
        #fig = pyplot.figure()
        fig = figure()
        ax = fig.gca(projection='3d')
        fa, fe = numpy.meshgrid(a, e) 
        surf = ax.plot_surface(fa, fe, numpy.transpose(fm), \
            rstride=1, cstride=1, \
            linewidth=0, antialiased=False)
        #ax.set_zlim3d(-1, 1)
        ax.w_zaxis.set_major_locator(LinearLocator(6))
        show()

    if plot_option == 1:
        g('set parametric')
        g('set data style lines')
        g('set hidden')
        g('set contour base')
        g.title(toptitle)
        g.xlabel(xtitle)
        g.ylabel(ytitle)
        g.splot(Gnuplot.GridData(fm,a,e, binary=0))
        input('Please press return to continue...\n')

    if plot_option ==2:
        rpy2.robjects.r.X11()
        # see https://stat.ethz.ch/pipermail/r-help/2010-May/237375.html
        # see R: help(persp)
        #rpy2.robjects.r.library("rgl")
        #rpy2.robjects.r.persp3d(a, e, fm , col = 'skyblue')
        rpy2.robjects.r.persp(a, e, fm, xlab=xtitle, ylab=ytitle, \
            zlab=ztitle, axes="TRUE", ticktype = "detailed", \
            theta = 30, phi = 30,col = "lightblue", shade = 0.75)
        input("Press ENTER to continue")

    if plot_option ==3:
        #import PyQt4.Qt as qt
        #from PyMca import ScanWindow
        #app = qt.QApplication([])
        from PyMca import MaskImageWidget
        m=MaskImageWidget.MaskImageWidget()
        m.setImageData(fm)
        m.show()
        app.exec_()

    if plot_option ==4:
        #import pidly
        #idl = pidly.IDL('/scisoft/xop2.3/xop -d none')
        idl.x = e
        idl.y = a
        idl.z = fm
        idl.toptitle = toptitle
        idl.xtitle = xtitle
        idl.ytitle = ytitle
        idl.ztitle = ztitle
        idl('help,z,x,y')
        idl('xsurface1,z,x,y,xtitle=xtitle,ytitle=ytitle')
        input("Press ENTER to continue")
        idl('exit')


    #exit()
#    

#

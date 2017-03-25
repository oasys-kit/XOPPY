
import xraylib
import numpy
import scipy.constants as codata

toangstroms = codata.h * codata.c / codata.e * 1e10

#=======================================================================================================================
#  GENERIC UTILITIES
#=======================================================================================================================
def write_spec_file(file_out,data,titles,scan_title=""):
    """
    Writes a spec-formatted file
    :param file_out: Name of output file
    :param data: the numpy.array with data (ncolumns, npoints)
    :param titles: a list with labels of the columns
    :param scan_title: a scan title
    :return:
    """
    #
    # write SPEC file for data[number_of_columns, number_of_points]
    #
    if len(titles) != data.shape[0]:
        raise Exception("Unmatched dimensions: titles: %d, data: (%d,%d)"%(len(titles),data.shape[0],data.shape[1]))

    f = open(file_out,"w")
    f.write("#F %s\n"%file_out)
    f.write("\n#S 1 %s\n"%scan_title)
    f.write("#N %d\n"%(data.shape[0]))
    f.write("#L")
    for ititle in titles:
        f.write("  %s"%(ititle))
    f.write("\n")
    for i in range(data.shape[1]):
        f.write(('%g '*(data.shape[0])+'\n')%( tuple(data[:,i]) ))
    f.close()
    print("File written to disk: %s"%file_out)

def parse_formula(formula): # included now in xraylib, so not used but kept for other possible uses
    """

    :param formula: a formule (e.g. H2O)
    :return: a dictionary with tags: "Symbols","Elements","n","atomicWeight","massFractions","molecularWeight"

    """
    import re
    tmp = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    elements = []
    fatomic = []
    atomic_weight = []
    zetas = []
    massFractions = []
    for element,str_number in tmp:
        if str_number == '':
            number = 1
        else:
            number = int(str_number)

        elements.append(element)
        fatomic.append(number)
        zetas.append(xraylib.SymbolToAtomicNumber(element))
        atomic_weight.append(xraylib.AtomicWeight(xraylib.SymbolToAtomicNumber(element)))
        massFractions.append(number*xraylib.AtomicWeight(xraylib.SymbolToAtomicNumber(element)))

    mweight = 0.0
    for i in range(len(fatomic)):
        mweight += atomic_weight[i] * fatomic[i]
    print("Molecular weight: ",mweight)

    for i in range(len(massFractions)):
        massFractions[i] /= mweight

    return {"Symbols":elements,"Elements":zetas,"n":fatomic,"atomicWeight":atomic_weight,"massFractions":massFractions,"molecularWeight":mweight}


#=======================================================================================================================
#  CROSS SECTIONS, MIRROR AND FILTER UTILITIES
#=======================================================================================================================
# used by xpower TODO: merge with interface_reflectivity
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

    #TODO: do it in another way
    from srxraylib.sources.srfunc import m2ev

    wavelength_m = m2ev / photon_energy_ev
    debyewaller = numpy.exp( -(4.0*numpy.pi*numpy.sin(theta1)*rough1/(wavelength_m*1e10))**2 )

    return rs*debyewaller, rp*debyewaller, runp*debyewaller

def interface_reflectivity(alpha,gamma,theta1):
    """
    Calculates the reflectivity of an interface using Fresnel formulas.

    Code adapted from XOP and SHADOW
    :param alpha: the array with alpha values (alpha=2 delta, n=1-delta+i beta)
    :param gamma: the array with gamma (gamma=2 beta)
    :param theta1: a scalar with the grazing angle in rad
    :return:
    """

    rho =  numpy.sin(theta1)**2 - alpha
    rho += numpy.sqrt( ( (numpy.sin(theta1))**2 - alpha)**2 + gamma**2)
    rho = numpy.sqrt(rho / 2)
    # ;** Computes now the reflectivity for s-pol


    rs1 = 4 * (rho**2) * (numpy.sin(theta1) - rho)**2 + gamma**2
    rs2 = 4 * (rho**2) * (numpy.sin(theta1) + rho)**2 + gamma**2
    rs = rs1 / rs2

    # ;** Computes now the polarization ratio


    ratio1 = 4 * rho**2 * (rho * numpy.sin(theta1) - numpy.cos(theta1))**2 + gamma**2 * numpy.sin(theta1)**2
    ratio2 = 4 * rho**2 * (rho * numpy.sin(theta1) + numpy.cos(theta1))**2 + gamma**2 * numpy.sin(theta1)**2
    ratio = ratio1 / ratio2

    rp = rs * ratio
    runp = 0.5 * (rs + rp)

    return rs,rp,runp


def f1f2_calc(descriptor,energy,theta=3.0e-3,F=0,density=None,rough=0.0):
    """
    calculate the elastic Photon-Atom anonalous f1 and f2  coefficients as a function of energy.
    It also gives the refractive index components delta and beta (n=1-delta - i beta),
    the absorption photoelectric coefficient and the reflectivities (s,p and unpolarized).
    :param descriptor: string with the element symbol or integer with Z
    :param energy: array with energies (eV)
    :param theta: array with grazing angles (rad)
    :param F: calculation flag:

           F=0 (default) returns a 2-col array with f1 and f2
           F=1  returns f1
           F=2  returns f2
           F=3  returns delta  [n = 1 -delta -i beta]
           F=4  returns betaf  [n = 1 -delta -i beta]
           F=5  returns Photoelectric linear absorption coefficient
           F=6  returns Photoelectric mass absorption coefficient
           F=7  returns Photoelectric Cross Section
           F=8  returns s-polarized reflectivity
           F=9  returns p-polarized reflectivity
           F=10  returns unpolarized reflectivity
           F=11  returns delta/betaf
    :param density: the density to be used for some calculations. If None, get it from xraylib
    :param rough: the roughness RMS in Angstroms for reflectivity calculations
    :return: a numpy array with results
    """

    energy = numpy.array(energy,dtype=float).reshape(-1)
    theta = numpy.array(theta,dtype=float).reshape(-1)

    if isinstance(descriptor,str):
        Z = xraylib.SymbolToAtomicNumber(descriptor)
        symbol = descriptor
    else:
        Z = descriptor
        symbol = xraylib.AtomicNumberToSymbol(descriptor)

    if density == None:
        density = xraylib.ElementDensity(Z)


    if F == 0:   # F=0 (default) returns a 2-col array with f1 and f2
        out = numpy.zeros((2,energy.size))
        for i,ienergy in enumerate(energy):
            out[0,i] = Z + xraylib.Fi(Z,1e-3*ienergy)
            out[1,i] = - xraylib.Fii(Z,1e-3*ienergy)
    elif F == 1: # F=1  returns f1
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = Z + xraylib.Fi(Z,1e-3*ienergy)
    elif F == 2: # F=2  returns f2
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = - xraylib.Fii(Z,1e-3*ienergy)
    elif F == 3: # F=3  returns delta  [n = 1 -delta -i beta]
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = (1e0-xraylib.Refractive_Index_Re(symbol,1e-3*ienergy,density))
    elif F == 4: # F=4  returns betaf  [n = 1 -delta -i beta]
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = (1e0-xraylib.Refractive_Index_Im(symbol,1e-3*ienergy,density))
    elif F == 5: # F=5  returns Photoelectric linear absorption coefficient
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = density * xraylib.CS_Photo(Z,1e-3*ienergy)
    elif F == 6: # F=6  returns Photoelectric mass absorption coefficient
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = xraylib.CS_Photo(Z,1e-3*ienergy)
    elif F == 7: # F=7  returns Photoelectric Cross Section
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = xraylib.CSb_Photo(Z,1e-3*ienergy)
    elif F == 11: # F=11  returns delta/betaf
        out = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            out[i] = (1e0-xraylib.Refractive_Index_Re(symbol,1e-3*ienergy,density))
            out[i] /= xraylib.Refractive_Index_Im(symbol,1e-3*ienergy,density)

    if F >= 8 and F <=10: # reflectivities
        atwt = xraylib.AtomicWeight(Z)
        avogadro = codata.Avogadro
        toangstroms = codata.h * codata.c / codata.e * 1e10
        re = codata.e**2 / codata.m_e / codata.c**2 / (4*numpy.pi*codata.epsilon_0) * 1e2 # in cm

        molecules_per_cc = density * avogadro / atwt
        wavelength = toangstroms / energy  * 1e-8 # in cm
        k = molecules_per_cc * re * wavelength * wavelength / 2.0 / numpy.pi

        f1 = numpy.zeros_like(energy)
        f2 = numpy.zeros_like(energy)
        for i,ienergy in enumerate(energy):
            f1[i] = Z + xraylib.Fi(Z,1e-3*ienergy)
            f2[i] = - xraylib.Fii(Z,1e-3*ienergy)

        alpha = 2.0 * k * f1
        gamma = 2.0 * k * f2

        rs,rp,runp = interface_reflectivity(alpha,gamma,theta)

        if rough != 0:
            debyewaller = numpy.exp( -( 4.0 * numpy.pi * numpy.sin(theta) * rough / wavelength)**2)
        else:
            debyewaller = 1.0

        if F == 8:   # returns s-polarized reflectivity
            out = rs * debyewaller
        elif F == 9: # returns p-polarized reflectivity
            out = rp * debyewaller
        elif F == 10: # returns unpolarized reflectivity
            out = runp * debyewaller

    return out


def f1f2_calc_mix(descriptor,energy,theta=3.0e-3,F=0,density=None,rough=0.0):
    """
    Like f1f2_calc but for a chemical formula. S

    :param descriptor: string with the element symbol or integer with Z
    :param energy: array with energies (eV)
    :param theta: array with grazing angles (rad)
    :param F: calculation flag:

           F=0 (default) returns a 2-col array with f1 and f2
           F=1  returns f1
           F=2  returns f2
           F=3  returns delta  [n = 1 -delta -i beta]
           F=4  returns betaf  [n = 1 -delta -i beta]
           F=5  returns Photoelectric linear absorption coefficient
           F=6  returns Photoelectric mass absorption coefficient
           F=7  returns Photoelectric Cross Section
           F=8  returns s-polarized reflectivity
           F=9  returns p-polarized reflectivity
           F=10  returns unpolarized reflectivity
           F=11  returns delta/betaf
    :param density: the density to be used for some calculations.
    :param rough: the roughness RMS in Angstroms for reflectivity calculations
    :return: a numpy array with results
    """
    energy = numpy.array(energy,dtype=float).reshape(-1)

    Zarray = xraylib.CompoundParser(descriptor)
    # Zarray = parse_formula(descriptor)
    zetas = Zarray["Elements"]
    weights = numpy.array(Zarray["nAtoms"])
    atwt = Zarray["molarMass"]
    print("molarMass: %g"%atwt)


    print("f1f2_calc_mix: Zs: ",zetas," n: ",weights)

    f1 = numpy.zeros_like(energy)
    f2 = numpy.zeros_like(energy)
    for i,zi in enumerate(zetas):
        f1i = f1f2_calc(xraylib.AtomicNumberToSymbol(zi),1e-3*energy,theta,F=1)
        f2i = f1f2_calc(xraylib.AtomicNumberToSymbol(zi),1e-3*energy,theta,F=2)
        f1 += f1i * weights[i]
        f2 += f2i * weights[i]

    if F == 0:
        return numpy.vstack((f1,f2))
    elif F == 1:
        return f1
    elif F == 2:
        return f2

    if density == None:
        raise Exception("Please define density.")

    avogadro = codata.Avogadro
    toangstroms = codata.h * codata.c / codata.e * 1e10
    re = codata.e**2 / codata.m_e / codata.c**2 / (4*numpy.pi*codata.epsilon_0) * 1e2 # in cm

    molecules_per_cc = density * avogadro / atwt
    wavelength = toangstroms / energy  * 1e-8 # in cm
    k = molecules_per_cc * re * wavelength * wavelength / 2.0 / numpy.pi

    # ;
    # ; calculation of refraction index
    # ;

    delta = k * f1
    beta = k * f2
    mu = 4.0 * numpy.pi * beta / wavelength

    if F == 3: return delta
    if F == 4: return beta
    if F == 5: return mu
    if F == 6: return mu/density
    if F == 7: return mu/molecules_per_cc*1e24
    if F == 11: return delta/beta

    #
    # interface reflectivities
    #

    alpha = 2.0 * k * f1
    gamma = 2.0 * k * f2

    rs,rp,runp = interface_reflectivity(alpha,gamma,theta)

    if rough != 0:
        debyewaller = numpy.exp( -( 4.0 * numpy.pi * numpy.sin(theta) * rough / wavelength)**2)
    else:
        debyewaller = 1.0

    if F == 8: return rs*debyewaller # returns s-polarized reflectivity
    if F == 9: return rp*debyewaller # returns p-polarized reflectivity
    if F == 10: return runp*debyewaller# returns unpolarized reflectivity

    raise Exception("Why am I here? ")

def cross_calc(descriptor,energy,calculate=0,unit=None,density=None):
    """
    calculate the atomic cross sections and attenuation coefficients.
    :param descriptor: string with the element symbol or integer with Z
    :param energy: array with energies (eV)
    :param calculate:
            0: total cross section
            1: photoelectric cross section
            2: rayleigh cross serction
            3: compton cross section
            4: total minus raileigh cross section
    :param unit:An flag indicating the unit of the output array
            None (default) return all units in multiple columns
            0: barn/atom (Cross Section calculation)
            1: cm^2 (Cross Section calculation)
            2: cm^2/g (Mass Attenuation Coefficient)
            3: cm^-1 (Linear Attenuation Coefficient)
    :param density: the material density in g/cm^3
    :return:  if unit=None an array (5, npoints) with energy and unit=0 to 4, else returns one-column array
    """


    energy = numpy.array(energy,dtype=float).reshape(-1)
    out = numpy.zeros_like(energy)

    if isinstance(descriptor,str):
        Z = xraylib.SymbolToAtomicNumber(descriptor)
        symbol = descriptor
    else:
        Z = descriptor
        symbol = xraylib.AtomicNumberToSymbol(descriptor)

    tmp = numpy.zeros_like(energy)

    if calculate == 0:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Total(Z,1e-3*ienergy)
    elif calculate == 1:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Photo(Z,1e-3*ienergy)
    elif calculate == 2:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Rayl(Z,1e-3*ienergy)
    elif calculate == 3:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Compt(Z,1e-3*ienergy)
    elif calculate == 4:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Total(Z,1e-3*ienergy) - xraylib.CSb_Rayl(Z,1e-3*ienergy)

    if density == None:
        density = xraylib.ElementDensity(Z)

    out = numpy.zeros((5,energy.size))
    out[0,:] = energy
    out[1,:] = tmp         # barn/atom (Cross Section calculation)
    out[2,:] = tmp * 1e-24 #  cm^2 (Cross Section calculation)
    out[3,:] = tmp * 1e-24 * codata.Avogadro / xraylib.AtomicWeight(Z)           # cm^2/g (Mass Attenuation Coefficient)
    out[4,:] = tmp * 1e-24 * codata.Avogadro / xraylib.AtomicWeight(Z) * density # cm^-1 (Linear Attenuation Coefficient)

    if unit == None:
        return out
    else:
        return out[1+unit,:].copy()


def cross_calc_mix(descriptor,energy,calculate=0,unit=None,parse_or_nist=0,density=None):
    """
    Same as cross_calc, but for a compund (formula or name in the NIST compound list)
    :param descriptor: a compound descriptor (as in xraylib)
    :param energy: photon energy array in eV
    :param calculate:
            0: total cross section
            1: photoelectric cross section
            2: rayleigh cross serction
            3: compton cross section
            4: total minus raileigh cross section
    :param unit:An flag indicating the unit of the output array
            None (default) return all units in multiple columns
            0: barn/atom (Cross Section calculation)
            1: cm^2 (Cross Section calculation)
            2: cm^2/g (Mass Attenuation Coefficient)
            3: cm^-1 (Linear Attenuation Coefficient)
    :param parse_or_nist: 0 for compound (default), 1 for name in the NIST compound list
    :param density: the material density in g/cm^3
    :return:
    """

    energy = numpy.array(energy,dtype=float).reshape(-1)
    out = numpy.zeros_like(energy)

    if parse_or_nist == 0:
        if (density == None):
            raise Exception("Please define density")
    else:
        if isinstance(descriptor,int):
            nist_compound = xraylib.GetCompoundDataNISTByIndex(descriptor)
            descriptor = nist_compound["name"]
        if (density == None):
            nist_compound = xraylib.GetCompoundDataNISTByName(descriptor)
            density = nist_compound["density"]

    print("cross_calc_mix: Using density %g g/cm3"%density)
    tmp = numpy.zeros_like(energy)
    tmp2 = numpy.zeros_like(energy)

    if calculate == 0:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Total_CP(descriptor,1e-3*ienergy)
            tmp2[i] = xraylib.CS_Total_CP(descriptor,1e-3*ienergy)
    elif calculate == 1:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Photo_CP(descriptor,1e-3*ienergy)
            tmp2[i] = xraylib.CS_Photo_CP(descriptor,1e-3*ienergy)
    elif calculate == 2:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Rayl_CP(descriptor,1e-3*ienergy)
            tmp2[i] = xraylib.CS_Rayl_CP(descriptor,1e-3*ienergy)
    elif calculate == 3:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Compt_CP(descriptor,1e-3*ienergy)
            tmp2[i] = xraylib.CS_Compt_CP(descriptor,1e-3*ienergy)
    elif calculate == 4:
        for i,ienergy in enumerate(energy):
            tmp[i] = xraylib.CSb_Total_CP(descriptor,1e-3*ienergy) - xraylib.CSb_Rayl_CP(descriptor,1e-3*ienergy)
            tmp2[i] = xraylib.CS_Total_CP(descriptor,1e-3*ienergy) - xraylib.CS_Rayl_CP(descriptor,1e-3*ienergy)


    out = numpy.zeros((5,energy.size))
    out[0,:] = energy
    out[1,:] = tmp # barn/atom (Cross Section calculation)
    out[2,:] = tmp * 1e-24 #  cm^2 (Cross Section calculation)
    out[3,:] = tmp2 # cm^2/g (Mass Attenuation Coefficient)
    out[4,:] = tmp2 * density # cm^-1 (Linear Attenuation Coefficient)

    if unit == None:
        return out
    else:
        return out[1+unit,:].copy()


def xpower_calc(energies=numpy.linspace(1000.0,50000.0,100),source=numpy.ones(100),
                substance=["Be"],flags=[0],dens=["?"],thick=[0.5],angle=[3.0],roughness=0.0,
                output_file=None):
    """
    Apply reflectivities/transmittivities of optical elements on a source spectrum

    :param energies: the array with photon energies in eV
    :param source: the spectral intensity or spectral power
    :param substance: a list with descriptors of each optical element  material
    :param flags: a list with 0 (filter or attenuator) or 1 (mirror) for all optical elements
    :param dens: a list with densities of o.e. materials. "?" is accepted for looking in the database
    :param thick: a list with the thickness in mm for all o.e.'s. Only applicable for filters
    :param angle: a list with the grazing angles in mrad for all o.e.'s. Only applicable for mirrors
    :param roughness:a list with the roughness RMS in A for all o.e.'s. Only applicable for mirrors
    :param output_file: name of the output file (default=None, no output file)
    :return: a dictionary with the results
    """


    nelem = len(substance)

    for i in range(nelem):
        try:
            rho = float(dens[i])
        except:
            rho = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber(substance[i]))
            print("Density for %s: %g g/cm3"%(substance[i],rho))

        dens[i] = rho



    outArray = numpy.hstack( energies )
    outColTitles = ["Photon Energy [eV]"]
    outArray = numpy.vstack((outArray,source))
    outColTitles.append("Source")

    txt = ""
    txt += "*************************** power results ******************\n"
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

    ncol = len(outColTitles)
    npoints = energies.size

    if output_file is not None:
        f = open(output_file,"w")
        f.write("#F "+output_file+"\n")
        f.write("\n")
        f.write("#S 1 power: properties of optical elements\n")

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
        print("File written to disk: " + output_file)

    return {"data":outArray,"labels":outColTitles,"info":txt}



#=======================================================================================================================
#  CRYSTAL UTILITIES
#=======================================================================================================================

#TODO: in future we will use xraylib, by now we use this.
def f0_xop(Z):
    """
    Returns the f0 value as stired in the f0_xop DABAX file:

    Parametrization of f0 (the non-dispersive part of the atomic scttering factor) vs sin(theta/lambda).
    This file contains a Waasmaier&Kirfel-like parametrization
    for the f0 data evaluated by Kissel using modified relativistic form
    factor [1]. For the fitting, model and the data error as in [2] are used.
    The parametrization was calculating by fitting the
    original data in the RTAB database [1] (also in the DABAX file
    f0_mf_Kissel.dat) using the MPFIT IDL procedure of Markwardt
    (http://cow.physics.wisc.edu/~craigm/idl/idl.html) usind the
    function [2]:
       f0[k] = c + [SUM a_i*EXP(-b_i*(k^2)) ]
                   i=1,5
     where k = sin(theta) / lambda and c, a_i and b_i
     are the coefficients tabulated in this file (in columns:
     a1  a2  a3  a4  a5  c  b1  b2  b3  b4  b5

    References
    [1] L. Kissel, Radiation physics and chemistry 59 (2000) 185-200
        available at:
        http://www-phys.llnl.gov/Research/scattering/RTAB.html
    [2] D. Waasmaier & A. Kirfel (Acta Cryst. (1995). A51, 416-413)


     Remarks:
     1) This file contains data for only neutral atoms. For ionic states
        other DABAX files (like f0_WaasKirf.dat) could be used.
     2) The coefficients in this file are prepared for xop2.1 and are
        unpublished.
     3) We created this file for being used as a default for XOP2.1. The
        reasons were two:
        i) It is more practical to use a parametrization rather than to use
           the direct data in file f0_mf.dat because of spped and storage
           reasons.
        ii) The previous defaulty file for XOP 2.0 was f0_WaasKirf.dat, which
           contained a published parametrization [2], but the original data
           is from the International Tables for X-ray Crystallography, vol C,
           (1995) Edited by AJC Wilson, Kluwer Academic Press, table 6.1.1.3
           which contains data from multiple origins (and references). We
           prefer to use evaluated data in the same conditions for all elements
           to keep some consistency in their origin.
           Additionally, Kissel data for f1f2 and CrossSec are also used in XOP.

    Column description: a1  a2  a3  a4  a5  c  b1  b2  b3 b4  b5

    :param Z: the atomic number
    :return: the 11 coefficients for buiding f0
    """
    tmp = [
    [ 0.30426303,     0.45440815,     0.07977026,     0.15268426,     0.00871624,     0.00006937,     9.61768510,    23.52152246,     3.33237545,    53.49579285,     0.80301704],
    [ 0.79971010,     0.63926998,     0.25291139,     0.27260951,     0.03475295,     0.00044196,    10.35354478,     3.93677741,     1.38554540,    25.50380187,     0.34363759],
    [ 0.93188799,     0.17034671,     0.71602201,     0.35839485,     0.82020547,     0.00260460,     4.17494209,     0.33818181,    85.52950781,   175.66836887,     1.37984909],
    [ 1.35769775,     0.71952631,     0.76849159,     0.14970777,     0.99985829,     0.00347440,    37.89541686,     0.66643295,    92.11060309,     0.17800503,     1.90321664],
    [ 2.11021585,     0.94826030,     1.03175074,     0.17991800,     0.72039282,     0.00538888,    21.36228681,     1.17425000,    65.42872639,     0.12888999,     0.44259026],
    [ 2.75491071,     1.06083859,     1.39000885,   -61.38969569,     0.72824752,    61.44921510,    13.55853062,     0.76518509,    43.40152845,    -0.00002249,     0.23756415],
    [ 0.59731711,     2.28313328,     0.63580984,     2.26859990,     1.18920099,     0.02241857,     0.13665445,    17.86124963,    47.32019642,     7.67047709,     0.49262938],
    [ 2.85010001,     2.54410664,     0.64919585,     0.79765894,     1.12558170,     0.02853916,    12.89518279,     5.45538842,     0.11296751,    35.32893278,     0.38721225],
    [ 3.40542650,     2.84112029,     0.71156027,     0.94857450,     1.05115146,     0.03584797,     9.84065316,     4.07801707,     0.09701872,    27.57669889,     0.31753486],
    [ 3.93418627,     3.17292749,     0.78988890,     1.08878497,     0.96122888,     0.04476065,     7.82568355,     3.17536738,     0.08620371,    22.24803408,     0.27139624],
    [ 4.67888021,     3.31246434,     1.20302749,     1.11030781,     0.60080617,     0.07903453,     2.97160025,     8.01401365,     0.09917076,   119.87596938,     0.36875620],
    [ 4.85834741,     1.50402245,     1.53555848,     0.95416075,     3.00404753,     0.13060425,     4.35307904,    95.26343316,     0.11044872,    31.99246407,     1.75670443],
    [ 4.68669359,     2.38879059,     1.52287056,     1.07903978,     3.16354871,     0.14361992,     3.40015051,    36.83643520,     0.09557493,   114.27524168,     1.47492947],
    [ 4.98816795,     3.35710271,     1.50292204,     1.22172882,     2.76143663,     0.15142442,     2.53600438,    29.97580504,     0.08254945,    88.73513838,     1.16712390],
    [ 2.10509260,     4.36716206,     1.48028761,     1.33409382,     5.53780604,     0.15604602,     0.89460753,    24.41881968,     0.07145192,    69.85860169,     1.90671824],
    [ 6.20239600,     5.39538819,     1.45887725,     1.42806579,     1.33894393,     0.15420384,     1.46090299,    20.14653917,     0.06164271,    56.73801104,     0.64755460],
    [ 1.42704046,     6.77857375,     6.41364632,     1.52938606,     0.68790919,     0.13835865,     0.05185139,     1.14744676,    16.83234374,    47.08267330,     0.39585031],
    [ 7.12496467,     6.96362577,     0.40535492,     1.69961663,     1.50025574,     0.27745601,     0.91908882,    14.15475105,    14.15474574,    39.07709506,     0.06417165],
    [ 8.37197122,     7.07989232,     1.01347196,     0.77223727,     1.46667316,     0.26287737,    11.89949237,     0.78056461,   198.44072308,    41.56210501,     0.05445260],
    [ 8.64392994,     1.46357896,     1.56066861,     1.05545005,     7.04009562,     0.19999674,     9.69070226,     0.04305143,    72.04776233,   166.55421240,     0.66621783],
    [ 1.68383652,     1.47480433,     1.37047425,     9.24659290,     7.02207943,     0.16099853,    49.92976638,     0.03653814,   134.31889317,     8.45519757,     0.58503649],
    [ 9.88746586,     1.50747326,     1.90635535,     1.54310395,     7.00376164,     0.10558296,     7.44889667,     0.03084452,    38.16657035,   115.68708856,     0.51848158],
    [10.51693874,     1.57393530,     2.16699802,     1.69193955,     6.98396214,     0.01430187,     6.58802517,     0.02534021,    30.05889048,   101.44514004,     0.46207981],
    [11.07627441,     1.58619669,     2.93288168,     1.37491086,     6.96664643,     0.00459082,     5.94437112,     0.02328655,    20.59115302,    96.88722975,     0.41908215],
    [11.73712145,     1.82995875,     2.81141301,     1.90065220,     6.94066322,    -0.28355091,     5.23367741,     0.01636240,    20.53719746,    82.01631881,     0.37401385],
    [12.30434401,     2.32437385,     3.18807287,     1.99400470,     6.92612145,    -0.80737786,     4.69095987,     0.01074597,    17.39159075,    74.61601310,     0.33856083],
    [12.87035966,     4.43881362,     3.58294665,     2.06698965,     6.91586723,    -2.95253425,     4.22745007,     0.00461408,    15.08330800,    68.44820515,     0.30788472],
    [13.40782101,     6.90042218,     3.99539727,     2.14745733,   283.90205482,  -282.43818444,     3.82465894,     0.28165040,    13.17017325,    62.81493664,     0.00006082],
    [13.75399998,   297.69542224,     5.21908965,     1.58299921,     6.87528047,  -296.22007511,     3.49108135,     0.00005604,    11.26181897,    62.07734534,     0.26153431],
    [14.43242183,     6.83363443,     4.86041106,     2.31023153,   518.74776544,  -517.28462315,     3.16729215,     0.24008925,    10.34604629,    53.61746648,     0.00002943],
    [15.57306569,     6.80777698,     4.48158313,     2.55416620,   237.18610925,  -235.71998143,     2.94104939,     0.22275367,    11.54501025,    63.56972773,     0.00006123],
    [16.29213242,   271.89501093,     4.17901049,     3.17804713,     6.76929988,  -270.43761631,     2.69207459,     0.00004947,    12.10034542,    55.59088173,     0.20581071],
    [16.79861850,   336.43256975,     4.18039017,     3.72954296,     6.72535523,  -334.99650264,     2.44950901,     0.00003586,    12.83743210,    47.67503824,     0.18952317],
    [17.16712180,   336.96736021,     4.71747652,     3.89487231,     6.68380463,  -335.56546318,     2.22463287,     0.00003080,    14.03902313,    42.86632703,     0.17412989],
    [17.40231392,     5.93891344,   354.54400524,     3.52445295,     6.64817985,  -353.19765239,     2.01532010,    15.16569556,     0.00002303,    40.69766838,     0.15923958],
    [17.53267157,     7.44816522,   267.89934293,     2.98742575,     6.61999042,  -266.63403399,     1.82191497,    15.41761348,     0.00002029,    39.30642110,     0.14476941],
    [ 8.87288109,     1.56926290,     6.66073618,     1.08275119,    17.57340057,     1.08665457,    14.34390518,    35.97531308,     0.12903646,   209.51615220,     1.64279492],
    [17.59670810,     9.94862630,     6.04462400,     2.61652635,     0.54472165,     1.07329335,     1.49577834,    13.12002382,     0.11972149,   119.44032856,     0.11972149],
    [17.65536751,    10.43931521,     5.65885161,     3.13610892,     0.86203672,     1.06017183,     1.36826402,    12.12449612,     0.11133571,    95.69676914,     0.11133576],
    [17.70896284,    11.09168541,     5.76424243,     3.49865793,     0.68990337,     1.04561396,     1.25477542,    11.37544137,     0.10372418,    80.89514696,     0.10372414],
    [17.82410279,    12.34652807,     4.93750714,     3.19055176,     1.46016577,     1.02630932,     1.15717637,    11.35742646,     0.09662928,    69.39554321,     0.09662930],
    [ 6.17787753,    17.84044504,    13.24473559,     3.35857771,     0.15154195,     0.99960433,     0.08963202,     1.06333880,    10.67451656,    61.58100361,     0.08963181],
    [17.74278282,     3.79497777,     0.79808174,    13.24774635,     6.24221603,     0.95794137,     0.97113299,    42.86390771,   132.10191226,     9.26979654,     0.08236923],
    [ 6.18155275,    17.80169136,    14.63083035,     3.59439161,     0.64428903,     0.91877951,     0.07624173,     0.89717697,     9.12737711,    36.30062507,   130.83719947],
    [ 6.12780040,    17.79870560,     3.70551025,     0.61262679,    15.64710027,     0.86745289,     0.07028489,     0.82885382,    33.92215621,   126.42588650,     8.60698534],
    [ 6.09085570,     4.68870690,    17.15641530,     3.84300712,    13.15123080,     0.80254284,     0.06457257,     0.76863619,     8.38997512,    34.11521928,     0.76863617],
    [ 6.05724103,    17.76734177,     3.85910747,     0.54976811,    17.79132902,     0.70865971,     0.05857511,     7.66424959,    30.20483695,   121.19639558,     0.70979037],
    [ 6.04036427,    18.38160827,     4.20316493,     0.75471621,    17.74206099,     0.59841397,     0.05297111,     7.01093020,    30.72014689,   106.80764634,     0.65631719],
    [ 6.06154651,    19.00060821,     4.45915941,     1.04270193,    17.69494384,     0.44547768,     0.04732772,     6.43011640,    31.38897338,   129.84310238,     0.60802939],
    [19.44406366,     6.14105459,     5.04240100,     1.19460095,    17.63952092,     0.22942056,     5.87081521,     0.04153040,    32.37864163,   114.94916342,     0.56396218],
    [ 6.01179028,     6.25268840,    19.69743565,     1.16859113,    17.56401079,    -0.01748380,    32.17182048,     0.03634623,     5.33340196,   103.27699871,     0.52334570],
    [ 7.27011998,     6.55126218,    19.86580814,     0.95229359,    17.52010619,    -0.49670130,    31.27680875,     0.02990172,     4.84670590,   100.88905997,     0.48406725],
    [19.93807829,     7.09598483,     8.55254548,     0.81322939,    17.46003963,    -1.21189020,     4.40199492,     0.02378768,    29.37558678,    96.37033204,     0.44869824],
    [19.95850428,     8.36420076,     9.90402346,     0.65245953,    17.40931309,    -2.65593783,     4.00466253,     0.01705338,    27.35376466,    96.62465241,     0.41685323],
    [17.37569453,    12.13586009,    10.55273124,     1.29778936,    19.87680486,    -6.62800954,     0.38664179,     0.00966981,    23.44864968,   220.56960899,     3.64363491],
    [19.82277247,    17.37211521,    10.64912854,     2.42340529,    51.54683902,   -46.21974320,     3.34809910,     0.36080812,    20.04789088,   161.05858343,     0.00185019],
    [19.96684466,  2616.77020357,    11.08605976,     2.97061929,    17.30250838, -2611.52103692,     3.11105960,     0.00003320,    18.89301922,   126.40106401,     0.33961309],
    [17.29595781,  4345.36340933,    20.94755728,     2.49690482,    11.57180940, -4340.11668462,     0.32551631,     0.00001928,     3.04729063,   146.75357391,    17.76655273],
    [21.56386679,    17.23892858,    11.96705606,     2.55058606,  4645.78355064, -4640.56446888,     2.91250166,     0.30985101,    16.75073376,   139.14334527,     0.00001725],
    [17.18849734,  5256.12632558,    12.33127623,     2.58243269,    22.21683582, -5250.92543157,     0.29580553,     0.00001461,    15.88877581,   133.41685838,     2.79253798],
    [17.14790054,  5467.09133967,    12.67590249,     2.61445255,    22.89314617, -5461.92264966,     0.28225651,     0.00001335,    15.09888908,   128.17517281,     2.67966474],
    [23.57776892,  4336.95334631,    13.01186004,     2.65112019,    17.09246464, -4331.80653530,     2.57205344,     0.00001606,    14.35914195,   123.21157749,     0.26967441],
    [17.07135563,  5126.49069186,    13.33466886,     2.65426567,    24.27237487, -5121.36316596,     0.25889588,     0.00001297,    13.73081795,   120.24251547,     2.47764087],
    [24.64625088,    16.99747848,    13.36466048,     3.34514581,  4543.57338365, -4538.49039355,     2.34262325,     0.24679775,    12.90194424,    95.39774603,     0.00001379],
    [25.66612063,  4192.75632504,    13.95736847,     2.72815093,    17.00044486, -4187.69180909,     2.29102865,     0.00001424,    12.50615875,   111.05763849,     0.23787894],
    [26.38323252,  4398.24494424,    14.26736529,     2.76532287,    16.97289395, -4393.23947589,     2.20308248,     0.00001260,    11.95434176,   106.89618428,     0.22734974],
    [27.09405383,    16.93749917,    14.58634079,     2.80145206,  3698.14032223, -3693.18846082,     2.11867358,     0.21749694,    11.43043354,   102.92181598,     0.00001396],
    [27.81053249,  4104.64353871,    14.88325935,     2.83483528,    16.89331430, -4099.71721767,     2.04181579,     0.00001196,    10.95422544,    99.42542607,     0.20889623],
    [28.52850085,  2445.57145486,    15.22240776,     2.86116529,    16.92020688, -2440.77861007,     1.96383816,     0.00001716,    10.48926663,    96.46598501,     0.19884908],
    [29.24441972,  2212.27369164,    15.49510957,     2.92480251,    16.89099012, -2207.52991878,     1.89336193,     0.00001759,    10.05627636,    91.69307079,     0.19084871],
    [29.69788948,    15.47177518,  2097.86718749,     3.60694158,    16.82362572, -2093.19263162,     1.80307602,     9.47929223,     0.00001698,    77.64749351,     0.18222067],
    [30.11062139,    15.40407022,  2274.03155954,     4.38097094,    16.78436412, -2269.46340922,     1.71565360,     8.96253008,     0.00001361,    63.95107044,     0.17352112],
    [30.57052118,    15.57376402,  1353.88450796,     4.87958160,    16.74532612, -1349.42935153,     1.63430749,     8.68104102,     0.00001949,    56.83069217,     0.16513675],
    [30.98784842,    15.84365824,  1085.37020439,     5.34491722,    16.75914099, -1081.10872457,     1.55377182,     8.43294944,     0.00001745,    50.66121806,     0.15616127],
    [31.36764074,    16.20662904,  1140.89802522,     5.70714498,    16.65069139, -1136.66620413,     1.48081504,     8.26474305,     0.00001603,    45.63908603,     0.14966164],
    [31.75193454,    16.78095382,   410.94969397,     5.94974979,    16.75723964,  -407.05071307,     1.40570152,     8.12076847,     0.00001747,    42.41784435,     0.13977093],
    [31.76739790,     1.41742145,    16.74659192,    16.21969187,     6.34032022,     3.65295339,     1.32218506,    81.15672344,     0.13119994,     7.35439190,    26.57488749],
    [30.98992203,    18.15501717,    16.67920729,     6.30866056,     1.30977395,     3.63949590,     1.27222945,     7.83558995,     0.12654931,    36.86734925,     1.27222941],
    [16.88254232,    19.37581635,    32.62146048,     6.01941144,   432.23434409,  -429.07568590,     0.11690541,     7.87648778,     1.20474478,    32.97062267,    -0.00003099],
    [16.43979396,    19.91863890,    27.76463255,     6.41022928,     4.90481781,     3.58984976,     0.11673200,     7.55331808,     1.15426441,    33.30365931,     1.15426437],
    [16.27949672,    19.61124539,    32.52808287,     1.21893192,     6.82864702,     3.56321128,     0.11193237,     6.83979837,     1.09072759,   118.61695437,    25.09178834],
    [16.15573594,    32.56471040,     6.74799686,     1.62318006,    20.37867502,     3.53108830,     0.10731472,     1.03828673,    25.84002437,   104.03280242,     6.51727715],
    [16.05513439,    32.57219633,     7.10079270,     1.82264739,    20.92330655,     3.49908832,     0.10310727,     0.99041508,    26.79675111,    92.39516651,     6.16859916],
    [15.92966393,    32.53463621,    21.26597071,     1.85348130,     7.90481807,     3.45521535,     0.09871917,     0.94233879,     5.77485734,    84.25758041,    27.14259799],
    [15.82334418,    32.46748196,     9.01250570,     1.72434540,    21.46356994,     3.42272786,     0.09486320,     0.89843768,    27.00385753,    79.63992570,     5.39445822],
    [15.71714768,    32.36554794,    21.55254018,     1.54577949,    10.31957180,     3.38282129,     0.09111052,     0.85619893,     5.01523482,    76.65511543,    26.25222808],
    [15.61356578,    32.29005100,    21.58808798,     1.52079712,    11.49239752,     3.33918799,     0.08744016,     0.81690795,     4.68491604,   187.13075688,    24.42129865],
    [32.26137613,    21.47411433,    11.54875240,     2.70070705,    15.53353668,     3.29342205,     0.78242755,     4.39338862,    21.26815521,   145.78453108,     0.08389021],
    [15.44129352,    32.19461688,    21.67018557,    11.62375491,     3.60839956,     3.23867141,     0.08037991,     0.74781467,     4.14033299,    19.84028498,   113.68244239],
    [15.35041360,    32.15264867,    21.98489988,     4.20304734,    11.87984118,     3.17150887,     0.07685215,     0.71518502,     3.92354148,    96.69516744,    19.25785705],
    [32.41734383,    22.05085313,    13.10871855,     3.72910194,    15.28123528,     3.11865061,     0.68922416,     3.86872813,    17.74443730,   101.90118122,     0.07385957],
    [15.20314929,    32.53208188,    13.81186567,     3.76642798,    22.31042147,     3.04559348,     0.07066435,     0.66171756,    16.79213936,    97.72588956,     3.75457984],
    [32.64327679,    22.60430101,    14.43752068,     3.83052598,    15.12931302,     2.98794434,     0.63635924,     3.65636186,    15.88803466,    93.50959958,     0.06783444],
    [32.89114822,    23.09839499,    15.57640146,     3.06849154,    15.06334425,     2.89811885,     0.61290312,     3.63716663,    15.44356030,   103.61518316,     0.06473308],
    [33.02310917,    23.59414755,    16.08710719,     3.05160429,    15.00738866,     2.79583742,     0.58946182,     3.56398355,    14.80962925,   101.26355106,     0.06167575],
    [14.92952838,    33.03254055,    24.00228529,     3.79349958,    16.07933216,     2.68191187,     0.05858286,     0.56470268,     3.42619535,    86.81878918,    13.93081918],
    [14.87484815,    33.25429616,    24.75369621,     3.05890997,    16.98364667,     2.55564102,     0.05561473,     0.54346670,     3.41941648,    95.53275618,    13.62900417],
    [33.35395184,    25.38419399,    17.37894160,     3.08843097,    14.82268135,     2.41071058,     0.52171734,     3.34704782,    13.07655187,    91.79465535,     0.05263332],
    ]
    tmp = numpy.array(tmp)
    return tmp[Z-1].copy()


def bragg_metrictensor(a,b,c,a1,a2,a3,RETURN_REAL_SPACE=0,RETURN_VOLUME=0,HKL=None):
    """
    Returns the metric tensor in the reciprocal space

    :param a: unit cell a
    :param b: unit cell b
    :param c: unit cell c
    :param a1: unit cell alpha
    :param a2: unit cell beta
    :param a3: unit cell gamma
    :param RETURN_REAL_SPACE: set to 1 for returning metric tensor in real space
    :param RETURN_VOLUME: set to 1 to return the unit cell volume in Angstroms^3
    :param HKL: if !=None, returns the d-spacing for the corresponding [H,K,L] reflection
    :return: the returned value depends on the keywords used. If RETURN_REAL_SPACE=0,RETURN_VOLUME=0, and HKL=None
             then retuns the metric tensor in reciprocal space.
    """
    # input cell a,b,c,alpha,beta,gamma; angles in degrees
    a1 *= numpy.pi / 180.0
    a2 *= numpy.pi / 180.0
    a3 *= numpy.pi / 180.0
    # ;
    # ; tensor in real space
    # ;
    g = numpy.array( [ [a*a, a*b*numpy.cos(a3), a*c*numpy.cos(a2)], \
          [a*b*numpy.cos(a3), b*b, b*c*numpy.cos(a1)], \
          [a*c*numpy.cos(a2), b*c*numpy.cos(a1), c*c]] )

    if RETURN_REAL_SPACE: return g
    # print("g: ",g)

    # ;
    # ; volume of the lattice
    # ;
    volume2 = numpy.linalg.det(g)
    volume = numpy.sqrt(volume2)

    # print("Volume of unit cell: %g A^3",volume)

    if RETURN_VOLUME: return volume

    # ;
    # ; tensor in reciprocal space
    # ;
    ginv = numpy.linalg.inv(g)
    # ;print,gInv
    #

    # itmp = where(abs(ginv) LT 1d-8)
    # IF itmp[0] NE -1 THEN ginv[itmp]=0D

    itmp = numpy.where(numpy.abs(ginv) < 1e-8)
    ginv[itmp] = 0.0

    # print("ginv: ",ginv)

    if HKL != None:
    #   ; computes d-spacing
        dd = numpy.dot( numpy.array(HKL) , numpy.dot( ginv , numpy.array(HKL)))
        #
        # print("DD: ", dd)
        dd1 = 1.0 / numpy.sqrt(dd)
        # print("D-spacing: ",dd1)
        return dd1
    else:
        return ginv

def lorentz(theta_bragg_deg,return_what=0):
    """
    This function returns the Lorentz factor, polarization factor (unpolarized beam), geometric factor,
    or a combination of them.

    :param theta_bragg_deg: Bragg angle in degrees
    :param return_what: A flag indicating the returned variable:
                        0: (default) PolFac*lorentzFac
                        1: PolFac
                        2: lorentzFac
                        3: geomFac
    :return: a scalar value
    """
    tr = theta_bragg_deg * numpy.pi / 180.
    polarization_factor = 0.5 * (1.0 + (numpy.cos(2.0 * tr))**2)
    lorentz_factor = 1.0 / numpy.sin(2.0 * tr)
    geometrical_factor = 1.0 * numpy.cos(tr) / numpy.sin(2.0 * tr)

    if return_what == 0:
        return polarization_factor*lorentz_factor
    elif return_what == 1:
        return polarization_factor
    elif return_what == 2:
        return lorentz_factor
    elif return_what == 3:
        return geometrical_factor
    elif return_what == 4:
        return polarization_factor*lorentz_factor*geometrical_factor



def bragg_calc(descriptor="Si",hh=1,kk=1,ll=1,temper=1.0,emin=5000.0,emax=15000.0,estep=100.0,fileout=None):
    """
    Preprocessor for Structure Factor (FH) calculations. It calculates the basic ingredients of FH.

    :param descriptor: crystal name (as in xraylib)
    :param hh: miller index H
    :param kk: miller index K
    :param ll: miller index L
    :param temper: temperature factor (scalar <=1.0 )
    :param emin:  photon energy minimum
    :param emax: photon energy maximum
    :param estep: photon energy step
    :param fileout: name for the output file (default=None, no output file)
    :return: a dictionary with all ingredients of the structure factor.
    """

    output_dictionary = {}

    codata_e2_mc2 = codata.e**2 / codata.m_e / codata.c**2 / (4*numpy.pi*codata.epsilon_0)  # in m

    # f = open(fileout,'w')

    txt = ""
    txt += "# Bragg version, Data file type\n"
    txt += "2.4 1\n"

    cryst = xraylib.Crystal_GetCrystal(descriptor)
    volume = cryst['volume']

    #test crystal data - not needed
    itest = 0
    if itest:

        print ("  Unit cell dimensions are %f %f %f" % (cryst['a'],cryst['b'],cryst['c']))
        print ("  Unit cell angles are %f %f %f" % (cryst['alpha'],cryst['beta'],cryst['gamma']))
        print ("  Unit cell volume is %f A^3" % volume )
        print ("  Atoms at:")
        print ("     Z  fraction    X        Y        Z")
        for i in range(cryst['n_atom']):
            atom =  cryst['atom'][i]
            print ("    %3i %f %f %f %f" % (atom['Zatom'], atom['fraction'], atom['x'], atom['y'], atom['z']) )
        print ("  ")

    volume = volume*1e-8*1e-8*1e-8 # in cm^3
    dspacing = xraylib.Crystal_dSpacing(cryst, hh, kk, ll)
    rn = (1e0/volume)*(codata_e2_mc2*1e2)
    dspacing *= 1e-8 # in cm

    txt += "# RN = (e^2/(m c^2))/V) [cm^-2], d spacing [cm]\n"
    txt += "%e %e \n" % (rn , dspacing)

    output_dictionary["rn"] = rn
    output_dictionary["dspacing"] = dspacing

    atom = cryst['atom']
    list_Zatom = [ atom[i]['Zatom'] for i in range(len(atom))]
    list_fraction = [ atom[i]['fraction'] for i in range(len(atom))]
    list_x = [ atom[i]['x'] for i in range(len(atom))]
    list_y = [ atom[i]['y'] for i in range(len(atom))]
    list_z = [ atom[i]['z'] for i in range(len(atom))]

    unique_Zatom = set(list_Zatom)

    nbatom = (len(unique_Zatom))
    txt += "# Number of different element-sites in unit cell NBATOM:\n%d \n" % nbatom
    output_dictionary["nbatom"] = nbatom

    txt += "# for each element-site, the atomic number\n"
    for i in unique_Zatom:
        txt += "%d "%i
    txt += "\n"
    output_dictionary["atnum"] = list(unique_Zatom)

    #TODO: manage correctly fraction, the ones in non-representative atoms are ignored.
    txt += "# for each element-site, the occupation factor\n"
    unique_fraction = []
    for i in range(len(unique_Zatom)):
        unique_fraction.append(list_fraction[i])
        txt += "%g "%(unique_fraction[i])
    txt += "\n"
    output_dictionary["fraction"] = unique_fraction


    txt += "# for each element-site, the temperature factor\n" # temperature parameter
    list_temper = []
    for i in range(len(unique_Zatom)):
        txt += "%5.3f "%temper
        list_temper.append(temper)
    txt += "\n"
    output_dictionary["temper"] = list_temper

    #
    # Geometrical part of structure factor:  G and G_BAR
    #
    txt += "# for each type of element-site, COOR_NR=G_0\n"
    list_multiplicity = []
    for z in unique_Zatom:
        txt += "%d "%list_Zatom.count(z)
        list_multiplicity.append(list_Zatom.count(z))
    txt += "\n"
    output_dictionary["G_0"] = list_multiplicity

    txt += "# for each type of element-site, G and G_BAR (both complex)\n"
    list_g = []
    list_g_bar = []
    for z in unique_Zatom:
        ga = 0.0 + 0j
        for i,zz in enumerate(list_Zatom):
            if zz == z:
                ga += numpy.exp(2j*numpy.pi*(hh*list_x[i]+kk*list_y[i]+ll*list_z[i]))
        txt += "(%g,%g) \n"%(ga.real,ga.imag)
        txt += "(%g,%g) \n"%(ga.real,-ga.imag)
        list_g.append(ga)
        list_g_bar.append(ga.conjugate())
    output_dictionary["G"] = list_g
    output_dictionary["G_BAR"] = list_g_bar

    #
    # F0 part
    #
    txt += "# for each type of element-site, the number of f0 coefficients followed by them\n"
    list_f0 = []
    for zeta in unique_Zatom:
        tmp = f0_xop(zeta)
        # print(("%g "*11)%(tmp.tolist()))
        txt += ("11 "+"%g "*11+"\n")%(tuple(tmp))
        list_f0.append(tmp.tolist())
    output_dictionary["f0coeff"] = list_f0

    # f.write("# -----------------------------------------------\n")


    # zetas = numpy.array([atom[0]["Zatom"],atom[7]["Zatom"]])
    npoint  = int( (emax - emin)/estep + 1 )
    txt += "# The number of energy points NPOINT: \n"
    txt +=  ("%i \n") % npoint
    output_dictionary["npoint"] = npoint
    txt += "# for each energy point, energy, F1(1),F2(1),...,F1(nbatom),F2(nbatom)\n"
    list_energy = []
    out_f1 = numpy.zeros( (len(unique_Zatom),npoint), dtype=float)
    out_f2 = numpy.zeros( (len(unique_Zatom),npoint), dtype=float)
    out_fcompton = numpy.zeros( (len(unique_Zatom),npoint), dtype=complex)
    for i in range(npoint):
        energy = (emin+estep*i)
        txt += ("%20.11e \n") % (energy)
        list_energy.append(energy)

        for j,zeta in enumerate(unique_Zatom):
            f1a = xraylib.Fi(int(zeta),energy*1e-3)
            f2a = -xraylib.Fii(int(zeta),energy*1e-3) # TODO: check the sign!!
            txt +=  (" %20.11e %20.11e 1.000 \n")%(f1a, f2a)
            out_f1[j,i] = f1a
            out_f2[j,i] = f2a
            out_fcompton[j,i] = 1.0

    output_dictionary["energy"] = list_energy
    output_dictionary["f1"] = out_f1
    output_dictionary["f2"] = out_f2
    output_dictionary["fcompton"] = out_fcompton

    if fileout != None:
        with open(fileout,"w") as f:
            f.write(txt)
            print("File written to disk: %s" % fileout)

    return output_dictionary




def crystal_fh(input_dictionary,phot_in,theta=None,forceratio=0):
    """

    :param input_dictionary: as resulting from bragg_calc()
    :param phot_in: photon energy in eV
    :param theta: incident angle (half of scattering angle) in rad
    :return: a dictionary with structure factor
    """

    # outfil    = input_dictionary["outfil"]
    # fract     = input_dictionary["fract"]
    rn        = input_dictionary["rn"]
    dspacing  = numpy.array(input_dictionary["dspacing"])
    nbatom    = numpy.array(input_dictionary["nbatom"])
    atnum     = numpy.array(input_dictionary["atnum"])
    temper    = numpy.array(input_dictionary["temper"])
    G_0       = numpy.array(input_dictionary["G_0"])
    G         = numpy.array(input_dictionary["G"])
    G_BAR     = numpy.array(input_dictionary["G_BAR"])
    f0coeff   = numpy.array(input_dictionary["f0coeff"])
    npoint    = numpy.array(input_dictionary["npoint"])
    energy    = numpy.array(input_dictionary["energy"])
    fp        = numpy.array(input_dictionary["f1"])
    fpp       = numpy.array(input_dictionary["f2"])



    phot_in = numpy.array(phot_in,dtype=float).reshape(-1)

    toangstroms = codata.h * codata.c / codata.e * 1e10


    itheta = numpy.zeros_like(phot_in)
    for i,phot in enumerate(phot_in):

        if theta == None:
            itheta[i] = numpy.arcsin(toangstroms*1e-8/phot/2/dspacing)
        else:
            itheta[i] = theta

        # print("energy= %g eV, theta = %15.13g deg"%(phot,itheta[i]*180/numpy.pi))
        if phot < energy[0] or phot > energy[-1]:
            raise Exception("Photon energy %g eV outside of valid limits [%g,%g]"%(phot,energy[0],energy[-1]))

        if forceratio == 0:
            ratio = numpy.sin(itheta[i]) / (toangstroms / phot)
        else:
            ratio = 1 / (2 * dspacing * 1e8)
        # print("Ratio: ",ratio)

        F0 = numpy.zeros(nbatom)
        for j in range(nbatom):
            icentral = int(f0coeff.shape[1]/2)
            F0[j] = f0coeff[j,icentral]
            for i in range(icentral):
                F0[j] += f0coeff[j,i] * numpy.exp(-1.0*f0coeff[j,i+icentral+1]*ratio**2)

            # print("F0: ",F0,xraylib.FF_Rayl(int(atnum[j]),ratio))


        # ;C
        # ;C Interpolate for the atomic scattering factor.
        # ;C
        for j,ienergy in enumerate(energy):
            if ienergy > phot:
                break
        nener = j - 1


        F1 = numpy.zeros(nbatom,dtype=float)
        F2 = numpy.zeros(nbatom,dtype=float)
        F = numpy.zeros(nbatom,dtype=complex)

        for j in range(nbatom):
            F1[j] = fp[j,nener] + (fp[j,nener+1] - fp[j,nener]) * \
            (phot - energy[nener]) / (energy[nener+1] - energy[nener])
            F2[j] = fpp[j,nener] + (fpp[j,nener+1] - fpp[j,nener]) * \
            (phot - energy[nener]) / (energy[nener+1] - energy[nener])
            # print("F1,F2",F1,F2)

        r_lam0 = toangstroms * 1e-8 / phot
        for j in range(nbatom):
            F[j] = F0[j] + F1[j] + 1j * F2[j]
            # print("F",F)


        F_0 = 0.0 + 0.0j
        FH = 0.0 + 0.0j
        FH_BAR = 0.0 + 0.0j
        FHr = 0.0 + 0.0j
        FHi = 0.0 + 0.0j
        FH_BARr = 0.0 + 0.0j
        FH_BARi = 0.0 + 0.0j


        TEMPER_AVE = 1.0
        for j in range(nbatom):
            FH  += G[j] *   F[j] * 1.0
            FHr += G[j] * (F0[j] + F1[j])* 1.0
            FHi += G[j] *  F2[j] * 1.0
            F_0 += G_0[j] * ( atnum[j] + F1[j] + 1j * F2[j] ) * 1.0
            TEMPER_AVE *= (temper[j])**(G_0[j]/(G_0.sum()))

            FH_BAR  += (G_BAR[j] * F[j] * 1.0)
            FH_BARr += (G_BAR[j] * (F0[j]  + F1[j]) *1.0)
            FH_BARi += (G_BAR[j] *  F2[j] * 1.0)
            # print("TEMPER_AVE: ",TEMPER_AVE)


        # ;C
        # ;C multiply by the average temperature factor
        # ;C


        FH      *= TEMPER_AVE
        FHr     *= TEMPER_AVE
        FHi     *= TEMPER_AVE
        FH_BAR  *= TEMPER_AVE
        FH_BARr *= TEMPER_AVE
        FH_BARi *= TEMPER_AVE

        STRUCT = numpy.sqrt(FH * FH_BAR)

        # ;C
        # ;C   PSI_CONJ = F*( note: PSI_HBAR is PSI at -H position and is
        # ;C   proportional to fh_bar but PSI_CONJ is complex conjugate os PSI_H)
        # ;C


        psi_over_f = rn * r_lam0**2 / numpy.pi
        psi_h      = rn * r_lam0**2 / numpy.pi * FH
        psi_hr     = rn * r_lam0**2 / numpy.pi * FHr
        psi_hi     = rn * r_lam0**2 / numpy.pi * FHi
        psi_hbar   = rn * r_lam0**2 / numpy.pi * FH_BAR
        psi_hbarr  = rn * r_lam0**2 / numpy.pi * FH_BARr
        psi_hbari  = rn * r_lam0**2 / numpy.pi * FH_BARi
        psi_0      = rn * r_lam0**2 / numpy.pi * F_0
        psi_conj   = rn * r_lam0**2 / numpy.pi * FH.conjugate()

        # ;
        # ; Darwin width
        # ;
        # print(rn,r_lam0,STRUCT,itheta)
        ssvar = rn * (r_lam0**2) * STRUCT / numpy.pi / numpy.sin(2.0*itheta)
        spvar = ssvar * numpy.abs((numpy.cos(2.0*itheta)))
        ssr = ssvar.real
        spr = spvar.real

        # ;C
        # ;C computes refractive index.
        # ;C ([3.171] of Zachariasen's book)
        # ;C
        REFRAC = (1.0+0j) - r_lam0**2 * rn * F_0 / 2/ numpy.pi
        DELTA_REF = 1.0 - REFRAC.real
        ABSORP = 4.0 * numpy.pi * (-REFRAC.imag) / r_lam0


        txt = ""
        txt += '\n******************************************************'
        txt += '\n       at energy    = '+repr(phot)+' eV'
        txt += '\n                    = '+repr(r_lam0*1e8)+' Angstroms'
        txt += '\n       and at angle = '+repr(itheta*180.0/numpy.pi)+' degrees'
        txt += '\n                    = '+repr(itheta)+' rads'
        txt += '\n******************************************************'

        for j in range(nbatom):
            txt += '\n  '
            txt += '\nFor atom '+repr(j+1)+':'
            txt += '\n       fo + fp+ i fpp = '
            txt += '\n        '+repr(F0[j])+' + '+ repr(F1[j].real)+' + i'+ repr(F2[j])+" ="
            txt += '\n        '+repr(F0[j] + F1[j] + 1j * F2[j])
            txt += '\n       Z = '+repr(atnum[j])
            txt += '\n       Temperature factor = '+repr(temper[j])
        txt += '\n  '
        txt += '\n Structure factor F(0,0,0) = '+repr(F_0)
        txt += '\n Structure factor FH = '      +repr(FH)
        txt += '\n Structure factor FH_BAR = '  +repr(FH_BAR)
        txt += '\n Structure factor F(h,k,l) = '+repr(STRUCT)
        txt += '\n  '
        txt += '\n Psi_0  = '   +repr(psi_0)
        txt += '\n Psi_H  = '   +repr(psi_h)
        txt += '\n Psi_HBar  = '+repr(psi_hbar)
        txt += '\n  '
        txt += '\n Psi_H(real) Real and Imaginary parts = '   + repr(psi_hr)
        txt += '\n Psi_H(real) Modulus  = '                   + repr(numpy.abs(psi_hr))
        txt += '\n Psi_H(imag) Real and Imaginary parts = '   + repr(psi_hi)
        txt += '\n Psi_H(imag) Modulus  = '                   + repr(abs(psi_hi))
        txt += '\n Psi_HBar(real) Real and Imaginary parts = '+ repr(psi_hbarr)
        txt += '\n Psi_HBar(real) Modulus  = '                + repr(abs(psi_hbarr))
        txt += '\n Psi_HBar(imag) Real and Imaginary parts = '+ repr(psi_hbari)
        txt += '\n Psi_HBar(imag) Modulus  = '                + repr(abs(psi_hbari))
        txt += '\n  '
        txt += '\n Psi/F factor = '                           + repr(psi_over_f)
        txt += '\n  '
        txt += '\n Average Temperature factor = '             + repr(TEMPER_AVE)
        txt += '\n Refraction index = 1 - delta - i*beta'
        txt += '\n            delta = '                       + repr(DELTA_REF)
        txt += '\n             beta = '                       + repr(1.0e0*REFRAC.imag)
        txt += '\n Absorption coeff = '                       + repr(ABSORP)+' cm^-1'
        txt += '\n  '
        txt += '\n e^2/(mc^2)/V = '                           + repr(rn)+' cm^-2'
        txt += '\n d-spacing = '                              + repr(dspacing*1.0e8)+' Angstroms'
        txt += '\n SIN(theta)/Lambda = '                      + repr(ratio)
        txt += '\n  '
        txt += '\n Darwin width for symmetric s-pol [microrad] = ' + repr(2.0e6*ssr)
        txt += '\n Darwin width for symmetric p-pol [microrad] = ' + repr(2.0e6*spr)

    return {"PHOT":phot, "WAVELENGTH":r_lam0*1e-2 ,"THETA":itheta, "F_0":F_0, "FH":FH, "FH_BAR":FH_BAR,
	        "STRUCT":STRUCT, "psi_0":psi_0, "psi_h":psi_h, "psi_hbar":psi_hbar,
        	"DELTA_REF":DELTA_REF, "REFRAC":REFRAC, "ABSORP":ABSORP, "RATIO":ratio,
        	"ssr":ssr, "spr":spr, "psi_over_f":psi_over_f, "info":txt}


def mare_calc(descriptor,H,K,L,HMAX,KMAX,LMAX,FHEDGE,DISPLAY,lambda1,deltalambda,PHI,DELTAPHI,verbose=0):
    """
        Calculates:

      - Spaghetti plots (lambda versis Psi for multiple crystal reflection)

      - The Umweganregung peak location plot (the diffracted wavelength lambda vs. Psi) for a given primary
        reflection,i.e., an horizontal cut of the spaghetti plot.
      - The Glitches spectrum (the negative intensity for versus the wavelength) or a vertical cut of the spaghetti plot.

      Psi is the azimutal angle of totation, i.e., the totation around
        the H vector (main reflection)


     In other words, if a crystal is set with a particular Bragg angle to match a given reflection (inputs: H,K,L) at
     a given wavelength (input: WaveLength), many other (secondary) reflections are excited when the crystal is rotated
     around the azimutal angle Psi, without changing the Bragg angle.

     The plot (WaveLength,Psi) of the possible reflections is calculated and contains all possible reflection curves
     up to a maximum reflection (input: H Max,  K Max, L Max).

     Umweg plot:
     The intersection of these curves with an horizontal line at the wavelength of the primary reflection
     (input: WaveLength) gives the position of the peaks in the unweg plot. The width of each peak depends on the
     pendent of the curve at the intersection. For that, the Psi1 and Psi2 intersection angles with a band of width
     (input: DeltaWaveLength) are calculated. With this width and the intensity of the diffraction line, it is possible
     to compute a Gaussian that "roughly" describe the peak.


     Glitches plot:
     The intersection of these curves with a vertical line at a given Psi gives the position of the peaks in the
     glitches plot. The width of each peak is the difference between the wavelength values for Psi+/-DeltaPsi
     With this width and the intensity of the diffraction line, it is possible to compute a Gaussian that "roughly"
     describe the peak.


    :param descriptor: a valid crystal name for xraylib
    :param H:    the miller index H
    :param K:    the miller index K
    :param L:    the miller index L
    :param HMAX: the maximum miller index H
    :param KMAX: the maximum miller index K
    :param LMAX: the maximum miller index L
    :param FHEDGE: below this edge (structure factor value) the reflections are discarded
    :param DISPLAY:
            0: Create spaghetti plot script
            0: Create spaghetti+Umweg plot scripts
            0: Create spaghetti+Glitches plot scripts
            0: Create spaghetti+Umweg+Glitches plot scripts
    :param lambda1: wavelength in Angstroms for Umweg plot
    :param deltalambda: delta wavelength in Angstroms for Umweg plot
    :param PHI: phi angle in deg for the Glitches plot
    :param DELTAPHI: delta phi angle in deg for the Glitches plot
    :param verbose: set to 1 for a more verbose output
    :return:
    """

    list_of_scripts = []


    cryst = xraylib.Crystal_GetCrystal(descriptor)
    # volume = cryst['volume']
    #
    # #test crystal data - not needed
    #
    # print ("  Unit cell dimensions are %f %f %f" % (cryst['a'],cryst['b'],cryst['c']))
    # print ("  Unit cell angles are %f %f %f" % (cryst['alpha'],cryst['beta'],cryst['gamma']))
    # print ("  Unit cell volume is %f A^3" % volume )
    # print ("  Atoms at:")
    # print ("     Z  fraction    X        Y        Z")
    # for i in range(cryst['n_atom']):
    #     atom =  cryst['atom'][i]
    #     print ("    %3i %f %f %f %f" % (atom['Zatom'], atom['fraction'], atom['x'], atom['y'], atom['z']) )
    # print ("  ")


    fhEdge = FHEDGE
    fhMax = -1e0
    fhMaxIndex = -1

    flg_s = 0
    flg_u = 0
    flg_g = 0


    if DISPLAY == 0:
        flg_s = 1
    elif DISPLAY == 1:
        flg_s = 1
        flg_u = 1
    elif DISPLAY == 2:
        flg_s = 1
        flg_g = 1
    elif DISPLAY == 3:
        flg_s = 1
        flg_u = 1
        flg_g = 1


    # ;
    # ; compute the metric tensor in the reciprocal space
    # ;
    ginv = bragg_metrictensor(cryst['a'],cryst['b'],cryst['c'],cryst['alpha'],cryst['beta'],cryst['gamma'])

    # ;
    # ; wavelength (for intersections: unweg pattern)
    # ;
    # lambda1 = LAMBDA # ; for intersections
    # deltalambda = DELTALAMBDA
    lambdas = numpy.array([lambda1-deltalambda, lambda1, lambda1+deltalambda])

    # ;
    # ; phi (for intersections: glitches pattern)
    # ;
    phi = PHI
    deltaPhi = DELTAPHI
    phis = numpy.array([phi-deltaPhi, phi, phi+deltaPhi])

    # ;
    # ; Main reflection
    # ;
    P = numpy.array([H,K,L],dtype=int)
    p2 = (P[0]**2 + P[1]**2 + P[2]**2)
    pn = numpy.sqrt(p2)

    # ;
    # ; Calculate Reference axis (corresponding to phi =0)
    # ; This is a vector perpendicular to P
    # ;
    mm1 = numpy.dot(ginv,P.T)
    mm2 = [mm1[1],-mm1[0],0]
    mm3 = numpy.min(numpy.abs( mm1[numpy.where(mm1 != 0)]  ))
    M0 = (mm2/mm3)

    # ;
    # ; operational reflections (for permutations)
    # ;
    pmax = numpy.array([HMAX,KMAX,LMAX],dtype=float)
    hh = numpy.arange(pmax[0])+1
    hh = numpy.concatenate((-hh,[0],hh))
    kk = numpy.arange(pmax[1])+1
    kk = numpy.concatenate((-kk,[0],kk))
    ll = numpy.arange(pmax[2])+1
    ll = numpy.concatenate((-ll,[0],ll))

    # ;
    # ; calculate the structure needed for intensity calculations
    # ;

    energy = toangstroms/lambda1

    # ;
    # ; first call to bragg_inp, then calculates the intensity of the main reflection
    # ;
    fhInp = bragg_calc(descriptor,int(P[0]),int(P[1]),int(P[2]),emin=energy-100,emax=energy+100,estep=10.0)
    outInt = crystal_fh(fhInp,energy)

    bragg_angle = 180.0 / numpy.pi * numpy.arcsin(lambda1 * 1e-8/2 / fhInp['dspacing'])
    fhMain = outInt["STRUCT"].real
    intMain = lorentz(bragg_angle)*(fhMain**2)

    if verbose:
        print('Main reflection d-spacing [A]: ',fhInp["dspacing"]*1e8)
        print('Main reflection 1/2d=sin(theta)/lambda: ',1.0/(2*fhInp["dspacing"]*1e8))
        print('Main reflection Bragg angle (using lambda Umweg) [DEG]: ',outInt["THETA"]*180/numpy.pi)
        print('Main reflection Lorentz: ',lorentz(outInt["THETA"]*180/numpy.pi))
        print('Main reflection fh (real part): ',fhMain)
        print('Main reflection intensity: ',intMain)
    #
    # ;
    # ; creates abscissas for spaghettis
    # ;
    alpha = numpy.linspace(-90.0,90.0,500)

    # ;
    # ; main loop over permutations on operatinal reflections
    # ;
    out = numpy.zeros((18,15000))
    ngood = 0
    print("MARE: loop over %d reflections..."%(hh.size*kk.size*ll.size))

    norm = lambda vector: numpy.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)

    ijk = 0
    for ih in range(hh.size):
        for ik in range(kk.size):
            for il in range(ll.size):
                ijk += 1
                if verbose: print("\n-------------%d-------------,hkl: %d %d %d"%(ijk,hh[ih],kk[ik],ll[il]))
                r = numpy.array((hh[ih],kk[ik],ll[il]),dtype=int)

                rp = (r*P).sum() / p2 * P
                rp2 = (rp[0]**2 + rp[1]**2 + rp[2]**2)
                rpn = numpy.sqrt(rp2)

                p2new = numpy.dot( P , numpy.dot(ginv,P.T))
                rpnew = numpy.dot( r , numpy.dot(ginv,P.T)) / p2new
                rpnew = rpnew * P

                #   ;
                #   ; Alpha0
                #   ;
                cos_alpha0 = ((r-rp)*M0).sum() / norm(r-rp)/norm(M0)
                alpha0rad = numpy.arccos(cos_alpha0)

                #   ; NOTA BENE: alpha0 is calculating using the orthonormal scalar
                #   ; product. Should this be changed using the metric tensor for a
                #   ; generic structure?
                alpha0 = alpha0rad * 180 / numpy.pi

                #   ;
                #   ; k
                #   ;

                knew1 = 0.5 *  ( numpy.dot( r , numpy.dot( ginv , r.T))  - numpy.dot( r , numpy.dot( ginv , P.T)) )
                knew22 = numpy.dot(r , numpy.dot(ginv , r.T)) - numpy.dot(rpnew, numpy.dot(ginv , rpnew.T))
                knew2 = numpy.sqrt( knew22 )
                knew = knew1 / knew2

                if numpy.abs(knew22) > 1e-8:
                    goodRef = 1
                else:
                    goodRef = 0


                #   ;
                #   ; computes intensity
                #   ;

                fhInp = bragg_calc(descriptor,int(r[0]),int(r[1]),int(r[2]),emin=energy-100,emax=energy+100,estep=10.0,fileout=None)

                fhInp["f1"] *= 0.0
                fhInp["f2"] *= 0.0

                outInt = crystal_fh(fhInp,energy,forceratio=1)

                if outInt["STRUCT"].real < fhEdge:
                    goodRef = 0

                if goodRef == 1:
                    ngood += 1
                    braggAngleUmweg = outInt["THETA"] * 180 / numpy.pi
                    beta = alpha - alpha0
                    y3 = 1.0 / numpy.sqrt( (knew / numpy.cos(beta * numpy.pi / 180))**2 + p2new / 4 )
                    if verbose: print("Bragg angle (for Umweg): %g"%braggAngleUmweg)

                    theta1 = knew**2 / ((1/lambdas)**2 - p2new / 4)
                    if numpy.abs(theta1[1] > 1):
                        theta2 = [-1000,-1000,-1000]
                        theta3 = [-1000,-1000,-1000]
                    else:
                        theta1 = numpy.arccos(numpy.sqrt(theta1))
                        theta1 = theta1*180/numpy.pi
                        theta2 = alpha0 - theta1
                        theta3 = alpha0 + theta1 - 180
                    #     ;
                    #     ; lambda values for phi intervals (for glitches)
                    #     ;
                    lambdaIntersec = 1.0 / numpy.sqrt( (knew/numpy.cos((phis-alpha0)*numpy.pi/180))**2+p2new/4 )

                    if verbose: print("lambdaIntersec:  ",repr(lambdaIntersec))
                    if verbose: print(("d-spacing [A]: %g"%fhInp["dspacing"]))

                    braggAngleGlitches = lambdaIntersec[1]/2/fhInp["dspacing"]/1e8

                    if numpy.abs(braggAngleGlitches) <= 1:
                        braggAngleGlitches = numpy.arcsin(braggAngleGlitches)*180/numpy.pi
                    else:
                        braggAngleGlitches = 0

                    if verbose: print("Bragg angle (for Glitches): %g"%braggAngleGlitches)
                    #     ;
                    #     ; print/store results
                    #     ;
                    out[0,ngood-1]=r[0]
                    out[1,ngood-1]=r[1]
                    out[2,ngood-1]=r[2]
                    out[3,ngood-1]=alpha0
                    out[4,ngood-1]=knew
                    out[5,ngood-1]=p2new/4
                    out[6,ngood-1]=theta2[0]
                    out[7,ngood-1]=theta2[1]
                    out[8,ngood-1]=theta2[2]
                    out[9,ngood-1]=theta3[0]
                    out[10,ngood-1]=theta3[1]
                    out[11,ngood-1]=theta3[2]
                    out[12,ngood-1]=lambdaIntersec[0]
                    out[13,ngood-1]=lambdaIntersec[1]
                    out[14,ngood-1]=lambdaIntersec[2]
                    out[15,ngood-1]=braggAngleUmweg
                    out[16,ngood-1]=braggAngleGlitches
                    out[17,ngood-1]=(outInt["STRUCT"]).real

                    if outInt["STRUCT"].real > fhMax:
                        fhMax = outInt["STRUCT"].real
                        fhMaxIndex = ngood - 1

    if ngood == 0:
        print("Warning: No good reflections found.")
        return None


    out = out[:,0:(ngood)].copy()
    #
    # ;
    # ; common header for scripts
    # ;
    #
    txt0 = ""
    txt0 += "#\n"
    txt0 += "# xoppy/python macro created by MARE \n"
    txt0 += "# xoppy/mare multiple diffraction  \n"
    txt0 += "#  \n"
    txt0 += "# inputs:  \n"
    # txt0 += "# crystal index: %d\n"%(CRYSTAL)
    txt0 += "# crystal name: %s  \n"%(descriptor)
    txt0 += "# Main reflection: %d %d %d\n"%(H,K,L)
    txt0 += "# Max reflections: %d %d %d\n"%(HMAX,KMAX,LMAX)
    txt0 += "# Wavelength = %g A \n"%(lambda1)
    txt0 += "# Delta Wavelength = %g A\n"%(deltalambda)
    txt0 += "# Phi = %g deg \n"%(PHI)
    txt0 += "# Delta Phi = %g deg\n"%(DELTAPHI)
    txt0 += "# Display: %d \n"%(DISPLAY)
    txt0 += "# Using reflections with fh > %d \n"%(fhEdge)
    txt0 += "# \n"
    txt0 += "# Computed parameters: \n"
    txt0 += "# Number of good reflections: %d \n"%(ngood)
    txt0 += "# M vector (corresponding to phi=0)  %d %d %d \n"%(M0[0],M0[1],M0[2])
    txt0 += "# Intensity of main reflection: %g \n"%(intMain)
    txt0 += "# Structure Factor fh of main reflection: %g \n"%(fhMain)
    txt0 += "# Reflection with maximum intensity: \n"
    txt0 += "#            number: %d \n"%(fhMaxIndex)
    txt0 += "#            miller indices: %d %d %d \n"%(
        int(out[0,fhMaxIndex]),int(out[1,fhMaxIndex]),int(out[2,fhMaxIndex])   )
    txt0 += "#            fh value: %g \n"%(fhMax)



    # ;
    # ; plot script with spaghettis
    # ;

    txt = txt0
    txt += "import numpy\n"
    txt += "import matplotlib.pylab as plt\n"
    txt += "import matplotlib.pylab as plt\n"
    txt += "fig = plt.figure()\n"
    txt += "ax = fig.add_subplot(111)\n"
    txt += "parms = {'n':500, 'xmin':-90.,'xmax':90.,'A_or_eV':0,'ymin':0.,'ymax':3.5}\n"
    txt += "alpha = numpy.linspace(parms['xmin'],parms['xmax'],parms['n'],)\n"
    txt += "ytitle='Photon energy [eV]' if parms['A_or_eV'] == 1 else 'Wavelength [A]'\n"
    txt += "plt.title('MARE-spaghetti, Main diffraction: %d %d %d %s')\n"%(H,K,L,descriptor)
    txt += "plt.xlabel('Azimuthal angle [deg]')\n"
    txt += "plt.ylabel(ytitle)\n"

    txt += "lambdas = numpy."+repr(lambdas)+"\n"
    txt += "phis = numpy."+repr(phis)+"\n"
    txt += "yy =12398.419/lambdas if parms['A_or_eV'] == 1 else lambdas\n"

    for i in range(ngood):
        txt += "# --------------------------------\n"
        txt += "# Reflection nr: %d \n"%(i+1)
        txt += "#           h           k           l      alpha0           k        p2/4         th2         th2         th2         th3         th3         th3      lambda      lambda      lambda     BrgAngU     BrgAngG          fh\n"
        txt += ("#"+"%12d"*3+"%12.6g"*15+"\n")%(tuple(out[:,i]))
        txt += "y3 = 1.0/numpy.sqrt((%g/numpy.cos((alpha-%g)*numpy.pi/180))**2 + %g)\n"%(out[4,i],out[3,i],out[5,i])
        txt += "if parms['A_or_eV'] == 1: y3=12398.419/y3\n"
        txt += "fg = plt.plot(alpha,y3)\n"
        txt += "ilabel = int(numpy.random.rand()*(parms['n']-1))\n"%()
        txt += "ax.text(alpha[ilabel],y3[ilabel],'%d %d %d',color=fg[0].get_color())\n"%(int(out[0,i]),int(out[1,i]),int(out[2,i]))

    txt += "plt.show()\n"

    list_of_scripts.append(txt)
    if verbose: print(txt)

    # ;
    # ; plot macro with umweg pattern
    # ;
    #
    if flg_u:

        txt1 = txt0
        txt1 += "import numpy\n"
        txt1 += "import matplotlib.pylab as plt\n"
        txt1 += "import matplotlib.pylab as plt\n"
        txt1 += "fig = plt.figure()\n"
        txt1 += "ax = fig.add_subplot(111)\n"
        txt1 += "parms = {'n':500, 'xmin':-90.,'xmax':90.,'A_or_eV':0,'ymin':0.,'ymax':0}\n"
        txt1 += "alpha = numpy.linspace(parms['xmin'],parms['xmax'],parms['n'],)\n"
        txt1 += "umweg = alpha*0\n"
        txt1 += "plt.title('MARE-umweg, Main diffraction: %d %d %d %s at %g A')\n"%(H,K,L,descriptor,lambda1)
        txt1 += "plt.xlabel('Azimuthal angle [deg]')\n"
        txt1 += "plt.ylabel('Approximated intensity')\n"

        for i in range(ngood):
            txt1 += "# --------------------------------\n"
            txt1 += "# Reflection nr: %d \n"%(i+1)
            txt1 += "#           h           k           l      alpha0           k        p2/4         th2         th2         th2         th3         th3         th3      lambda      lambda      lambda     BrgAngU     BrgAngG          fh\n"
            txt1 += ("#"+"%12d"*3+"%12.6g"*15+"\n")%(tuple(out[:,i]))

            intens = out[17,i]**2 *lorentz(out[15,i])
            txt1 += "theta2 = numpy.array([%g,%g,%g])\n"%(out[6,i],out[7,i],out[8,i])
            txt1 += "theta3 = numpy.array([%g,%g,%g])\n"%(out[9,i],out[10,i],out[11,i])

            if numpy.abs(out[8,i]-out[6,i]) > 1e-6:
                ymax = intens/numpy.abs(out[8,i]-out[6,i])
                txt1 += "intens = %g**2 * %g\n"%(out[17,i],lorentz(out[15,i]))
                txt1 += "umweg +=  (intens/numpy.abs(theta2[2]-theta2[0]))*numpy.exp(-(alpha-theta2[1])**2/numpy.abs(theta2[2]-theta2[0])**2) \n"
            if numpy.abs(out[11,i]-out[9,i]) > 1e-6:
                ymax = intens/numpy.abs(out[8,i]-out[6,i])
                txt1 += "intens = %g**2 * %g\n"%(out[17,i],lorentz(out[15,i]))
                txt1 += "umweg +=  (intens/numpy.abs(theta3[2]-theta3[0]))*numpy.exp(-(alpha-theta3[1])**2/numpy.abs(theta3[2]-theta3[0])**2) \n"

        txt1 += "plt.plot(alpha,umweg)\n"

        txt1 += "plt.show()\n"
        #
        list_of_scripts.append(txt1)
        if verbose: print(txt1)




    # ;
    # ; plot macro with glitches pattern
    # ;
    if flg_g:

        txt2 = txt0
        txt2 += "import numpy\n"
        txt2 += "import matplotlib.pylab as plt\n"
        txt2 += "import matplotlib.pylab as plt\n"
        txt2 += "fig = plt.figure()\n"
        txt2 += "ax = fig.add_subplot(111)\n"
        txt2 += "parms = {'n':500, 'xmin':0.5,'xmax':3.5,'A_or_eV':0,'ymin':0.,'ymax':0}\n"
        txt2 += "xmin = parms['xmin']\n"
        txt2 += "xmax = parms['xmax']\n"
        txt2 += "if parms['A_or_eV'] == 1: xmin = 12398.419/xmin\n"
        txt2 += "if parms['A_or_eV'] == 1: xmax = 12398.419/xmax\n"

        txt2 += "xx = numpy.linspace(xmin,xmax,parms['n'],)\n"
        txt2 += "yy = xx*0\n"
        txt2 += "plt.title('MARE-glitches, Main diffraction: %d %d %d %s at %g deg')\n"%(H,K,L,descriptor,phis[1])
        txt2 += "xtitle='Wavelength [A]' if parms['A_or_eV']==0 else 'Photon energy [eV]'\n"
        txt2 += "plt.xlabel(xtitle)\n"
        txt2 += "plt.ylabel('Approximated intensity')\n"

        for i in range(ngood):
            txt2 += "# --------------------------------\n"
            txt2 += "# Reflection nr: %d \n"%(i+1)
            txt2 += "#           h           k           l      alpha0           k        p2/4         th2         th2         th2         th3         th3         th3      lambda      lambda      lambda     BrgAngU     BrgAngG          fh\n"
            txt2 += ("#"+"%12d"*3+"%12.6g"*15+"\n")%(tuple(out[:,i]))
            txt2 += "lambdas = numpy.array([%g,%g,%g])\n"%(out[12,i],out[13,i],out[14,i])
            txt2 += "intens = %g**2 * %g\n"%(out[17,i],lorentz(out[16,i]))
            if numpy.abs(out[14,i]-out[12,i]) > 1e-6:
                txt2 += "yy = yy + (intens/numpy.abs(lambdas[2]-lambdas[0]))*numpy.exp(-(xx-lambdas[1])**2/numpy.abs(lambdas[2]-lambdas[0])**2)\n"

        txt2 += "plt.plot(xx,-yy)\n"

        txt2 += "plt.show()\n"

        list_of_scripts.append(txt2)
        if verbose: print(txt2)


    return(list_of_scripts)

# def xpower_calc(SOURCE=1,DUMMY1="",DUMMY2="",DUMMY3="",ENER_MIN=1000.0,ENER_MAX=50000.0,ENER_N=100,\
#                       SOURCE_FILE="?",NELEMENTS=1,\
#                       EL1_FOR="Be",EL1_FLAG=0,EL1_THI=0.5,EL1_ANG=3.0,EL1_ROU=0.0,EL1_DEN="?",\
#                       EL2_FOR="Rh",EL2_FLAG=1,EL2_THI=0.5,EL2_ANG=3.0,EL2_ROU=0.0,EL2_DEN="?",\
#                       EL3_FOR="Al",EL3_FLAG=0,EL3_THI=0.5,EL3_ANG=3.0,EL3_ROU=0.0,EL3_DEN="?",\
#                       EL4_FOR= "B",EL4_FLAG=0,EL4_THI=0.5,EL4_ANG=3.0,EL4_ROU=0.0,EL4_DEN="?",\
#                       EL5_FOR="Pt",EL5_FLAG=1,EL5_THI=0.5,EL5_ANG=3.0,EL5_ROU=0.0,EL5_DEN="?"):





if __name__ == "__main__":

    #
    # parsers (not used, we use xraylib instead)
    #

    aw1 = parse_formula("H2O")
    print(aw1)

    # tmp = write_spec_file("tmp.spec",numpy.zeros((4,100)),titles=['x','y','z','more z'])



    #
    # f1f2_calc*
    #
    for i in range(12):
        tmp = f1f2_calc(26,[10000.0,22000],F=i)
        print(">>>>>>>>>>>>>>F=%d, Z=26,f1f2_calc="%i,tmp,tmp.shape )

    for i in range(12):
        # print(">>>>>>>>>>>>>>F=%d, f1f2_calc_mix="%i, f1f2_calc_mix("SiC",[10000.0],F=i,density=3.21))
        print(">>>>>>>>>>>>>>F=%d, f1f2_calc_mix for H2O="%i, f1f2_calc_mix("H2O",[10000.0],F=i,density=1.0))




    # #
    # # cross_calc*
    # #
    #
    # for unit in range(4):
    #     for calculate in range(5):
    #         print(">>>>>>>>>>>>>>unit=%d, calculate=%d, Z=26,result="%(unit,calculate), cross_calc(26,10000.0,unit=unit,calculate=calculate))
    #
    # for i in range(4):
    #     print(">>>>>>>>>>>>>>unit=%d, H2O,result="%i, cross_calc_mix("H2O",10000.0,unit=i,density=1.0,parse_or_nist=0))
    #
    # for i in range(4):
    #     print(">>>>>>>>>>>>>>unit=%d, Acetone,result="%i, cross_calc_mix("Acetone",10000.0,unit=i,density=None,parse_or_nist=1))
    #
    # #
    # # XPOWER
    # #
    #
    # energies = numpy.linspace(1000.0,50000.0,100)
    # source = numpy.ones_like(energies)
    # fileOut = xpower_calc(energies,source,substance=["Be","Rh"],flags=[0,1],dens=["?","?"],thick=[0.5,0.0],angle=[0.0,3.0],roughness=[0.0,0.0],output_file="xpower.spec")
    #
    #
    #
    #
    # #
    # # crystal tools
    # #
    #
    # print("f0 coefficisnts for Z=30",f0_xop(30))
    #
    # print("Bragg metric tensor for Si: ")
    # print("   d-spacing for 111: ",bragg_metrictensor(5.43,5.43,5.43,90.0,90.0,90.0,HKL=[1,1,1],RETURN_REAL_SPACE=0,RETURN_VOLUME=0))
    # print("   Volume of unit cell: ",bragg_metrictensor(5.43,5.43,5.43,90.0,90.0,90.0,RETURN_VOLUME=1))
    # print("   metric tensor in real spc: ",bragg_metrictensor(5.43,5.43,5.43,90.0,90.0,90.0,RETURN_REAL_SPACE=1))
    # print("   metric tensor in reciprocal spc: ",bragg_metrictensor(5.43,5.43,5.43,90.0,90.0,90.0))
    #
    # print("LORENTZ(5.039)",lorentz(10))
    #
    #
    # dic1 = bragg_calc(descriptor="Si",hh=1,kk=1,ll=1,temper=1.0,emin=7900.0,emax=8100.0,estep=5.0,fileout="bragg-tmp.dat")
    # print("KEYS: ",dic1.keys())
    # print(dic1)
    #
    # #
    # dic2 = crystal_fh(dic1,8000.0)
    #
    # print(dic2["info"])
    # print("KEYS: ",dic2.keys())
    #
    #
    # #
    # # MARE
    # #
    # # # descriptor,H,K,L,HMAX,KMAX,LMAX,FHEDGE,DISPLAY,lambda1,deltalambda,PHI,DELTAPHI,verbose=1)
    # list_of_scripts = mare_calc("Si2",2,2,2,3,3,3,2e-8,3,1.54,0.01,-20.0,0.1)
    # for script in list_of_scripts:
    #     exec(script)



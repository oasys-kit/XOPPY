from collections import OrderedDict


def bl_components_glossary(name=None,return_list=False):

    
    if return_list:
        list1=[
               "IC_PhotonBeamPencil",
               "IC_DriftSpace",
               "IC_Lens",
               "BC_ElectronBeamGaussian",
               "BC_BendingMagnet",
               "BC_InsertionDevice",
               "BC_Slit",
               "BC_OpticalSurface",
               "BC_Attenuator",
               "BC_Mirror",
               "BC_PerfectCrystal"]
        return list1
    
 
    if name == None:
        return None
    
    a = OrderedDict()
    if name == "IC_PhotonBeamPencil":
            a["__name"] = "IC_PhotonBeam" 
            a["__title"] = "Photon pencil beam" 
            a["__labels"] = ["Minimum photon energy [eV]", "Minimum photon energy [eV]"] 
            a["__flags"] = ["True","True"] 
            a["__help"] = ["Photon energy in eV","Photon energy in eV"] 
            a["energyMin"] = 1000.0  
            a["energyMax"] = 100000.0
            return a
    elif name == "IC_DriftSpace":
            a["__name"] = "IC_DriftSpace" 
            a["__title"] = "Drift space in vacuum" 
            a["__labels"] = ["Length"]
            a["__flags"] = ["True"]
            a["__help"] = ["Drift space length"]
            a["d"] = 0.0
        
    elif name == "IC_Lens":
            a["__name"] = "IC_Lens"
            a["__title"] = "Ideal lens"
            a["__labels"] = ["Focal length in horizontal", "Focal length in vertical"]
            a["__flags"] = ["True","True"]
            a["__help"] = ["Focal length in the horizontal plane","Focal length in the vertical plane"]
            a["FH"] = 1.0 
            a["FV"] = 1.0
        
        #TODO] =  add gamma
    elif name == "BC_ElectronBeamGaussian":
            a["__name"] = "BC_ElectronBeamGaussian"
            a["__title"] = "Gaussian electron beam"
            a["__labels"] = [
                        "Electron Energy in the storage ring",
                        "Electron current intensity [A]",
                        "Orbit offset (x,x',y,y',s,delta) from where initial conditions are defined",
                        "Type of description",
                        "Spread RMS of the energy of the electrons",
                        "Horizontal emittance",
                        "Vertical emittance",
                        "Beta function (Horizontal)",
                        "Beta function (Vertical)",
                        "Alpha function (Horizontal)",
                        "Alpha function (Vertical)",
                        "Bunch length",
                        "Dispersion (Horizontal)",
                        "Dispersion (Vertical)",
                        "Dispersion Derivative (Horizontal)",
                        "Dispersion Derivative (Vertical)",
                        "Sigma matrix",
                        "M matrix"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = [" "] * len(a["__labels"])
            a["ElectronEnergy"] = 1.0
            a["ElectronCurrent"] = 0.1
            a["OrbitOffset"] = "[0.0,0.0,0.0,0.0,0.0,0.0]"
            a["InputType"] = ["0","Twiss description","Full description"]
            a["ElectronEnergySpread"] = 0.0
            a["EmittanceH"] = 0.0
            a["EmittanceV"] = 0.0
            a["BetaH"] = 0.0
            a["BetaV"] = 0.0
            a["AlphaH"] = 0.0
            a["AlphaV"] = 0.0
            a["BunchLength"] = 0.0
            a["DispersionH"] = 0.0
            a["DispersionV"] = 0.0
            a["DispersionDerivH"] = 0.0
            a["DispersionDerivV"] = 0.0
            a["SigmaMatrix"] = """[ [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0] ]"""
            a["Mmatrix"] =  """[ [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0],\
                            [0.0,0.0,0.0,0.0,0.0,0.0] ]"""
        
    elif name == "BC_BendingMagnet":
            a["__name"] = "BC_BendingMagnet"
            a["__title"] = "_Bending Magnet source"
            a["__labels"] = ["Bending magnet magnetic field [T}",
                        "File with magnetic field errors",
                        "Length (angular) of the BM [mrad]"]
            a["__flags"] = ["True","True","True"]
            a["__help"] = ["Photon energy in eV","Photon energy in eV"]
            a["MagneticField"] = 1.0
            a["MagneticFieldErrors"] = "myfile.dat"
            a["HorizontalArc"] = 1.0
        
    elif name == "BC_InsertionDevice":
            a["__name"] = "InsertionDevice"
            a["__title"] = "Insertion Device source"
            a["__labels"] = ["Type of ID",
                        "B from",
                        "ID period [m]",
                        "Number of periods",
                        "K value (Horizontal)",
                        "K value (vertical)",
                        "Phase between H and V magnets",
                        "Gap taper (Horizontal)",
                        "Gap taper (vertical)",
                        "File with harmonics",
                        "File with magnetic field"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = [" "] * len(a["__labels"])
            a["IDType"] = ["0","Wiggler","Undulator"]
            a["InputType"] = ["0","K values","B from harmonics","B from table"]
            a["PeriodID"] = 1.0
            a["N"] = 100
            a["phase"] = 0.0
            a["taperH"] = 0.0
            a["taperV"] = 0.0
            a["Bharmonics"] = "myfile.dat"
            a["Btable"] = "myfile.dat"
        
    elif name == "BC_Slit":
            a["__name"] = "BC_Slit"
            a["__title"] = "Slit or aperture"
            a["__labels"] = ["Center (Horizontal)",
                        "Center (Vertical)",
                        "Shape",
                        "aperture of beam stop",
                        "gap/obstruction (Horizontal) [m]",
                        "gap/obstruction (vertical) [m]",
                        "polygone coordinates (Horizontal)",
                        "polygone coordinates (Vertical)"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = [" "] * len(a["__labels"])
            a["centerH"] = 0.0
            a["centerV"] = 0.0
            a["shape"] = ["0","None (fully opened)","rectangular","elliptical","free form (polygon"]
            a["Stop"] = ["0","Aperture/slit","beam stop"]
            a["gapH"] = 1.0
            a["gapV"] = 1.0
            a["coorH"] = 0.0
            a["coorV"] = 0.0
        
    elif name == "BC_OpticalSurface":
            a["__name"] = "BC_OpticalSurface"
            a["__title"] = "Optical Surface (form)"
            a["__labels"] = ["Limits",
                        "length [m]",
                        "Width [m]",
                        "shape",
                        "coeff",
                        "Geometry"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = [" "] * len(a["__labels"])
            a["limits"] = ["0","Infinite surface","rectangle","ellipse","free form"]
            a["length"] = 1.0
            a["width"] = 1.0
            a["oeshape"] = ["0","Plane","Conic coefficients","Sphere (conic)","Ellipsoid (conic)","paraboloid (conic)","hyperboloid (conic)","Toroid","Free (mesh)","Free (polynomial"]
            a["conicCoeff"] = "[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]"
            a["geometry"] = ["0","reflecting (e.g. mirrors)","transmitting (e.g., lenses, Laue crystals)","both (e.g., diamond crystals, beamsplitters)"]
        
    elif name == "BC_Attenuator":
            a["__name"] = "BC_Attenuator"
            a["__title"] = "BC Attenuator"
            a["__labels"] = ["material",
                        "thickness [m]",
                        "material density [g/cm^3]"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = ["String describing the material (e.g., Cu, H2O, etc)."
                      "Attenuator thickness",
                      "material thickness"]
            a["material"] = "Si"
            a["thickness"] = 1.0e-3
            a["density"] = 1.0
        
    elif name == "BC_Mirror":
            a["__name"] = "BC_Mirror"
            a["__title"] = "Mirror"
            a["__labels"] = ["coating material",
                        "coating thickness",
                        "coating density"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = ["String describing the coating material (e.g., Cu, B4C, etc).",
                      "Coating thickness [m]",
                      "Coating density [g/cm^3]"]
            a["coating"] = "Rh"
            a["thickness"] = 1e-6
            a["density"] = 10.0
        
    elif name == "BC_PerfectCrystal":
            a["__name"] = "BC_PerfectCrystal"
            a["__title"] = "Perfect Crystal"
            a["__labels"] = ["material",
                        "thickness",
                        "crystallographic cell parameters",
                        "number of atoms in unit cell",
                        "atomic number of atoms in unic cell",
                        "coordinates of atoms in crystallographic cell",
                        "occupancy",
                        "temperature at which unit cell is given [K]",
                        "Crystal temperature [K]",
                        "Miller indices",
                        "Asymmetry angle [deg]"]
            a["__flags"] = ["True"]* len(a["__labels"])
            a["__help"] = ["String describing the coating material (e.g., Si, Quartz, etc).",
                      "Crystal thickness [m]",
                      "Crystallographic cell parameters a,b,c,alpha,beta,gamma [A,deg]",
                      "Number of atoms in unit cell",
                      "Atomic number of atoms in unit cell",
                      "Coordinates of atoms in crystallographic cell",
                      "Occupancy coeff of atoms in unit cell",
                      "Temperature at which unit cell is given [K]",
                      "Crystal temperature [K]",
                      "Miller indices of selected reflection",
                      "Asymmetry angle [deg]"]
            a["material"] = "Si"
            a["thickness"] = 100e-6
            a["cell"] = "[5.430700,5.430700,5.430700,90,90,90]"
            a["Natoms"] = 8
            a["Zatoms"] = "[14,14,14,14,14,14,14,14]"
            #a["XYZ"] = "[0.000000,0.000000,0.000000] "
            a["XYZ"] = """[ [0.000000,0.000000,0.000000],\
                       [0.000000,0.500000,0.500000],\
                       [0.500000,0.000000,0.500000],\
                       [0.500000,0.500000,0.000000],\
                       [0.250000,0.250000,0.250000],\
                       [0.250000,0.750000,0.750000],\
                       [0.750000,0.250000,0.750000],\
                       [0.750000,0.750000,0.250000] ]"""
            a["occupancy"] = "[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]"
            a["Temperature0"] = 300.0
            a["Temperature"] = 330.0
            a["Miller"] = "[1,1,1]"
            a["AsymmetryAngle"] = 0.0
        
    #TODO] = 
    # add BC_Multilayer, BC_LensSingle, Compound elements...
        
    #
    # list all non-empty keywords
    #
    return a

if __name__ == "__main__":
    list1 = bl_components_glossary(return_list=True)
    
    for k in list1:
        print ("-----------------------%s ------------------------------"%(k))
        tmp = bl_components_glossary(k)
        for i,j in tmp.items():
            #print ("**%s** " % (i[:2]) )
            #if (i[:2] != "__"):
                print ("%s = %s" % (i,j))
        print ("   ")
    

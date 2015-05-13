
#
#----------------------------  IMPORT ------------------------------------------
#

import os
from collections import OrderedDict
import json
from srundplug import getBeamline


def writeJson(bl,file_name='tmp.json',titles=None,flags=None):

    bl2 = bl

    BL2 = OrderedDict()
    list_variable_names = []
    print ("-----------------------------------------------------")
    for indx,key in enumerate(bl2):
        print (">>>>>>>>>>> %s = %s ; %s " % (key,bl2[key],titles[indx]) )
        list_variable_names.append(key.upper())
        BL2[key.upper()] = bl2[key]
    print ("-----------------------------------------------------")
    print ("-----------------------------------------------------")

    json_string = json.dumps(BL2)
    f = open(file_name,'w')
    f.write(json_string)
    f.close()
    print(">>> File %s written to disk"%(file_name))



    f = open(file_name+'.ext','w')
    json.dump(titles,f)

    f.write("\n")
    json.dump(flags,f)

    f.write("\n")
    json.dump(list_variable_names,f)

    f.write("\n")
    json.dump(flags,f)

    f.close()
    print(">>> File %s written to disk"%(file_name+'.ext'))
    
    
#
#----------------------------  MAIN CODE -------------------------------------
#

if __name__ == '__main__':

    bl0 = getBeamline("ESRF_HB")

    titles0 = []
    titles0.append("Electron Energy [GeV]")
    titles0.append("Electron Energy Spread")
    titles0.append("Electron Current [A]")
    titles0.append("Electron Beam Size H [m]")
    titles0.append("Electron Beam Size V [m]")
    titles0.append("Electron Beam Divergence H [rad]")
    titles0.append("Electron Beam Divergence V [rad]")
    titles0.append("Period ID [m]")
    titles0.append("Number of periods")
    titles0.append("Kv [undulator K value vertical field]")
    titles0.append("Distance to slit [m]")
    titles0.append("Slit gap H [m]")
    titles0.append("Slit gap V [m]")

    #
    # undulator_flux to compute the undulator flux
    #
    bl = bl0.copy()
    titles = titles0.copy()

    bl['photonEnergyMin'] = 3000.0
    bl['photonEnergyMax'] = 55000.0
    bl['photonEnergyPoints'] = 500
    bl['method'] = ['0','US','URGENT','SRW']

    titles.append("photon Energy Min [eV]")
    titles.append("photon Energy Max [eV]")
    titles.append("photon Energy Points")
    titles.append("calculation code")

    flags = []
    for i in range(len(titles)): 
        flags.append('True')
    flags[1] = "self.METHOD != 1" # no energy spread for URGENT

    tmp = writeJson(bl,file_name='undulator_flux.json',titles=titles,flags=flags)

    #
    # undulator_power_density to compute the undulator power density
    #
    bl = bl0.copy()
    bl['gapH'] = 3.0e-3
    bl['gapV'] = 3.0e-3
    titles = titles0.copy()

    bl['hSlitPoints'] = 41
    bl['vSlitPoints'] = 41
    bl['method'] = ['0','US','URGENT','SRW']

    titles.append("Number of slit mesh points in H")
    titles.append("Number of slit mesh points in V")
    titles.append("calculation code")

    flags = []
    for i in range(len(titles)): 
        flags.append('True')
    flags[1] = "self.METHOD != 1" # no energy spread for URGENT

    tmp = writeJson(bl,file_name='undulator_power_density.json',titles=titles,flags=flags)



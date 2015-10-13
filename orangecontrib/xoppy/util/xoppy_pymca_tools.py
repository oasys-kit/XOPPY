# import PyMca5

from PyMca5.PyMcaIO import specfilewrapper as specfile

def xoppy_loadspec(fileName,verbose=0,index=None):
    """
    gets the data block of the last spec scan
    :param fileName:
    :param verbose:
    :return:
    """

    sf = specfile.Specfile(fileName)

    if verbose:
        print("Number of scans found %d"%(sf.scanno()))
        print(sf.list())
        print(type(sf.list()))

    if index == None: #go trought all scane
        for i in range(sf.scanno()):
            s1 = sf.select(str(i+1))
            if verbose:
                print("\nscan number %d, number of columns: %d "%(i+1,s1.cols()))
                print("  %s "%(s1.command()))

            h = s1.header("")
            for j in range(len(h)):
                if verbose: print("           %s"%h[j])
            if verbose: print("  Columns: " ,s1.alllabels())
            out = s1.data()
            print("data shape" ",out.shape")
    else:
        s1 = sf.select(str(index+1))
        out = s1.data()


    return out

if __name__ == "__main__":
    #out = loadspec("undulator_power_density.spec")

    out = xoppy_loadspec("undulator_power_density.spec",index=1)
    print("returned data shape: ",out.shape)

# print(s1.data())
# print(s1.alllabels())






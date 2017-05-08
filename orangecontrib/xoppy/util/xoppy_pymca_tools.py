# todo: remove this file or move function elsewhere it addafter being sure is not used anywhere

from silx.io.specfile import SpecFile,Scan

def xoppy_loadspec(fileName,verbose=1,index=None):
    """
    gets the data block of the last spec scan
    :param fileName:
    :param verbose:
    :return:
    """


    sf = SpecFile(fileName)

    if verbose:
        print("Number of scans found %d"%(len(sf)))
        print(sf.list())
        print(type(sf.list()))

    if index == None: #go trought all scane
        for index in range(len(sf)):
            s1 = sf[index]
            if verbose:
                print("\ndata shape: ",(s1.data.shape))

            h = s1.header
            for j in range(len(h)):
                if verbose: print("           %s"%h[j])

    else:
        s1 = sf[index]


    return s1.data

if __name__ == "__main__":
    #out = loadspec("undulator_power_density.spec")

    out = xoppy_loadspec("/users/srio/Oasys/undulator_power_density.spec",index=1)
    print("returned data shape: ",out.shape)

# print(s1.data())
# print(s1.alllabels())






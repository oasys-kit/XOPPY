# import PyMca5

from PyMca5.PyMcaIO import specfilewrapper as specfile


sf = specfile.Specfile("undulator_power_density.spec")

print("Number of scans found %d"%(sf.scanno()))

print(sf.list())

print(type(sf.list()))


for i in range(sf.scanno()):


    s1 = sf.select(str(i+1))
    print("scan number %d, number of columns: %d "%(i+1,s1.cols()))
    print("  %s "%(s1.command()))

    h = s1.header("")
    for j in range(len(h)):
        print("           %s"%h[j])

    print("  Columns: " ,s1.alllabels())



# print(s1.data())
# print(s1.alllabels())






from glossary import bl_components_glossary
from tabulate import tabulate



if __name__ == "__main__":

    list1 = bl_components_glossary(return_list=True)
    
    file1 = open("glossary.tex","w")
    print ("\documentclass{article}",file=file1)
    print ("\\begin{document}",file=file1)
    for k in list1:
        print ("%s-----------------------%s ------------------------------"%('%',k),file=file1)
        print ("\\section{%s}"%(k.replace("_","\_")),file=file1)
        print ("\\begin{tabular}{lr}",file=file1)
        print ("Name & Default value \\".__repr__().replace("'",""),file=file1)
        print ("\hline",file=file1)
        
        tmp = bl_components_glossary(k)
        b = {}
        for i,j in tmp.items():
            if (i[:2] != "__"):
                print ('%s & %s \\'.__repr__().replace("'","") % (i,j),file=file1)
                b[i] = j
        print ("   ",file=file1)
        print ("\end{tabular}",file=file1)
        print ("\n\n",file=file1)
        #print (b)
        #print (tabulate(b, headers=tmp["__labels"], tablefmt="latex"))
        #temp = []
        #dict_list = []
        #for key, value in dict.iteritems():
        #    temp = [key,value]
        #    dictlist.append(temp)
        #print(dict_list)
    print ("\end{document}",file=file1)
    if file1 != None:
        file1.close()

    



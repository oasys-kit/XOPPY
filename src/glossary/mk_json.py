from glossary import bl_components_glossary
import json



if __name__ == "__main__":

    list1 = bl_components_glossary(return_list=True)
    
    for k in list1:
        print ("-----------------------%s ------------------------------"%(k))
        
        tmp = bl_components_glossary(k)
        for i,j in tmp.items():
            #print ("**%s** " % (i[:2]) )
            if (i[:2] != "__"):
                print ("%s = %s" % (i,j))
        print ("   ")

        filename = k+".json"
        with open(filename, mode='w') as f: 
            json.dump(tmp, f, indent=2)
            print("Dumped file: %s \n"%(filename))
    



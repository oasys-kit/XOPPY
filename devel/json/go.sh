#!/bin/sh

#python version
MYPYTHON="python3"
echo "Using python: $MYPYTHON"

# initialize
cp ./../idl/go_all.txt  .
cp ./../idl/*.json*  .
rm xoppy_calc_template.py
#
# add to the list the json files modified or created by hand
#
echo "bm" >> go_all.txt
#echo "xsh_und_gauss" >> go_all.txt
#echo "xshwig" >> go_all.txt


# clean
for i in `cat go_all.txt`
do
   echo " "
   echo "===============  Processing application: $i"
   #clean
   rm $i.py
   #make
   $MYPYTHON create_widget_srio.py $i.json

   #install goes in a separate script
done


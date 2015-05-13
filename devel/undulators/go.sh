#!/bin/sh

#python version
MYPYTHON="python3"
echo "Using python: $MYPYTHON"

# initialize
rm go_all.txt
rm xoppy_calc_template.py
#
# add to the list the json files modified or created by hand
#
echo "undulator_flux" >> go_all.txt
echo "undulator_power_density" >> go_all.txt

$MYPYTHON make_json.py

# clean
for i in `cat go_all.txt`
do
   echo " "
   echo "===============  Processing application: $i"
   #clean
   rm $i.py
   $MYPYTHON create_widget_srio.py $i.json

done

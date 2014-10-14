#!/bin/sh

#python version
MYPYTHON="python3"
echo "Using python: $MYPYTHON"

# initialize
cp ./../idl/go_all.txt  .
cp ./../idl/*.json*  .
rm xoppy_calc_template.py


# clean
for i in `cat go_all.txt`
do
   echo " "
   echo "===============  Processing application: $i"
   #clean
   rm $i.py
   #make
   #$MYPYTHON create_widget_srio.py-old1 $i.json
   $MYPYTHON create_widget_srio.py $i.json

   #install
   mv $i.py ../../orangecontrib/xoppy/widgets/$i.py
   echo "file installed: "
   ls -l ../../orangecontrib/xoppy/widgets/$i.py
done

#clean *json*
#/bin/rm *json*

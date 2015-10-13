#!/bin/sh


# clean
for i in `cat go_all.txt`
do
   echo " "
   echo "===============  Installing application: $i"
   cp $i.py ../../orangecontrib/xoppy/widgets/xoppy/$i.py
   echo "file installed: "
   ls -l ../../orangecontrib/xoppy/widgets/xoppy/$i.py
done

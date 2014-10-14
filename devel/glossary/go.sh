#!/bin/sh

#
# create json files
#
rm *.json
python3 mk_json.py

#
#create latex table 
#
python3 mk_latex
latex glossary.tex
okular glossary.dvi &

#
# create widget code *.py)
#
for i in `ls *.json`
do
  echo "loop index: $i"
  python3 create_widget_glossary.py $i
  echo " ----------: ${i%.json}.py"
done

#
#run widgets
#
for i in `ls *.json`
do
  echo "starting file: ${i%.json}.py"
  python3 ${i%.json}.py
done

================================================
================================================
____  ___________ _________________________.___.
\   \/  /\_____  \\______   \______   \__  |   |
 \     /  /   |   \|     ___/|     ___//   |   |
 /     \ /    |    \    |    |    |    \____   |
/___/\  \\_______  /____|    |____|    / ______|
      \_/        \/                    \/       
================================================
================================================

This is the working project for XOPPY (XOP under python+orange3)

For XOP see: http://ftp.esrf.eu/pub/scisoft/xop2.3/
             http://www.esrf.fr/Instrumentation/software/data-analysis/xop2.3

For orange3 see: https://github.com/biolab/orange3

1) install orange3 
2) modify .../orange3/Orange/widgets/widgets.py as in widget.py in this directory
3) copy XOPPY directory in .../orange3/Orange/ (or elsewhere)
4) add xoppy entry in Orange/widgets/__init__.py, like in the file
   in_Orange_widgets___init__.py
5) start python -m Orange.canvas


Notes
-installing orange3 in ubuntu 14.04 gave a problem when installing the scikit-learn package. It can be installed from sources using: 
pip install git+https://github.com/scikit-learn/scikit-learn.git

-xoppy working directory is Orange/XOPPY/tmp

srio@esrf.eu 20140423  (Cervantes death anniversary)
srio@esrf.eu 20140521  changes after visit to Ljubljana

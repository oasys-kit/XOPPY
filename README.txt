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
2) modify .../orange3/Orange/widgets/widgets.py to add "show_at" method (as in widget.py in this directory)
3) copy XOPPY directory in .../orange3/Orange/
4) make a soft link .../orange3/Orange/XOPPY/widgets .../orange3/Orange/widgets/xoppy: 
   cd ~/orange3/Orange/widgets
   ln -s ../XOPPY/widgets/ xoppy
5) add xoppy entry in Orange/widgets/__init__.py, e.g.:
    pkgs = ["Orange.widgets.xoppy",
            "Orange.widgets.data",
            "Orange.widgets.visualize",
            "Orange.widgets.classify",
            "Orange.widgets.evaluate"]
6) Install ./tools/*.py somewhere available by python, e.g.:
   cd ~/orange3/Orange/XOPPY/tools
   cp srfunc.py ~/orange3env/lib/python3.4/
   cp xoppy_calc.py ~/orange3env/lib/python3.4/
7) start python -m Orange.canvas


Notes
-installing orange3 in ubuntu 14.04 gave a problem when installing the scikit-learn package. It can be installed from sources using: 
pip install git+https://github.com/scikit-learn/scikit-learn.git

-xoppy working directory is Orange/xoppy/tmp

srio@esrf.eu 20140423  (Cervantes death anniversary)

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
2) modify Orange/widgets/widgets.py to add "show_at" method
3) copy xoppy directory in Orange/
4) make a soft link Orange/xoppy/widgets Orange/widgets/xoppy
5) add xoppy entry in Orange/widgets/__init__.py
6) Install ./tools/*.py somewhere available by python
7) start python -m Orange.canvas


Notes
xoppy working directory is Orange/xoppy/tmp

srio@esrf.eu 20140423  (Cervantes death anniversary)

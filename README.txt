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

This is the WORKING project for XOPPY (XOP under python3+orange3)

For XOP see: http://ftp.esrf.eu/pub/scisoft/xop2.3/
             http://www.esrf.fr/Instrumentation/software/data-analysis/xop2.3

For orange3 see: https://github.com/biolab/orange3

Installation instructions (tentative, under development)

1) Recommended (not mandatory) to use the following folder structure:
   $HOME/Oasys 
   $HOME/Oasys/OASYS1  orange3 fork, get from: 
     git clone http://github.com/lucarebuffi/OASYS1
   $HOME/Oasys/Orange-XOPPY XOPPY package , get from: 
     git clone http://github.com/srio/Orange-XOPPY
   $HOME/Oasys/OrangeRun create this directory to put the running time files
                         Set the working directory to this folder.

2) install packages that orange3 needs. See them in: 
   https://github.com/biolab/orange3/wiki
   Notes: 
     - I prefer not using the virtual environment when working in my station
     - always use python3 and pip3 (instead of python and pip)
     - do not install orange3. See next point.

3) install OASYS1 (a fork of orange3) from: 
    - https://github.com/lucarebuffi/OASYS1

    Once installed (python3 setup.py build ; sudo python3 setup.py install)
    you should be able to open python3 and "import Orange" without errors. 

    From my experience, I needed to install manually bottlechest 
    (https://github.com/biolab/bottlechest) and sklean
    (pip3 install -U numpy scipy scikit-learn)

4) install XOPPY as:
   method 1 (developer):
       cd $HOME/Oasys/Orange-XOPPY
       sudo python3 setup.py develop
   method 2 (user):
       From the Oasys (Orange) window, got to "Options", "Add-ons" and 
       check XOPPY. Quit Oasys.

5) start XOPPY as:
   python3 -m Orange.canvas
   at this point you should see in the menu panel (on your left) the XOPPY
   menus.



Notes
-installing orange3 in ubuntu 14.04 gave a problem when installing the scikit-learn package. It can be installed from sources using: 
pip install git+https://github.com/scikit-learn/scikit-learn.git


srio@esrf.eu 20140423  (Cervantes death anniversary)
srio@esrf.eu 20140521  changes after visit to Ljubljana
srio@esrf.eu 20141022  changes after Luca's visit. Oasys introduced.
srio@esrf.eu 20150513  New applications in xoppy

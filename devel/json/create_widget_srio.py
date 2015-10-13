import sys
import os


def read_json(json_name):
    json_text = open(json_name).read()
    json_dict = eval(json_text)
    json = sorted(json_dict.items(),
                  key=lambda x: json_text.index('"{}"'.format(x[0])))
    #print(json)
    #json_lowercase = dict((k.lower(), v) for k, v in json.iteritems())
    json_lowercase = json
    return json_lowercase


#def create_flags(json):
#    flags = '["True", "True", "True", "self.RB_CHOICE == 0", "self.RB_CHOICE == 1"]'
#    return flags
#
#def create_labels(json):
#    labels = '["Electron energy [GeV]","Electron current [A]","B from","Magnetic radius [m]","Magnetic field [T]"]'
#    return labels

def create_settings(json):
    settings = ""
    for name, value in json:
        if isinstance(value, str):
            settings += '    {} = Setting("{}")\n'.format(name, value)
        elif isinstance(value, list):
            settings += '    {} = Setting({})\n'.format(name, value[0])
        else:
            settings += '    {} = Setting({})\n'.format(name, value)
    return settings

def create_calc_args_default(json):
    settings = ""
    i = -1
    for name, value in json:
        i += 1
        if isinstance(value, str):
            settings += '{}="{}"'.format(name, value).rstrip('\n')
        elif isinstance(value, list):
            settings += '{}={}'.format(name, value[0]).rstrip('\n')
        else:
            settings += '{}={}\n'.format(name, value).rstrip('\n')
        if i < (len(json)-1):
           settings += ','
    return settings

def create_calc_args(json):
    calc_args = ""
    i = -1
    for name, value in json:
        i += 1
        calc_args += '{}=self.{}'.format(name, name)
        if i < (len(json)-1):
           calc_args += ','
    return calc_args


def create_controls(json):
    controls = ""
    controls += '        box0 = gui.widgetBox(self.controlArea, " ",orientation="horizontal") \n'
    controls += '        #widget buttons: compute, set defaults, help\n'
    controls += '        gui.button(box0, self, "Compute", callback=self.compute)\n'
    controls += '        gui.button(box0, self, "Defaults", callback=self.defaults)\n'
    controls += '        gui.button(box0, self, "Help", callback=self.help1)\n'
    controls += '        self.process_showers()\n'


    controls += '        box = gui.widgetBox(self.controlArea, " ",orientation="vertical") \n'
    idx = -1
    #controls += '        box = gui.widgetBox(self.controlArea, "Set parameters") \n'
    #controls += '        box = gui.widgetBox(self.controlArea, " ") \n'
    controls += '        \n'
    controls += '        \n'
    controls += '        idx = -1 \n'


    for name, value in json:
        idx += 1
        controls += '        \n'
        controls += '        #widget index '+str(idx)+' \n'
        controls += '        idx += 1 \n'
        controls += '        box1 = gui.widgetBox(box) \n'
        if isinstance(value, list):
            controls += list_template.format(name=name,values=str(value[1:]))
        else:
            controls += line_edit_templates[type(value)].format(name=name)


        controls += '        self.show_at(self.unitFlags()[idx], box1) \n'


    return controls


def main():
    json_name = sys.argv[1]
    base = os.path.splitext(json_name)[0]
    py_name =  base + ".py"
    calc_name = "xoppy_calc_template.py"
    if os.path.exists(py_name):
        print("file overwritten: "+py_name+"\n")
    else:
        print("file written: "+py_name+"\n")
    if os.path.exists(calc_name):
        print("appended to file: "+calc_name+"\n")

    json = read_json(json_name)
    widget_name = base
    widget_class_name = widget_id_name = base.replace(" ", "")
    settings = create_settings(json)
    controls = create_controls(json)
    calc_args = create_calc_args(json)
    calc_args_default = create_calc_args_default(json)

    f = open(json_name+'.ext')
    lines = f.readlines()
    f.close()
    #print(lines[0])
    #flags = create_flags(json)
    #labels = create_labels(json)
    labels = lines[0] #["Electron energy [GeV]","Electron current [A]","B from","Magnetic radius [m]","Magnetic field [T]"]
    flags = lines[1] #["True", "True", "True", "self.RB_CHOICE == 0", "self.RB_CHOICE == 1"]
    mynames = lines[2]
    flagsold = lines[3]
    open(py_name, "wt").write(widget_template.format_map(vars()))
    #open(py_name, "wt").write(widget_template)
    open(calc_name, "a").write(calc_template.format_map(vars()))


control_template = """        gui.{}(box1, self, "{{name}}",
                     label=self.unitLabels()[idx], addSpace=True"""


str_template = control_template.format("lineEdit") + ")\n"

int_template = control_template.format("lineEdit") + """,
                    valueType=int, validator=QIntValidator())
"""

float_template = control_template.format("lineEdit") + """,
                    valueType=float, validator=QDoubleValidator())
"""

line_edit_templates = {str: str_template, int: int_template,
                       float: float_template}

list_template = control_template.format("comboBox") + """,
                    items={values},
                    valueType=int, orientation="horizontal")
"""



widget_template = """import sys
import numpy as np
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from PyMca5.PyMcaIO import specfilewrapper as specfile
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

try:
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_doc
except ImportError:
    print("Error importing: xoppy_doc")
    raise

try:
    from orangecontrib.xoppy.util.xoppy_calc import xoppy_calc_{widget_class_name}
except ImportError:
    print("compute pressed.")
    print("Error importing: xoppy_calc_{widget_class_name}")
    raise

class OW{widget_class_name}(widget.OWWidget):
    name = "{widget_name}"
    id = "orange.widgets.data{widget_id_name}"
    description = "xoppy application to compute..."
    icon = "icons/xoppy_{widget_class_name}.png"
    author = "create_widget.py"
    maintainer_email = "srio@esrf.eu"
    priority = 10
    category = ""
    keywords = ["xoppy", "{widget_class_name}"]
    outputs = [{{"name": "xoppy_data",
                "type": np.ndarray,
                "doc": ""}},
               {{"name": "xoppy_specfile",
                "type": str,
                "doc": ""}}]

    #inputs = [{{"name": "Name",
    #           "type": type,
    #           "handler": None,
    #           "doc": ""}}]

    want_main_area = False

{settings}

    def __init__(self):
        super().__init__()

{controls}
        gui.rubber(self.controlArea)

    def unitLabels(self):
         return {labels}

    def unitFlags(self):
         return {flags}

    #def unitNames(self):
    #     return {mynames}

    def compute(self):
        fileName = xoppy_calc_{widget_class_name}({calc_args})
        #send specfile

        if fileName == None:
            print("Nothing to send")
        else:
            self.send("xoppy_specfile",fileName)
            sf = specfile.Specfile(fileName)
            if sf.scanno() == 1:
                #load spec file with one scan, # is comment
                print("Loading file:  ",fileName)
                out = np.loadtxt(fileName)
                print("data shape: ",out.shape)
                #get labels
                txt = open(fileName).readlines()
                tmp = [ line.find("#L") for line in txt]
                itmp = np.where(np.array(tmp) != (-1))
                labels = txt[itmp[0]].replace("#L ","").split("  ")
                print("data labels: ",labels)
                self.send("xoppy_data",out)
            else:
                print("File %s contains %d scans. Cannot send it as xoppy_table"%(fileName,sf.scanno()))

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        xoppy_doc('{widget_class_name}')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OW{widget_class_name}()
    w.show()
    app.exec()
    w.saveSettings()
"""
calc_template = """


def xoppy_calc_{widget_class_name}({calc_args_default}):
    print("Inside xoppy_calc_{widget_class_name}. ")
    return(None)
"""

main()


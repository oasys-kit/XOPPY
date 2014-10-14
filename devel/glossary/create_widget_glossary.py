import sys
import os
import re


#def read_json(json_name):
#    json_text = open(json_name).read()
#    json_dict = eval(json_text)
#    json = sorted(json_dict.items(),
#                  key=lambda x: json_text.index('"{}"'.format(x[0])))
#    #print(json)
#    #json_lowercase = dict((k.lower(), v) for k, v in json.iteritems())
#    json_lowercase = json
#    return json_lowercase



re_dict_entry = re.compile(r'"(?P<name>.*?)"\s*:')

def read_json(json_name):
    json_text = open(json_name).read()
    key_order = [mo.group('name') for mo in re_dict_entry.finditer(json_text)]
    json_dict = eval(json_text)
    json = sorted(json_dict.items(), key=lambda x: key_order.index(x[0]))
    #print(json)
    #json_lowercase = dict((k.lower(), v) for k, v in json.iteritems())
    json_lowercase = json
    return json_lowercase

if __name__ == "__main__":
    a = read_json("IC_Lens.json")
    for i,j in a:
        print("--- %s   %s   "%(i,j))
    b = read_json("BC_PerfectCrystal.json")
    for i,j in b:
        print("--- %s   %s   "%(i,j))



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
        if name[:2] != "__":
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
        if name[:2] != "__":
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
    calc_name = "bl_glossary_template.py"
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

    dir(json)
   
    labels = None
    flags = None
    name = None
    kk = 0
    for i,j in json:
        if i == "__labels": 
            labels = j
            print(">   %d labels found. \n "%(len(labels)))
        elif i == "__flags": 
            flags = j
            print(">   %d flags found. \n "%(len(flags)))
        elif i == "__name": 
            name = j
            print(">   found name %s: \n "%(name))
        else:
            if i[:2] != "__": 
                kk += 1
                print(">   found entry number %d:  %s \n "%(kk,i))
    print(">   found entries (without __) %d: \n "%(kk))

    open(py_name, "wt").write(widget_template.format_map(vars()))
    #open(calc_name, "a").write(calc_template.format_map(vars()))


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
                    valueType=list, orientation="horizontal")
"""



widget_template = """import sys
from PyQt4.QtGui import QIntValidator, QDoubleValidator, QApplication, QSizePolicy
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.data import Table, Domain, ContinuousVariable
import numpy as np

#try:
#    from ..tools.xoppy_calc import xoppy_doc
#except ImportError:
#    print("Error importing: xoppy_doc")
#    raise

#try:
#    from ..tools.xoppy_calc import xoppy_calc_{widget_class_name}
#except ImportError:
#    print("compute pressed.")
#    print("Error importing: xoppy_calc_{widget_class_name}")
#    raise

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
    outputs = [#{{"name": "xoppy_data",
               # "type": np.ndarray,
               # "doc": ""}},
               {{"name": "xoppy_table",
                "type": Table,
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
        self.process_showers()
        gui.rubber(self.controlArea)

    def unitLabels(self):
         return {labels}

    def unitFlags(self):
         return {flags}


    def compute(self):
        print("compute executed.")
        #table = Table.from_numpy(domain, out)
        #self.send("xoppy_table",table)

    def defaults(self):
         self.resetSettings()
         self.compute()
         return

    def help1(self):
        print("help pressed.")
        #xoppy_doc('{widget_class_name}')





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


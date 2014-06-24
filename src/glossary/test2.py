import re
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


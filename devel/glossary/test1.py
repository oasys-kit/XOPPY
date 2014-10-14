def read_json(json_name):
    json_text = open(json_name).read()
    json_dict = eval(json_text)
    json = sorted(json_dict.items(),
                  key=lambda x: json_text.index('"{}"'.format(x[0])))
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


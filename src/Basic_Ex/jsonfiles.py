import json
with open("ex.json") as json_file:
    content=json_file.read()
    print(json.loads(content))

my_dict= {"jan":1, "feb":2}

my_js = json.dumps(my_dict)

with open("ex.json", "w") as json_file2:
    json_file2.write(my_js)
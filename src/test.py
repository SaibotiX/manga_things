import json

infile = open("grow.json")

data = json.load(infile)

nested_dict = data[0]

last_key = list(nested_dict.keys())[-1]
last_value = nested_dict[last_key]

new_item = {last_key : last_value}

keys = list(nested_dict.keys())

for i in keys:
    if i == "test2":
        print(i)












#print(data)
#
#print()
#
#print(json.dumps(nested_dict, indent=4))
#
#print()
#
#print(last_key)
#
#print()
#
#print(last_value)
#
#print()
#
#print(new_item)

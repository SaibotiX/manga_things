import json
import random

raw = open("manga.json")

inp = json.load(raw)

nested_dict = list(inp[0])

for i in range(20):
    random_inp = random.choice(nested_dict)
    print(json.dumps(random_inp, indent=4, ensure_ascii=False))

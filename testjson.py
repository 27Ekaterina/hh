import json

with open('hhparsing.json', 'r') as f:
    result = json.load(f)
    print(result)
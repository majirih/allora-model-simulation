import json
with open("credentials.json") as f:
    print(json.dumps(json.load(f)))

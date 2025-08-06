import json

with open("credentials.json", "r") as f:
    creds = json.load(f)

escaped = json.dumps(creds).replace("\\n", "\\\\n")
print(escaped)

import json
import os

creds_file = os.path.abspath(os.path.join('..', "credentials/test.json"))

a_dict = {'new_key': 'new_value'}

with open(creds_file) as f:
    data = json.load(f)

data.update(a_dict)

with open(creds_file, 'w') as f:
    json.dump(data, f)

json_data = {"AccessToken": 10, "key2": 23}

if "AccessToken" in json_data:
    print("this will execute")

if "nonexistent key" in json_data:
    print("this will not")
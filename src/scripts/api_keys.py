import requests

url = "https://www.googleapis.com/drive/v3/files"

querystring = {"alt":"media","export":"download"}

headers = {
    'Authorization': "Bearer TOKEN",
    'Host': "www.googleapis.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(vars(response))
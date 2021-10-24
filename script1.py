import json
import http.client

conn = http.client.HTTPSConnection("api.tagmatch.io")

file = open('Taglist.txt', 'r')

lines = file.readlines()
file.close()

total_list = []

# remove trailing new spaces
for line in lines:
    line = line.strip("\n")
    payload = "{\"query\":\"mutation addNewTag ($input: NewTag!) {\\n    addNewTag (input: $input) {\\n        Name\\n        Weight\\n    }\\n}\",\"variables\":{\"input\":{\"Name\":\"" + line +"\",\"Weight\":1}}}"
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/query", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

out_file = open("test1.json", "w")
json.dump(total_list, out_file, indent = 4, sort_keys= False)
out_file.close()
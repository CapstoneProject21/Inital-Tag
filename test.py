import json
#import http.client

#conn = http.client.HTTPSConnection("staging.api.tagmatch.io")
main_lis = []
file = open('tags.txt', 'r')
lines = file.readlines()
file.close()

for line in lines:
    lis = line.split(",")
    child_lis = []
    parent = lis[0].strip()
    if len(lis) > 1:
        for i in lis[1:]:
            child_lis.append(i.strip())
    #payload = "{\"query\":\"mutation addNewTag ($input: NewTag!) {\\n    addNewTag (input: $input) {\\n        Name\\n       Weight\\n        }\\n}\",\"variables\":{\"input\":{\"Name\":\"" + line +"\",\"Weight\":1}}}"
    temp_dict = {}
    temp_dict["Name"] = parent
    temp_dict["Weight"] = 1
    temp_dict["Opposite"] = "null"
    temp_dict["Image"] = "null"
    temp_dict["TagId"] = "null"
    temp_dict["Alias"] = []
    temp_dict["Parents"] = []
    temp_dict["Children"] = child_lis
    main_lis.append(temp_dict)
    # headers = {
    # 'Content-Type': 'application/json'
    # }
    # conn.request("POST", "\query", payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    print(main_lis)


out_file = open("test.json", "w")
json.dump(main_lis, out_file, indent = 4, sort_keys = False)
out_file.close()
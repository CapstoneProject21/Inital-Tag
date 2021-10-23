import json

file = open('tags.txt', 'r')

lines = file.readlines()
file.close()
total_list = []

for line in lines:
    dict = {}
    line = line.strip("\n")
    dict["TagID"] = None
    dict["Name"] = line 
    dict["Alias"] = []
    dict["Children"] = []
    dict["Parent"] = []
    dict["Weight"] = 1
    dict["Opposite"] = None
    dict["Image"] = None
    total_list.append(dict)

out_file = open("test.json", "w")
json.dump(total_list, out_file, indent = 4, sort_keys = False)
out_file.close()
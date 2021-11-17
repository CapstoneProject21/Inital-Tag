import json
import http.client

conn = http.client.HTTPSConnection("staging.api.tagmatch.io")

#adding new tag
def add_new_tag(tag_name):
    try:
        payload = "{\"query\":\"mutation addNewTag ($input: NewTag!) {\\n    addNewTag (input: $input) {\\n        TagID\\n        Name\\n        Alias\\n        Children\\n        Parent\\n        Weight\\n        Opposite\\n        Image\\n    }\\n}\",\"variables\":{\"input\":{\"Name\":\""+tag_name+"\",\"Alias\":[\"\"],\"Children\":[0],\"Parent\":[0],\"Weight\":1,\"Opposite\":0,\"Image\":\"\"}}}"
        headers = {
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/query", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    except:
        print("{} Already exists".format(tag_name))

# querying all tags
def list_all_tags():
    payload = "{\"query\":\"query allTags {\\n    allTags {\\n        TagID\\n        Name\\n        Alias\\n        Children\\n        Parent\\n        Weight\\n        Opposite\\n        Image\\n    }\\n}\",\"variables\":{}}"
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/query", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response  = data.decode("utf-8")

    all_tags_list = json.loads(response).get('data').get('allTags')
    return all_tags_list


def read_data_from_file(input_file):
    file = open(input_file ,'r')
    lines = file.readlines()
    file.close()
    return lines


def load_data_to_file(all_tags_list, output_file):
    out_file = open(output_file, "w")
    json.dump(all_tags_list, out_file, indent = 4, sort_keys = False)
    out_file.close()


#requesting tags by their tag id
def get_tag_by_id(tag_id):
    payload = "{\"query\":\"query tagByID ($tagid: ID!) {\\n    tagByID (tagid: $tagid) {\\n        TagID\\n        Name\\n        Alias\\n        Children\\n        Parent\\n        Weight\\n        Opposite\\n        Image\\n    }\\n}\",\"variables\":{\"tagid\":\"617a0e598438745d7666ba7f\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/query", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data


#requesting tags by their tag name
def get_tag_by_name(tag_id):
    payload = "{\"query\":\"query tagByName ($name: Name!) {\\n    tagByName (name: $name) {\\n        TagID\\n        Name\\n        Alias\\n        Children\\n        Parent\\n        Weight\\n        Opposite\\n        Image\\n    }\\n}\",\"variables\":{\"name\":\"Travel\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/query", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data


#adding tag parent
def add_tag_parent():
    payload = "{\"query\":\"mutation addTagParent ($tagid: ID!, $parentsID: ID!) {\\n    addTagParent (tagid: $tagid, parentsID: $parentsID) {\\n        TagID\\n        Name\\n        Alias\\n        Children\\n        Parent\\n        Weight\\n        Opposite\\n        Image\\n    }\\n}\",\"variables\":{\"tagid\":\"617a0e598438745d7666ba7f\",\"parentsID\":123}}"
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/query", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data


#adding tag child
def add_tag_child(tag_id,child_tag_id):
    print(tag_id,child_tag_id)
    payload = "{\"query\":\"mutation addTagChild ($tagid: ID!, $childsID: ID!) {\\n    addTagChild (tagid: $tagid, childsID: $childsID) {\\n        TagID\\n        Name\\n        Alias\\n        Children\\n        Parent\\n        Weight\\n        Opposite\\n        Image\\n    }\\n}\",\"variables\":{\"tagid\":\""+tag_id+"\",\"childsID\":\""+child_tag_id+"\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/query", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data


def get_tag_id_by_name(all_tags_list,name):
    
    for i in all_tags_list:
        if i['Name']==name:
            print(name, i['TagID'])
            return(i['TagID'])


def main():
    
    parent_child_dict = {}

    input_file = 'Unt.txt' 
    output_file = 'test.json'
    total_list = []
    first_chid_list = []
    lines = read_data_from_file(input_file)
    
    #Creating a list of tags and dictionary for parent-child relationship
    for line in lines:
        line = line.strip("\n")
        
        row = line.split(',')
        print(row)
        row = [x.strip() for x in row]

        if len(row) > 1:
            parent_child_dict[row[0]] = row[1:]

        if row[0] != "UNT":
            first_chid_list.append(row[0])
        total_list.extend(row)

    print(parent_child_dict)          

    print(first_chid_list)
    #Add all tags to database
    for tag_name in total_list:
        add_new_tag(tag_name)

    # Get key value pairs and 
    all_tags_list = list_all_tags()

    for tag_name in total_list:
        tag_id = get_tag_id_by_name(all_tags_list,tag_name)    

    unt_tag_id = get_tag_id_by_name(all_tags_list,"UNT") 

    for tag_name in first_chid_list:
        tag_id = get_tag_id_by_name(all_tags_list,tag_name) 
        add_tag_child(unt_tag_id,tag_id)
    for key, val in parent_child_dict.items():
        tag_id = get_tag_id_by_name(all_tags_list,key) 
        child_tag_id_list = [get_tag_id_by_name(all_tags_list,x) for x in val]
        print(tag_id, child_tag_id_list)
        print("--------------")
        print(val)
        for child_tag_id in child_tag_id_list: 
            add_tag_child(tag_id,child_tag_id)

    all_tags_list = list_all_tags()
    print("----------------ALL TAGS LIST---------------------------")
    
    load_data_to_file(all_tags_list, output_file)

if __name__ == '__main__':
    main()
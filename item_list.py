# Read json file into variable
import json, datetime
from subprocess import check_output
from tabnanny import check
def read_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

json_data = read_json("item_list.json")

# If today's day is in list of days, print the item list
def print_char_ascension(json_data):
    today = datetime.datetime.today().strftime("%A")
    print(f"Today: {today}")
    found_item = False
    for i in json_data["talent_books"]:
        for a in i["days"]:
            if a == today:
                for a in i["items"]:
                    for b in a:
                        print(f"-- {b}:")
                        for c in a[b]:
                            print(c)
                found_item = True
            else:
                if found_item == True:
                    pass
                else:
                    found_item = False
    if found_item == False:
        return(False)
    else:
        return(True)
todays_char_list = print_char_ascension(json_data)
print(todays_char_list)

# If today's day is in list of days, print the item list
def print_wep_ascension(json_data):
    today = datetime.datetime.today().strftime("%A")
    print(f"Today: {today}")
    found_item = False
    for i in json_data["weapon_materials"]:
        for a in i["days"]:
            if a == today:
                for a in i["items"]:
                    for b in a:
                        print(f"-- {b}:")
                        for c in a[b]:
                            print(c)
                found_item = True
            else:
                if found_item == True:
                    pass
                else:
                    found_item = False
    if found_item == False:
        return(False)
    else:
        return(True)
todays_wep_list = print_wep_ascension(json_data)
print(todays_wep_list)

# Pretty json file
def pretty_json(json_data):
    with open("item_list.json", "w") as f:
        json.dump(json_data, f, indent=4)
pretty_json(json_data)
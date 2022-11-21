#!/usr/bin/env python3

import json
from project_50.formatters.stylish import stylish, list_indent


def make_proper_values(dic):
    for key in dic:
        if isinstance(dic[key], dict):
            make_proper_values(dic[key])
        if dic[key] == True:
            dic[key] = 'true'
        elif dic[key] == False:
            dic[key] = 'false'
        elif dic[key] == None:
            dic[key] = 'null'
    return dic


json1 = make_proper_values(json.load(open('tests/fixtures/file1.json')))
json2 = make_proper_values(json.load(open('tests/fixtures/file2.json')))


def generate_diff(old_dic, new_dic, format=lambda x: x):
    diff_lst = []
    all_keys = sorted(set(old_dic) | set(new_dic))
    general_keys = set(old_dic) & set(new_dic)
    old_keys = set(old_dic) - set(new_dic)
    new_keys = set(new_dic) - set(old_dic)
    for key in all_keys:
        if key in general_keys:
            if isinstance(new_dic[key], dict) and isinstance(old_dic[key], dict):
                diff_lst.append({
                            "key": key,
                            "status": "same",
                            "value": generate_diff(old_dic[key], new_dic[key], format)
                                })
            elif old_dic[key] == new_dic[key]:
                diff_lst.append({
                            "key": key,
                            "status": "same",
                            "value": old_dic[key]
                                })
            elif old_dic[key] != new_dic[key]:
                diff_lst.append({
                            "key": key,
                            "status": "changed",
                            "old_value": old_dic[key],
                            "new_value": new_dic[key]
                                })
        elif key in old_keys:
            diff_lst.append({
                        "key": key,
                        "status": "removed",
                        "value": old_dic[key]
                            })
        elif key in new_keys:
            diff_lst.append({
                        "key": key,
                        "status": "added",
                        "value": new_dic[key]
                            })
    return format(diff_lst)


print(generate_diff(json1, json2, list_indent))

def main():
    pass


if __name__ == '__main__':
    main()

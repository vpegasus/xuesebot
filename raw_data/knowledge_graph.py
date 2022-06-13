#!/usr/bin/env python
# -*- coding: utf-8 -*-


import py2neo
import pymongo
import os
import json

def get_data(filepath="./characters/"):
    dirs = os.listdir(filepath)
    outpout =[]
    for file in dirs:
        datarow = open(filepath+file,"r",encoding="utf-8").readlines()
        outpout.append(datarow)
    return outpout

def create_node(label,node_ls,kg):
    for n in node_ls:
        node = py2neo.Node(label,name=n)
        print(node)
        try:
            kg.create(node)
        except:
            print("建立%s节点时报错"%label)

def two_str(input):
    if type(input) ==str:
        return input
    if type(input) ==list:
        return ",".join(i for i in input)

def two_ls(input):
    if type(input) == list:
        return input
    if type(input) == str:
        if "," in input:
            return input.split(",")
        else:
            return [input]

def create_people_property(data,kg):
    for row in data:
        row = json.loads("".join(i for i in row))
        # 名、字、号、别称、所属势力、职位、侍奉的帝王、家庭成员
        name = row["name"]
        if row.get("courtesyName"):
            courtesyName = two_str(row["courtesyName"])
            order = "match(n:people) where n.name ='%s' " \
                    "set n.courtesyName = '%s'"%(name,courtesyName)
        if row.get("pseudonym"):
            pseudonym = two_str(row["pseudonym"])
            order += "set n.pseudonym = '%s'"%pseudonym
        if row.get("aliase"):
            aliase = row["aliase"]
            alias = "".join(i["name"] for i in aliase)
            order += "set n.alias ='%s'"%alias
        faction = row["faction"]
        position = row["position"]
        monarch = row["monarch"]
        family = row["family"]
        if order:
            try:
                kg.run(order)
            except:
                print("创建人物属性时报错")
                print(order)

def extract_data_and_create_node(data):
    kg = py2neo.Graph(
        "localhost:7474",
        username="neo4j",
        password="password"
    )
    name_ls = []
    faction_ls =[]
    monarch_ls = []
    for row in data:
        row = json.loads("".join(i for i in row))
        name_ls.append(row["name"])
        if type(row["faction"]) is not list:
            if row["faction"] is not None:
                faction_ls.append(row["faction"])
        monarch_ls.append(row["monarch"])

    for i in faction_ls:
        if "," in i:
            faction_ls+=i.split(",")
            faction_ls.remove(i)

    name_ls = list(set(name_ls))
    faction_ls = list(set(faction_ls))
    # create_node("people",name_ls,kg)
    # create_node("faction",faction_ls,kg)
    # create_people_property(data,kg)
    create_monarch_rel(data,kg)
    create_faction_rel(data,kg)

def create_monarch_rel(data,kg):
    for row in data:
        print(row)
        row = json.loads("".join(i for i in row))
        name = row["name"]
        if row.get("monarch"):
            monarch = row["monarch"]
            monarch = two_ls(two_str(monarch))
            for i in monarch:
                order = "match(n:people) where n.name = '%s' " \
                        "match(m:people) where m.name= '%s'" \
                        "merge (n)-[r:has_monarch]-(m)"%(name,i)
                kg.run(order)

def create_faction_rel(data,kg):
    for row in data:
        row = json.loads("".join(i for i in row))
        name = row["name"]
        if row.get("faction"):
            faction = row["faction"]
            faction = two_ls(two_str(faction))
            for i in faction:
                order = "match(n:people) where n.name = '%s' " \
                    "match(m:faction) where m.name= '%s'" \
                    "merge (n)-[r:work_for_faction]-(m)"%(name,i)
                kg.run(order)

if __name__ == '__main__':
    data = get_data()
    extract_data_and_create_node(data)
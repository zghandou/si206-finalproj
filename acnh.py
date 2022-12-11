import json
import unittest
import os
import requests
import sqlite3

# Name: Zeinab Ghandour
# Email: zghandou@umich.edu
# ID: 84727401
#worked with woojin kang
#testing 

'''API_KEY = "https://acnhapi.com/v1/"


def write_json(cache_filename, dict):
    with open(cache_filename, 'w') as f:
        j =json.dumps(dict)
        f.write(j)

'''
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

    
def get_data(villager_id):

    link = f"http://acnhapi.com/v1/villagers/{villager_id}"
    response = requests.get(link)
    r = response.text
    data = json.loads(r)

    #make_villager_table(data, cur, conn)
    #print(data)

    return data 

def create_villager_table(cur, conn):
     cur.execute("CREATE TABLE IF NOT EXISTS Villager (id INTEGER PRIMARY KEY, name TEXT UNIQUE,\
        gender_id INTEGER, species_id STRING, personality_id STRING, hobby_id STRING)")
    
    
def make_gender_table(data, cur, conn):
    gender_list = []

    for villager in data:
        gender_type = villager['gender']
            #print(gender_type)
        if gender_type not in gender_list:
            g = gender_list.append(gender_type)
            #print(g)
            
    cur.execute("CREATE TABLE IF NOT EXISTS Gender (id INTEGER PRIMARY KEY, gender TEXT UNIQUE)")
    for i in range(len(gender_list)):
        cur.execute("INSERT OR IGNORE INTO Gender (id,gender) VALUES (?,?)",(i,gender_list[i]))


    conn.commit()

def make_species_table(data, cur, conn):
    species_list = []

    for villager in data:
        species_type = villager['species']
            #print(gender_type)
        if species_type not in species_list:
            s= species_list.append(species_type)
            #print(g)
            
    cur.execute("CREATE TABLE IF NOT EXISTS Species (id INTEGER PRIMARY KEY, species TEXT UNIQUE)")
    for i in range(len(species_list)):
        cur.execute("INSERT OR IGNORE INTO Species (id,species) VALUES (?,?)",(i,species_list[i]))
    conn.commit()

def make_p_table(data, cur, conn):
    personality_list = []

    for villager in data:
        personality_type = villager['personality']
            #print(gender_type)
        if personality_type not in personality_list:
            p = personality_list.append(personality_type)
            #print(g)
            
    cur.execute("CREATE TABLE IF NOT EXISTS Personality (id INTEGER PRIMARY KEY, personality TEXT UNIQUE)")
    for i in range(len(personality_list)):
        cur.execute("INSERT OR IGNORE INTO Personality (id,personality) VALUES (?,?)",(i,personality_list[i]))
    conn.commit()

def make_hobby_table(data, cur, conn):
    hobby_list = []

    for villager in data:
        hobby_type = villager['hobby']
            #print(hobby_type)
        if hobby_type not in hobby_list:
            h = hobby_list.append(hobby_type)
            #print(g)
            
    cur.execute("CREATE TABLE IF NOT EXISTS Hobby (id INTEGER PRIMARY KEY, hobby TEXT UNIQUE)")
    for i in range(len(hobby_list)):
        cur.execute("INSERT OR IGNORE INTO Hobby (id,hobby) VALUES (?,?)",(i,hobby_list[i]))
    conn.commit()


def add_villager(data, cur, conn):

    count = 0
    stuff = []

    #cur.execute("CREATE TABLE IF NOT EXISTS Villager (name TEXT UNIQUE PRIMARY KEY,\
        #gender_id INTEGER, birthday_string STRING, species STRING, personality STRING, hobby STRING)")
    
    #count = 0
    #might move the birthday thing, it doesnt contribute to our data calculations

    cur.execute ("SELECT COUNT (*) FROM Villager")
    villager_count = cur.fetchone()[0]
    print(villager_count)



    for i in data[villager_count : min(villager_count+25,len(data))]: 
        name = i["name"]['name-USen']
        gender_name = i["gender"]
        cur.execute("SELECT id FROM Gender WHERE gender = ?" ,(gender_name,)) 
        gender_id = int(cur.fetchone()[0])
        #birthday_string= i["birthday-string"]
        species_name = i[ "species"]
        cur.execute("SELECT id FROM Species WHERE species = ?" ,(species_name,)) 
        species_id = int(cur.fetchone()[0])
        personality_name = i["personality"]
        cur.execute("SELECT id FROM Personality WHERE personality = ?" ,(personality_name,)) 
        personality_id = int(cur.fetchone()[0])
        hobby_name = i["hobby"]
        cur.execute("SELECT id FROM Hobby WHERE hobby = ?" ,(hobby_name,)) 
        hobby_id = int(cur.fetchone()[0])

        cur.execute("INSERT OR IGNORE INTO Villager (name, gender_id, species_id, personality_id, hobby_id) VALUES(?,?,?,?,?)",\
            (name, gender_id, species_id, personality_id, hobby_id))
        #count += 1
        #if (count % 25 == 0):
            #break


    conn.commit()
    

def main():
    cur, conn = setUpDatabase('island.db')
    #make a loop to call first function, make the count villager id num update: not in the main 

    #stuff = []
    #for x in range(1,26): instead on using (1,26) use [i +1 : i+25]
        #stuff.append(get_data(x))

    #i = SELECT count (column) FROM table 
    #first 25, then 26-50

    stuff = []
    for x in range(1,101):
        stuff.append(get_data(x))

    create_villager_table(cur, conn)
    make_gender_table(stuff, cur, conn)
    make_species_table(stuff,cur,conn)
    make_p_table(stuff,cur,conn)
    make_hobby_table(stuff,cur,conn)
    add_villager(stuff, cur, conn)

    
    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
import json
import unittest
import os
import requests
import sqlite3
import os
import matplotlib.pyplot as plt

#import [filename] as [name]
#reference functions from the file
#filename.function


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_style_table(cur, conn):
    params = {"format": "json"}
    response = requests.get(f"https://api.nookipedia.com/nh/clothing", params=params, headers={"Accept-Version": "1.0.0", "X-API-KEY":"55812024-1e72-4393-989e-9669fe7e2c0f"})
    data = response.json()
    style_list = []
    s = style_list.append("Normal")

    for style in data:
        for style_type in style['styles']:
            if style_type not in style_list:
                s = style_list.append(style_type)
            #print(g)
            
    cur.execute("CREATE TABLE IF NOT EXISTS Style (id INTEGER PRIMARY KEY, style TEXT UNIQUE)")
    for i in range(len(style_list)):
        cur.execute("INSERT OR IGNORE INTO Style (id,style) VALUES (?,?)",(i,style_list[i]))
    conn.commit()

def clothes(cur, conn):
    params = {"format": "json"}
    response = requests.get(f"https://api.nookipedia.com/nh/clothing", params=params, headers={"Accept-Version": "1.0.0", "X-API-KEY":"55812024-1e72-4393-989e-9669fe7e2c0f"})
    clothes_lst = response.json()
    # print(clothes_lst[2])
    # {'url': 'https://nookipedia.com/wiki/Item:3D_glasses_(New_Horizons)', 'name': '3D glasses', 'category': 'Accessories', 'sell': 122, 'variation_total': 2, 'vill_equip': True, 'seasonality': 'All year', 'version_added': '1.0.0', 'unlocked': True, 'notes': '', 'label_themes': ['Party'], 'styles': ['Active'], 'availability': [{'from': 'Able Sisters', 'note': ''}], 'buy': [{'price': 490, 'currency': 'Bells'}, {'price': 440, 'currency': 'Poki'}], 'variations': [{'variation': 'White', 'image_url': '', 'colors': ['Colorful', 'White']}, {'variation': 'Black', 'image_url': '', 'colors': ['Black', 'Colorful']}]}

    cur.execute("CREATE TABLE IF NOT EXISTS Clothes (id INTEGER PRIMARY KEY, name TEXT UNIQUE, style_id TEXT, price INTEGER)")

    multiply = 4
    for i in range(0, multiply):
        for j in range(i * 25, (i + 1) * 25):
            name = clothes_lst[j]['name']
            try:
                style_name = clothes_lst[j]['styles'][0]
            except:
                style_name = "Normal"
            cur.execute("SELECT id FROM Style WHERE style = ?" ,(style_name,)) 
            style_id = int(cur.fetchone()[0])
            price = clothes_lst[j]['sell']
            cur.execute("INSERT OR IGNORE INTO Clothes (name, style_id, price) VALUES(?, ?, ?)", (name, style_id, price))
    conn.commit()

def normal_avg(cur, conn):
    cur.execute('SELECT name, price FROM Clothes WHERE Clothes.style_id = 0')
    total = 0
    count = 0
    for i in cur:
        print(i[1])
        total += i[1]
        print(total)
        count += 1
    avg = total/count
    print(avg)
    conn.commit()
    return avg

def main():
    cur, conn = setUpDatabase('island.db')
    # link = "https://api.nookipedia.com/villagers"
    # 55812024-1e72-4393-989e-9669fe7e2c0f"
    # get_fishes(cur, conn)
    '''stuff = []
    for x in range[1,101]:
        stuff.append(get_info[x])'''
   # data = get_info()
    make_style_table(cur,conn)
    clothes(cur, conn)
    normal_avg(cur, conn)

    conn.close()
    
 
if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
import sqlite3
import os 
import matplotlib.pyplot as plt
import numpy as np
import csv

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calc_gender(cur,conn):
    #res = cur.execute("SELECT * FROM Gender JOIN Villagers ON Gender.gender_id = Villagers.gender_id")
    #res.fetchall()
    #print(res)
    male = cur.execute("SELECT Gender.gender, COUNT(Villager.gender_id) FROM Gender JOIN Villager ON Gender.id = Villager.gender_id WHERE Gender.gender = 'Male'") 
    res= male.fetchall()[0][1]
    female = cur.execute("SELECT Gender.gender, COUNT(Villager.gender_id) FROM Gender JOIN Villager ON Gender.id = Villager.gender_id WHERE Gender.gender = 'Female'") 
    res2 = female.fetchall()[0][1]
    #print(res2)
    #print(res)
    #f = res2[1]
    #print(f)
    
    return [res, res2]
    

    #calculation: which gender has more villagers (pie chart or female/male) or gender per hobby

def calc_personality(cur,conn):

    p_dict ={}
    query = cur.execute("SELECT * FROM Personality")
    p_list = query.fetchall()

    #cur.execute("SELECT COUNT(*) FROM Villagers WHERE personality_id = 0")
    #p_dict["cranky"] = cur.fetchone()[0]
    #data = cur.fetchall()[0]

    for id,p in p_list :
        cur.execute("SELECT COUNT(*) FROM Villager WHERE personality_id = ?",(id,))
        p_dict[p] = cur.fetchone()[0]  

    #print(p_dict)
    return p_dict

def calc_species(cur,conn):

    s_dict ={}
    query = cur.execute("SELECT * FROM Species")
    s_list = query.fetchall()

    #cur.execute("SELECT COUNT(*) FROM Villagers WHERE personality_id = 0")
    #p_dict["cranky"] = cur.fetchone()[0]
    #data = cur.fetchall()[0]

    for id,s in s_list :
        cur.execute("SELECT COUNT(*) FROM Villager WHERE species_id = ?",(id,))
        s_dict[s] = cur.fetchone()[0]  

    #print(p_dict)
    return s_dict

#most common personality/ personality type breakdown 
    #(amount of villagers per personality)'''

def write_data(data,filename):
    
    headings = ["Personality Type", "Number of Villagers"] 

    #step 2: writes the data to a csv file, and saves it to the passed filename
    with open(filename, "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(headings)  # write header
    #For each tuple in the data, write a new row to the csv,
        for tup in data.items(): 
            writer.writerow(tup)
            #print(tup)
        return None

def write_data2(data2,filename2):
    
    headings = ["Villager Species", "Number of Villagers"] 

    #step 2: writes the data to a csv file, and saves it to the passed filename
    with open(filename2, "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(headings)  # write header
    #For each tuple in the data, write a new row to the csv,
        for tup in data2.items(): 
            writer.writerow(tup)
            #print(tup)
        return None


def write_data3(data3,filename3):
    
    headings = ["Gender", "Number of Villagers"] 

    #step 2: writes the data to a csv file, and saves it to the passed filename
    with open(filename3, "w") as file:
        writer = csv.writer(file)
        writer.writerow(headings)  # write header
        writer.writerow(("Male", data3[0]))
        writer.writerow(("Female", data3[1]))



def personality_graph(p):

    personalities =list(p.keys())
    amount = list(p.values())

    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel("Number of Villagers")
    ax.set_xlabel("Personality Type")
    ax.bar(personalities, amount, color = ['darkgray',"cornflowerblue", "pink", "lightgreen", "plum", "rosybrown", "khaki", "lightcoral"])
    plt.title("Villager Personality Frequency")
    plt.show()
    plt.close()

def species_graph(s):

    species =list(s.keys())
    amount = list(s.values())

    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel("Number of Villagers")
    ax.set_xlabel("Species")
    ax.bar(species, amount, color = ["darkgray","lightblue", "pink", "lightgreen", "plum", "rosybrown", "khaki", "lightcoral", 'cornflowerblue'])
    plt.title("Villager Species Frequency")
    plt.show()
    plt.close()

#def gender_graph(g):  
    #plotting = [gender[1] for gender in g]
    #print(plotting)

    #mylabels = ["Male", "Female"]
    #values = [46, 54]
    

    #mycolors = ["lightblue","pink"]
    #plt.figure()
    #fig1, ax1 = plt.subplots()
    #ax1.pie(g, labels=mylabels, autopct='%1.1f%%', startangle=90, color = mycolors)
    #plt.axis('equal')
    #plt.pie(values, labels = mylabels)
    #plt.title("Villager Genders")
    #plt.show()
    



def main():
    cur, conn = setUpDatabase('island.db')
    calc_gender(cur,conn)
    calc_personality(cur,conn)
    data = calc_personality(cur,conn)
    data2 = calc_species(cur,conn)
    data3= calc_gender(cur,conn)
    filename = "personality types.csv"
    filename2 = "species.csv"
    filename3 = "gender.csv"
    write_data(data,filename)
    write_data2(data2,filename2)
    write_data3(data3,filename3)
    personality_graph(data)
    species_graph(data2)


if __name__ == "__main__":
    main()

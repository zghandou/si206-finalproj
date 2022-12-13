import sqlite3
import os
import matplotlib.pyplot as plt
import csv

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_styles_and_prices(cur):
    cur.execute('SELECT Style.style, Clothes.price FROM Clothes JOIN Style ON Style.id = Clothes.style_id')
    # SELECT employees.first_name, employees.last_name FROM employees JOIN Jobs ON employees.job_id = Jobs.job_id WHERE employees.salary ? Jobs.max_saary OR employees.salary < jobs.min_salary
    prices = cur.fetchall()
    # print(prices)
    return prices

def get_styles(cur):
    s_dict = {}
    query = cur.execute("SELECT * FROM Style")
    s_list = query.fetchall()

    for id,s in s_list: 
        cur.execute("SELECT COUNT(*) FROM Clothes WHERE style_id = ?",(id,))
        s_dict[s] = cur.fetchone()[0]
    #print(s_dict)
    return(s_dict)

def style_avg_price(style_and_prices):
    count = 0
    total = 0
    totals = {}
    avgerages_dict = {}

    for i in style_and_prices:
        if i[0] not in totals.keys():
            totals[i[0]] = {"count":1, "total_price":i[1], "price list":[i[1]]}
        else:
            totals[i[0]]["count"] += 1
            totals[i[0]]["total_price"] += i[1]
            totals[i[0]]["price list"].append(i[1])
    for k in totals.keys():
        avgerages_dict[k] = totals[k]['total_price']/totals[k]['count']

    # print(avgerages_dict)
    # print(totals)
    return avgerages_dict, totals

    # {'Active': 244.23529411764707, 'Simple': 341.85714285714283, 'Elegant': 536.9285714285714, 'Cute': 550.0952380952381, 'Cool': 733.625, 'Normal': 424.7142857142857, 'Gorgeous': 526.0}
    
    # {'Active': {'count': 17, 'total_price': 4152, 'price list': [122, 175, 240, 375, 220, 140, 280, 35, 210, 280, 440, 375, 245, 280, 260, 200, 275]}, 'Simple': {'count': 28, 'total_price': 9572, 'price list': [140, 420, 330, 500, 160, 350, 660, 180, 210, 175, 220, 325, 180, 300, 300, 360, 240, 10, 385, 200, 270, 280, 2400, 157, 180, 240, 260, 140]}, 'Elegant': {'count': 14, 'total_price': 7517, 'price list': [520, 630, 800, 910, 630, 630, 180, 630, 550, 260, 122, 220, 630, 805]}, 'Cute': {'count': 21, 'total_price': 11552, 'price list': [220, 2400, 700, 630, 140, 580, 1600, 1000, 140, 480, 140, 425, 150, 720, 122, 325, 280, 425, 500, 375, 200]}, 'Cool': {'count': 8, 'total_price': 5869, 'price list': [262, 275, 240, 3000, 625, 630, 400, 437]}, 'Normal': {'count': 7, 'total_price': 2973, 'price list': [1400, 210, 192, 392, 405, 187, 187]}, 'Gorgeous': {'count': 5, 'total_price': 2630, 'price list': [450, 630, 330, 600, 620]}}

def write_out_averages(nested_dict, filename):
    headings = ["Clothing Style", "total amount", "average style cost"] 

    #step 2: writes the data to a csv file, and saves it to the passed filename
    with open(filename, "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(headings)  # write header
    #For each tuple in the data, write a new row to the csv,
        for tup in nested_dict.items(): 
            style = tup[0]
            tot = tup[1]['count']
            average = (tup[1]['total_price'])/(tup[1]['count'])
            new_tup = (style, tot, average)
            writer.writerow(new_tup)
        return None
    
def box_plot(data): 
    plotting = []
    labels = []
    for i in data[1]:
        plotting.append(data[1][i]['price list'])
        labels.append(i)
    colors = ["pink","bisque","lightgreen", "slategrey", "lavender", "lightblue", "lightcoral", "yellow"]
    box = plt.boxplot(plotting, labels=labels, patch_artist = True)
    plt.xlabel("Clothing Styles")
    plt.ylabel("Prices (in bells)")
    plt.title("Distribution of Prices by Style")

    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    plt.show() 

def styles_graph(s):
    styles =list(s.keys())
    amount = list(s.values())

    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel("Number of Styles")
    ax.set_xlabel("Style Type")
    ax.bar(styles, amount, color = ["lightblue","pink", "bisque", "lightgreen", "lavender", "slategrey", "lightcoral"])
    plt.title("Clothing Style Frequency")
    plt.show()




def main(): 
    cur, conn = setUpDatabase('island.db') 
    style_and_prices = get_styles_and_prices(cur)
    dictionaries= style_avg_price(style_and_prices)
    averages = dictionaries[0]
    count_tot_price = dictionaries[1]
    averages2 = get_styles(cur)
    box_plot(dictionaries)
    styles_graph(averages2)
    filename = "Clothing_Style_Calculation.csv"
    write_out_averages(count_tot_price, filename)

    conn.close()

if __name__ == "__main__":
    main()
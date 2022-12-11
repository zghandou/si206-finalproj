import os
import sqlite3
import acnh as z
import nook as w

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():  
    z.main()
    w.main()
#make my join statements here 
#conn.close()

if __name__ == "__main__":
    main()
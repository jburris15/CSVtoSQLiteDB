import csv, sqlite3
from sqlite3 import Error
import os
from pathlib import Path

def create_table(create_table_s):
    database = r"C:\your\path\to\database.db" # change to your preferred db path + filename
    db_exists = False
    if not db_exists:
        try:
            Path(database).touch()
            db_exists = True
        except:
            print("File already exists. Continuing")
    try:
        con = sqlite3.connect(database)
    except Error as e:
        print(e)
        exit(1)
    cur = con.cursor()
    cur.execute(create_table_s) # use your column names here
    read_header = False
    con.commit()
    con.close()

def insertToDB(to_db,col_names,table_name):
    database = r"C:\Users\lilbu\Projects\StarWars\StarWars.db"
    try:
        con = sqlite3.connect(database) # change to 'sqlite:///StarWars.db"
    except Error as e:
        print(e)
        exit(1)
    cur = con.cursor()
    read_header = False
    q = ("?,"*len(col_names.split(","))).rstrip(",")
    cur.executemany("INSERT INTO {} ({}) VALUES ({});".format(table_name,col_names,q), to_db)
    con.commit()
    con.close()


def readCSV(full_file):
    with open(full_file,'r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        col_names = ""
        table_name = Path(full_file).stem
        read_col_header = False
        to_db = []
        for row in dr:
            if not read_col_header:
                num_cols = len(dr.fieldnames)
                for col in row:
                    col_names = col_names + col +","
                read_col_header = True
                col_names = col_names.rstrip(',')
                create_table_s = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, col_names)
                create_table(create_table_s)

            if read_col_header:
                to_db.append([(row[cn]) for cn in col_names.split(",")])
        insertToDB(to_db,col_names,table_name)

path = os.getcwd() + "\\data"
files = [x for x in os.listdir(path)]
for file in files:
    full_file = path + '\\' + file
    readCSV(full_file)

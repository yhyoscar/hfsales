import argparse
import glob 
import os
import datetime
import sqlite3

fn_db = "db.sqlite3"

def update_table(app, table):
    db_bak = f"{fn_db}.{datetime.datetime.now().isoformat()}"
    cmd = f"cp {fn_db} {db_bak}"; os.system(cmd)
    cmd = f"python3 manage.py makemigrations {app}"; os.system(cmd)
    cmd = "python3 manage.py migrate"; os.system(cmd)
    
    connection = sqlite3.connect('db.sqlite3_bak')
    return

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--app", type=str, required=True,
        default='', help="app to update")
    parser.add_argument("-t", "--table", type=str, required=True,
        default='', help="table to update")
    args = parser.parse_args()




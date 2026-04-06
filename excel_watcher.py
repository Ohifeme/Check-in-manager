import pandas as pd
import sqlite3
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


FILE = "Cookout_F25.xlsx"
DB_FILE = "database/database.db"

class ExcelHandler(FileSystemEventHandler):

    def process_existing_rows(self):
        """Process all existing NetIDs in the Excel file"""
        print(f"Printing pre exisitng data from {FILE}...\n")
        df = pd.read_excel(FILE)
        valid_no=0
        for _, row in df.iterrows():
            netid = row.iloc[3] 
            year=row.iloc[9]
            major=row.iloc[8]
            scan_time=row.iloc[0]
            if type(netid)is str:
                valid_no+=1
                process_netid(netid, scan_time, year, major)

    def on_modified(self, event):
        """Handle file modifications - process only the new row"""
        if event.src_path.endswith("Cookout_F25.xlsx"):

            df = pd.read_excel(FILE)

            last_row = df.iloc[-1]
            netid = last_row["D"] #read from column D

            process_netid(netid)

def process_netid(netid,scantime=None, year=None, major=None):
    # print(index," New scan:", netid, " ", year, " ", major)
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Insert the NetID
        cursor.execute('''
            INSERT INTO scans (netid, year, major, scan_time, processed)
            VALUES (?, ?, ?, ?, ?)
        ''', (netid, year, major, scantime, 1))
        
        conn.commit()
        conn.close()
        print(f"Saved {netid} to database")
        
    except Exception as e:
        print(f" Error saving to database: {e}")


handler = ExcelHandler()
handler.process_existing_rows()

observer = Observer()
observer.schedule(handler, ".", recursive=False)

observer.start()
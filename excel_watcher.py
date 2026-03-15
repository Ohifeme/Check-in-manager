import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE = "Cookout_F25.xlsx"

class ExcelHandler(FileSystemEventHandler):

    def process_existing_rows(self):
        """Process all existing NetIDs in the Excel file"""
        print(f"Printing pre exisitng data from {FILE}...\n")
        df = pd.read_excel(FILE)
        valid_no=0
        for _, row in df.iterrows():
            netid = row.iloc[3] 
            if type(netid)is str:
                valid_no+=1
                process_netid(netid,valid_no)

    def on_modified(self, event):
        """Handle file modifications - process only the new row"""
        if event.src_path.endswith("Cookout_F25.xlsx"):

            df = pd.read_excel(FILE)

            last_row = df.iloc[-1]
            netid = last_row["D"] #read from column D

            process_netid(netid)

def process_netid(netid,index=None):
    print(index," New scan:", netid)

handler = ExcelHandler()
handler.process_existing_rows()

observer = Observer()
observer.schedule(handler, ".", recursive=False)

observer.start()
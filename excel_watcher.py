import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE = "scanner_output.xlsx"

class ExcelHandler(FileSystemEventHandler):

    def process_existing_rows():
        df = pd.read_excel(FILE)

        for _, row in df.iterrows():
            netid = row["NetID"]
            process_netid(netid)

    def on_modified(self, event):

        if event.src_path.endswith("scanner_output.xlsx"):

            df = pd.read_excel(FILE)

            last_row = df.iloc[-1]
            netid = last_row["NetID"]

            process_netid(netid)

def process_netid(netid):
    print("New scan:", netid)

handler = ExcelHandler()
observer = Observer()
observer.schedule(handler, ".", recursive=False)

observer.start()
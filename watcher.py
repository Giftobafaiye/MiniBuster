import time
import pandas as pd
from sklearn.ensemble import IsolationForest
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            print(f"\n📁 New file detected: {event.src_path}")
            try:
                df = pd.read_csv(event.src_path)
                model = IsolationForest(contamination=0.2)
                model.fit(df)
                df['anomaly'] = model.predict(df)
                anomalies = df[df['anomaly'] == -1]
                print(f"🚨 {len(anomalies)} anomalies found in {event.src_path}")
            except Exception as e:
                print(f"❌ Error processing file: {e}")

if __name__ == "__main__":
    folder = "./logs"
    print(f"👀 Watching folder: {folder}")
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

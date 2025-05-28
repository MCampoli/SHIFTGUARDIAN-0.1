import subprocess
import threading
import time
import random

def run_client(client_id):
    time.sleep(random.uniform(0.1, 1.0))
    subprocess.run(["python", "client.py", str(client_id)])

if __name__ == "__main__":
    threads = []
    for i in range(1, 7):
        t = threading.Thread(target=run_client, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

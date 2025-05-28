# client.py

import socket
import pickle
import threading
import time
import sys

from classes import Employee, Shift, Department

HOST = 'localhost'
PORT = 12345

try:
    client_id = int(sys.argv[1])
except (IndexError, ValueError):
    client_id = 1

class Client(threading.Thread):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id
        self.classes_to_request = ['Employee', 'Shift', 'Department']  # usunięto 'Project'

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(pickle.dumps(self.client_id))
                status = pickle.loads(s.recv(1024))
                print(f"Client {self.client_id} connection status: {status}")

                if status == "REFUSED":
                    return

                for cls_name in self.classes_to_request:
                    s.sendall(pickle.dumps(cls_name))
                    data = s.recv(4096)
                    try:
                        objs = pickle.loads(data)

                        if not isinstance(objs, list):
                            print(f"Client {self.client_id}: Unexpected data format")
                            continue

                        print(f"Client {self.client_id} received {len(objs)} objects of class '{cls_name}':")
                        for obj in objs:
                            try:
                                if cls_name == "Employee" and isinstance(obj, Employee):
                                    print(f"Client {self.client_id}: {obj}")
                                elif cls_name == "Shift" and isinstance(obj, Shift):
                                    print(f"Client {self.client_id}: {obj}")
                                elif cls_name == "Department" and isinstance(obj, Department):
                                    print(f"Client {self.client_id}: {obj}")
                                else:
                                    raise TypeError(f"Type mismatch for class {cls_name}")
                            except Exception as e:
                                print(f"Client {self.client_id}: Error casting object: {e}")

                        time.sleep(0.5)

                    except Exception as e:
                        print(f"Client {self.client_id}: Error deserializing data: {e}")

        except Exception as e:
            print(f"Client {self.client_id} error: {e}")

if __name__ == "__main__":
    client = Client(client_id)
    client.start()
    client.join()

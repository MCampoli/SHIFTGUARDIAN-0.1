# server.py

import socket
import threading
import pickle
import time
import random

from classes import Employee, Shift, Department

MAX_CLIENTS = 3
PORT = 12345
HOST = 'localhost'

class Server:
    def __init__(self):
        self.data_map = {}
        self.connected_clients = set()
        self.lock = threading.Lock()
        self.init_data()

    def init_data(self):
        for i in range(1, 5):
            self.data_map[f'employee_{i}'] = Employee(i, f'Employee {i}')
            self.data_map[f'shift_{i}'] = Shift(f'2025-06-0{i}', f'{8+i}:00-16:00')
            self.data_map[f'department_{i}'] = Department(f'Department {i}', 5 + i)
        print(f"Initialized data keys: {list(self.data_map.keys())}")

    def client_thread(self, conn, addr):
        try:
            o = conn.recv(1024)
            client_id = pickle.loads(o)
            with self.lock:
                if len(self.connected_clients) >= MAX_CLIENTS or client_id in self.connected_clients:
                    conn.sendall(pickle.dumps("REFUSED"))
                    print(f"Refused client {client_id} from {addr}")
                    conn.close()
                    return
                self.connected_clients.add(client_id)
                conn.sendall(pickle.dumps("OK"))
                print(f"Accepted client {client_id} from {addr}")

            for _ in range(5):
                data = conn.recv(1024)
                class_name = pickle.loads(data).lower()
                time.sleep(random.uniform(0, 2))

                objs = [obj for key, obj in self.data_map.items() if key.startswith(class_name + "_")]
                if not objs:
                    if self.data_map:
                        objs = [next(iter(self.data_map.values()))]

                conn.sendall(pickle.dumps(objs))
                print(f"Sent {len(objs)} objects of class '{class_name}' to client {client_id}")

            print(f"Client {client_id} done")
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            with self.lock:
                self.connected_clients.discard(client_id)
            conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.client_thread, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    Server().start()

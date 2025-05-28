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
        # Tworzymy przykładowych pracowników z rozbiciem imienia i nazwiska oraz innymi polami
        self.data_map['employee_1'] = Employee(1, "Jan", "Kowalski", "Programista", "IT")
        self.data_map['employee_2'] = Employee(2, "Anna", "Nowak", "Tester", "QA")
        self.data_map['employee_3'] = Employee(3, "Piotr", "Wiśniewski", "Manager", "HR")
        self.data_map['employee_4'] = Employee(4, "Kasia", "Zielińska", "Analityk", "Finanse")

        self.data_map['shift_1'] = Shift('2025-06-01', '08:00-16:00')
        self.data_map['shift_2'] = Shift('2025-06-02', '10:00-18:00')
        self.data_map['shift_3'] = Shift('2025-06-03', '12:00-20:00')
        self.data_map['shift_4'] = Shift('2025-06-04', '09:00-17:00')

        self.data_map['department_1'] = Department('IT', 10)
        self.data_map['department_2'] = Department('QA', 5)
        self.data_map['department_3'] = Department('HR', 3)
        self.data_map['department_4'] = Department('Finanse', 8)

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
                    # Jeśli nie ma obiektów danej klasy, wysyłamy pustą listę
                    objs = []

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

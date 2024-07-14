import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()

    def customer_arrival(self):
        customer_number = 1
        while customer_number <= 20:
            print(f"Посетитель номер {customer_number} прибыл")
            customer = Customer(customer_number, self)
            customer_number += 1
            customer.start()
            time.sleep(1)

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.customer_number} сел за стол {table.number} ")
                time.sleep(5)
                print(f"Посетитель номер {customer.customer_number} покушал и ушёл ")
                table.is_busy = False
                self.check_queue()
                break
        else:
            self.queue.put(customer)
            print(f"Посетитель номер {customer.customer_number} ожидает свободный стол ")

    def check_queue(self):
        if not self.queue.empty():
            customer = self.queue.get()
            self.serve_customer(customer)

class Customer(threading.Thread):
    def __init__(self, customer_number, cafe):
        super().__init__()
        self.customer_number = customer_number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]


cafe = Cafe(tables)


customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()
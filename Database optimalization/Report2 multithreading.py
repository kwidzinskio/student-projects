
import numpy as np
import time
import cx_Oracle
import functools
from threading import Thread
import random

tables = ["products", "invoices", "departments", "customers", "means_of_transport", "purchase_positions", "units", "purchase", "product_types", "supplieres"]
executiontimes = 100
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XEPDB1')

def timeit(func):
    global print_func_time
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        # print('function [{}] finished in {} ms'.format(func.__name__, int(elapsedTime * 1000)))
    return newfunc



class UserThread(Thread):
    available_methods = []
    
    def __init__(self, user_type, index):
        Thread.__init__(self)
        self.user_type = user_type
        self.index = index
        self.cursor = self._connect(user_type, index)
    
    @staticmethod
    def _connect(user_type, index):
        login = user_type + str(index)
        connection = cx_Oracle.connect(user=login, password=login, dsn=dsn_tns)
        return connection.cursor()
    
    def run(self):
        assert self.available_methods, 'You have to define at least one available method'
        timer = []
        print(self.getName(), 'has started')
        for i in range(0, executiontimes):
            time_start = time.time()
            if self.index%2:
                self.available_methods[0]()
            else:
                self.available_methods[1]()
            timer.append(time.time() - time_start)
            secondsToSleep = 7.52
            time.sleep(secondsToSleep)
        print('{}: finished, avarege time of execution: {}'.format(self.getName(), round(np.mean(timer), 4)))



class Admin(UserThread):
    
    def __init__(self, user_type, index):
        super().__init__(user_type, index)
        self.available_methods = [self.add_dept, self.add_prod]
        if self.index%2:
            self.setName('Thread ADMIN{} adding records to departments'.format(index + 1))
        else:
            self.setName('Thread ADMIN{} adding records to products'.format(index + 1))
        
    @timeit
    def add_dept(self, *args, **kwargs):
        self.cursor.execute('''SELECT max(department_code) FROM sklepp.departments''')
        last_id = self.cursor.fetchone()[0]
        self.cursor.execute(''' 
                            INSERT INTO sklepp.departments(department_code, department_name, head_id, city)
                            VALUES ({}, {}, 5, 'Lodz')'''.format(last_id + 1, " 'kappa' "))
        self.cursor.execute('''COMMIT''')
        
    @timeit
    def add_prod(self, *args, **kwargs):
        self.cursor.execute('''SELECT max(id) FROM sklepp.products''')
        last_id = self.cursor.fetchone()[0]
        self.cursor.execute(''' 
            INSERT INTO sklepp.products(ID, PRODUCT_NAME, PRODUCT_TYPE, SELL_PRICE, BUY_PRICE, TAX_RATE, UNIT, SUPPLIER)
            VALUES ({}, {}, 'NAS', 5, 7, 23, 'KG', 7)'''.format(last_id + 1, " 'kappa' "))
        self.cursor.execute('''COMMIT''')    
        
        
        
class Head(UserThread):
    
    def __init__(self, user_type, index):
        super().__init__(user_type, index)
        self.available_methods = [self.upd_empl, self.upd_prod]
        if self.index%2:
            self.setName('Thread HEAD{} updating employees'.format(index + 1))
        else:
            self.setName('Thread HEAD{} updating products'.format(index + 1))
            
    @timeit
    def upd_empl(self, *args, **kwargs):
        self.cursor.execute('''SELECT max(id) FROM sklepp.employees''')
        last_id = self.cursor.fetchone()[0]
        self.cursor.execute('''UPDATE sklepp.employees SET salary={} WHERE id={}'''.format(random.randint(2000,9000), random.randint(0, last_id)))
        self.cursor.execute('''COMMIT''')
        
    @timeit
    def upd_prod(self, *args, **kwargs):
        self.cursor.execute('''SELECT max(id) FROM sklepp.products''')
        last_id = self.cursor.fetchone()[0]
        self.cursor.execute('''UPDATE sklepp.products SET sell_price={} WHERE id={}'''.format(random.randint(1,20), random.randint(0, last_id)))
        self.cursor.execute('''COMMIT''')  
        
        
        
class Cashier(UserThread):
    
    def __init__(self, user_type, index):
        super().__init__(user_type, index)
        self.available_methods = [self.sel_rand, self.sel_comp]
        if self.index%2:
            self.setName('Thread CASHIER{} selecting from random table'.format(index + 1))
        else:
            self.setName('Thread CASHIER{} selecting complex'.format(index + 1))
            
    @timeit
    def sel_rand(self, *args, **kwargs):
        self.cursor.execute('''SELECT * FROM sklepp.{}'''.format(random.choice(tables)))
        self.cursor.execute('''COMMIT''')
        
    @timeit
    def sel_comp(self, *args, **kwargs):
        self.cursor.execute('''SELECT sklepp.employees.surname, sklepp.employees.salary, sklepp.departments.department_code 
        FROM sklepp.departments JOIN sklepp.employees 
        ON sklepp.departments.department_code = sklepp.employees.department_id 
        WHERE sklepp.employees.salary > 5000 ORDER BY sklepp.employees.salary''')
        self.cursor.execute('''COMMIT''')  
        
    
    
if __name__ == '__main__':
    
    admins = [Admin('admin', i) for i in range(0, 5)]
    for admin in admins:
        admin.start()
        time.sleep(0.43)
        
    heads = [Head('head', i) for i in range(0, 15)]
    for head in heads:
        head.start()
        time.sleep(0.87)
    
    cashiers = [Cashier('cashier', i) for i in range(0, 35)]
    for cashier in cashiers:
        cashier.start()
        time.sleep(0.51)
        

    
    


    


 



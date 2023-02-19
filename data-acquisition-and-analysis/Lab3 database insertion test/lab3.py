import time
import mysql.connector
import csv

def create_connection():
    connect = mysql.connector.connect(**{"database": "lab3", "host": "localhost", "user": "root"})
    cursor = connect.cursor()
    return connect, cursor

def create_table(cursor, test_type):
    if test_type == "No pk":
        cursor.execute("CREATE TABLE tab (date INT NOT NULL, temp INT NOT NULL)")
    elif test_type == "With pk":
        cursor.execute("CREATE TABLE tab (date INT NOT NULL, temp  INT NOT NULL, PRIMARY KEY (date))")
    elif test_type == "With autopk":
        cursor.execute("CREATE TABLE tab (date INT NOT NULL AUTO_INCREMENT, temp INT NOT NULL, PRIMARY KEY (date))")

def insert_row(cursor, i, test_type):
    if test_type == "With autopk":
        cursor.execute(f"INSERT INTO tab (temp) VALUES ({i})")
    else:
        cursor.execute(f"INSERT INTO tab (date, temp) VALUES ({i}, {i})")

def db_execute(cursor, i, test_type):
    timer_start = time.time()
    insert_row(cursor, i, test_type)
    timer_stop = time.time()
    insertion_time = timer_stop - timer_start
    return insertion_time

def db_execute_commit(cursor, i, test_type):
    timer_start = time.time()
    insert_row(cursor, i, test_type)
    cursor.execute("COMMIT")
    timer_stop = time.time()
    insertion_time = timer_stop - timer_start
    return insertion_time

def db_execute_conn(i, test_type, isolation_level):
    timer_start = time.time()
    connect, cursor = create_connection()
    cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level}")
    insert_row(cursor, i, test_type)
    timer_stop = time.time()
    insertion_time = timer_stop - timer_start
    connect.close()
    return insertion_time

def db_execute_conn_commit(i, test_type, isolation_level):
    timer_start = time.time()
    connect, cursor = create_connection()
    cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level}")
    insert_row(cursor, i, test_type)
    cursor.execute("COMMIT")
    timer_stop = time.time()
    insertion_time = timer_stop - timer_start
    connect.close()
    return insertion_time

def main():
    isolation_levels = ["READ COMMITTED", "READ UNCOMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
    test_types = ['No pk', 'With pk', 'With autopk']
    insertions = 10000

    with open(f'data{insertions}.csv', 'w', newline='') as file:
        data = []
        writer = csv.writer(file)

        mode = "CONNECTION: one, COMMIT: no"
        print(f"\n------- {mode} -------")
        for isolation_level in isolation_levels:
            connect, cursor = create_connection()
            cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level}")
            print("---", isolation_level, "---")
            for test_type in test_types:
                total_time = 0
                time.sleep(1)
                create_table(cursor, test_type)
                for insertion in range(insertions):
                    insertion_time = db_execute(cursor, insertion, test_type)
                    total_time  += insertion_time
                time.sleep(1)
                cursor.execute("DROP TABLE IF EXISTS tab")
                print(f"{test_type}:", total_time / insertions)
                data.append(total_time / insertions)
            connect.close()
        for i in range(len(isolation_levels)):
            writer.writerows([[mode + " " + isolation_levels[i]], test_types, data[(3*i):(3*(i+1))]])
        data = []

        mode = "CONNECTION: one, COMMIT: after each insertion"
        print(f"\n------- {mode} -------")
        for isolation_level in isolation_levels:
            connect, cursor = create_connection()
            cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level}")
            print("---", isolation_level, "---")
            for test_type in test_types:
                total_time = 0
                time.sleep(1)
                create_table(cursor, test_type)
                for insertion in range(insertions):
                    insertion_time = db_execute_commit(cursor, insertion, test_type)
                    total_time  += insertion_time
                time.sleep(1)
                cursor.execute("DROP TABLE IF EXISTS tab")
                print(f"{test_type}:", total_time / insertions)
                data.append(total_time / insertions)
            connect.close()
        for i in range(len(isolation_levels)):
            writer.writerows([[mode + " " + isolation_levels[i]], test_types, data[(3*i):(3*(i+1))]])
        data = []

        mode = "CONNECTION: before each insertion, COMMIT: no"
        print(f"\n------- {mode} -------")
        for isolation_level in isolation_levels:
            print("---", isolation_level, "---")
            for test_type in test_types:
                total_time = 0
                time.sleep(1)
                connect, cursor = create_connection()
                create_table(cursor, test_type)
                connect.close()
                for insertion in range(insertions):
                    insertion_time = db_execute_conn(insertion, test_type, isolation_level)
                    total_time += insertion_time
                time.sleep(1)
                connect, cursor = create_connection()
                cursor.execute("DROP TABLE IF EXISTS tab")
                connect.close()
                print(f"{test_type}:", total_time / insertions)
                data.append(total_time / insertions)
        for i in range(len(isolation_levels)):
            writer.writerows([[mode + " " + isolation_levels[i]], test_types, data[(3*i):(3*(i+1))]])
        data = []

        mode = "CONNECTION: before each insertion, COMMIT: after each insertion"
        print(f"\n------- {mode} -------")
        for isolation_level in isolation_levels:
            print("---", isolation_level, "---")
            for test_type in test_types:
                total_time = 0
                time.sleep(1)
                connect, cursor = create_connection()
                create_table(cursor, test_type)
                connect.close()
                for insertion in range(insertions):
                    insertion_time = db_execute_conn_commit(insertion, test_type, isolation_level)
                    total_time += insertion_time
                time.sleep(1)
                connect, cursor = create_connection()
                cursor.execute("DROP TABLE IF EXISTS tab")
                connect.close()
                print(f"{test_type}:", total_time / insertions)
                data.append(total_time / insertions)
        for i in range(len(isolation_levels)):
            writer.writerows([[mode + " " + isolation_levels[i]], test_types, data[(3*i):(3*(i+1))]])
        data = []





if __name__ == "__main__":
    main()



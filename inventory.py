import os, csv
import time
from datetime import datetime

PATH = 'key.csv'
LOG_PATH = 'register_log.txt'

class Inventory:
    inv = {}

    def __init__(self):
        self.read()

    def check(self, key):
        with open(PATH, 'r', encoding='UTF8') as file:
            stor = list(csv.reader(file))[:][0]
        return key in stor

    def read(self):
        inv = {}
        count = 0
        with open(PATH, 'r', encoding='UTF8') as file:
            reader = csv.readesr(file)
            for row in reader:
                inv[row[0]] = tuple(row[1:])
                count += 1
        print(f"[SYS] Read {count} values")
        self.inv = inv

    def write(self, key, id, name):
        if self.check(key):
            print(f"[SYS] WARNING: Card is already in use. Existing entry will be overwritten.")
            self.mod(key, id, name)
            self.read()
            return

        with open(PATH, 'a', newline='', encoding='UTF8') as file:
            entry = [key, id, name]
            writer = csv.writer(file)
            writer.writerow(entry)
        print(f"[LOG] Card ID {key} registered to [{id} {name}]")
        self.inv[key] = (id, name)

        log = open(LOG_PATH, 'a')
        log.write(f'{datetime.now().strftime("%m-$s %H:%M:%S")} ADD {key}')
        log.close()

    def rm(self, name, isKey=False):
        rows = []
        key = ''

        with open(PATH, 'r', encoding='UTF8') as file:
            for row in csv.reader(file):
                if not isKey:
                    if row[2] != name:
                        rows.append(row)
                    else:
                        key = row[0]
                else:
                    if row[0] != name:
                        rows.append(row)
                    else:
                        key = row[0]

        os.remove(PATH)
        with open(PATH, 'w', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        del self.inv[key]

        log = open(LOG_PATH, 'a')
        log.write(f'{datetime.now().strftime("%m-$s %H:%M:%S")} RM  {key}')
        log.close()

    def mod(self, key, id, name):
        previous = self.entryAt(key)
        self.rm(key, isKey=True)
        self.write(key, id, name)

        log = open(LOG_PATH, 'a')
        log.write(f'{datetime.now().strftime("%m-$s %H:%M:%S")} MOD {previous[0]}, {previous[1]} TO {id}, {name}')
        log.close()

    def entryAt(self, key):
        try:
            return self.inv[key]
        except KeyError:
            return -1

    def debug_print(self):
        print('[DBG] ', self.inv)

    def sanity_check(self):
        with open(PATH, 'r', encoding='UTF8') as file:
            reader = csv.reader(file)
            file_len = len(list(reader))
            inv_len = len(self.inv)
            if file_len < inv_len:
                print("[DBG] WARNING: Inventory larger than file")
                log = open(LOG_PATH, 'a')
                log.write(f'{datetime.now().strftime("%m-$s %H:%M:%S")} SANITY FAIL IGF')
                log.close()
                return False
            elif file_len == inv_len:
                return True
            else:
                print("[DBG] WARNING: Inventory smaller than file")
                log = open(LOG_PATH, 'a')
                log.write(f'{datetime.now().strftime("%m-$s %H:%M:%S")} SANITY FAIL ILF')
                log.close()
                return False


def sanity_check(PATH):
    log = []
    with open(PATH, 'r', newline='', encoding='UTF8') as file:
        reader = csv.reader(file)
        log = list(reader)[:][0]
    if sorted(log) == log:
        return True
    else:
        return False
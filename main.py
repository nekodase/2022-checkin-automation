from inventory import Inventory, sanity_check
from attendance import check_sequence
from register import register_sequence
from mfrc522 import MFRC522
# https://github.com/pimylifeup/MFRC522-python/blob/master/mfrc522/MFRC522.py

menu = """[0]: Register new cards
          [1]: Begin attendance"""
inv = Inventory()

try:
    print("[SYS] RFID comms check...")
    reader = MFRC522()
except:
    print("[ERR] Unable to get a response, check wiring")

inp = 'a'
print(menu)
while inp not in ('0','1'):
    inp = input()
if inp == '0':
    register_sequence(reader, inv)
if inp == '1':
    check_sequence(reader, inv)
import RPi.GPIO as GPIO
import time

class InventoryException(Exception):
    def __init__(self):
        super().__init__("Inventory size mismatch")

def register_sequence(reader, inv):
    CHECK_TERM = 10
    cnt = 0
    sane = True
    print("[SYS] Reading...")

    try:
        while True:
            time.sleep(1)

            if cnt == CHECK_TERM:
                cnt = 0
                sane = inv.sanity_check()
            if not sane:
                raise InventoryException()

            status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                print(f"[SYS] Reading card")

            status, UID = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                UID = ''.join([str(x) for x in UID])
                print(f"[SYS] Read in {UID}")
                id = input("Student ID: ")
                name = input("Your name: ")
                inv.write(UID, id, name)

            cnt += 1

    except KeyboardInterrupt:
        print("[SYS] KeyboardInterrupt recognised, cleaning up...")
    except InventoryException:
        print(f"[ERR] Inventory size mismatch from last {CHECK_TERM} entries, check inventory_log.txt")
    finally:
        GPIO.cleanup()
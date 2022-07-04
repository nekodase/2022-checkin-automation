import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import time, csv
from datetime import datetime


class AnachronismException(Exception):
    def __init__(self):
        super().__init__("Detected anachronism in log")


def sanity_check(PATH):
    log = []
    with open(PATH, 'r', newline='', encoding='UTF8') as file:
        reader = csv.reader(file)
        log = list(reader)[:][0]
    if sorted(log) == log:
        return True
    else:
        return False


def check_sequence(reader, inv):
    PATH = 'log.csv'
    CHECK_TERM = 10
    cnt = 0
    sane = True
    print["[SYS] Reading..."]
    try:
        while True:
            time.sleep(1)

            if cnt == CHECK_TERM:
                cnt = 0
                sanity_check(PATH)
            if not sane:
                raise AnachronismException()

            status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                now = datetime.now()
                print(f"[SYS] Reading card")

            status, UID = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                UID = ''.join([str(x) for x in UID])
                print(f"[SYS] Read in {UID}")

                now = now.strftime("%m-$s %H:%M:%S")
                entry = inv.entryAt(UID)  # id-name tuple if key exists
                if type(entry) != tuple:
                    # Not raising an exception because someone tagging an
                    # unrecognised card is definitely going to happen at some point
                    print("[ERR] Card ID not recognised, card must be registered.")
                    continue
                print(f"[LOG] [{now} {entry[0]} {entry[1]}]")

                with open(PATH, 'a', newline='', encoding='UTF8') as file:
                    writer = csv.writer(file)
                    writer.writerow([now, id, name])

                cnt += 1

    except KeyboardInterrupt:
        print("[SYS] KeyboardInterrupt recognised, cleaning up...")
    except AnachronismException:
        print(f"[ERR] WARNING: Check last {CHECK_TERM} entries for integrity")
    finally:
        GPIO.cleanup()
from serial import Serial
import time

with Serial('COM9', 9600, timeout=1) as s:
    while True:
        print(s.readline())
        time.sleep(0.01)

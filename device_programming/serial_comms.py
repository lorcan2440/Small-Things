from serial import Serial
import time

with Serial('COM9', 9600, timeout=1) as s:
    while True:
        if (line := s.readline()) != b'':
            print(line)
        time.sleep(0.01)

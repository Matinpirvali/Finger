import serial
import time

ser = serial.Serial("/dev/serial0", 57600, timeout=1)

try:
    print("چک کردن سنسور...")
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print("داده دریافت شد:", data.hex())
        time.sleep(1)
except:
    print("خطا! مطمئن شو سنسور وصل و روشن باشه.")
finally:
    ser.close()

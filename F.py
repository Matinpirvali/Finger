import serial
import time

# تنظیم پورت سریال (بسته به اتصالت ممکنه /dev/ttyUSB0 یا /dev/ttyS0 باشه)
ser = serial.Serial(
    port='/dev/ttyS0',  # پورت رو درست تنظیم کن
    baudrate=57600,     # نرخ باود پیش‌فرض ZFM-60
    timeout=1
)

# بسته دستور برای روشن کردن LED (مثال)
# این باید با دیتاشیت ZFM-60 V1 مطابقت داشته باشه
led_on = bytearray([0xEF, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x03, 0x35, 0x01, 0x00, 0x3A])

try:
    ser.write(led_on)  # ارسال دستور
    response = ser.read(12)  # پاسخ سنسور (معمولاً 12 بایت)
    print("Response:", response.hex())
    if response[9] == 0x00:  # کد تأیید موفقیت
        print("LED روشن شد!")
    else:
        print("خطا در روشن کردن LED")
except Exception as e:
    print("خطا:", e)
finally:
    ser.close()

import serial

# تنظیم پورت سریال
PORT = '/dev/ttyS0'  # پورت UART رزبری
BAUD_RATE = 57600    # نرخ باود پیش‌فرض ZFM60

# باز کردن پورت
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

# ارسال دستور ساده (مثلاً گرفتن نسخه سنسور)
command = bytearray([0xEF, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x03, 0x25, 0x00, 0x00, 0x29])
ser.write(command)

# خواندن پاسخ
response = ser.read(12)
print("Response from sensor:", response.hex())

# بستن پورت
ser.close()

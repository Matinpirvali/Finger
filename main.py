import serial
import time

# تنظیم پورت سریال
PORT = '/dev/ttyAMA0'  # پورتی که قبلاً کار کرد
BAUD_RATE = 57600      # نرخ باود پیش‌فرض

# تابعی برای ساخت بسته دستور
def send_command(command_byte, parameters):
    contents = [command_byte] + parameters
    length = len(contents)
    packet = [0xEF, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, (length >> 8) & 0xFF, length & 0xFF] + contents
    checksum = 0
    for byte in packet[6:]:
        checksum += byte
    packet.append((checksum >> 8) & 0xFF)
    packet.append(checksum & 0xFF)
    return bytearray(packet)

# باز کردن پورت
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

# 1. ثبت اثر انگشت (Enroll)
def enroll_fingerprint(id_number):
    command = send_command(0x01, [0x00, 0x03, (id_number >> 8) & 0xFF, id_number & 0xFF, 0x00])
    ser.write(command)
    time.sleep(1)
    response = ser.read(12)
    print("Enroll Response:", response.hex())
    if response and response[9] == 0x00:
        print(f"اثر انگشت با ID {id_number} ثبت شد!")
    else:
        print("خطا در ثبت اثر انگشت:", response[9] if response else "بدون پاسخ")

# 2. شناسایی اثر انگشت (Identify)
def identify_fingerprint():
    command = send_command(0x03, [0x01, 0x00])
    ser.write(command)
    time.sleep(1)
    response = ser.read(16)
    print("Identify Response:", response.hex())
    if response and response[9] == 0x00:
        id_number = (response[10] << 8) + response[11]
        print(f"اثر انگشت شناسایی شد! ID: {id_number}")
    else:
        print("اثر انگشت شناسایی نشد:", response[9] if response else "بدون پاسخ")

# اجرای توابع
try:
    print("ثبت اثر انگشت با ID 1...")
    enroll_fingerprint(1)  # انگشتت رو 3 بار بذار (هر بار چند ثانیه)
    time.sleep(5)

    print("شناسایی اثر انگشت...")
    identify_fingerprint()

except Exception as e:
    print("خطا:", e)

finally:
    ser.close()
    print("پورت بسته شد.")

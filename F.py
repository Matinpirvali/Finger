import serial
import time

# تنظیمات پورت سریال
ser = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)

def send_command(command):
    """ارسال فرمان به سنسور و دریافت پاسخ"""
    ser.write(command)
    time.sleep(0.5)
    response = ser.read(12)  # دریافت پاسخ 12 بایتی
    return response

def enroll_fingerprint():
    """ثبت اثر انگشت جدید"""
    print("لطفاً انگشت خود را روی سنسور قرار دهید...")

    # فرمان گرفتن تصویر اثر انگشت
    command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'
    response = send_command(command)

    if response and response[9] == 0x00:
        print("انگشت اسکن شد، لطفاً دوباره قرار دهید.")
        time.sleep(1)

        # مرحله دوم اسکن
        command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x02\x00\x06'
        response = send_command(command)

        if response and response[9] == 0x00:
            print("اثر انگشت تأیید شد! در حال ذخیره...")
            
            # ذخیره اثر انگشت با ID=1
            command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x06\x01\x00\x01\x00\x0F'
            response = send_command(command)

            if response and response[9] == 0x00:
                print("اثر انگشت با موفقیت ذخیره شد!")
            else:
                print("خطا در ذخیره اثر انگشت!")
        else:
            print("اثر انگشت تطبیق ندارد، دوباره امتحان کنید.")
    else:
        print("اسکن اثر انگشت ناموفق بود!")

def search_fingerprint():
    """جستجوی اثر انگشت"""
    print("لطفاً انگشت خود را روی سنسور قرار دهید...")

    # فرمان اسکن اثر انگشت
    command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'
    response = send_command(command)

    if response and response[9] == 0x00:
        print("اثر انگشت اسکن شد، در حال بررسی...")

        # جستجو در پایگاه داده
        command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x08\x04\x00\x00\x00\x64\x00\x71'
        response = send_command(command)

        if response and response[9] == 0x00:
            fingerprint_id = response[10]
            print(f"اثر انگشت شناخته شد! شماره ID: {fingerprint_id}")
        else:
            print("اثر انگشت ثبت نشده است.")
    else:
        print("خطا در اسکن اثر انگشت!")

# اجرای برنامه
while True:
    print("\n1: ثبت اثر انگشت جدید")
    print("2: جستجوی اثر انگشت")
    print("3: خروج")
    choice = input("انتخاب کنید: ")

    if choice == "1":
        enroll_fingerprint()
    elif choice == "2":
        search_fingerprint()
    elif choice == "3":
        print("خروج از برنامه...")
        break
    else:
        print("گزینه نامعتبر!")

import time
import serial
import adafruit_fingerprint

# تنظیمات ارتباط سریال با سنسور اثر انگشت
uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():
    """ شناسایی اثر انگشت """
    print("لطفاً انگشت خود را روی سنسور قرار دهید...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass  # صبر می‌کنیم تا انگشت روی سنسور قرار بگیرد

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("خطا در پردازش تصویر!")
        return False

    if finger.finger_search() != adafruit_fingerprint.OK:
        print("اثر انگشت شناسایی نشد.")
        return False

    print(f"اثر انگشت شناسایی شد! ID: {finger.finger_id}")
    return True

def enroll_fingerprint():
    """ ثبت اثر انگشت جدید """
    print("ثبت اثر انگشت جدید...")
    for finger_id in range(1, 127):  # جستجو برای اولین ID خالی
        if not finger.load_model(finger_id):
            break
    else:
        print("حافظه سنسور پر است!")
        return False

    print(f"ثبت اثر انگشت در ID: {finger_id}")
    for i in range(1, 3):  # دو بار اسکن برای ثبت اثر انگشت
        print(f"لطفاً انگشت خود را ({i}/2) روی سنسور قرار دهید...")
        while finger.get_image() != adafruit_fingerprint.OK:
            pass
        if finger.image_2_tz(i) != adafruit_fingerprint.OK:
            print("خطا در پردازش تصویر!")
            return False
        if i == 1:
            print("انگشت خود را بردارید و دوباره قرار دهید...")
            time.sleep(2)

    if finger.create_model() != adafruit_fingerprint.OK:
        print("خطا در ترکیب داده‌های اثر انگشت!")
        return False

    if finger.store_model(finger_id) != adafruit_fingerprint.OK:
        print("خطا در ذخیره‌سازی اثر انگشت!")
        return False

    print(f"اثر انگشت با موفقیت ثبت شد! ID: {finger_id}")
    return True

# اجرای برنامه
while True:
    print("\n1: ثبت اثر انگشت")
    print("2: شناسایی اثر انگشت")
    print("3: خروج")

    choice = input("انتخاب کنید: ")
    
    if choice == "1":
        enroll_fingerprint()
    elif choice == "2":
        get_fingerprint()
    elif choice == "3":
        break
    else:
        print("انتخاب نامعتبر! دوباره امتحان کنید.")

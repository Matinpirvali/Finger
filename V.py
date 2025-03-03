import serial

PORT = '/dev/ttyAMA0'
BAUD_RATE = 57600

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print("Port opened successfully!")

    # دستور ساده برای گرفتن وضعیت
    command = bytearray([0xEF, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x03, 0x25, 0x00, 0x00, 0x29])
    ser.write(command)
    response = ser.read(12)
    print("Response from sensor:", response.hex())

except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals():
        ser.close()
        print("Port closed.")

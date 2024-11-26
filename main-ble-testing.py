import serial

ser = serial.Serial("COM10", 9600, timeout = 1) #Change your port name COM... and your baudrate

def retrieveData():
    ser.write(b'P,24,0,')
    data = ser.readline().decode('ascii')
    return data

def retrieveData1():
    ser.write(b'P,38,1,')
    data = ser.readline().decode('ascii')
    return data

def retrieveData2():
    ser.write(b'P,90,0,')
    data = ser.readline().decode('ascii')
    return data

while(True):
    uInput = input("Retrieve data? ")
    if uInput == '1':
        print(retrieveData1())
    elif uInput == '2':
        print(retrieveData2())

    else:
        print(retrieveData())

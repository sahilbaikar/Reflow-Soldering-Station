# V2

# REflow Final Main - Code
# OK tested - working - code

import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from turtle import bgcolor
from flask import flash
import serial

root = Tk()
root.geometry("600x600")
root.configure(bg='#9ECE9A')
root.title("Reflow Panel")

# Declaration of variables
trig = 0
tog = 0
count = 0
coin = True

thisdict = {"Temp": "55", "Relay": "0", "Status": "Below Range"}


TempLab = Label(text="Temperature",  fg="#4D243D",
                bg="#9ECE9A", font=("Helvetica", 20))
TempLab.place(x=230, y=280)

bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300)
bar.pack(pady=20)
bar.place(x=160, y=200)

Temp = Label(text=thisdict["Temp"], fg="#074F57",
             bg="#9ECE9A", font=("Helvetica", 18))
Temp.pack(pady=20)
Temp.place(x=290, y=240)

# Button(root, text="Download", command=start).pack(pady=20)

RelayVal = Label(text=thisdict["Relay"], fg="#074F57",
                 bg="#9ECE9A", font=("Helvetica", 18))
RelayVal.place(x=300, y=380)

RelayLabel = Label(text="Relay Status", fg="#3C1B43",
                   bg="#9ECE9A", font=("Helvetica", 18))
RelayLabel.place(x=242, y=420)


RangeS = Label(text=thisdict["Status"], fg="#074F57",
               bg="#9ECE9A", font=("Helvetica", 18))
RangeS.place(x=240, y=460)

RangeSLabel = Label(text="Relay Status", fg="#3C1B43",
                    bg="#9ECE9A", font=("Helvetica", 18))
RangeSLabel.place(x=242, y=500)


def submit():
    global trig
    global tog
    global count
    global coin

    arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)
    ser = serial.Serial("COM5", 9600, timeout = 1) 

    # error : print("Machine Not Connected")

    while trig == 0:
        # try:
        #     ser = serial.Serial("COM10", 9600, timeout = 1) 

        # except:   
        #     pass
        # num = ("P,Temp,"+thisdict["Temp"] + "," + "Relay," + thisdict["Relay"] + ",")
        # thisdict["Temp"] = str(count)
        # thisdict["Relay"] = str(coin)
        coin = False
        if tog == 0:
            # arduino.write(num.encode('utf-8'))
            tog = 1
            time.sleep(.05)
            # print("Write")

        elif tog > 0:
            data = arduino.readline()
            data = str(data.decode())
            tog += 1
            time.sleep(.1)
            SerialDataIn = data.split(",")
            # print("read")
            if data:
                
                print("Raw Data: ", data)
                # print("Splitted Data: ", SerialDataIn)
                temp = int(SerialDataIn[2])
                thisdict["Temp"] = temp
                thisdict["Relay"] = SerialDataIn[4]
                thisdict["Status"] = SerialDataIn[5]

                def retrieveData(Btemp, Brelval):  #bluetooth relay vale, Bluetooth temp
                    # ser.write(b'P,24,0,')
                    bval = "P," + str(Btemp) + "," + str(Brelval) + ","
                    print("Ble: ", bval)
                    ser.write(bval.encode('utf-8'))
                    # dataBle = ser.readline().decode('ascii')
                    # return dataBle

                if temp > 30:
                    s = ttk.Style()
                    s.theme_use('clam')
                    s.configure("red.Horizontal.TProgressbar",
                                foreground='red', background='red')
                    bar.config(style="red.Horizontal.TProgressbar")

                else:
                    s = ttk.Style()
                    s.theme_use('clam')
                    s.configure("green.Horizontal.TProgressbar",
                                foreground='green', background='green')
                    bar.config(style="green.Horizontal.TProgressbar")

                retrieveData(thisdict["Temp"],thisdict["Relay"])

                Temp.config(text=thisdict["Temp"])
                RelayVal.config(text=thisdict["Relay"])
                if thisdict["Status"] == "B":
                    RangeS.config(text="Below Range")
                    # retrieveData(thisdict["Temp"],thisdict["Relay"])
                    


                    
                elif thisdict["Status"] == "I":
                    RangeS.config(text="IN Range")
                    # retrieveData(thisdict["Temp"],thisdict["Relay"])
                    


                elif thisdict["Status"] == "A":
                    RangeS.config(text="Above Range")
                    # retrieveData(thisdict["Temp"],thisdict["Relay"])
                    



                bar.config(value=temp)
                # bar['value']+=10
                time.sleep(.09)
                coin = True

                # trig += 1
                root.update()
        if tog >= 3:
            tog = 0
            count += 1
            # print("RUN-TOG-3")
            # trig += 1
        compareTemp = int(thisdict["Temp"])
        if compareTemp > 25 and compareTemp < 30:
            coin = False
        elif compareTemp < 25:
            coin = True
        else:
            coin = False

# def retrieveData(Btemp, Brelval):
#     # ser.write(b'P,24,0,')
#     bval = "P," + str(Btemp) + "," + str(Brelval) + ","
#     print("Ble: ", bval)
#     ser.write(bval.encode('utf-8'))
#     # dataBle = ser.readline().decode('ascii')
#     # return dataBle

# def Hello():
#     retrieveData(thisdict["Temp"],thisdict["Relay"])


btn = Button(root, text='Start Reflow', bd='5',
                        command=submit)
btn.place(x=275, y=40)

# btn1 = Button(root, text='Start ble', bd='5',
#                         command=Hello)
# btn1.place(x=275, y=140)
# infinite loop which is required to run tkinter program infinitely
# until an interrupt occurs
root.mainloop()

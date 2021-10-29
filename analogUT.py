import threading

import Adafruit_BBIO.ADC as ADC
import csv
import time

# Legger inn addresse til bus i en variabel
bus = "/sys/bus/w1/devices/28-00000bc667df/w1_slave"

temp = open(bus, "r").read()
temp = (float(temp.split("t=")[-1]) / 1000)
endThread = True


def Thread_getTemp():
    global temp
    global endThread

    while endThread:
        # leser temperaturverdi fra bus
        temp = open(bus, "r").read()
        temp = (float(temp.split("t=")[-1]) / 1000)
    print("Ending Thread..")


thread = threading.Thread(target=Thread_getTemp)
thread.start()

# Seter opp analoge porter på Beaglebone
ADC.setup()

# åpner en tom fil med skrivetilgang, og legger den i en variabel
f = open('/home/pycharm/csv', 'w')

# starter en instans av writer, med den tomme filen
writer = csv.writer(f)

# tar vare på første tidsberegning i variabel first
first = time.time()

# en for-løkke som settes til 150 runder
for i in range(150):
    # leser verdien fra pin P9_40
    value = ADC.read("P9_40")

    # legger til tida i millisekund, og lest verdi i et array, som legges i variabel data
    data = [(time.time() - first) * 1000, value, temp]

    # skriver avlest temperatur til terminalvindu, fjerner uønsket karakterer,
    # regner om til celsius
    print("Temperaturen er " + str(temp) + " grader")

    # skriver arrayet data til cvs, via writer
    writer.writerow(data)

    # skriver lest verdi til terminal vinduet
    print(value)

    # setter en sleep verdi på 0.15, dvs det kjøres en måling flere ganger i sekundet.
    time.sleep(0.15)

# lukker filen
f.close()
endThread = False

# importing the dependencies
import os
import glob
import time
from libdw import pyrebase
import numpy as np

url = "https://temperature-981f5.firebaseio.com/" # This is to connect to our firebase 
apikey = "-"

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# base code to calculate temperature
os.system('modprobe w1-gpio') # using the default GPIO(4)
os.system('modprobe w1-therm') 

base_dir = '/sys/bus/w1/devices/' # change of directory to the devices
device_folder = glob.glob(base_dir + '28*')[0] # connect to the unique temperature sensor ID
device_file = device_folder + '/w1_slave'
start = time.time() # start of the timing

# this is to read the raw file that the sensor append the values to
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# this is to read the temperature and returning it in a tuple form
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        a = time.time() - start
        return temp_c, a # returns the temperature in celcius and time(a)

# appending the first 5 values of gradient in the time taken to reach.
lstemp = []
lstime = []
lstemp.append(read_temp()[0]) # this is the temperature in celcius
lstime.append(read_temp()[1]) # this is the time

lstemp.append(read_temp()[0])
lstime.append(read_temp()[1])

lstemp.append(read_temp()[0])
lstime.append(read_temp()[1])

lstemp.append(read_temp()[0])
lstime.append(read_temp()[1])

lstemp.append(read_temp()[0])
lstime.append(read_temp()[1])


m,b = np.polyfit(lstime,lstemp,1) # this is to calculate the gradient of the 5 data values
print(m) #gradient
print(time.time() - start)
value = str(round(19.29787009 * float(m) + 26.806586355170374 ,2)) # we used this linear equation as our Rpi cannot run smoothly with kivy
time1 = str(round(time.time() - start,3)) # this gives the time taken for the 5 values
print(value)
db.child("temp").set(value) # this uploads predicted temperature to the firebase one time
db.child("time").set(time1) # this uploads the time taken to predict to firebase

print("Hao Le:: Now printing sensor data") # this is to print the real time temperature data and time
while True:
    print(read_temp())
    db.child('temp_actual').set(read_temp()[0]) # this is to upload to firebase continuously in the while loop
    db.child('time_actual').set(round(read_temp()[1],2)) # this is to upload the real time data of the time when the app is started
    
    # we decided to upload the time assosciated with the it takes to predict into firebase, to provide a more accurate time reading, instead
    # of using the kivy clock and inbuilt timer in our GUI as it doesnt sync as well for the time.




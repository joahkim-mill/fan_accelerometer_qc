import time
import pandas as pd
import board 
import busio 
import adafruit_adxl34x 
import numpy as np 
from collections import deque

## make sure to change the name of the file it gets saved to, or it will get overwritten
i2c = board.I2C() 
accelerometer = adafruit_adxl34x.ADXL345(i2c)

print("type in a name for the data to get saved to [excluding .csv]")
filename = input() 
filepath = f"/home/pi/fan_qc/vibration_testing/accel_data/{filename}.csv"
tf = 10 # endtime [sec]

# initialize deque to contain all of the data --> O(1) time
accel_data = deque()  # [time [sec], x_acc, y_acc, z_acc] 

print("Beginning data collection:")
t0 = time.time()  # starting time
while (time.time() - t0 < tf):
    accel_data.append([(time.time() - t0), accelerometer.acceleration[0], accelerometer.acceleration[1], accelerometer.acceleration[2]])
   
a=pd.DataFrame(accel_data)
a.columns=["time", "x_accel", "y_accel", "z_accel"]  # time[s], accelerations [m/s^2]
a.to_csv(filepath)
print(f"Success! File saved to: {filepath}")
import time
import pandas as pd
import board 
import busio 
import adafruit_adxl34x 
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import numpy as np 

i2c = board.I2C() 
accelerometer = adafruit_adxl34x.ADXL345(i2c)
i=0
tf = 5  # endtime [sec]
# sample_rate = accelerometer.data_rate  # currently 10 [Hz] ? but can be changed
sample_rate = 500
dt = 1/sample_rate
num_samples = (int)(tf * sample_rate)

# initialize list to contain all of the data
accel_data = []  # [time [sec], x_acc, y_acc, z_acc]
t0 = time.time()  # starting time 

for i in range(num_samples):
    # print out accelerations [m/s^2]
    # print(time.time()-t0, "%f %f %f" % accelerometer.acceleration)
    accel_data.append([(time.time() - t0), accelerometer.acceleration[0], accelerometer.acceleration[1], accelerometer.acceleration[2]])
    time.sleep(dt)
   
# a=pd.DataFrame(accel_data)
# a.columns=["time", "x_accel", "y_accel", "z_accel"]  # time[s], accelerations [m/s^2]
# print(a)
# a.to_csv("/home/pi/fan_qc/sample_acceleration.csv")

a = np.asarray(accel_data)[:, 1:] # leave out the time for now
v = [np.zeros((3,))] # initialize velocity as 0
p = [(0,0,0)] # initialize position as 0

for j in range(1, num_samples):
    v.append(a[j-1]*dt + v[j-1])
    p.append(0.5*a[j-1]*dt*dt + v[j-1]*dt + p[j-1])

v = np.asarray(v)
p = np.asarray(p)
t = np.arange(0, tf, dt)

fig = make_subplots(rows=3, cols=1,
                    subplot_titles=("X", "Y", "Z")
                    )

fig.add_trace(
    go.Scatter(x=t, y=a[:,0], name="accel"),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t, y=v[:,0], name="vel"),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t, y=p[:,0], name="pos"),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=t, y=a[:,1], name="accel"),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t, y=v[:,1], name="vel"),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t, y=p[:,1], name="pos"),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=t, y=a[:,2], name="accel"),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t, y=v[:,2], name="vel"),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t, y=p[:,2], name="pos"),
    row=3, col=1
)

fig.show()
"""

# vel_data = []

v_x = [0] # start off with no velocity
p_x = [0] 
# v_x = 
# print(np.asarray(accel_data))
a_x = np.asarray(accel_data)[:,1]
# print(a_x)
## integrate twice for position --> plot to visualize, fft for frequencies (possibly smooth data)
for j in range(1, num_samples):
    # v_f = a_i*t + v_i
    # p_f = 1/2 * a_i * t^2 + v_i*t + p_i
    # v_x[j] = a_x[j-1] * dt + v_x[j-1]  # using constant dt for now based on data rate, but could change to actual change in t later on
    v_x.append(a_x[j-1] * dt + v_x[j-1])
    p_x.append(0.5*a_x[j-1]*dt*dt + v_x[j-1]*dt + p_x[j-1])

v_x = np.asarray(v_x)
p_x = np.asarray(p_x)
t = np.arange(0, tf, dt)
print(t.shape)
print(a_x.shape)
print(v_x.shape)
print(p_x.shape)
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=a_x, name="accel_x"))
fig.add_trace(go.Scatter(x=t, y=v_x, name="vel_x"))
fig.add_trace(go.Scatter(x=t, y=p_x, name="pos_x"))
fig.show()

"""
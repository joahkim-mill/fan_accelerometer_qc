import pandas as pd 
import numpy as np 
from plotly import graph_objects as go 

# read in csv to access data 
filename = "./accel_data/bad_1.csv" # depends on which folder you're in
accelerations = pd.read_csv(filename)

# make them into columns
t = np.asarray(accelerations["time"]).reshape((-1,1))
a_x = np.asarray(accelerations["x_accel"]).reshape((-1,1))
a_y = np.asarray(accelerations["y_accel"]).reshape((-1,1))
a_z = np.asarray(accelerations["z_accel"]).reshape((-1,1))
a = np.hstack((a_x, a_y, a_z))

num_samples = t.shape[0]
dt = t[1:] - t[:-1] 

# integrate twice to get position 
v_x = np.zeros((num_samples, 1))
p_x = np.zeros((num_samples, 1))

v_y = np.zeros((num_samples, 1))
p_y = np.zeros((num_samples, 1))

v_z = np.zeros((num_samples, 1))
p_z = np.zeros((num_samples, 1))

for i in range(1, num_samples):
    v_x[i] = a_x[i-1] * dt[i-1] + v_x[i-1]
    p_x[i] = 0.5 * a_x[i-1] * dt[i-1] * dt[i-1] + v_x[i-1] * dt[i-1] + p_x[i-1]

    v_y[i] = a_y[i-1] * dt[i-1] + v_y[i-1]
    p_y[i] = 0.5 * a_y[i-1] * dt[i-1] * dt[i-1] + v_y[i-1] * dt[i-1] + p_y[i-1]

    v_z[i] = a_z[i-1] * dt[i-1] + v_z[i-1]
    p_z[i] = 0.5 * a_z[i-1] * dt[i-1] * dt[i-1] + v_z[i-1] * dt[i-1] + p_z[i-1]


# plot --> based on plot, if very off, apply some smoothing/interpolation/calibration/re-zeroing ?
# fig_x = go.Figure()
# fig_x.add_trace(go.Scatter(x=t.ravel(), y=a_x.ravel(), name="accel_x"))
# fig_x.add_trace(go.Scatter(x=t.ravel(), y=v_x.ravel(), name="vel_x"))
# fig_x.add_trace(go.Scatter(x=t.ravel(), y=p_x.ravel(), name="pos_x"))
# fig_x.update_layout(title="Plot of Vibrating Fan X")

# fig_y = go.Figure()
# fig_y.add_trace(go.Scatter(x=t.ravel(), y=a_y.ravel(), name="accel_y"))
# fig_y.add_trace(go.Scatter(x=t.ravel(), y=v_y.ravel(), name="vel_y"))
# fig_y.add_trace(go.Scatter(x=t.ravel(), y=p_y.ravel(), name="pos_y"))
# fig_y.update_layout(title="Plot of Vibrating Fan Y")

fig_z = go.Figure()
fig_z.add_trace(go.Scatter(x=t.ravel(), y=a_z.ravel(), name="accel_z"))
fig_z.add_trace(go.Scatter(x=t.ravel(), y=v_z.ravel(), name="vel_z"))
fig_z.add_trace(go.Scatter(x=t.ravel(), y=p_z.ravel(), name="pos_z"))
fig_z.update_layout(title="Plot of Vibrating Fan Z")

# fig_x.show()
# fig_y.show()
fig_z.show()
# fft for frequencies


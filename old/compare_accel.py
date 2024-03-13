import pandas as pd 
import numpy as np 
from plotly import graph_objects as go 
from plotly.subplots import make_subplots
from scipy.signal import find_peaks 


#region -- good fan data
#### --------- GOOD FAN DATA --------- ####
# -- GOOD 7 -- #
# read in csv to access data 
good7 = pd.read_csv("./accelerometer/accel_data/good_7.csv")

# make them into columns
t_g7 = np.asarray(good7["time"])
ax_g7 = np.asarray(good7["x_accel"])
ay_g7 = np.asarray(good7["y_accel"])
az_g7 = np.asarray(good7["z_accel"])
a_g7 = np.hstack((ax_g7.reshape((-1,1)), ay_g7.reshape((-1,1)), az_g7.reshape((-1,1))))

# -- GOOD 8 -- #
# read in csv to access data 
good8 = pd.read_csv("./accelerometer/accel_data/good_8.csv")

# make them into columns
t_g8 = np.asarray(good8["time"])
ax_g8 = np.asarray(good8["x_accel"])
ay_g8 = np.asarray(good8["y_accel"])
az_g8 = np.asarray(good8["z_accel"])
a_g8 = np.hstack((ax_g8.reshape((-1,1)), ay_g8.reshape((-1,1)), az_g8.reshape((-1,1))))

# -- GOOD 9 -- #
# read in csv to access data 
good9 = pd.read_csv("./accelerometer/accel_data/good_9.csv")

# make them into columns
t_g9 = np.asarray(good9["time"])
ax_g9 = np.asarray(good9["x_accel"])
ay_g9 = np.asarray(good9["y_accel"])
az_g9 = np.asarray(good9["z_accel"])
a_g9 = np.hstack((ax_g9.reshape((-1,1)), ay_g9.reshape((-1,1)), az_g9.reshape((-1,1))))

# -- GOOD 10 -- #
# read in csv to access data 
good10= pd.read_csv("./accelerometer/accel_data/good_10.csv")

# make them into columns
t_g10 = np.asarray(good10["time"])
ax_g10 = np.asarray(good10["x_accel"])
ay_g10 = np.asarray(good10["y_accel"])
az_g10 = np.asarray(good10["z_accel"])
a_g10 = np.hstack((ax_g10.reshape((-1,1)), ay_g10.reshape((-1,1)), az_g10.reshape((-1,1))))

#endregion -- good fan data

#region -- bad fan data
#### --------- BAD FAN DATA --------- ####
# -- BAD 1 -- #
bad1 = pd.read_csv("./accelerometer/accel_data/bad_1.csv")

# make them into columns
t_b1 = np.asarray(bad1["time"])
ax_b1 = np.asarray(bad1["x_accel"])
ay_b1 = np.asarray(bad1["y_accel"])
az_b1 = np.asarray(bad1["z_accel"])
a_b1 = np.hstack((ax_b1.reshape((-1,1)), ay_b1.reshape((-1,1)), az_b1.reshape((-1,1))))

# -- BAD 2 -- #
bad2 = pd.read_csv("./accelerometer/accel_data/bad_2.csv")

# make them into columns
t_b2 = np.asarray(bad2["time"])
ax_b2 = np.asarray(bad2["x_accel"])
ay_b2 = np.asarray(bad2["y_accel"])
az_b2 = np.asarray(bad2["z_accel"])
a_b2 = np.hstack((ax_b2.reshape((-1,1)), ay_b2.reshape((-1,1)), az_b2.reshape((-1,1))))

# -- BAD 3 -- #
bad3 = pd.read_csv("./accelerometer/accel_data/bad_3.csv")

# make them into columns
t_b3 = np.asarray(bad3["time"])
ax_b3 = np.asarray(bad3["x_accel"])
ay_b3 = np.asarray(bad3["y_accel"])
az_b3 = np.asarray(bad3["z_accel"])
a_b3 = np.hstack((ax_b3.reshape((-1,1)), ay_b3.reshape((-1,1)), az_b3.reshape((-1,1))))

#endregion -- bad fan data

data_g = [a_g7, a_g8, a_g9,]  ## NOTE : exluding good fan 10 bc it's not actually that good --> i think it should be labeled bad
data_b = [a_b1, a_b2, a_b3] 

num_fans_g = len(data_g)
num_fans_b = len(data_b)


#region -- plots
#### --------- CREATE PLOTS --------- ####
fig = make_subplots(rows=3, cols=1,
                    subplot_titles=("X", "Y", "Z"), 
                    vertical_spacing=0.05
                    )

# acceleration in x
fig.add_trace(
    go.Scatter(x=t_b1, y=ax_b1, name="ax_b1", line=dict(color="#aa81f0")),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t_b2, y=ax_b2, name="ax_b2", line=dict(color="#41adf0")),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t_b3, y=ax_b3, name="ax_b3", line=dict(color="#40b892")),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t_g7, y=ax_g7, name="ax_g7", line=dict(color="#f5bad4")),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t_g8, y=ax_g8, name="ax_g8", line=dict(color="#f5bad4")),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=t_g9, y=ax_g9, name="ax_g9", line=dict(color="#f5bad4")),
    row=1, col=1
)

# acceleration in y
fig.add_trace(
    go.Scatter(x=t_b1, y=ay_b1, name="ay_b1", line=dict(color="#aa81f0")),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t_b2, y=ay_b2, name="ay_b2", line=dict(color="#41adf0")),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t_b3, y=ay_b3, name="ay_b3", line=dict(color="#40b892")),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t_g7, y=ay_g7, name="ay_g7", line=dict(color="#f5bad4")),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t_g8, y=ay_g8, name="ay_g8", line=dict(color="#f5bad4")),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=t_g9, y=ay_g9, name="ay_g9", line=dict(color="#f5bad4")),
    row=2, col=1
)

# acceleration in z
fig.add_trace(
    go.Scatter(x=t_b1, y=az_b1, name="az_b1", line=dict(color="#aa81f0")),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t_b2, y=az_b2, name="az_b2", line=dict(color="#41adf0")),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t_b3, y=az_b3, name="az_b3", line=dict(color="#40b892")),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t_g7, y=az_g7, name="az_g7", line=dict(color="#f5bad4")),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t_g8, y=az_g8, name="az_g8", line=dict(color="#f5bad4")),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=t_g9, y=az_g9, name="az_g9", line=dict(color="#f5bad4")),
    row=3, col=1
)

fig.update_layout(title="Comparison of Acceleration Data between Fans", 
                  height = 900,
                  width = 1200)
fig.show()

#### ------ END PLOTS -------- ####

#endregion -- plots


#region -- calc stats

#### ------ CALCULATE STATS ------- ####

# 1. take averages of raw data : means are all pretty similar ---> std dev looks promising !! the bad ones are roughly 2x those of the good ones
print("good fans std dev (of absolute values)")
avg_std_g = np.zeros((3,))
for g in data_g: 
    # print(f"avg : ", np.mean(g, axis=0))
    # print(f"std dev : ", np.std(g, axis=0))
    std_dev = np.std(np.abs(g), axis=0)
    avg_std_g += std_dev
    print(" "*7, std_dev)

avg_std_g = avg_std_g / num_fans_g
print("avg std dev of good fans: ", avg_std_g)
print("-" * 50)

print("bad fans std dev (of absolute values)")
avg_std_b = np.zeros((3,))
for b in data_b:
    # print(f"avg : ", np.mean(b, axis=0))
    # print(f"std dev : ", np.std(b, axis=0))
    std_dev = np.std(np.abs(b), axis=0)
    avg_std_b += std_dev
    print(" "*7, std_dev)

avg_std_b = avg_std_b / num_fans_b
print("avg std dev of bad fans: ", avg_std_b)
print("-" * 50)


"""
# 2. max [absolute] amplitude --> doens't seem relevant ... except the y accel for bad fans are pretty bad
# print("good fans")
# for g in data_g:
#     # absolute = np.abs(g)
#     print("max amplitude : ", np.amax(g, axis=0))

# print("bad fans")
# for b in data_b:
#     # absolute = np.abs(b)
#     print("max amplitude : ", np.amax(b, axis=0))
"""

"""
# 3. use find peaks ?? FINISH HERE !
fig = go.Figure()
fig_b = go.Figure()
t_g = [t_g7, t_g8, t_g9]
t_b = [t_b1, t_b2, t_b3]
threshold = [1, 1, 11.25]

num_peaks_g = np.zeros((num_fans_g, 3)) # each column is an axis, each row is a good fan
for fan in range(num_fans_g):
    for axis in range(3):
        peaks, _ = find_peaks(data_g[fan][:,axis], threshold[axis])
        fig.add_trace(go.Scatter(x=t_g[fan].ravel(), y=data_g[fan][:,axis].ravel(), name=f"good fan {fan + 7}_axis {axis}"))
        fig.add_trace(go.Scatter(x=t_g[fan][peaks], y=data_g[fan][:,axis][peaks], mode='markers', name=f"good fan {fan + 7}_axis {axis} peaks"))
        num_peaks_g[fan, axis] = peaks.shape[0] 
print("Number of peaks above threshold for good fans :")
print(num_peaks_g)

num_peaks_b = np.zeros((num_fans_b, 3)) # each column is an axis, each row is a good fan
for fan in range(num_fans_b):
    for axis in range(3):
        peaks, _ = find_peaks(data_b[fan][:,axis], threshold[axis])
        fig_b.add_trace(go.Scatter(x=t_b[fan].ravel(), y=data_b[fan][:,axis].ravel(), name=f"bad fan {fan + 1}_axis {axis}"))
        fig_b.add_trace(go.Scatter(x=t_b[fan][peaks], y=data_b[fan][:,axis][peaks], mode='markers', name=f"bad fan {fan + 1}_axis {axis} peaks"))
        num_peaks_b[fan, axis] = peaks.shape[0] 
print("Number of peaks above threshold for bad fans : ")
print(num_peaks_b)

fig.update_layout(height=400, width=1000)
fig_b.update_layout(height=400, width=1000)
# fig.show()
# fig_b.show()
"""


# 4.  maybe determine at what theshold the amplitude hits a percentile ?


#endregion -- calc stats
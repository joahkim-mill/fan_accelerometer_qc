import pandas as pd
import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from scipy.fft import fft, fftfreq
# import streamlit as st 


dataname = 'P1'
data = pd.read_csv(f'./factory_data/{dataname}.csv')
# print(data)
data.columns = ['index', 'time', 'x_accel', 'y_accel', 'z_accel']

t = np.asarray(data["time"])
ax = np.asarray(data["x_accel"])
ay = np.asarray(data["y_accel"])
az = np.asarray(data["z_accel"])
a = np.hstack((ax.reshape((-1,1)), ay.reshape((-1,1)), az.reshape((-1,1))))  # [ax , ay, az] columnwise

N = len(t)
sample_rate = 1100 # Hz 
T = 1/sample_rate 
yf_z = fft(az)
xf_z = fftfreq(N, T)[:N//2]
y_z = 2.0/N * abs(yf_z[0:N//2])

fig = go.Figure()
# fig.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=f"Bad Fan - Case 1", line=dict(width=0.75, color='blue')) )

dataname = 'P2'
data = pd.read_csv(f'./factory_data/{dataname}.csv')
# print(data)
data.columns = ['index', 'time', 'x_accel', 'y_accel', 'z_accel']

t = np.asarray(data["time"])
ax = np.asarray(data["x_accel"])
ay = np.asarray(data["y_accel"])
az = np.asarray(data["z_accel"])
a = np.hstack((ax.reshape((-1,1)), ay.reshape((-1,1)), az.reshape((-1,1))))  # [ax , ay, az] columnwise

N = len(t)
sample_rate = 1100 # Hz 
T = 1/sample_rate 
yf_z = fft(az)
xf_z = fftfreq(N, T)[:N//2]
y_z = 2.0/N * abs(yf_z[0:N//2])

fig.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=f"Bad Fan - Case 2", line=dict(width=0.75, color='blue')) )

dataname = 'P5'
data = pd.read_csv(f'./factory_data/{dataname}.csv')
# print(data)
data.columns = ['index', 'time', 'x_accel', 'y_accel', 'z_accel']
t = np.asarray(data["time"])
ax = np.asarray(data["x_accel"])
ay = np.asarray(data["y_accel"])
az = np.asarray(data["z_accel"])
a = np.hstack((ax.reshape((-1,1)), ay.reshape((-1,1)), az.reshape((-1,1))))  # [ax , ay, az] columnwise

N = len(t)
sample_rate = 1100 # Hz 
T = 1/sample_rate 
yf_z = fft(az)
xf_z = fftfreq(N, T)[:N//2]
y_z = 2.0/N * abs(yf_z[0:N//2])
fig.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=f"Good Fan", line=dict(width=0.75, color='orange')))
thsd_1_x = [0, 200]
thsd_1_y = [0.4, 0.4]
thsd_2_x = [201, 550]
thsd_2_y = [0.2, 0.2]
fig.add_trace(go.Scatter(x=thsd_1_x, y=thsd_1_y, name='Threshold 1', line=dict(color='red')))
fig.add_trace(go.Scatter(x=thsd_2_x, y=thsd_2_y, name='Threshold 2', line=dict(color='green')))
fig.update_layout(title=f"FFT Plot - Case 2 Comparison", xaxis_title='Hz', 
                plot_bgcolor='white')
fig.update_yaxes(range=[0, 1])
fig.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
fig.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
fig.show()

# st.plotly_chart(fig)

# good = [11, 12, 14, 23, 28, 68, 73, 74, 76, 77]
# borderline = [13, 19, 32, 69, 71]
# bad = [6, 10, 33, 70, 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b19', 'b20']

# fig = make_subplots(rows=3, cols=1,
#                     subplot_titles=("X", "Y", "Z"), 
#                     vertical_spacing=0.05
#                     )
# for bl in borderline:
#     dataname = bl
#     data = pd.read_csv(f'./new_accel_data/100 pwm/{dataname}.csv',)

# # fig = go.Figure()

#     t = np.asarray(data["time"])
#     ax = np.asarray(data["x_accel"])
#     ay = np.asarray(data["y_accel"])
#     az = np.asarray(data["z_accel"])
#     a = np.hstack((ax.reshape((-1,1)), ay.reshape((-1,1)), az.reshape((-1,1))))  # [ax , ay, az] columnwise

#     N = len(t)
#     sample_rate = 1100 # Hz 
#     T = 1/sample_rate 
#     yf_x = fft(ax)
#     xf_x = fftfreq(N, T)[:N//2]
#     y_x = 2.0/N * abs(yf_x[0:N//2])
#     fig.add_trace(go.Scatter(x=xf_x, y=y_x, line_shape='linear', name=f"{bl}_x"),
#                   row=1, col=1) 

#     yf_y = fft(ay)
#     xf_y = fftfreq(N, T)[:N//2]
#     y_y = 2.0/N * abs(yf_y[0:N//2])
#     fig.add_trace(go.Scatter(x=xf_y, y=y_y, line_shape='linear', name=f"{bl}_y"),
#                   row=2,col=1) 

#     yf_z = fft(az)
#     xf_z = fftfreq(N, T)[:N//2]
#     y_z = 2.0/N * abs(yf_z[0:N//2])
#     fig.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=f"{bl}_z"),
#                   row=3,col=1) 
#     # print(f"{dataname}: {np.sum(y_z[1:] > 0.4)}")

# fig.update_layout(title=f"Fan FFT of iffy fans at 100 pwm", 
#                 xaxis_title="Frequency [Hz]", 
#               #   yaxis_title="SPL [dB]",
#                 height=1000,
#                 width=1200)
# fig.update_yaxes(range=[0, 1])
# fig.show()

# fig_g = make_subplots(rows=3, cols=1,
#                     subplot_titles=("X", "Y", "Z"), 
#                     vertical_spacing=0.05
#                     )
# for g in good:
#     dataname = g
#     data = pd.read_csv(f'./new_accel_data/100 pwm/{dataname}.csv',)

# # fig = go.Figure()

#     t = np.asarray(data["time"])
#     ax = np.asarray(data["x_accel"])
#     ay = np.asarray(data["y_accel"])
#     az = np.asarray(data["z_accel"])
#     a = np.hstack((ax.reshape((-1,1)), ay.reshape((-1,1)), az.reshape((-1,1))))  # [ax , ay, az] columnwise

#     N = len(t)
#     sample_rate = 1100 # Hz 
#     T = 1/sample_rate 
#     yf_x = fft(ax)
#     xf_x = fftfreq(N, T)[:N//2]
#     y_x = 2.0/N * abs(yf_x[0:N//2])
#     fig_g.add_trace(go.Scatter(x=xf_x, y=y_x, line_shape='linear', name=f"{g}_x"),
#                   row=1, col=1) 

#     yf_y = fft(ay)
#     xf_y = fftfreq(N, T)[:N//2]
#     y_y = 2.0/N * abs(yf_y[0:N//2])
#     fig_g.add_trace(go.Scatter(x=xf_y, y=y_y, line_shape='linear', name=f"{g}_y"),
#                   row=2,col=1) 

#     yf_z = fft(az)
#     xf_z = fftfreq(N, T)[:N//2]
#     y_z = 2.0/N * abs(yf_z[0:N//2])
#     fig_g.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=f"{g}_z"),
#                   row=3,col=1) 

# fig_g.update_layout(title=f"Fan FFT of good fans at 100 pwm", 
#                 xaxis_title="Frequency [Hz]", 
#               #   yaxis_title="SPL [dB]",
#                 height=1000,
#                 width=1200)
# fig_g.update_yaxes(range=[0, 1])
# fig_g.show()


# # for b in bad:
# #     dataname = b
# #     data = pd.read_csv(f'./new_accel_data/100 pwm/{dataname}.csv',)

# # # fig = go.Figure()

# #     t = np.asarray(data["time"])
# #     ax = np.asarray(data["x_accel"])
# #     ay = np.asarray(data["y_accel"])
# #     az = np.asarray(data["z_accel"])
# #     a = np.hstack((ax.reshape((-1,1)), ay.reshape((-1,1)), az.reshape((-1,1))))  # [ax , ay, az] columnwise

# #     N = len(t)
# #     sample_rate = 1100 # Hz 
# #     T = 1/sample_rate 
# #     yf_x = fft(ax)
# #     xf_x = fftfreq(N, T)[:N//2]
# #     y_x = 2.0/N * abs(yf_x[0:N//2])
# #     fig.add_trace(go.Scatter(x=xf_x, y=y_x, line_shape='linear', name=f"{b}_x"),
# #                   row=1, col=1) 

# #     yf_y = fft(ay)
# #     xf_y = fftfreq(N, T)[:N//2]
# #     y_y = 2.0/N * abs(yf_y[0:N//2])
# #     fig.add_trace(go.Scatter(x=xf_y, y=y_y, line_shape='linear', name=f"{b}_y"),
# #                   row=2,col=1) 

# #     yf_z = fft(az)
# #     xf_z = fftfreq(N, T)[:N//2]
# #     y_z = 2.0/N * abs(yf_z[0:N//2])
# #     fig.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=f"{b}_z"),
# #                   row=3,col=1)  
# #     print(f"{dataname}: ",np.sum(y_z[1:] > 0.4))  #don't want to include spike at 0Hz

# # fig.update_layout(title=f"Fan FFT of bad fans at 100 pwm", 
# #                 xaxis_title="Frequency [Hz]", 
# #               #   yaxis_title="SPL [dB]",
# #                 height=1000,
# #                 width=1600)
# # fig.update_yaxes(range=[0, 1])
# # # fig.show()
# # st.plotly_chart(fig)
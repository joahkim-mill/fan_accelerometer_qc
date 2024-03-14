from src.utils.testing import Testing ,Comparator, Assembly, Test
from src.utils.oscar import Oscar
from src.utils.factory_ble_scanner import BleScanner
from src.utils.adxl345 import ADXL345
from time import sleep, time 
from collections import deque
import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import plotly.graph_objects as go
import threading

class O2Fan:

    # Init will be called once when chewie-test starts
    def __init__(self) -> None:

        print("Station Init")

        # Mutex to limit 1 test to run at a time
        self.mutex = threading.Lock()

        # Testing and Oscar objects will be added automatically, set as None for now
        self.oscar: Oscar = Oscar(skip_board_check = True, device_version = 'o2')
        # self.oscar: Oscar = None
        self.test: Testing = None
        self.accelerometer = ADXL345(0x53)
        self.ble = BleScanner()
        self.input = ''

        # Define the test sequence
        self.tests = [
            # Test(self.check_connection, 'Check Connection to Device'),
            Test(self.test_fan, 'Test Fan')
        ]

        # Station name that shows up in Grafana
        self.station_name = 'O2 Fan Station'

        # Define the MES station here, None will push nothing to MES
        self.mes_station = None

        # Text displayed to operator
        self.test_status_text = 'Station is ready'

    # def check_connection(self):
    #     connected = self.oscar.serial_number != None
    #     # self.test.test_parameter(connected, 'Check connection to oscar', None, True, None, comparator = Comparator.E)
    #     # if connected and self.oscar.serial_number != None:
    #     self.test.serial_number = self.oscar.serial_number
    #     print(f'Setting serial number to {self.test.serial_number}')
    #     return connected

    # def check_connection(self):
    #     connected = self.oscar.checkConnection()
    #     self.test.test_parameter(connected, 'Check connection to oscar', None, True, None, comparator = Comparator.E)
    #     if connected and self.oscar.serial_number != None:
    #         self.test.serial_number = self.oscar.serial_number
    #         print(f'Setting serial number to {self.test.serial_number}')
    #     return connected

    # Test sequence will not start until this function returns True
    # input is the input from the serial number text field
    # Check things like E-Stop, lid switch, serial numbers
    def ready(self, input) -> bool:
        self.sn = input
        ## !! replace this since the delta fan serial number != self.input  ??
        if input[:3] == 'DEL': 
            return True
        else:
            self.test_status_text = f'Invalid serial number {input}'
            return False

    # Cleanup will be called once all tests are complete or an error occurs
    def cleanup(self):
        pass

    # Declare as many test functions as you want with any name you want
    def test_fan(self):
        o = self.oscar
        t = self.test
    
        ## !! change to actual sn 
        sn = self.sn
        # print("sn: ", sn)
        t.request_ok_input('Put accelerometer on fan')
        t.request_ok_input('Place fan on fixture')
       
        sleep(3)
        # Show prompt and request OK to be pressed
        # t.request_ok_input("Do something and press OK when done")

        t.set_prompt("Testing at 45 PWM")
        ## !! doesn't move fan at all !
        o.setExhaustFanSpeed(45)  # wait for ramp up
        sleep(5)

        ## collect data and save / export to grafana
        # change to sn eventually
        ## !! will we need to locally save data files ??
        filepath = f"/home/pi/ChewieFactoryTest/45pwm/{sn}.csv"
        
        a_45, results_45 = self.collect_data(sn, filepath)
        ## export to grafana

        # set fan speed to 100pwm
        t.set_prompt("Testing at 100PWM")
        ## !! doesn't move fan
        o.setExhaustFanSpeed(100)
        sleep(5)  # wait to ramp up

        ## collect data and save  / export 
        # change sn
        filepath = f"/home/pi/ChewieFactoryTest/100pwm/{sn}_100pwm.csv"
        a_100, results_100 = self.collect_data(sn, filepath)
        ## export to grafana

        ## turn off fan
        o.setExhaustFanSpeed(0)
        t.set_prompt("Turning off fans")

        # output plot (& save plots ?) 
        t_sec = np.asarray(a_100["time"])
        az = np.asarray(a_100["z_accel"])

        N = len(t_sec)
        sample_rate = 1100 # Hz 
        T = 1/sample_rate 
        yf_z = fft(az)
        xf_z = fftfreq(N, T)[:N//2]
        y_z = 2.0/N * abs(yf_z[0:N//2])

        # plot and save plot of fft
        fig = self.plot_data(sn)  
        t.display_image(f"./plots/{sn}.png")

        result = self.is_it_good(xf_z, y_z)
        print(f"TEST: ", {result})
        if result == "FAIL":
            t.test_result = False

        # need to reformat from numpy array to dataframe for display_plot function
        # t.display_plot(xf_z, y_z, plot_title=f"FFT of {sn}", x_title="Hz")
       
        # output fail, pass message 
        # fft signal magnitudes [excluding 0hz] should be under 0.4 to be considered a good fan
        
        ## ! prints to serial, not testing page
        # if sum(results_100) < 1 :
        #     t.set_prompt("PASS : GOOD FAN") 
        # else:
        #     t.set_prompt("FAIL : BAD FAN")
        #     t.test_result = False

    
        # t.test_parameter(sum(results_100), 'Verify Fan Vibration [100PWM]', None, 0, 2)
        
        ## send pass/fail to grafana
  
    # function to collect data from accelerometer
    def collect_data(self, sn, filepath):
        accelerometer = self.accelerometer
        accel_data = deque()
        # filepath = f"/home/pi/ChewieFactoryTest/45pwm/{input}.csv"
        print("Beginning data collection for 10 seconds:")
        t0 = time()
        duration = 10

        tf = t0 + duration
        while (time() < tf):
            axes = accelerometer.get_all_axes()
            accel_data.append([(time() - t0), axes['x'], axes['y'], axes['z']])

        # save to csv
        a=pd.DataFrame(accel_data)
        a.columns=["time", "x_accel", "y_accel", "z_accel"]  # time[s], accelerations [m/s^2]
        a.to_csv(filepath)
        print(f"Success! File saved to: {filepath}")

        # analyze data with fft focusing on z_accel data for now
        t = np.asarray(a["time"]) 
        az = np.asarray(a["z_accel"])

        N = len(t)
        sample_rate = 1100 # Hz 
        T = 1/sample_rate 
        yf_z = fft(az)
        xf_z = fftfreq(N, T)[:N//2] # (5603,)
        y_z = 2.0/N * abs(yf_z[0:N//2])
        crossed_1 = np.sum(y_z[1:2100] > 0.4)
        crossed_2 = np.sum(y_z[2100:] > 0.2)

        #change to sn
        # print(f"{sn} : {crossed_1}, {crossed_2}")

        return a, (crossed_1, crossed_2)

    def is_it_good(self, x, y):

        threshold_y = [0]
        threshold_y1 = [0.5 for x in x[1:2100]]
        threshold_y2 = -(0.3/340) * x[2100:] + (0.5 + 0.3 / 350 * 210)
        # print("t y 1: ", threshold_y1)
        # print("t y 2: ", threshold_y2)

        threshold_y.extend(threshold_y1)
        threshold_y.extend(threshold_y2)

        y1 = y[1:2100]
        crossed_1 = y1[y[1:2100]>threshold_y[1:2100]]

        y2 = y[2100:]
        crossed_2 = y2[y[2100:] > threshold_y[2100:]]

        if len(crossed_1) > 1 and max(crossed_1) > 0.9:
            result = "FAIL"
        elif len(crossed_2) > 1:
            result = "FAIL"
        else :
            result = "PASS"

        return result
    
    def plot_data(self, sn):
        # dataname = 'DEL407500649810204_100pwm'
        data = pd.read_csv(f'./100pwm/{sn}_100pwm.csv')
        # print(data)
        data.columns = ['index', 'time', 'x_accel', 'y_accel', 'z_accel']

        t_sec = np.asarray(data["time"])
        az = np.asarray(data["z_accel"])
       
        N = len(t_sec)
        sample_rate = 1100 # Hz 
        T = 1/sample_rate 
        yf_z = fft(az)
        xf_z = fftfreq(N, T)[:N//2]
        y_z = 2.0/N * abs(yf_z[0:N//2])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xf_z, y=y_z, line_shape='linear', name=sn, line=dict(width=0.8,)) )

        thsd_1_x = [0, 200]
        thsd_1_y = [0.5, 0.5]
        thsd_2_x = [201, 550]
        thsd_2_y = [0.5, 0.2]
        fig.add_trace(go.Scatter(x=thsd_1_x, y=thsd_1_y, name='Threshold 1', line=dict(color='gray', dash='dash'), mode='lines'))
        fig.add_trace(go.Scatter(x=thsd_2_x, y=thsd_2_y, name='Threshold 2', line=dict(color='gray', dash='dash'), mode='lines'))
        fig.update_layout(title=f"{sn} - 100 PWM", xaxis_title='Hz', 
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
        fig.write_image(f"./plots/{sn}.png")
        # fig.show()
        return fig
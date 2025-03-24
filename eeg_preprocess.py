import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

file_path = "focused/BrainFlow-RAW_focus3_0.csv" 
'''
with open(file_path, "r") as f:
    for _ in range(5):
        print(f.readline())

'''

read_files = pd.read_csv(file_path, header=None, delimiter = "\t", skiprows=1) #reading csv file, note the \t because the csv is separated by tabs instead of the usual comma

read_files.columns = ["Sample Index", "EXG 0", "EXG 1", "EXG 2", "EXG 3", "EXG 4", "EXG 5", "EXG 6", "EXG 7",
    "Accel 0", "Accel 1", "Accel 2", "Not Used 1", "Digital 0", "Digital 1", "Digital 2", "Digital 3",
    "Not Used 2", "Digital 4", "Analog 0", "Analog 1", "Analog 2", "Timestamp", "Marker"]
#above was taken from the .txt file, assigned them to the csv file because it lacks labels

eeg_channels = ["EXG 0", "EXG 1", "EXG 2", "EXG 3", "EXG 4", "EXG 5", "EXG 6", "EXG 7"] #the main columns that we care about

eeg_data = read_files[eeg_channels]

data_scaler = StandardScaler()

adjusted_data = data_scaler.fit_transform(eeg_data)

window_size = 5*250 #for 1250 samples, 5 seconds * 250 Hz

segments = []

for i in range (0, len(eeg_data) - window_size + 1, window_size):
    window = eeg_data[i:i + window_size]
    flat_window = window.to_numpy().flatten() #converted to numpy array and then flattened since panda data can't have numpy commands applied to them
    segments.append(flat_window)

#for i in range(0, 5, 1):
#    print (segments[i])
#^^^to check if array is flattened into 1D

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut/nyq
    high = highcut/nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs = 250 #samples
lowcut = 1 #lowest frequency
highcut = 50 #highest frequency

filtered_data = eeg_data.copy() 

for channel in eeg_channels:
    filtered_data[channel] = butter_bandpass_filter(eeg_data[channel], lowcut, highcut, fs)

'''
to plot the eeg data...

time = np.arange(len(filtered_data["EXG 0"])) / 400

plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(time, filtered_data["EXG 0"], color='red')
plt.title('Channel 0 signal EXG 0')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.ylim(-100, 100)

plt.tight_layout()
plt.show()
'''

if "focused" in file_path.lower():
    label = 0
elif "distracted" in file_path.lower():
    label = 1
else:
    print ("Error with subfolder label assignment.")
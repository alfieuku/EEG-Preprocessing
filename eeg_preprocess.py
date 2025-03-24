import pandas as pd
from sklearn.preprocessing import StandardScaler

file_path = "focused/OpenBCI-RAW-2025-03-03_22-26-49.txt"

read_files = pd.read_csv(file_path)

eeg_channels = ["EXG Channel 0", "EXG Channel 1", "EXG Channel 2", "EXG Channel 3", "EXG Channel 4", "EXG Channel 5", "EXG Channel 6", "EXG Channel 7"]

eeg_data = read_files[eeg_channels]

data_scaler = StandardScaler()

adjusted_data = data_scaler.fit_transform(eeg_data)

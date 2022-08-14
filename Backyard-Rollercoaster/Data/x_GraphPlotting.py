import csv
from matplotlib import pyplot as plt

files = ['NormalAccelerationData.csv',
         'TangentialAccelerationData.csv',
         'VerticalAccelerationData.csv',
         'MagnitudeAccelerationData.csv',
         'VelocityData.csv']
y_ranges = [(0, 30), (-20, 20), (-10, 20), (0, 30), (0, 20)]
time_dataset, results_dataset = [], []
for f in files:
     time, data = [], []
     with open(f, newline = '\n') as file:
          reader = csv.reader(file, delimiter = ',')
          for row in reader:
               try:
                    time.append(float(row[0]))
                    data.append(float(row[1]))
               except ValueError:
                    pass
     time_dataset.append(time)
     results_dataset.append(data)

for i in range(len(files)):
     plt.plot(time_dataset[i], results_dataset[i])
     plt.ylim(y_ranges[i][0], y_ranges[i][1])
     plt.show()



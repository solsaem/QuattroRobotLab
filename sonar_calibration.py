from time import sleep 
# import robot 
import Help_Functions
import math 
import numpy as np
from matplotlib import pyplot as plt


data1E = [260, 260, 260, 260, 260]
data1 = [267, 268, 268, 268, 268]

data2E = [505, 505, 505, 505, 505]
data2 = [503, 503, 503, 503, 503]

data3E = [925, 925, 925, 925, 925]
data3 = [922, 921, 922, 921, 921]

data4E = [1370, 1370, 1370, 1370, 1370]
data4 = [1369, 1369, 1370, 1364, 1365]

data5E = [2740, 2740, 2740, 2740, 2740]
data5 = [2734, 2735, 2734, 2734, 2733]

distances= [260, 505, 925, 1370, 2740]

measurements = [data1, data2, data3, data4, data5]



## Initialise figure (fig) and axis (ax)
#fig, ax = plt.subplots(figsize=(15,15))
## Plot in axis, add label to data
#ax.plot(data1, data1E, label="data 1", linewidth=10) # (*)
#ax.plot(data2, data2E, label="data 2", linewidth=10, marker="o", markersize=20) # (*)
#ax.plot(data3, data3E, label="data 3", linewidth=10) # (*)
#ax.plot(data4, data4E, label="data 4", linewidth=10) # (*2
#ax.plot(data5, data5E, label="data 5", linewidth=10) # (*2
## Set labels and title
#ax.set_xlabel("X axis")
#ax.set_ylabel("Y axis")
#ax.set_title("Title")
## Add grid
#ax.grid(alpha=0.2)
## Set axes limits
#ax.set_ylim(0,3000)
## Add legend (remember to label the data as shown above (*))
#ax.legend()
## Show plot
#plt.show()
## Save plot to some local path
#name = ("test.png")
#fig.savefig(name)


# Calculate mean measurements at each distance
mean_measurements = [np.mean(measurements[i]) for i in range(len(distances))]

# Calculate measurement errors
measurement_errors = [[measurement - mean_measurements[i] for measurement in measurements[i]] for i in range(len(distances))]

# Calculate squared deviations
squared_deviations = [[error**2 for error in measurement_errors[i]] for i in range(len(distances))]

# Calculate variance
variance = [np.mean(squared_deviations[i]) for i in range(len(distances))]

# Calculate standard deviation
standard_deviation = [np.sqrt(variance[i]) for i in range(len(distances))]


for i in range(len(distances)):
    print(f"Distance {distances[i]}: Standard Deviation = {standard_deviation[i]}")



plt.figure(figsize=(10, 6))

for i in range(len(distances)):
    plt.scatter([distances[i]]*5, measurements[i], label=f'Distance {distances[i]}', alpha=0.7)

plt.plot(distances, distances, linestyle='--', color='red', label='Actual Distances')
plt.title('Measured Distances vs. Actual Distances')
plt.xlabel('Actual Distance')
plt.ylabel('Measured Distance')
plt.legend()
plt.grid(True)
plt.show()

plt.clf()

plt.figure(figsize=(10, 6))
plt.plot(distances, standard_deviation, marker='o')
plt.title('Standard Deviation vs. Distance')
plt.xlabel('Distance')
plt.ylabel('Standard Deviation')
plt.grid(True)
plt.show()



## Standard deviation
#print("26cm std : " + str(np.std(data1)))
#print("50.5cm std : " + str(np.std(data2)))
#print("92.5cm std : " + str(np.std(data3)))
#print("137cm std : " + str(np.std(data4)))
#print("274cm std : " + str(np.std(data5)))











    
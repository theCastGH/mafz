from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime

time = []
brightness = []

# bruk starData5.csv for best resultat, dette på grunn av at det er samensatt av mer nøyaktige målinger fra mer politlige observatorier
with open("starData5.csv") as file:
    next(file)  
    for line in file:
        try:    
            line = line.rstrip()
            t, b = line.split(",")
            date_obj = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            timestamp = date_obj.timestamp()
            time.append(timestamp)

            print(timestamp,b)

            brightness.append(-float(b))
        except ValueError as e:
            print(f"Skipping line due to error: {e}")

time = np.array(time)
brightness = np.array(brightness)


A = float((max(brightness)-min(brightness))/2)
periode = 463622.39999999997
c = float((2*np.pi)/periode)
d = float((max(brightness) + min(brightness))/2)
phi = (3*np.pi/2 - c * (time[1] - min(time)))

print(c)
print(f"{round(A,2)}sin({round(c,2)}x+{round(phi,2)})+{round(d,2)}")


# print(f"A:{A} \nperiode:{periode} \nc:{c} \nd:{d} \nphi:{phi}") # FOR DEBUGGING

def model(x):
    return A*np.sin(x*c+phi)+d

x_model = np.linspace(min(time), max(time), 1000)
y_model = model(x_model - min(time)) 

plt.figure(figsize=(10, 6))
plt.scatter(time, brightness, color='blue', label='Lys styrke', alpha=0.5)

plt.plot(x_model, y_model, color='red', label='Modell')
#plt.plot(x_model2, y_model2, color='blue', label='no phi')

plt.xlabel('Tid (Unix Timestamp)')
plt.ylabel('Lys Styrke')
plt.title('Lys styrke over tid')
plt.legend()
plt.show()


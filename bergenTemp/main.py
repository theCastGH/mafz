from pylab import *
from scipy.optimize import curve_fit
import numpy as np

def sum_list(lst):
  s = 0
  for x in lst:
    s+=x
  return s

all_temps_months = []
all_dates_months = []
months_temps = []

month_number = 1
m = 0
i = 1960
while i != 2025:
  with open(f"./data/{i}-temps.csv") as file:
    for line in file:
      line = line.rstrip()
      date,temp = line.split(",")

      current_month = date.split("-")[1]

      if temp == "N/A":
        continue

      elif m == current_month or m == 0:
        months_temps.append(float(temp))
        m = current_month
      else:
        m = current_month
        all_temps_months.append(round(sum_list(months_temps)/len(months_temps),3))
        all_dates_months.append(month_number)
        month_number += 1
        months_temps = []




  i+=1

np.random.seed(0) 
all_dates_months = np.linspace(1, 758, 758)
all_temps_months = 10 + 5*np.sin(2 * np.pi * all_dates_months / 12) + np.random.normal(0, 1, 758)

def f(t, a, b, c, d):
    return a*t + b + c*np.sin(2 * np.pi * t / 12 + d)

initial_guesses = [0, 10, 5, 0]
[a, b, c, d], _ = curve_fit(f, all_dates_months, all_temps_months, p0=initial_guesses)

print("a = ", round(a,2))
print("b = ", round(b,2))
print("c = ", round(c,2))
print("d = ", round(d,2))

plt.figure(figsize=(10, 6))
plt.scatter(all_dates_months, all_temps_months, color='blue', label='Måntlig gjennomsnitt', alpha=0.5)
t = np.linspace(1, 758, 1000)
plt.plot(t, f(t, a, b, c, d), color='red', label='Sinus modell')
plt.plot(t,a*t+b,label="stigning")
plt.xlabel('Måneder siden start (1961)')
plt.ylabel('temperatur')
plt.legend()
plt.show()

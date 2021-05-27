#Detection format :
#(time, moon_phase, order/familly, temperature, weather, air pollution quality)

from datetime import timedelta, datetime
import numpy as np
import random
from numpy.random import default_rng
import matplotlib.pyplot as plt
import sys

import math, decimal, datetime
dec = decimal.Decimal

def time_generator(base_date,detections):
    classes=["geometridae","noctuidae","odonata","orthoptera","hemiptera","hymenoptera","trichoptera","diptera","coleoptera"]
    weather=["rainy","clear","cloudy"]
    temperature=list(range(10,25))
    current_weather=random.choice(weather)
    current_temperature=random.choice(temperature)
    if current_weather=="rainy" or current_temperature < 14:
        mean_number_detections=52
        std_detections=4
    else:
        mean_number_detections=257
        std_detections=25

    #date begins at 11pm and ends at 6am
    date=base_date
    n = int(np.random.normal(mean_number_detections,std_detections,1)[0])
    mu,sigma=3.5,1
    s=np.random.normal(mu,sigma,n)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
    s.sort()
    for i in s:
        #print("before {} {}".format(date.hour, date.minute))
        date=base_date+timedelta(hours=int(i),minutes=(i % 1 )*60)
        #print("after {} {}".format(date.hour, date.minute))
        pos=position(date)
        phasename=phase(pos)
        #roundedpos = round(float(pos), 3)
        result="{},{},{},{},{}\n".format(date.strftime("%d:%m:%Y|%H:%M:%S"),random.choice(classes),str(float(current_temperature-(int(i)*0.5))),current_weather,phasename)
        detections.append(result)
    #print(detections)
    #plt.show()

"""
moonphase.py - Calculate Lunar Phase
Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
"""
def position(now=None): 
   if now is None: 
      now = datetime.datetime.now()

   diff = now - datetime.datetime(2001, 1, 1)
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   return lunations % dec(1)

"""
moonphase.py - Calculate Lunar Phase
Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
"""
def phase(pos): 
   index = (pos * dec(8)) + dec("0.5")
   index = math.floor(index)
   return {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }[int(index) & 7]


def main(args):
    date=datetime.datetime(2020,2,20,23)
    #time_generator(date)
    n_days=15
    detections = []
        
    for i in range(n_days):
        date+=timedelta(days=1)
        time_generator(date,detections)
    
    with open("detections.csv","w") as f:
        for detection in detections:
            f.write(detection)

if __name__=="__main__":
    main(sys.argv)

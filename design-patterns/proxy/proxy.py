# -*- coding: utf-8 -*-

'''
In principle, the program presents the characteristics of selected data read from the file.
At first, the program displays numerical characteristics and graph substitutes to follow
the client asks to display the charts in full glory. Displaying charts may not
be required, and due to the long time of drawing them, it can be replaced with a substitute
'''



import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


class Data:
   def __init__(self, filename):
       self._filename = filename
   
       flow = []
       temp_sup = []
       temp_air = []
       dif_temp = []
       power = []

       with open(self._filename, newline='') as csvfile:
           data = csv.reader(csvfile, delimiter=',')
       
           next(data)
           for observation in data:
             try:
                 flow.append(float(observation[6]))
                 temp_sup.append(float(observation[7]))
                 temp_air.append(float(observation[8]))
                 dif_temp.append(float(observation[9]))
                 power.append(float(observation[12]))
             except ValueError:
                 print("Value error")
                 sys.exit(0)
        
           self._zmienne = {"temp_sup":temp_sup, "temp_air":temp_air,
                     "dif_temp":dif_temp, "flow":flow, "power":power}
      
        
       print("... LOADING FILE ...", self._filename, '...' )
        
        
   def show( self ):
        for nazwa, zmienna in self._zmienne.items():
            print()
            print("Characteristic:",nazwa)
            print("MIN:", min(zmienna))   
            print("MAX:", max(zmienna))
            print("MEAN:", np.mean(zmienna))
            print("MEDIAN:", np.median(zmienna))
            print("MEDIANA QUANTILE 0.25:" , np.quantile(zmienna, 0.25))
            print("MEDIANA QUANTILE 0.75:" , np.quantile(zmienna, 0.75))
            print("RANGE:", np.ptp(zmienna))
            print("STANDARD DEVIATION:", np.std(zmienna))
            print("VARIANCE:", np.var(zmienna))
            print("PERCENTILE 90%:", np.percentile(zmienna,90) )
            print("HISTOGRAM:", np.histogram(zmienna))
            
            plt.hist(0, 1)                  # namiastka wykresu
            plt.show()
   
   def show_precised(self):                 # precyzyjny wykres
            for name, variable in self._zmienne.items():
                    plt.hist(variable, 200)
                    plt.title('Histogram : ' + name)
                    plt.xlabel('Section')
                    plt.ylabel('Number of observations')
                    plt.show()



class Proxy:    
                        
   def __init__(self, data):
      self._data = data
      self._preciseplot = 'No'



class ProxyPlot(Proxy):
             
   def display_output(self):
      if self._preciseplot == 'No':
         self._data.show()
         self._preciseplot = 'Yes'
      else:
          self._data.show_precised()
           



if __name__ == '__main__':    

    proxy_image1 = ProxyPlot(Data("data.csv"))
    proxy_image1.display_output() 
    
    user_action = ''

    print('------------------')
    user_action = input('Press enter to show precised plots')
    print('')
    if user_action == '':
        proxy_image1.display_output()

    
    

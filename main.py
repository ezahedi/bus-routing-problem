import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

demand = pd.read_csv('demand.csv')
stops = pd.read_csv('stops.csv')

x_origin = np.array(demand['OriginX'])
y_origin = np.array(demand['OriginY'])

x_dest = np.array(demand['DestinationX'])
y_dest = np.array(demand['DestinationY'])

x_stops = np.array(stops['X'])
y_stops = np.array(stops['Y'])

plt.plot(x_origin,y_origin,'g.')
plt.plot(x_dest,y_dest,'r.')
plt.plot(x_stops,y_stops,'b.')

plt.savefig('points.png',ppi=300)
# plt.show()

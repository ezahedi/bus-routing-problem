import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
from numpy import unravel_index

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


# Find the density matrix of origin coordinates,
# D[i][j]= the number of passengers in [i-1,i]x[j-1,j] 
s = (int(math.ceil(np.max(x_origin))), int(math.ceil(np.max(y_origin))))
Density_origin = np.zeros(s)  
Dict_dest = {}
for i in range(len(x_origin)):
    x = math.floor(x_origin[i])
    y = math.floor(y_origin[i])
    Dict_dest[(x,y)] = []  #corresponding to origin density (x,y) gives destination locations

for i in range(len(x_origin)):
    x = int(math.floor(x_origin[i]))
    y = int(math.floor(y_origin[i]))
    Density_origin[x][y] += 1 
    Dict_dest[(x,y)].append((x_dest[i], y_dest[i]))
 

# Find the density matrix of bus stations
# D[i,j] = the number of passengers can use the bus station at (i,j) 
s = (np.max(x_stops), np.max(y_stops))
Density_bus_stops = np.zeros(s)         
for a in range(len(x_stops)):
    i = x_stops[a]
    j = y_stops[a]
    if i != len(Density_origin) and j != len(Density_origin[0]):
        Density_bus_stops[i][j] =  Density_origin[i-1][j-1]\
                                  +Density_origin[i-1][j]  \
                                  +Density_origin[i][j-1]  \
                                  +Density_origin[i][j]

# average distance map from (x,y) in Density_origin to (s1,s2) that preserved the density in destination
Dict_dest_avg = {}
for k,v in Dict_dest.items():
    s = [0,0]
    for it in v:
        s[0] += it[0]
        s[1] += it[1]
    s[0] //= len(v)
    s[1] //= len(v)
    Dict_dest_avg[k] = tuple(s)
    Dict_dest
  
    
# find the proper map from choosing S_O to the corresponding destination, S_D.
Dict_O2D = {}
for k,v in Dict_dest_avg.items(): 
    a = k[0]+1
    b = k[1]+1
    Dict_O2D[(a,b)] = v    
        
  
# dictionary with key : bus IDs and values: [bus stations, start pnt, endpnt, length of rout] 
L_M = 18 
M   = 15           
Rout_Dict = {}
for i in range (M):           
     (a,b) = unravel_index(Density_bus_stops.argmax(), Density_bus_stops.shape) 
     if (a,b) in Dict_O2D:
         Rout_Dict[i+1] = [[Dict_O2D[(a,b)], (a,b)], (a,b), Dict_O2D[(a,b)],0]
         
     Density_bus_stops[a][b] = 0
Done = True
while Done:
    (c,d) = unravel_index(Density_bus_stops.argmax(), Density_bus_stops.shape) 
    
    if (c,d) in Dict_O2D:
        (x,y) = Dict_O2D[(c,d)]
        for i in range (M): 
            (a,b) = Rout_Dict[i+1][1]
            (u,v) = Rout_Dict[i+1][2]
            if (abs(x-a) + abs(y-b)) >(abs(x-c) + abs(y-d)):
                if (Rout_Dict[i+1][3]  +  (abs(c-a) + abs(d-b) )  +  (abs(c-x) + abs(d-y) ) ) <= L_M:
                    Rout_Dict[i+1][0].append((c,d))
                    Rout_Dict[i+1][1] = (c,d)
                    Rout_Dict[i+1][2] = (x,y)
                    Rout_Dict[i+1][3] += (abs(c-a) + abs(d-b) ) #distance from (a,b) to (c,d)
                    Density_bus_stops[c][d] = 0
                    break
     
    Density_bus_stops[c][d] = 0
    if  np.max(Density_bus_stops) == 0:
        Done = False    


## plot routes
#colors = cm.jet(np.linspace(0, 1, len(Rout_Dict)))
#counter = 0
#for k,v in Rout_Dict.items():
#    x = [i[0] for i in v[0]]
#    y = [i[1] for i in v[0]]
#    x.append(x[0])
#    y.append(y[0])
#    x = x[1:]
#    y = y[1:]
#    plt.plot(x,y,color=colors[counter])
#    plt.plot(x,y,'o',color=colors[counter])
#    counter +=1
#plt.savefig('routes.png',ppi=600)
            

# dictionary with key : passanger location and values: stop ID 
stopXY2stopID = {}
for idx in range(len(stops['StopId'])):
    stopXY2stopID[(stops['X'][idx],stops['Y'][idx])] = stops['StopId'][idx]
                    
stopID2stopXY = {v:k for k,v in stopXY2stopID.items()}


# dictionary with key : bus IDs and values: bus stations 
output_dict = {}
for k,v in Rout_Dict.items():
    seq = [stopXY2stopID[t] for t in v[0]]
    seq.append(seq[0])
    seq = seq[1:]
    output_dict[k] = seq


# remove the repeated bus stops  
Chec_list = []
for i in range(M):
    Chec_list += output_dict[M-i]
for i in range(M):
    l     = len(output_dict[M-i])
    ID = output_dict[M-i][-1]
    cnt   = Chec_list.count(ID)
    if cnt > 1:   
        item_index = Chec_list.index(ID)
        output_dict[M-i].pop()


 # write in a text file       
with open('output.txt','w') as f:
    f.write('100\n')
    for v in output_dict.values():
        for i in v[:-1]:
            f.write('%d,'%i)
        f.write('%d'%v[-1])
        f.write('\n')
         
# find the distance
def dist_manhattan(origin_tuple,dest_list_tuples):
    d_manh = []
    for dest_tuple in dest_list_tuples:
        d_manh.append(abs(origin_tuple[0]-dest_tuple[0])+abs(origin_tuple[1]-dest_tuple[1]))
    return d_manh

# compute optimal routes and their probabilities
p_i = []
for i in range(demand.shape[0]):
    pi_route_j = []
    for j in output_dict:
        stopXY_tuples = [stopID2stopXY[st] for st in output_dict[j]]
        # compute the probability of customer i taking route j
        # step 1: find closest point on route to origin
        dist_origin2allStops = dist_manhattan( (demand['OriginX'][i],demand['OriginY'][i]) , stopXY_tuples )
        d_o = sorted(dist_origin2allStops)[0]

        # step 2: find closest point on route to destination
        dist_dest2allStops = dist_manhattan( (demand['DestinationX'][i],demand['DestinationY'][i]) , stopXY_tuples )
        d_d = sorted(dist_dest2allStops)[0]

        # step 3: compute the probability
        pi_route_j.append(max( 0 , 1 - (d_o+d_d)/2. ))

    # compute probability of customer take bus
    # this is the maximum route-wise probability
    p_i.append(sorted(pi_route_j)[-1])

# compute profit from customers
K = 4
profit_customers = 0
for i in range(demand.shape[0]):
    # use probability from previous step
    profit_customers += K * p_i[i]

# compute costs
Cf = 100
Cv = 5
costs = 0
for j in Rout_Dict:
    # compute cost per route
    costs += Cf + Cv * Rout_Dict[j][3]

# compute total profit
profit_total = profit_customers - costs

print('Total profit is %f' % profit_total)







 
    
    
    

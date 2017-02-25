# bus-routing-problem

## Short review
This problem is an NP-complete problem. So it can not be solved using either dynamic programming  or greedy algorithm. 
Of course brute force algorithm is an option but it is time consuming. Here I use parallel search algorithm inspired by 
evolutionary framework to attack the problem. As the data is shown as follows: 

![alt tag](https://raw.githubusercontent.com/ezahedi/bus-routing-problem/master/points.png)

where the green, red and blu show the riders location, rider destinations and potential bus stops, respectively.

## Plan of attack

My solution consists of the following steps:

- step 1: Partition
I do grid partitioning the covered space to `1x1` squares since `0<d(O,S_o)+d(D,S_D)<2`
and Find the squares which have more density.
- step 2:  Select bus stops
Select a bus stop `S_O` for a square `O` which has the minimum average distance to the square `O`, to get more likely maximum 
number of riders for that bus stop. This happens because more likely the probability of a potential customers in the square `O` who wants to 
go from the selected bus stop, `S_O`, is more, based on the origin 
location.
- step 3:

## Results

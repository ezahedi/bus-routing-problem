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
- step 2:  Select bus stops for origin
Select a bus stop `S_O` for a square `O` which has the minimum average distance to the square `O`, to get more likely maximum 
number of riders for that bus stop. This happens because more likely the probability of a potential customers in the square `O` who wants to 
go from the selected bus stop, `S_O`, is more, based on the origin 
location.
- step 3: Select bus stops for destination
Select a bus stop `S_D` which has minimum average distance to 
destinations of elements in square `O`, that you called `D`. The 
advantage of this selection is increasing the probability of a 
potential customer who wants to go from origin `O` to destination `D` 
chooses to get on a bus at stop `S_O` and get off at stop `S_D`.

- step 4: parallel search
Using parallel search algorithm start from 'M' different `S_O` s. 
These start bus stations are chosen uniformly in random.
And then using BFS algorithm with two conditions that `S_O` goes to `S_O'`  
if

`1)  d(s_o,s_d)  > d(s_o', s_d)`

`2) L_S_o + d(s_o,s_o') < L_M`

`3) d(s_o,s_o') + d(s_d, s_d') = Min_n [d(s_o,s_n) + d(s_d, s_n)`, where n is in the `M`

This helps to increase the benefit by getting these shortest paths.

Step5) Termination

a)For each simulation running step 4, ten times.
b)Select the one out of ten with maximum profit.

## Results

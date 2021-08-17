# Sensor operation
The location probability is calculated for the 4 orientation directions independently.

The matrix T consists of 4 sub-matrices for which the value of the transition factor is calculated.
Suitable for [N, E, S, W] directions. After performing the forward action, there is a 0.95 chance that the robot
will move and 0.05 that it will stay in place. For a trading action, there is 1 chance that it will stay in place.

The matrix O consists of 4 sub-matrices for which the value of the sensor factor is calculated.
Suitable for [N, E, S, W] directions. For each location, it compares the sensor reading with its neighbors
cells and calculates the value of prob. Everything is done 4 times for 4 directions "translating"
sensor reading percept ['fwd', 'bckwd', 'left', 'right'] on percept_tmp [N, E, S, W].

Finally, the 4 T and 4 O sub-matrices are respectively multiplied. The result is entered
to the cumulative probability distribution of self.P

When starting a new step, if the previous action was a rotation, it converts accordingly
self.P submarines among themselves, taking into account eps.move (e.g. after turnleft P [0] will be at 5% P [0],
and for 95% P [1])

The sensor "does not travel" over time. Below is a photo of the action for n = 500
![alt text](https://github.com/wojdzi1607/Projekt_SI/blob/master/500n.png?raw=true)

# Including a bump
If there was a bump, i.e. the robot hit the opposite wall then:

When calculating the T matrix, the value of the transition factor at the current location = 1. (same as for rotation).

In computing the O matrix:
- the probability that there is a wall in front of the robot is 1 ('fwd' in the sensor is correct
for 1, not a 0.95 chance)
- the probability that the robot is at the location it is facing so that it is not
has walls is 0

PS. at the beginning of the function call, the 'bump' flag is set, and it is changed in the [bump] sensor
to [fwd], or [fwd] is added if the sensor failed to detect [fwd].
 
# Heureistics

Moving along the left wall will result in visiting all the spaces on the board.

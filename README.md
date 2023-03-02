# ProjectilePy
A python library aimed at simulating and solving projectile motion problems. Includes various methods for running accurate numerical discrete-time simulations, both with and without drag. 

---

### Features:
* Configurable drag or drag-less simulations for projectiles.
* Real world atmospheric data for improved accuracy with Newtonian drag.
* Itterative root finding methods for calculating firing solutions to targets.
* Easy to use simulator object class, with included examples.

---

### Installation:
Currently the package is only availble from this repository. 
In the future it may be published to the PyPi for easier installation.

---

### Usage:
#### There are usage eamples in the src/examples folder, I encourage you to look through them for specific use cases.
1. Create a new intance of the simulator class passing the approapriate arguments to the constructor.
2. To run a straightforward simulation invoke the run() method on your simulator object.
3. To examine the results, either invoke the analysis methods (such as final_position or time_of_flight), or directly access the positionValues list for the raw x-y coordiante pairs.

# ProjectilePy
A python library aimed at simulating and solving projectile motion problems. Includes various methods for running accurate numerical discrete-time simulations, both with and without drag. 

## Features:
* Configurable drag or drag-less simulations for projectiles.
* Real world atmospheric data for improved accuracy with Newtonian drag.
* Itterative root finding methods for calculating firing solutions to targets.
* Easy to use simulator object class, with included examples.

## Installation:
You can install the package easily though pip by running the command `pip install ProjectilePy`

## Usage:
#### There are usage eamples in the src/examples folder, I encourage you to look through them for specific use cases.
1. Create a new intance of the simulator class passing the approapriate arguments to the constructor eg.
    `mySimulator = projectilepy.model(150,30)`
2. To run a straightforward simulation invoke the run() method on your simulator object.
    `mySimulator.run()`
3. To examine the results, either invoke the analysis methods (such as final_position or time_of_flight), or directly access the positionValues list for the raw x-y coordiante pairs.
    ```
    final_position = mySimulator.final_position()
    time_of_flight = mySimulator.time_of_flight()
    x, y = zip(*mySimulator.positionValues)
    ```
4. If you have matplotlib installed, you can visualise the trajectory of your projectile using a plot.
    ```
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()
    ```

# ProjectilePy
Have you ever wondered how far you can throw a ball on the moon, or how much wind-resistance really affects a cannonball? This python library provides all the tools to answer those questions, and more.

ProjectilePy is a library aimed at simulating and solving projectile motion problems. This library includes a class with a host of methods for simulating and analysing ballistic trajectories both with and without drag.

## Features:
* Configurable drag or drag-less simulations for projectiles.
* Real world atmospheric data for simulations.
* Itterative root finding algorithms for solving initial value problems.
* Easy to use simulator object class, with included examples.

## Installation:
The package is availble through the Python Package Index, and can be easily installed using pip.
In your system shell, run the command `pip install ProjectilePy`

## Usage:

 In this example we will create a simple simulation of a pumpkin being fired from an air cannon, a [real sport!](https://en.wikipedia.org/wiki/Punkin_chunkin).

1. We'll start by creating a new intance of the simulator class, which we use for running all of our physics simulations. The constructor can take many arguments, but here we'll just use the `initial_velocity` and `initial_angle` arguments. Let's assume our theorhetical air cannon can fire a pumpkin at 75 m/s, and it's being fired 30 degrees above the horizon.
    ```
    import projectilepy
    mySimulator = projectilepy.model(initial_velocity=75, initial_angle=30)
    ```
2. Now that our class is set up, we can run a quick simulation. This can be done by invoking the `run()` method on our simulator class.
    ```
    mySimulator.run()
    ```
3. But nothing happened? That's right, the `run()` method but doesn't provide us any information on it's own, it only runs a simulation. Instead, we get information by querying the class using various methods after a simulation is complete. For example, we can invoke the `final_position()` method, which returns an x-y tuple of where our pumpkin landed. The x-value will be our total distance in meters.
    ```
    final_position = mySimulator.final_position()
    distance = final_position[0]
    print("Our pumpkin flew a total of", distance, "meters!")
    ```
4. Well well, our pumpkin flew a total of 488 meters, not bad! If you have matplotlib installed, you can visualise the trajectory of the pumpkin using a scatterplot. But first we'll need to format our data a bit. Our simulation model stores positional data as a list of x-y tuples, but matplotlib works with seperate x and y lists. We can fix this with a quick zip command on our model's position values.
    ```
    import matplotlib.pyplot as plt
    x, y = zip(*mySimulator.positionValues) #Formats coordinate pairs as two lists
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()
    ```
5. Now dragless simulations are all well and good, but Earth has an atmosphere, so let's run a simulation using a Newtonian drag model. We'll specify this by setting the `drag` attribute of our model to "Newtonian". We'll also need to make sure our model has a couple aerodynamic values for our projectile. Specifically, we need to provide the `mass`, `drag_coefficient`, and `cross_sectional_area` for our pumpkin.
    ```
    mySimulator.drag = "Newtonian"
    mySimulator.mass = 8 #8kg of mass
    mySimulator.drag_coefficient = 0.35 #ballpark drag number
    mySimulator.cross_sectional_area = 0.07 #from a diameter of 30cm
    ```
6. Now that our model knows we want a Newtonian drag model and has all the required information, we can invoke the `run()` method to execute a new simulation.
    ```
    mySimulator.run()
    ```
7. We can once again check how far our pumpkin made it using the `final_position()` method.
    ```
    final_position = mySimulator.final_position()
    distance = final_position[0]
    print("With drag, our pumpkin flew a total of", distance, "meters!")
    ```
8. Now our pumpkin only flew a total of 308 meters, drag is a killer. Let's have a look at the plot of our trajectory, it should look a little different now the simulation is modelling drag.
    ```
    x, y = zip(*mySimulator.positionValues)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()
    ```
9. Those are the basics of running a simulation, but this package can do much more than run static models. Let's instead say we wanted to beat the world record Punkin Chunkin distance of 4694.68 ft (1430.94 m) set in 2013. Then we need to know how fast to fire our pumpkin. We can find this using the `solve_velocity()` method which calculates the velocity needed to hit a target vector. In this case we want to beat the world record, so we'll set our target to `[1450, 0]` which means it will have traveled a total of 1450 m before impact.
    ```
    muzzle_velocity = mySimulator.solve_velocity([1450,0])
    print("We would need a muzzle velocity of", muzzle_velocity, "m/s")
    ```
10. And that's the basics of using ProjectilePy, but there are many more methods you can try out on your own. I encourage you to experiment, and let your curiosity guide your learning, good luck!

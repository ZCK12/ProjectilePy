# from src.ProjectilePy import ProjectileSimulator
from src.projectilepy.projectilesimulator import ProjectileSimulator
import matplotlib.pyplot as plt
import numpy as np

"""#DEMO 1, FINDING NEWTONIAN DRAG FIRING SOLUTIONS
mySimulator = ProjectileSimulator(150,30,drag="Newtonian", mass=43, drag_coefficient=0.45, cross_sectional_area=0.1)
angle1 = mySimulator.solve_angle([950, 0], False)
angle2 = mySimulator.solve_angle([950, 0], True)

mySimulator.run(override_angle=angle1)
fig, ax = plt.subplots()
x1, y1 = zip(*mySimulator.positionValues)

mySimulator.run(override_angle=angle2)
x2, y2 = zip(*mySimulator.positionValues)
ax.plot(x2, y2)
ax.plot(x1, y1)

plt.title("Finding Both Firing Solutions with Drag")"""

"""#DEMO 2, DEMONSTRATING THE EFFECT OF DRAG ON TRAJECTORY
fig, ax = plt.subplots()

mySimulator = ProjectileSimulator(827, 30, drag="Newtonian", mass=43, drag_coefficient=0.25, cross_sectional_area=0.0188)
mySimulator.run()
x1, y1 = zip(*mySimulator.positionValues)
ax.plot(x1, y1)

mySimulator = ProjectileSimulator(827, 30, drag="Newtonian", mass=43, drag_coefficient=0.05, cross_sectional_area=0.0188)
mySimulator.run()
x2, y2 = zip(*mySimulator.positionValues)
ax.plot(x2, y2)

mySimulator.drag = "None"
mySimulator.run()
x3, y3 = zip(*mySimulator.positionValues)
ax.plot(x3, y3)

plt.title("Effect of Newtonian Drag on Trajectory")"""

plt.show()

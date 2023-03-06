import numpy as np
import matplotlib.pyplot as plt
import projectilepy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEMO 3, DEMONSTRATING THE EFFECT OF DRAG ON TRAJECTORY
mySimulator = projectilepy.model(827, 30, drag="Newtonian", mass=43, drag_coefficient=0.25, cross_sectional_area=0.0188)
mySimulator.run()
x1, y1 = zip(*mySimulator.positionValues)

mySimulator = projectilepy.model(827, 30, drag="Newtonian", mass=43, drag_coefficient=0.05, cross_sectional_area=0.0188)
mySimulator.run()
x2, y2 = zip(*mySimulator.positionValues)

mySimulator.drag = "None"
mySimulator.run()
x3, y3 = zip(*mySimulator.positionValues)

fig, ax = plt.subplots()
ax.plot(x1, y1)
ax.plot(x2, y2)
ax.plot(x3, y3)
plt.title("Effect of Newtonian Drag on Trajectory")
plt.show()

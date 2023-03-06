import numpy as np
import matplotlib.pyplot as plt
import projectilepy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEMO 2, FINDING NEWTONIAN DRAG FIRING SOLUTIONS
mySimulator = projectilepy.model(150, 30, drag="Newtonian", mass=43, drag_coefficient=0.45, cross_sectional_area=0.1)
angle1 = mySimulator.solve_angle([950, 0], False)
angle2 = mySimulator.solve_angle([950, 0], True)

mySimulator.run(override_angle=angle1)
fig, ax = plt.subplots()
x1, y1 = zip(*mySimulator.positionValues)
mySimulator.run(override_angle=angle2)
x2, y2 = zip(*mySimulator.positionValues)

ax.plot(x2, y2)
ax.plot(x1, y1)
plt.title("Finding Both Firing Solutions with Drag")
plt.show()

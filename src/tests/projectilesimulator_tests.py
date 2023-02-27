#from src.ProjectilePy import ProjectileSimulator
from src.ProjectilePy.projectilesimulator import ProjectileSimulator
import matplotlib.pyplot as plt
import numpy as np


mySimulator = ProjectileSimulator(827, 30, drag="Newtonian", mass=43, drag_coefficient=0.15, cross_sectional_area=0.0188)

"""angle1 = mySimulator.solve_angle([950, 0], False)
angle2 = mySimulator.solve_angle([950, 0], True)

mySimulator.run(override_angle=angle1)
print(angle1, mySimulator.final_position())

mySimulator.run(override_angle=angle2)
print(angle2, mySimulator.final_position())

velocity1 = mySimulator.solve_velocity([1100, 0])
mySimulator.run(override_velocity=velocity1)
print(velocity1, mySimulator.final_position())"""

mySimulator.run()

fig, ax = plt.subplots()
x, y = zip(*mySimulator.positionValues)
ax.plot(x,y)
plt.show()
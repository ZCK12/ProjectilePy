import numpy as np
import matplotlib.pyplot as plt
import projectilepy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEMO 1, BASIC DRAGLESS SIMULATION
mySimulator = projectilepy.model(150, 30)
mySimulator.run()

fig, ax = plt.subplots()
x1, y1 = zip(*mySimulator.positionValues)
ax.plot(x1, y1)
plt.title("Basic Dragless Simulation")
plt.show()
#from src.ProjectilePy import ProjectileSimulator
from src.ProjectilePy.projectilesimulator import ProjectileSimulator

mySimulator = ProjectileSimulator(100, 30)

angle1 = mySimulator.solve_angle([950, 0], False)
angle2 = mySimulator.solve_angle([950, 0], True)

mySimulator.run(override_angle=angle1)
print(angle1, mySimulator.final_position())

mySimulator.run(override_angle=angle2)
print(angle2, mySimulator.final_position())

velocity1 = mySimulator.solve_velocity([1100, 0])
mySimulator.run(override_velocity=velocity1)
print(velocity1, mySimulator.final_position())

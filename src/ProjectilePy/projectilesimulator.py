import math


class ProjectileSimulator:
    def __init__(self, initial_velocity=None, initial_height=0, initial_angle=0, gravity=9.981, time_step=0.01,
                 drag="None", ):
        assert drag in ["None", "Stokes", "Newtonian"]
        self.drag = drag
        self.initial_angle = initial_angle
        self.initial_height = initial_height
        self.initial_velocity = initial_velocity
        self.gravity = gravity
        self.time_step = time_step

        self.positionValues = []
        self.velocityValues = []

    def run(self, stop_height=0, override_drag=None):
        drag = self.drag
        if override_drag is not None:
            assert override_drag in ["None", "Stokes", "Newtonian"]
            drag = override_drag

        if drag is "None":
            return self.__simulate_dragless(stop_height)
        elif drag is "Stokes":
            return self.__simulate_stokes(stop_height)
        elif drag is "Newtonian":
            return self.__simulate_newtonian(stop_height)
        else:
            return

    def __simulate_dragless(self, stop_height):
        positionVec = [0, 0]
        velocityVec = [math.cos(self.initial_angle) * self.initial_velocity,
                       math.sin(self.initial_angle) * self.initial_velocity]
        self.positionValues = [[positionVec[0], positionVec[1]]]
        self.velocityValues = [[velocityVec[0], velocityVec[1]]]

        while positionVec[1] >= stop_height:  # numerical integration (Euler method)
            positionVec[0] += self.time_step * velocityVec[0]
            positionVec[1] += self.time_step * velocityVec[1]
            velocityVec[1] -= self.time_step * self.gravity
            self.positionValues.append([positionVec[0], positionVec[1]])
            self.velocityValues.append([velocityVec[0], velocityVec[1]])

    def __simulate_newtonian(self, stop_height):
        raise NotImplementedError

    def __simulate_stokes(self, stop_height):
        raise NotImplementedError

    def surface_impact(self, surface_height, descending_impact=True):
        matches = [pos for pos in self.positionValues if pos[1] >= surface_height]
        if descending_impact is True:
            return matches[-1]
        return matches[0]

    def final_position(self):
        return self.positionValues[-1]

    def max_height(self):
        return max([pos[1] for pos in self.positionValues])

    def time_of_flight(self):
        return len(self.positionValues) * self.time_step

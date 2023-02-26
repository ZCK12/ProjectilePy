import math


class ProjectileSimulator:
    def __init__(self, initial_velocity, initial_angle, initial_height=0, time_step=0.0005, gravity=9.981,
                 drag="None", ):
        assert drag in ["None", "Stokes", "Newtonian"], "Drag type not recognised"
        self.drag = drag
        self.initial_angle = initial_angle
        self.initial_height = initial_height
        self.initial_velocity = initial_velocity
        self.gravity = gravity
        self.time_step = time_step

        self.positionValues = []
        self.velocityValues = []

    def run(self, stop_height=0, override_drag=None, override_angle=None, override_velocity=None):
        if override_drag is not None:
            assert override_drag in ["None", "Stokes", "Newtonian"], "Drag type not recognised"
            drag = override_drag
        else:
            drag = self.drag

        if override_angle is not None:
            assert type(override_angle) == int or type(override_angle) == float, "Angle must be numerical"
            assert -90 <= override_angle <= 90, "Angle must be between -90 and 90 degrees"
            angle = override_angle
        else:
            angle = self.initial_angle

        if override_velocity is not None:
            assert type(override_velocity) == int or type(override_velocity) == float, "Velocity must be numerical"
            assert override_velocity >= 0, "Initial velocity must be positive or zero"
            velocity = override_velocity
        else:
            velocity = self.initial_velocity

        if drag == "None":
            self.positionValues, self.velocityValues = \
                self.__simulate_dragless(angle, velocity, stop_height)
        elif drag == "Stokes":
            self.positionValues, self.velocityValues = \
                self.__simulate_stokes(angle, velocity, stop_height)
        elif drag == "Newtonian":
            self.positionValues, self.velocityValues = \
                self.__simulate_newtonian(angle, velocity, stop_height)
        else:
            raise ValueError("Drag type not recognised")

    def solve_angle(self, target_vec, lofted=False, max_error=0.1):
        if lofted:
            angle = 85
        else:
            angle = 5
        deltaPhi = 0.05

        for iterations in range(50):
            try:
                self.run(override_angle=angle)
            except AssertionError:
                return False
            impact1 = self.surface_impact(target_vec[1])

            try:
                self.run(override_angle=angle + deltaPhi)
            except AssertionError:
                return False
            impact2 = self.surface_impact(target_vec[1])

            dx = (impact2[0] - impact1[0]) / deltaPhi
            error = target_vec[0] - impact1[0]

            angle += min(error / dx, 5)
            deltaPhi = (error / target_vec[0]) + 0.01 # relative error

            if error < max_error:
                return angle
            elif iterations > 15 and (error / target_vec[0]) >= 0.01:
                return False

        return False

    def solve_velocity(self):
        raise NotImplementedError

    def solve_height(self):
        raise NotImplementedError

    def __simulate_dragless(self, angle, velocity, stop_height):
        positionVec = [0, 0]
        velocityVec = [math.cos(math.radians(angle)) * velocity, math.sin(math.radians(angle)) * velocity]

        positionValues = [positionVec[:]]
        velocityValues = [velocityVec[:]]

        while True:  # numerical integration (Euler method)
            positionVec[0] += self.time_step * velocityVec[0]
            positionVec[1] += self.time_step * velocityVec[1]
            velocityVec[1] -= self.time_step * self.gravity
            positionValues.append(positionVec[:])
            velocityValues.append(velocityVec[:])

            if positionValues[-1][1] < positionValues[-2][1] < stop_height:
                break

        return positionValues, velocityValues

    def __simulate_newtonian(self, angle, velocity, stop_height):
        raise NotImplementedError

    def __simulate_stokes(self, angle, velocity, stop_height):
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

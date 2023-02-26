import math


class ProjectileSimulator:
    def __init__(self, initial_velocity, initial_angle, initial_height=0, time_step=0.0005, gravity=9.981,
                 drag="None", ):
        """A projectile simulation object with associated methods for simulating projectile motion and solving for
        various firing solutions. To start a simulation use the run method.

        Parameters
        ----------
        initial_velocity : float
            The initial launch velocity of the projectile.
        initial_angle : float
            The initial launch angle of the projectile.
        initial_height : float
            The initial launch height of the projectile.
        time_step : float
            The global time step used in all numerical simulations for this object.
        gravity : float
            The acceleration due to gravity that the projectile experiences.
        drag : string
            The method for calculating drag in each projectile simulation.
        """
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
        """Manages a numerical projectile motion simulation using the object parameters or method overrides.
        This replaces the stored simulation points from previous simulations with newly computed values.

        Parameters
        ----------
        stop_height : float, optional
            Height at which the numerical simulation will be halted during the descending path.
        override_drag : string, optional
            Override that forces using a specific drag model for the numerical simulation.
        override_angle : float, optional
            Override that forces using a given initial launch angle in degrees between -90 and 90.
        override_velocity : float, optional
            Override that forces using a given initial launch velocity, if given it must be at least zero.
        """
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
        """Runs an iterative secant solving algorithm for obtaining a launch angle firing solution on the target.
        There are always two possible solutions for launch angles. If a firing solution cannot be found, the method
        will return None.

        Parameters
        ----------
        target_vec : array_like
            The first two elements of the object should correspond to the target distance and relative height.
        lofted : bool
            Defines whether the calculated firing angle should be the lofted or un-lofted solution.
        max_error : float
            Defines the termination accuracy for the iterative solving algorithm. Lower errors may require more
            computation to obtain. May also depend on the global time_step parameter.

        Returns
        -------
        angle : float
            Firing solution angle in degrees, or None if not found.
        """
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
            deltaPhi = (error / target_vec[0]) + 0.01

            if error < max_error:
                return angle
            elif iterations > 15 and (error / target_vec[0]) >= 0.01:
                return None

        return None

    def solve_velocity(self, target_vec, max_error=0.1):
        """Runs an iterative secant solving algorithm for obtaining a launch velocity firing solution on the target.
        If a firing solution cannot be found, the method will return None.

        Parameters
        ----------
        target_vec : array_like
            The first two elements of the object should correspond to the target distance and relative height.
        max_error : float
            Defines the termination accuracy for the iterative solving algorithm. Lower errors may require more
            computation to obtain. May also depend on the global time_step parameter.

        Returns
        -------
        velocity : float
            Firing solution velocity in meters per second, or None if not found.
        """
        velocity = 100
        deltaV = 1

        for iterations in range(50):
            try:
                self.run(override_velocity=velocity)
            except AssertionError:
                return False
            impact1 = self.surface_impact(target_vec[1])

            try:
                self.run(override_velocity=velocity + deltaV)
            except AssertionError:
                return False
            impact2 = self.surface_impact(target_vec[1])

            dx = (impact2[0] - impact1[0]) / deltaV
            error = target_vec[0] - impact1[0]

            velocity += min(error / dx, 20)
            deltaV = (error / target_vec[0]) + 0.05

            if error < max_error:
                return velocity
            elif iterations > 15 and (error / target_vec[0]) >= 0.01:
                return False

        return False

    def solve_initial_height(self, target_vec):
        """Solves for the required initial height of the fired projectile in order to impact the target.

        Parameters
        ----------
        target_vec : array_like
            The first two elements of the object should correspond to the target distance and relative height.

        Returns
        -------
        height : float
            The initial height of the fired projectile required to impact the target.
        """
        self.run(stop_height=-1000)
        matches = [pos for pos in self.positionValues if pos[0] <= target_vec[0]]
        return target_vec[1] - matches[-1][1]

    def __simulate_dragless(self, angle, velocity, stop_height):
        """Runs a single numerical simulation for a dragless projectile.

        Parameters
        ----------
        angle : float
            The initial angle of the fired projectile.
        velocity : float
            The initial velocity of the fired projectile.
        stop_height : float
            The height at which the simulation will halt during the descending phase.

        Returns
        -------
        positionValues, velocityValues : list
            Output lists of coordinate pairs for both position and velocity.
        """
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
        """Runs a single numerical simulation for a projectile as influenced by Newtonian drag.

        Parameters
        ----------
        angle
        velocity
        stop_height
        """
        raise NotImplementedError

    def __simulate_stokes(self, angle, velocity, stop_height):
        """Runs a single numerical simulation for a projectile as influenced by Stokes drag.

        Parameters
        ----------
        angle
        velocity
        stop_height
        """
        raise NotImplementedError

    def surface_impact(self, surface_height, descending_impact=True):
        """Finds the coordinates of the projectile when it passed through the given surface height.
        By default, this gives the impact in the descending portion of the simulation.

        Parameters
        ----------
        surface_height : float
            The height of the surface to find a projectile impact for.
        descending_impact : bool
            Should the method return the projectile impact for the descending trajectory.

        Returns
        -------
        impact : tuple
            The distance-height coordinate pair for the impact at the specified height.
        """
        matches = [pos for pos in self.positionValues if pos[1] >= surface_height]
        if descending_impact is True:
            return tuple(matches[-1])
        return tuple(matches[0])

    def final_position(self):
        """Returns the final position of the projectile. This is the position of the projectile after passing the
        `stop_height` parameter during the last simulation.

        Returns
        -------
        position : tuple
            The distance-height coordinate pair of the final projectile position as a list.
        """
        return tuple(self.positionValues[-1])

    def max_height(self):
        """Finds the maximum height achieved by the projectile in the last simulation.

        Returns
        -------
        height : float
            The maximum height the projectile attained in the last simulation.
        """
        return max([pos[1] for pos in self.positionValues])

    def time_of_flight(self):
        """Calculates the total time of flight for the projectile after reaching its final position.

        Returns
        -------
        time : float
            The total time of flight for the projectile in seconds.
        """
        return len(self.positionValues) * self.time_step

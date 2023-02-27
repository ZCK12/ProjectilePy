import math
import numpy as np


class ProjectileSimulator:
    def __init__(self, initial_velocity, initial_angle, initial_height=0, time_step=0.0005, gravity=9.981,
                 drag="None", mass=None, drag_coefficient=None, cross_sectional_area=None):
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

        self.cross_sectional_area = cross_sectional_area
        self.drag_coefficient = drag_coefficient
        self.mass = mass

        # Credit to www.engineeringtoolbox.com for this data.
        self.default_earth_atmospheric_density = [[-1000, 1.347], [0, 1.225], [1000, 1.112], [2000, 1.007],
                                                  [3000, 0.9093], [4000, 0.8194], [5000, 0.7364], [6000, 0.6601],
                                                  [7000, 0.5900], [8000, 0.5258], [9000, 0.4671], [10000, 0.4135],
                                                  [15000, 0.1948], [20000, 0.08891], [25000, 0.04008], [30000, 0.01841],
                                                  [40000, 0.003996], [50000, 0.001027], [60000, 0.0003097],
                                                  [70000, 0.00008283], [80000, 0.00001846], [90000, 0]]

        # Construct an air density lookup table with entries at multiples of 50 meters using linear interpolation
        self.default_earth_atmospheric_density = \
            self.__construct_linearised_dictionary(self.default_earth_atmospheric_density)

        self.positionValues = []
        self.velocityValues = []

    def __construct_linearised_dictionary(self, input_list, interval=50):
        x_list, y_list = zip(*input_list)
        interpolated_x = range(input_list[0][0] + interval, input_list[-1][0], interval)
        dictionary = {}

        for x in interpolated_x:
            dictionary[x] = self.__linear_interpolation(x, x_list, y_list)
        return dictionary

    def __linear_interpolation(self, x, x_data, y_data):
        """Perform linear interpolation to estimate the value of y at a given value of x.

        Parameters
        ----------
        x : float
            The x value at which to estimate y.
        x_data : array-like
            A 1-D array of x values.
        y_data : array-like
            A 1-D array of y values corresponding to the x values.

        Returns
        -------
        float
            The estimated value of y at the given value of x.

        Raises
        ------
        ValueError
            If the input arrays do not have the same length or if the x value is out of range of the input data.
        """
        # Check that the input lists have the same length
        if len(x_data) != len(y_data):
            raise ValueError("The input lists must have the same length.")

        # Find the indices of the two x values that bracket x
        i = np.searchsorted(x_data, x) - 1
        if i < 0 or i >= len(x_data) - 1:
            raise ValueError("The x value is out of range of the input data.")
        j = i + 1

        # Perform linear interpolation
        y = y_data[i] + ((y_data[j] - y_data[i]) / (x_data[j] - x_data[i])) * (x - x_data[i])

        return y

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

            # Apply gravity
            velocityVec[1] -= self.time_step * self.gravity

            # Record position and velocity
            positionValues.append(positionVec[:])
            velocityValues.append(velocityVec[:])

            if positionValues[-1][1] < positionValues[-2][1] < stop_height:
                break

        return positionValues, velocityValues

    def __simulate_newtonian(self, angle, velocity, stop_height, mass, drag_coefficient, cross_sectional_area,
                             fluid_density_profile="Default"):
        """Runs a single numerical simulation for a projectile as influenced by Newtonian drag.

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
        assert mass is not None, "A mass must be specified for drag simulation"
        assert type(mass)==float or type(mass)==int, "Mass must be Numerical"
        assert mass >= 0, "A positive mass must be specified for drag simulation"

        assert drag_coefficient is not None, "A drag coefficient must be specified for drag simulation"
        assert type(drag_coefficient) == float or type(drag_coefficient) == int, "Drag coefficient must be Numerical"
        assert drag_coefficient >= 0, "A positive drag coefficient must be specified for drag simulation"

        assert cross_sectional_area is not None, "A cross-sectional area must be specified for drag simulation"
        assert type(cross_sectional_area) == float or type(cross_sectional_area) == int, "Cross-sectional area must be Numerical"
        assert cross_sectional_area >= 0, "A positive cross-sectional area must be specified for drag simulation"

        if fluid_density_profile == "Default":
            fluid_density_profile = self.default_earth_atmospheric_density

        positionVec = [0, 0]
        velocityVec = [math.cos(math.radians(angle)) * velocity, math.sin(math.radians(angle)) * velocity]

        positionValues = [positionVec[:]]
        velocityValues = [velocityVec[:]]

        while True:  # numerical integration (Euler method)
            positionVec[0] += self.time_step * velocityVec[0]
            positionVec[1] += self.time_step * velocityVec[1]

            # Calculate drag forces and velocity
            phi = math.atan2(velocityVec[1], velocityVec[0])
            vel = math.sqrt(velocityVec[0] ** 2 + velocityVec[1] ** 2)
            try:
                drag = self.__calculate_drag_force(vel, fluid_density_profile[(positionVec[1]//50)*50],
                                                   drag_coefficient, cross_sectional_area)
            except KeyError:
                raise ValueError("The used fluid density profile does not contain needed values")
            vel -= (drag/mass) * self.time_step

            # Update velocity vector
            velocityVec[0] = math.cos(phi)*vel
            velocityVec[1] = math.sin(phi)*vel

            # Apply gravity
            velocityVec[1] -= self.time_step * self.gravity

            # Record position and velocity
            positionValues.append(positionVec[:])
            velocityValues.append(velocityVec[:])

            if positionValues[-1][1] < positionValues[-2][1] < stop_height:
                break

        return positionValues, velocityValues

    def __calculate_drag_force(self, velocity, density, drag_coefficient, cross_sectional_area):
        return 0.5 * density * velocity * velocity * drag_coefficient * cross_sectional_area

    def __simulate_stokes(self, angle, velocity, stop_height):
        """Runs a single numerical simulation for a projectile as influenced by Stokes drag.

        Parameters
        ----------
        angle
        velocity
        stop_height
        """
        raise NotImplementedError

    def run(self, stop_height=0, override_drag=None, override_angle=None, override_velocity=None, override_density_profile=None):
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

        if override_density_profile is not None:
            assert type(override_velocity) == dict, "Density profile must be dictionary with keys as multiples of 50"
            density_profile = override_density_profile
        else:
            density_profile = self.default_earth_atmospheric_density

        if drag == "None":
            self.positionValues, self.velocityValues = \
                self.__simulate_dragless(angle, velocity, stop_height)
        elif drag == "Stokes":
            self.positionValues, self.velocityValues = \
                self.__simulate_stokes(angle, velocity, stop_height)
        elif drag == "Newtonian":
            self.positionValues, self.velocityValues = \
                self.__simulate_newtonian(angle, velocity, stop_height, self.mass, self.drag_coefficient,
                                          self.cross_sectional_area, density_profile)
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

    def time_of_flight(self, surface_height=None, descending_impact=True):
        """Calculates the total time of flight for the projectile after reaching its final position.

        Parameters
        ----------
        surface_height : float
            The height of the surface to find time of flight to, or None for total time of flight.
        descending_impact : bool
            Should the method return the time for projectile impact on the descending trajectory.

        Returns
        -------
        time : float
            The time of flight for the projectile in seconds.
        """
        if surface_height is not None:
            matches = [pos for pos in self.positionValues if pos[1] >= surface_height]
            if descending_impact is True:
                return self.positionValues.index(matches[-1]) * self.time_step
            else:
                return self.positionValues.index(matches[0]) * self.time_step
        else:
            return len(self.positionValues) * self.time_step

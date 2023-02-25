class simulator:
    def __init__(self, initial_velocity=None, initial_height=0, initial_angle=0, gravity=9.981, time_step=0.01, drag=None, ):
        self.initial_angle = initial_angle
        self.initial_height = initial_height
        self.initial_velocity = initial_velocity
        self.gravity = gravity
        self.time_step = time_step

    def run(self):
        raise NotImplementedError
        # Code to simulate projectile motion
        pass

    def impact(self, surface_height, descending_impact=True):
        raise NotImplementedError
        # Code to find the impact at a specified height
        pass

    def max_height(self):

        raise NotImplementedError
        # Code to calculate the maximum height
        pass

    def max_range(self):
        raise NotImplementedError
        # Code to calculate the maximum range
        pass

    def time_of_flight(self):
        raise NotImplementedError
        # Code to calculate the time of flight
        pass

from robomaster import robot


class Robot:
    def __init__(self, **kwargs):
        # Chassis
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.z = kwargs.get('z', 0)

        # Sensors
        self.detect = kwargs.get('detect', False)

        # Robotic arm
        self.has_object = kwargs.get('has_object', False)

    #
    # Get
    #
    @property
    def get_x(self):
        return self.x

    @property
    def get_y(self):
        return self.y

    @property
    def get_z(self):
        return self.z

    @property
    def get_detect(self):
        return self.detect

    @property
    def get_has_object(self):
        return self.has_object

    #
    # Management
    #

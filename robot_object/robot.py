from robomaster import robot


class Robot:
    def __init__(self, **kwargs):
        # Common
        self.ep_robot = robot.Robot()

        # Chassis
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.z = kwargs.get('z', 0)
        self.speed = kwargs.get('speed', 0)

        # Sensors
        self.detect = kwargs.get('detect', False)

        # Robotic arm
        self.has_object = kwargs.get('has_object', False)

    #
    # Get
    #
    @property
    def get_x(self):
        """
        Get x position of the robot
        :return:
            x position
        """
        return self.x

    @property
    def get_y(self):
        """
        Get y position of the robot
        :return:
            y position
        """
        return self.y

    @property
    def get_z(self):
        """
        Get z position of the robot
        :return:
            z position
        """
        return self.z

    @property
    def get_speed(self):
        """
        Get speed value of the robot
        :return:
            speed value
        """
        return self.speed

    @property
    def get_detect(self):
        """
        Get whether robot is detected
        :return:
            Detect if robot is detected
        """
        return self.detect

    @property
    def get_has_object(self):
        """
        Get whether robot has object
        :return:
            Detect if robot has object
        """
        return self.has_object

    #
    # Init & Close robot
    #
    def init(self, conn_type="ap"):
        """
        Initialize the robot object
        :param conn_type: connection type, ap by default
        """
        self.ep_robot.initialize(conn_type=conn_type)
        print("Robot initialized")
        self.move(x=self.x, y=self.y, z=self.z, speed=self.speed)

    def close(self):
        """
        Close the robot object
        """
        self.ep_robot.close()
        print("Robot closed")

    #
    # Move robot
    #
    def move(self, **kwargs):
        """
        Move the robot object
        :param kwargs:
        """
        x = kwargs.get('x', 0)
        if not isinstance(x, (int, float)):
            raise TypeError(f"x must be an int or a float, not {type(x)}")

        y = kwargs.get('y', 0)
        if not isinstance(y, (int, float)):
            raise TypeError(f"y must be an int or a float, not {type(y)}")

        z = kwargs.get('z', 0)
        if not isinstance(z, (int, float)):
            raise TypeError(f"z must be an int or a float, not {type(z)}")

        speed = kwargs.get('speed', 0)
        if not isinstance(speed, (int, float)):
            raise TypeError(f"speed must be an int or a float, not {type(speed)}")

        ep_chassis = self.ep_robot.chassis
        ep_chassis.move(x=x, y=y, z=z, xy_speed=speed).wait_for_completed()

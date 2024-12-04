from robomaster import robot
import time
from enum import Enum


class Etat(Enum):
    INIT = 1
    FORWARD = 2
    SLIDE = 3


class EtatSlide(Enum):
    EXTREME_LEFT = 1
    EXTREME_RIGHT = 2
    OFF = 3


class Robot:
    def __init__(self, **kwargs):
        # Common
        self.ep_robot = robot.Robot()

        # Chassis movement
        self.x     = kwargs.get('x', 0)
        self.y     = kwargs.get('y', 0)
        self.z     = kwargs.get('z', 0)
        self.speed = kwargs.get('speed', 0)

        # Chassis position
        self.x_pos = kwargs.get('x_pos', 0)
        self.y_pos = kwargs.get('y_pos', 0)
        self.z_pos = kwargs.get('z_pos', 0)

        self.y_direction    = 1
        self.y_speed        = 0.5
        self.x_max_distance = kwargs.get('x_max_distance', 5)
        self.y_max_distance = kwargs.get('x_max_distance', 2)

        self.state       = Etat.INIT
        self.state_slide = EtatSlide.OFF

        # Sensors
        self.sensor_val = kwargs.get('sensor_val', 0)

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
        ep_chassis = self.ep_robot.chassis
        ep_sensor  = self.ep_robot.sensor

        ep_sensor.sub_distance(freq=20, callback=self.sub_data_handler)
        ep_chassis.sub_position(freq=10, callback=self.sub_position_handler)
        time.sleep(3)
        self.move_distance(y=1, speed=1)

    def close(self):
        """
        Close the robot object
        """
        self.move_speed(x=0, y=0)
        self.ep_robot.close()
        print("Robot closed")

    #
    # Move robot
    #
    def move_distance(self, **kwargs):
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

    def move_speed(self, **kwargs):
        x = kwargs.get('x', 0)
        if not isinstance(x, (int, float)):
            raise TypeError(f"x must be an int or a float, not {type(x)}")

        y = kwargs.get('y', 0)
        if not isinstance(y, (int, float)):
            raise TypeError(f"y must be an int or a float, not {type(y)}")

        z = kwargs.get('z', 0)
        if not isinstance(z, (int, float)):
            raise TypeError(f"z must be an int or a float, not {type(z)}")

        timeout = kwargs.get('timeout', 0)
        if not isinstance(timeout, (int, float)):
            raise TypeError(f"timeout must be an int or a float, not {type(timeout)}")
        self.state = Etat.FORWARD
        self.state_slide = EtatSlide.OFF

        ep_chassis = self.ep_robot.chassis
        ep_chassis.drive_speed(x=x, y=y, z=z, timeout=timeout)

    def goToObstacle(self, **kwargs):
        x = kwargs.get('x', 0)
        if not isinstance(x, (int, float)):
            raise TypeError(f"x must be an int or a float, not {type(x)}")

        y = kwargs.get('y', 0)
        if not isinstance(y, (int, float)):
            raise TypeError(f"y must be an int or a float, not {type(y)}")

        z = kwargs.get('z', 0)
        if not isinstance(z, (int, float)):
            raise TypeError(f"z must be an int or a float, not {type(z)}")

        timeout = kwargs.get('timeout', 0)
        if not isinstance(timeout, (int, float)):
            raise TypeError(f"timeout must be an int or a float, not {type(timeout)}")

        self.state       = Etat.FORWARD
        self.state_slide = EtatSlide.OFF
        self.ep_robot.sensor.unsub_distance()
        self.ep_robot.sensor.sub_distance(freq=20, callback=self.sub_data_drivespeed)
        self.move_speed(x=x, y=y, z=z, timeout=timeout)

    def slideObstacle(self, **kwargs):
        y = kwargs.get('y', 0)
        if not isinstance(y, (int, float)):
            raise TypeError(f"y must be an int or a float, not {type(y)}")

        direction_speed = self.y_speed * self.y_direction

        print("actual y :", self.y_pos, "direction : ", direction_speed)

        self.state = Etat.SLIDE
        self.ep_robot.sensor.unsub_distance()
        self.ep_robot.sensor.sub_distance(freq=20, callback=self.sub_data_slidespeed)
        self.move_speed(y=direction_speed)

    #
    # Manage position
    #
    def sub_position_handler(self, position_info):
        print("Position", position_info)
        self.x_pos, self.y_pos, self.z_pos = position_info
        self.y_direction = -self.y_direction
        if self.x_pos >= 7:
            self.close()
        if self.state == Etat.SLIDE:
            if self.state_slide != EtatSlide.EXTREME_RIGHT and abs(self.y_pos) >= 1.5:
                print("EXTREME DROITE")
                self.state_slide = EtatSlide.EXTREME_RIGHT
                self.slideObstacle()

            elif self.state_slide != EtatSlide.EXTREME_LEFT and abs(self.y_pos) <= 0.5:
                print("EXTREME GAUCHE")
                self.state_slide = EtatSlide.EXTREME_LEFT
                self.slideObstacle()
            else:
                pass

    #
    # Measure distance
    #
    def sub_data_handler(self, distance):
        print("Distance", distance[0])
        self.sensor_val = distance[0]

    def sub_data_drivespeed(self, distance):
        print("driveSpeed:", distance[0])
        self.sensor_val = distance[0]
        if self.sensor_val < 500:
            self.move_speed(x=0)
            self.slideObstacle(y=1)

    def sub_data_slidespeed(self, distance):
        print("slideSpeed:", distance[0])
        self.sensor_val = distance[0]
        if self.sensor_val > 700:
            self.move_speed(x=0)
            self.goToObstacle(x=1)

    def measure_distance(self):
        current_sensor_val = self.sensor_val
        return current_sensor_val

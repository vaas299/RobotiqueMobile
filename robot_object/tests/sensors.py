import time

from robot_object.robot import Robot

if __name__ == '__main__':
    r = Robot()
    r.init()
    # print(r.detect_object())
    r.goToObstacle(x=1)
    time.sleep(2)
    # r.move_distance(x=-1, speed=1)
    time.sleep(11.5)
    # r.close()

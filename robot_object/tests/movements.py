import time

from robot_object.robot import Robot

if __name__ == '__main__':
    r = Robot()
    r.init()
    # r.move_speed(x=1)
    r.move_distance(x=2, speed=1)
    time.sleep(2)
    print(r.x_pos, r.y_pos, r.z_pos)
    # time.sleep(30)
    """r.move_distance(x=-1, speed=1)
    print(r.x_pos, r.y_pos, r.z_pos)
    r.move_distance(y=-1, speed=1)
    print(r.x_pos, r.y_pos, r.z_pos)"""
    # r.close()

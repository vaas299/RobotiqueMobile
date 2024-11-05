from robot_object.robot import Robot

if __name__ == '__main__':
    r = Robot()
    r.init()
    r.move(x=0.5)
    r.move(y=0.5)
    r.move(x=-0.5)
    r.move(y=-0.5)
    r.close()

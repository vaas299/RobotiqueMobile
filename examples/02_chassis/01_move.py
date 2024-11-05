import robomaster
from robomaster import robot
import keyboard  # Nécessite d'installer 'keyboard' avec `pip install keyboard`

# Initialiser le robot
ep_robot = robot.Robot()
ep_robot.initialize(conn_type="ap")  # Connexion Wi-Fi

# Initialiser le moteur
ep_chassis = ep_robot.chassis

# Fonction pour arrêter le mouvement
def stop():
    ep_chassis.drive_speed(x=0, y=0, z=0)

# Contrôle du robot avec les touches directionnelles
try:
    print("Utilise les flèches directionnelles pour déplacer le robot. Appuie sur 'Esc' pour arrêter.")
    while True:
        if keyboard.is_pressed("up"):
            ep_chassis.drive_speed(x=0.5, y=0, z=0)  # Avancer
        elif keyboard.is_pressed("down"):
            ep_chassis.drive_speed(x=-0.5, y=0, z=0)  # Reculer
        elif keyboard.is_pressed("left"):
            ep_chassis.drive_speed(x=0, y=0, z=-30)  # Tourner à gauche
        elif keyboard.is_pressed("right"):
            ep_chassis.drive_speed(x=0, y=0, z=30)  # Tourner à droite
        elif keyboard.is_pressed("esc"):
            stop()
            break
        else:
            stop()
finally:
    # Arrêter le robot et fermer la connexion proprement
    stop()
    ep_robot.close()

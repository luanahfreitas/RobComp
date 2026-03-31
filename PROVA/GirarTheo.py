import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist
from robcomp_util.odom import Odom

class Girar(Node, Odom): 
    def __init__(self):
        super().__init__('girar_node')
        Odom.__init__(self)
        self.timer = None

        self.robot_state = 'done' # Comece em 'done' - reset iniciará a ação
        self.state_machine = { # Adicione quantos estados forem necessários
            'girar': self.girar,
            'stop': self.stop,
            'done': self.done
        }

        # Inicialização de variáveis
        # ...

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers
        # ...
    
    
    def ajuste_angulo(self, angulo):
        return np.arctan2(np.sin(angulo), np.cos(angulo))
    def reset(self, rotacao):
        self.rotacao = rotacao
        self.twist = Twist()
        self.robot_state = 'girar' 
        if self.timer is None:
            self.timer = self.create_timer(0.25, self.control) 
        self.goal_yaw = self.ajuste_angulo(self.yaw + self.rotacao)

    def girar(self):
        erro = self.ajuste_angulo(self.goal_yaw - self.yaw)

        print(f"Erro angular: {np.degrees(erro):.2f}")

        if abs(erro) < np.deg2rad(7):
            self.robot_state = 'stop'
            return
        k = 0.3
        velocidade = k * erro

        self.twist.angular.z = velocidade
        self.twist.linear.x = 0.0


    def stop(self):
        self.twist = Twist()
        print("Parando o robô.")
        self.timer.cancel() 
        self.timer = None 
        self.robot_state = 'done' 
    
    def done(self):
        self.twist = Twist()

    def control(self): 
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]() 
        self.cmd_vel_pub.publish(self.twist) 
def main(args=None):
    rclpy.init(args=args) # Inicia o ROS2
    ros_node = Girar() # Cria o nó

    rclpy.spin_once(ros_node) # Processa as callbacks uma vez
    ros_node.reset() # Reseta o nó para iniciar a ação

    while not ros_node.robot_state == 'done': # Enquanto a ação não estiver finalizada
        rclpy.spin_once(ros_node, timeout_sec=1) # Processa os callbacks e o timer

    ros_node.destroy_node() # Destroi o nó
    rclpy.shutdown()    # Finaliza o ROS2

if __name__ == '__main__': 
    main()
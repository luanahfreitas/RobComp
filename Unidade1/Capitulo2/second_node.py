import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile

class SecondNode(Node):
    def __init__(self):
        super().__init__('second_node')
        self.x = 0.0
        self.y = 0.0

        #assina o tópico /odom recebendo mensagens Odometry
        self.odom_sub = self.create_subscription(
            Odometry, #tipo: obtido com o ros2 topic info /odom
            '/odom', #nome do tópico assinado
            self.odom_callback, #executada a cada mensegem recebida
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE) #perfil de qualidade de serviço (opcional)
        )

        self.timer = self.create_timer(0.25, self.control)

    #atualiza x e y com a posição do robo
    def odom_callback(self, msg: Odometry):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

    #imprime periodicamente as posições
    def control(self):
        print(f'Posição x: {self.x:.3f}')
        print(f'Posição y: {self.y:.3f}\n')


def main(args=None):
    rclpy.init(args=args)
    node = SecondNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
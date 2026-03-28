import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class FirstNode(Node):
    def __init__(self):
        super().__init__('first_node') #cria um nó chamado first_node
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10) #recebe 3 argumentos (tipo da mensagem que será publicada, nome do tópico que será publicado,tamanho da fila de mensagens(opcional))
        self.timer = self.create_timer(0.25, self.control) #recebe 2 argumentos (tempo entre execuções da função, função que será executada)

    def control(self):
        msg = Twist() #cria uma mensagem do tipo Twist
        msg.linear.x = 0.2  # m/s --> velocidade linear
        self.vel_pub.publish(msg) #publica a mensagem no topico cmd_vel


def main(args=None):
    rclpy.init(args=args) #inicializa o módulo rclpy (ROS Client Library for Python)
    node = FirstNode() #cria uma instância da classe FirstNode
    rclpy.spin(node) #mantém o nó em execução até que ele seja finalizado
    node.destroy_node() #finaliza o nó
    rclpy.shutdown() #finaliza o módulo rclpy

if __name__ == '__main__':
    main()
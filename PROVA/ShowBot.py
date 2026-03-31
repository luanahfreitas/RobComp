import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist, Point

from robcomp_interfaces.msg import OrquestratorMSG

# Importar a classe da acao do arquivo, como por exemplo
from robcomp_util.andar import Andar
from treino_ai.girar import Girar
from builtin_interfaces.msg import Time #PRA COLOCAR HORÁRIO INCIAL
# Adicione aqui os imports necessários


class ShowBot(Node): # Mude o nome da classe
    def __init__(self):
        super().__init__('showbot_node') # Mude o nome do nó
        # Outra Herança que você queira fazer
        self.andar_node = Andar() # Cria o nó da Acao
        self.girar_node = Girar()

        self.robot_state = 'READY'
        self.state_machine = {
            'READY': self.iniciar,
            'done': self.done,
            'ESPERAR': self.esperar,
            'IN_PROGRESS': self.andar,
            'girar': self.girar,
            'feedback': self.feedback,

        }

        self.estados_clientes = ['IN_PROGRESS', 'girar'] # Coloque aqui os estados que são "cliente de ação" - TÃO EM OUTRO ARQUIVO

        # Inicialização de variáveis
        self.twist = Twist()
        self.orquestrador = OrquestratorMSG() #INICIALIZEI MINHA MSG 
        self.time = Time()
        self.contador = 0
        self.formas_completas = 0
        
        # Subscribers
        ## Coloque aqui os subscribers
        self.sub = self.create_subscription( #ORDEM DOS PARÂMETROS; tipo da msg, depois tópico, depois a função que roda toda vez q recebe uma msg desse tipo desse tópico
            OrquestratorMSG,
            '/showbot',
            self.callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )

        self.timer = self.create_timer(0.25, self.control)

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers
        self.pub = self.create_publisher(OrquestratorMSG, 'showbot', 10)

        ## Por fim, inicialize o timer
        self.timer = self.create_timer(0.1, self.control)
    

    #callback eh a função que Lê
    def callback(self, msg:OrquestratorMSG): #RODA TODA VEZ Q RECEBER UMA MSG 
        if msg.status != 'READY' and msg.status != 'DONE': # pq é o inicial e o final- pra nao dar erro e ficar no loop infinito de ready ready ready
            self.robot_state = msg.status
        if msg.status == "IN_PROGRESS":
            self.angulo = msg.angle_deg
            self.lado = msg.side
        if msg.status == 'FEEDBACK':
            self.deriva = msg.drift_m

    def iniciar(self):
        self.orquestrador.status = "READY"
        self.currenttime = self.get_clock().now().to_msg()
        self.orquestrador.horario = self.currenttime.sec + self.currenttime.nanosec/10**9 # JEITO CERTO DE CALCULAR O TEMPO AGORA 
        self.orquestrador.student_name = "Luana Hughes"
        self.pub.publish(self.orquestrador)
        self.robot_state = 'ESPERAR'

    def andar(self):
        if self.andar_node.robot_state == 'done': # Se a ação NÂO FOI INICIADA
            print("\nIniciando [ANDAR]...")
            rclpy.spin_once(self.andar_node, timeout_sec=1) # Processa as callbacks uma vez
            self.andar_node.reset(distancia=self.lado) # RECEBE A DISTÂNCIA 

        rclpy.spin_once(self.andar_node, timeout_sec=1) # Processa os callbacks e o timer

        if self.andar_node.robot_state == 'done': # Se a ação FOI FINALIZADA
            self.andar_node.control() # Garante que o robo é parado antes de finalizar a ação
            print("[ANDAR] Finalizada.")
            self.contador += 1
            if self.contador < 360/self.angulo: # só gira se a forma ainda não foi completada 
                self.robot_state = 'girar' # MUDA PRO PRÓXIMO ESTADO Q EU QUERO
            else:
                self.robot_state = 'done'

    def girar(self):
        if self.girar_node.robot_state == 'done': # Se a ação NÂO FOI INICIADA
            print("\nIniciando [GIRAR]...")
            rclpy.spin_once(self.girar_node, timeout_sec=1) # Processa as callbacks uma vez
            self.girar_node.reset(rotacao=np.deg2rad(self.angulo)) # RECEBE A O ANGULO EM RAD

        rclpy.spin_once(self.girar_node) # Processa os callbacks e o timer

        if self.girar_node.robot_state == 'done': # Se a ação FOI FINALIZADA
            self.girar_node.control() # Garante que o robo é parado antes de finalizar a ação
            print("[GIRAR] Finalizada.")
            self.robot_state = 'IN_PROGRESS' # MUDA PRO PRÓXIMO ESTADO Q EU QUERO



    def done(self):
        self.twist = Twist()
        self.orquestrador.status = 'DONE'
        self.pub.publish(self.orquestrador)
        self.robot_state = 'ESPERAR'
        self.contador = 0
    

    def esperar(self):
        self.twist = Twist()
    
    def feedback(self):
        self.get_logger().info(str(self.deriva))
        self.orquestrator.status = 'READY' #publicar que está pronto é DIFERENTE de estar pronto - a msg nesse caso nao eh igual ao robot state 
        self.pub.publish(self.orquestrador)
        self.robot_state = 'ESPERAR'
        self.formas_completas += 1



    def control(self): # Controla a máquina de estados - eh chamado pelo timer
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]() # Chama o método do estado atual 
        if self.robot_state not in self.estados_clientes: # Se o estado atual não é um estado "cliente de ação"
            self.cmd_vel_pub.publish(self.twist) # Publica a velocidade
 
def main(args=None):
    rclpy.init(args=args) # Inicia o ROS2
    ros_node = ShowBot() # Cria o nó

    while not ros_node.formas_completas == 2: # ele para tudo e destrói quando ele tem duas formas completas 
        rclpy.spin_once(ros_node) # Processa os callbacks e o timer

    ros_node.destroy_node() # Destroi o nó
    rclpy.shutdown() # Encerra o ROS2

if __name__ == '__main__':
    main()
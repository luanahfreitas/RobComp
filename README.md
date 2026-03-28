# RobComp
**gravar a tela no linux:** Ctrl + Alt + Shift + R

# UNIDADE 1
## CAPÍTULO 1
### - Terminal
cd .. --> acessar o diretório anterior
pwd --> verificar o caminho do diretório
ls --> utilizado pra visualizar o conteúdo de um diretório
ls -la --> listar infos mais detalhadas
chmod

### - ROS2
ros2 launch my_gazebo pista-23B.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
ros2 run rqt_image_view rqt_image_view --> visualização de imagem

ctrl + r --> reiniciar o mundo simulado



## CAPÍTULO 2
**Nodes**: Um nó é um processo que executa uma tarefa específica na ROS 2.
**Topics**: Por meio deles, nós publicamos e nos inscrevemos (assinamos) para enviar e receber mensagens.
**Messages**: Mensagens são estruturas de dados que carregam informações. São usadas para publicar e receber informações nos tópicos.

### - Navegando nos Tópicos da ROS 2
ros2 topic list --> lista topicos disponíveis
ros2 topic info nome_do_topico --> para descobrir o **tipo** a mensagem de um tópico especifico 
ros2 topic echo nome_do_topico --> Para **ver** as mensagens sendo publicadas em um tópico

### - Criando um novo Pacote na ROS 2
ros2 pkg create --build-type ament_python nome_pacote --dependencies rclpy std_msgs geometry_msgs

### - Criando um Publisher na ROS 2
**Publisher**: nó que envia mensagens para um tópico específico (publica no tópico).

touch nome_node.py --> cria o arquivo do nó
chmod +x *.py --> concede permissão de execução aos arquivos Python **(necessário para executá‑los como nós)**

**Para executar o nó:**
- Criar uma entrada em setup.py para expor o executável.
- Compilar o pacote e atualizar o ambiente.

**Rodando o nó:**
ros2 run nome_pacote nome_node

### - Criando um Subscriber na ROS 2
**Subscriber**: nó que recebe mensagens de um tópico específico (assina no tópico).

touch nome_node.py --> cria o arquivo do nó
chmod +x *.py --> concede permissão de execução aos arquivos Python **(necessário para executá‑los como nós)**

**Para executar o nó:**
- Criar uma entrada em setup.py para expor o executável.
- Compilar o pacote e atualizar o ambiente.

**Rodando o nó:**
ros2 run nome_pacote nome_node



## CAPÍTULO 3
Nó base: *base.py*
Nó de ação *base: base_action.py*
Nó "cliente" da ação: *base_control.py*

### Sensor Laser

# UNIDADE 2

import time
from util import Mapa

class Control(Mapa): # Herdando de Mapa
    def __init__(self):
        # Inicializa a classe Pai
        super().__init__()
    
        self.robot_state = 'forward'
        self.state_machine = {
            'forward': self.forward,
            'left': self.left,
            'right': self.right,
            'stop': self.stop,
        }
    
    def forward(self) -> None:
        # Move pra cima subtraindo 1 de i
        linha_atual, coluna_atual = self.posicao
        nova_posicao = (linha_atual - 1, coluna_atual)

        # Chama o método de atualização de posição
        self.atualizar_posicao(nova_posicao)

        pass

    def left(self) -> None:
        # Move pra esquerda subtraindo 1 de j
        linha_atual, coluna_atual = self.posicao
        nova_posicao = (linha_atual, coluna_atual - 1)
        
        # Chama o método de atualização de posição
        self.atualizar_posicao(nova_posicao)

        pass

    def right(self) -> None:
        # Move pra direita somando 1 a j
        linha_atual, coluna_atual = self.posicao
        nova_posicao = (linha_atual, coluna_atual + 1)

        # Chama o método de atualização de posição
        self.atualizar_posicao(nova_posicao)

        pass
    
    def stop(self) -> None:
        # Não faz nada
        pass

    def control(self) -> None:
        # A lógica de controle do carro deve mudar o estado do carro (self.robot_state)
        # Não chame direto os métodos de movimento, mas sim mude o estado do carro.

        linha_atual, coluna_atual = self.posicao

        # Pare quando estiver na primeira linha mudando o estado para 'stop'.
        if linha_atual == 0:
            self.robot_state = 'stop'

            # Verifique se a posição acima está livre, se sim, mude o estado para 'forward'.
            # Se não, verifique se a posição à esquerda ou à direita está livre, se sim, mude o estado para 'left' ou 'right'.
            # IMPORTANTE: Certifique-se de que o carro não saia dos limites do mapa.
        else:
            acima = (linha_atual - 1, coluna_atual)

            if self.grade_init[acima] == 2:
                left = (linha_atual, coluna_atual - 1)
                right = (linha_atual, coluna_atual + 1)
                if self.grade_init[left] != 2 and coluna_atual != 0: 
                    self.robot_state = 'left'
                else:
                    if coluna_atual != 6 and self.grade_init[right] != 2:
                        self.robot_state = 'right'
                    else:
                        self.robot_state = 'stop'
            else:
                self.robot_state = 'forward'
        
        # Chamada do método de movimento a partir do dicionário
        self.state_machine[self.robot_state]()

        # Mostra a grade atual
        self.mostrar()
def main():
    control = Control()
    control.mostrar()

    i = 40

    while not control.robot_state == 'stop' and i > 0:
        control.control()
        time.sleep(1)
        i -= 1

if __name__=="__main__":
    main()

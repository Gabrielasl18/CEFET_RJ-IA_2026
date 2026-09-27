import search

# Questao 8 
class DeliveryRobotState:
    """
    Representa o estado do robo por:
    - localizacao atual
    - nivel de bateria
    - se ja realizou a recarga obrigatoria
    """

    # Conexoes bidirecionais entre os locais
    CONNECTIONS = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'E'],
        'E': ['D']
    }

    MAX_BATTERY = 3

    def __init__(self, location, battery, recharged=False):
        self.location = location
        self.battery = battery
        self.recharged = recharged

    def isGoal(self):
        """
        O objetivo e chegar a E depois de realizar a recarga.
        """
        return self.location == 'E' and self.recharged

    def legalMoves(self):
        """
        Retorna as acoes aplicaveis ao estado atual.
        """

        moves = []

        # O robo so pode se deslocar se tiver bateria.
        if self.battery > 0:
            moves.extend(self.CONNECTIONS[self.location])

        # A recarga so pode acontecer em C.
        if self.location == 'C' and not self.recharged:
            moves.append('RECARREGAR')

        return moves

    def result(self, action):
        """
        Retorna um NOVO estado apos executar a acao.
        Nao modifica o estado atual.
        """

        if action not in self.legalMoves():
            raise ValueError(
                f'Acao ilegal: {action} no estado {self}'
            )

        # Acao de recarga
        if action == 'RECARREGAR':
            return DeliveryRobotState(
                location=self.location,
                battery=self.MAX_BATTERY,
                recharged=True
            )

        # Acao de deslocamento
        return DeliveryRobotState(
            location=action,
            battery=self.battery - 1,
            recharged=self.recharged
        )

    def __eq__(self, other):
        """
        Dois estados sao iguais quando possuem a mesma
        localizacao, bateria e situacao de recarga.
        """

        if not isinstance(other, DeliveryRobotState):
            return False

        return (
            self.location == other.location
            and self.battery == other.battery
            and self.recharged == other.recharged
        )

    def __hash__(self):
        """
        Permite utilizar os estados em conjuntos e
        dicionarios durante a busca.
        """

        return hash((
            self.location,
            self.battery,
            self.recharged
        ))

    def __str__(self):
        return (
            f'(local={self.location}, '
            f'bateria={self.battery}, '
            f'recarregou={self.recharged})'
        )

    def __repr__(self):
        return self.__str__()


class DeliveryRobotSearchProblem(search.SearchProblem):
    """
    Define o problema de busca do robo entregador.
    """

    def __init__(self):
        # Estado inicial: A, bateria 2, ainda nao recarregou.
        self.startState = DeliveryRobotState(
            location='A',
            battery=2,
            recharged=False
        )

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        return state.isGoal()

    def expand(self, state):
        """
        Retorna uma lista de:
        (proximo_estado, acao, custo)
        """

        children = []

        for action in self.getActions(state):
            nextState = self.getNextState(state, action)

            cost = self.getActionCost(
                state,
                action,
                nextState
            )

            children.append((
                nextState,
                action,
                cost
            ))

        return children

    def getActions(self, state):
        return state.legalMoves()

    def getNextState(self, state, action):
        return state.result(action)

    def getActionCost(self, state, action, next_state):
        assert next_state == state.result(action), (
            'Estado seguinte incorreto.'
        )

        # Tanto deslocamentos quanto recarga custam 1.
        return 1

    def getCostOfActionSequence(self, actions):
        """
        Calcula o custo total e verifica se as acoes
        formam uma sequencia valida.
        """

        if actions is None:
            return 999999

        currentState = self.getStartState()
        totalCost = 0

        for action in actions:

            if action not in self.getActions(currentState):
                return 999999

            nextState = self.getNextState(
                currentState,
                action
            )

            totalCost += self.getActionCost(
                currentState,
                action,
                nextState
            )

            currentState = nextState

        return totalCost


# Execucao do problema de busca
if __name__ == '__main__':

    problem = DeliveryRobotSearchProblem()

    initialState = problem.getStartState()

    print('=== QUESTAO 8 - ROBO ENTREGADOR ===')

    print('\nEstado inicial:')
    print(initialState)

    print('\nAcoes aplicaveis no estado inicial:')
    print(problem.getActions(initialState))

    print('\nO estado inicial e objetivo?')
    print(problem.isGoalState(initialState))

    # Executa a busca em largura
    path = search.breadthFirstSearch(problem)

    print('\n=== SOLUCAO ENCONTRADA PELA BFS ===')

    print('Acoes:', path)

    print(
        'Custo total:',
        problem.getCostOfActionSequence(path)
    )

    # Mostra a sequencia de estados
    currentState = initialState

    print('\n=== SEQUENCIA DE ESTADOS ===')

    print('Estado 0 (inicial):')
    print(currentState)

    for i, action in enumerate(path, start=1):

        previousState = currentState

        currentState = problem.getNextState(
            currentState,
            action
        )

        print(f'\nPasso {i}')
        print('Acao:', action)
        print('Antes:', previousState)
        print('Depois:', currentState)

    print('\n=== RESULTADO FINAL ===')

    print('Estado final:', currentState)

    print(
        'Objetivo alcancado?',
        problem.isGoalState(currentState)
    )

    print(
        'Custo da solucao:',
        problem.getCostOfActionSequence(path)
    )
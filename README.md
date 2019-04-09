# Specification
Example command to play game
```
> python pacman.py -p ReflexAgent -l testClassic
```
## pacman.py
### Classes
```python
class GameState:
    explored = set()

    def initialize(layout, nunGhostAgents):

    def generateSuccessor(agentIndex, action):
        """
        apply action and return next state
        """
        state = GameState(self) # copy current state
        if pacman: # pacman
            PacmanRules.applyAction(state, action)
        else:
            GhostRules.applyAction(state, action, agentIndex)
        
        # check time
        if pacman:
            # TIME_PENALTY = 1
            state.data.scoreChange -= TIME_PENALTY
        # eat food + 10
        # num food = 0 +500 (win)
        # collide scared ghost +200
        # collied ghost -500 (lose)
        # time penalty -1
        # scared time = 40
        state.data.score += state.data.scoreChange
        GameState.explored.add(state)
        return state

class ClassicGameRules:
    def newGame(layout, pacmanAgent, ghostAgents, display, quiet):
        initState = GameState()
        initState.initialize()
        game = Game() # from game.py
        game.state = initState
        return game
    
    def process(state, game):
        """
        check game lose or win
        and set game.gameOver to True or False
        """

class GameStateData:
```
### Functions
```python
# parse command line options to argv
def readCommand(argv):
    parseCommandOptions
    loadLayout
    # load ghost and pacman agent
    pacmanType = loadAgent()
    args['pacman'] = pacmanType()
    ghostType = loadAgent()
    args['ghosts'] = [ghostType() for i in numGhosts]

    loadDisplayFormat
    loadOtherOptions
    return args

def runGames(layout, pacman, ghosts, display, numGames, record, numTraining):
    rules = ClassicGameRules(timeout)
    games = []
    for i in range(numGames):
        game = rules.newGame()
        game.run()
    # not quiet
    games.append(game)
    # numGames > numTraining
    printResult

def loadAgent(agent, nographics):
    """
    default agent:
    - pacman: KeyboardAgent (from -p options)
    - ghost: RandomGhost
    return value:
    Ex: KeyboardAgent, RandomGhost, GreedyAgent,...
    """
    modules = list_module_end_with('gents.py')
    for module in modules:
        import module
        if agent in dir(module)
            # keyboardAgent only allowed when graphic mode is enabled
            return getattr(module, agent)

def main():
    readCommand()
    runGames()
```

## game.py
### Classes
```python
class Game:
    def run():
        self.display.initialize()
        self.numMoves = 0
        # initial for each agents
        for i in numAgents:
            self.agent[i].registerInitialState(self.state)
        agentIndex = self.startIndex # 0 by default
        while not self.gameOver:
            agent = self.agents[agentIndex]
            # if observationFunction not being used
            currentState = self.state
            # if not catch exception
            action = agent.getAction(currentState)
            # if not catch exception execute action (generate next state)
            self.state = self.state.generateSuccessor(agentIndex, action)

            # update display
            self.display.update(self.state.data)

            # check rule (winning, losing, etc)
            self.rules.process(self.state)
            if agentIndex == numAgents + 1:
                self.numMoves += 1
            agentIndex = (agentIndex + 1) % numAgents
        
        self.display.finish()
```
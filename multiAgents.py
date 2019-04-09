# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        additionalScore = 0

        # consider food positions
        foodList = newFood.asList()
        distance = min([manhattanDistance(newPos, food)
                        for food in foodList]) if len(foodList) else 0
        additionalScore += 10.0/(distance + 1)

        # consider ghost position
        distance = min([manhattanDistance(newPos, ghost.getPosition())
                        for ghost in newGhostStates]) if len(newGhostStates) else 0
        additionalScore -= 10.0/(distance + 1)
        if distance < 2:
            additionalScore = -50.0

        # print action, additionalScore
        return successorGameState.getScore() + additionalScore


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
            Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
                Returns the minimax action from the current gameState using self.depth
                and self.evaluationFunction.

                Here are some method calls that might be useful when implementing minimax.

                gameState.getLegalActions(agentIndex):
                Returns a list of legal actions for an agent
                agentIndex=0 means Pacman, ghosts are >= 1

                gameState.generateSuccessor(agentIndex, action):
                Returns the successor game state after an agent takes an action

                gameState.getNumAgents():
                Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        _, action = self.minimax(gameState, self.depth, self.index)
        return action

    def minimax(self, gameState, depth, agent):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        curValue, curAction = None, None

        # update depth and nextAgent
        nextDepth = depth - 1 if agent == gameState.getNumAgents() - 1 else depth
        nextAgent = (agent + 1) % gameState.getNumAgents()

        # update current minimax value base on type of agent
        for action in gameState.getLegalActions(agent):
            nextValue, _ = self.minimax(gameState.generateSuccessor(
                agent, action), nextDepth, nextAgent)
            if curValue == None:
                curValue, curAction = nextValue, action
            elif agent == 0 and nextValue > curValue:
                curValue, curAction = nextValue, action
            elif agent > 0 and nextValue < curValue:
                curValue, curAction = nextValue, action
        return curValue, curAction


class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
                Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        _, action = self.minimax(gameState, self.depth, self.index)
        return action

    def minimax(self, gameState, depth, agent, alpha=-999999999, beta=99999999):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        curValue, curAction = None, None

        # update depth and nextAgent
        nextDepth = depth - 1 if agent == gameState.getNumAgents() - 1 else depth
        nextAgent = (agent + 1) % gameState.getNumAgents()

        # update current minimax value base on type of agent
        for action in gameState.getLegalActions(agent):
			nextValue, _ = self.minimax(gameState.generateSuccessor(agent, action), nextDepth, nextAgent, alpha, beta)
			if curValue == None:
				curValue, curAction = nextValue, action
			elif agent == 0 and nextValue > curValue:
				curValue, curAction = nextValue, action
			elif agent > 0 and nextValue < curValue:
				curValue, curAction = nextValue, action
			# update alpha, beta
			if agent == 0: # pacman
				alpha = max(alpha, curValue)
			else:
				beta = min(beta, curValue)
			if alpha > beta:
				break
        return curValue, curAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
            Returns the expectimax action using self.depth and self.evaluationFunction

            All ghosts should be modeled as choosing uniformly at random from their
            legal moves.
        """
        "*** YOUR CODE HERE ***"
        _, action = self.expectimax(gameState, self.depth, self.index)
        return action

    def expectimax(self, gameState, depth, agent):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        curValue, curAction = None, None

        # update depth and nextAgent
        nextDepth = depth - 1 if agent == gameState.getNumAgents() - 1 else depth
        nextAgent = (agent + 1) % gameState.getNumAgents()

        # update current expectimax value base on type of agent
        numActions = 0
        for action in gameState.getLegalActions(agent):
            nextValue, _ = self.expectimax(gameState.generateSuccessor(agent, action), nextDepth, nextAgent)
            if curValue == None:
                curValue, curAction = nextValue, action
            elif agent == 0 and nextValue > curValue:
                curValue, curAction = nextValue, action
            elif agent > 0:
                curValue += nextValue
            numActions += 1
        if agent == 0:
            return curValue, curAction
        return curValue/float(numActions), curAction
        # return curValue, curAction if agent == 0 else curValue/float(numActions), curAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    additionalScore = 0

    # consider food positions
    foodList = food.asList()
    distance = min([manhattanDistance(pos, food) for food in foodList]) if len(foodList) else 0
    additionalScore += 10.0/(distance + 1)

    # consider ghost position
    distance = min([manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]) if len(ghostStates) else 0
    additionalScore -= 10.0/(distance + 1)
    if distance < 2:
        additionalScore = -500.0

    # consider scared ghost
    for scaredTime in scaredTimes:
        additionalScore += 200.0*scaredTime/40

    # timer
    additionalScore += 1

    # print action, additionalScore
    return currentGameState.getScore() + additionalScore
    


# Abbreviation
better = betterEvaluationFunction

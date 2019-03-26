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
import random, util

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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return betterEvaluationFunction(successorGameState)

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        return self.minimax(gameState, 0, agent=0)[1]

    def next_depth_agent(self,state, agent, depth):
        next_agent = (agent+1) % state.getNumAgents()
        if next_agent == 0:
            next_depth = depth+1
        else:
            next_depth = depth
        return next_depth, next_agent

    def minimax(self, state, depth, agent):
        if len(state.getLegalActions(agent)) == 0:
            return self.evaluationFunction(state), None
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state), None
        bound = 0
        if agent == 0:
            bound = -10000000
        else:
            bound = 10000000

        for action in state.getLegalActions(agent):
            next_state = state.generateSuccessor(agent, action)
            next_depth, next_agent = self.next_depth_agent(next_state, agent, depth)
            value, move = self.minimax(next_state, next_depth, next_agent)
            if agent == 0 and value > bound:
                bound = value
                best_move = value, action
            if agent != 0 and value < bound:
                bound = value
                best_move = value, action
        return best_move
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alpha_beta(gameState, 0, 0, -10000000, 10000000)[1]
        util.raiseNotDefined()

    def next_depth_agent(self,state, agent, depth):
        next_agent = (agent+1) % state.getNumAgents()
        if next_agent == 0:
            next_depth = depth+1
        else:
            next_depth = depth
        return next_depth, next_agent

    def alpha_beta(self, state, depth, agent, alpha, beta):
        if len(state.getLegalActions(agent)) == 0:
            return self.evaluationFunction(state), None
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state), None
        best_move = None, None
        if agent == 0:
            bound = -10000000
        else:
            bound = 10000000

        for action in state.getLegalActions(agent):
            next_state = state.generateSuccessor(agent, action)
            next_depth, next_agent = self.next_depth_agent(next_state, agent, depth)
            value, move = self.alpha_beta(next_state, next_depth, next_agent, alpha, beta)
            if agent == 0:
                if value > bound:
                    bound = value
                    best_move = value, action
                if value >= beta:
                    return best_move
                alpha = max(value, alpha)
            if agent != 0:
                if value < bound:
                    bound = value
                    best_move = value, action
                if value <= alpha:
                    return best_move
                beta = min(value, beta)
        return best_move

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
        return self.expectimax(gameState, 0, 0)[1]
        util.raiseNotDefined()

    def next_depth_agent(self,state, agent, depth):
        next_agent = (agent+1) % state.getNumAgents()
        if next_agent == 0:
            next_depth = depth+1
        else:
            next_depth = depth
        return next_depth, next_agent

    def expectimax(self, state, depth, agent):
        if len(state.getLegalActions(agent)) == 0:
            return self.evaluationFunction(state), None
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state), None
        bound = 0
        if agent == 0:
            bound = -1000000000
        else:
            node_value = 0.0
            prob = 1./(len(state.getLegalActions(agent)))

        for action in state.getLegalActions(agent):
            next_state = state.generateSuccessor(agent, action)
            next_depth, next_agent = self.next_depth_agent(next_state, agent, depth)
            value, move = self.expectimax(next_state, next_depth, next_agent)
            if agent == 0 and value > bound:
                bound = value
                best_move = value, action
            if agent != 0:
                node_value += prob*value
        if agent != 0:
            best_move = node_value, None
        return best_move


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def valid(i):
        if i == 99999:
            return 1
        else:
            return i

    def quad_relu(i):
        if i > 8:
            return 0
        else:
            return i**i
    #Factors to consider:
    # food around
    # ghosts
    # capsules
    # will we be able to eat the ghost during scared time?

    meal = currentGameState.getFood().asList()
    losers = currentGameState.getGhostStates()
    loser_distances = []
    scared_times = []
    capsules = currentGameState.getCapsules()
    current_pos = currentGameState.getPacmanPosition()
    current_score = currentGameState.getScore()

    closest_food = 99999.0
    closest_capsule = 99999.0

    #ghost calcs

    no_scared = True
    dead = False

    for loser in losers:
        loser_pos = loser.getPosition()
        dist = util.manhattanDistance(loser_pos, current_pos)
        loser_distances.append(dist)
        if dist == 0:
            dead = True
        if loser.scaredTimer > 1:
            no_scared = False
        scared_times.append(loser.scaredTimer)

    if dead:
        return -1000

    ghost_pts = 0

    for i in range(len(loser_distances)):
        if scared_times[i] < 1:
            if loser_distances[i] < 3:
                ghost_pts += -10 + 1/(loser_distances[i])**2
            else:
                ghost_pts += -1/(loser_distances[i])

    for capsule in capsules:
        dist = util.manhattanDistance(capsule,current_pos)
        if dist < closest_capsule:
            closest_capsule = dist

    if len(capsules) == 0:
        capsule_pts = 0.0

    else:
        capsule_pts = 1/closest_capsule

    if no_scared:
        capsule_pts *= -10
    else:
        capsule_pts *= 200
    # foodpts

    food_const = 10
    for food in meal:
        dist = util.manhattanDistance(food, current_pos)
        if dist < closest_food:
            closest_food = dist

    food_pts = food_const/closest_food


    return food_pts + ghost_pts + capsule_pts + current_score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


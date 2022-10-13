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

def GetClosestPos( fromP, positions):
        dist = float('inf')
        rPos = ()
        for p in positions:
            d = util.manhattanDistance(fromP, p)
            if d < dist:
                dist = d
                rPos = p
        return rPos, dist

def GetFarthestPos(fromP, positions):
    dist = float('-inf')
    rPos = ()
    for p in positions:
        d = util.manhattanDistance(fromP, p)
        if d > dist:
            dist = d
            rPos = p
    return rPos, dist

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
        #newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostsPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        closestGhostMultiplier = 1
        closestGhostPos, cgD = GetClosestPos(newPos, newGhostsPositions)
        if cgD < 3:
            closestGhostMultiplier = 2.0    
        
        currentFood = currentGameState.getFood()
        currentFoodList = currentFood.asList()
        closestFoodPos, cfDist = GetClosestPos(newPos, currentFoodList)        

        result = cgD * closestGhostMultiplier - cfDist * 2.0
        
        return result

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
        
        return self.minimax(0, 0, gameState)[0]

    def minimax(self, agentIndex, currentDepth, gameState):
        
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            currentDepth += 1
            if currentDepth >= self.depth:
                return None, self.evaluationFunction(gameState)
        
        bestAction = None

        if agentIndex == 0:
            bestScore = float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                _, score = self.minimax(agentIndex + 1, currentDepth, successor)
                
                if score > bestScore:
                    bestScore = score
                    bestAction = action
        else:
            bestScore = float('inf')
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                _, score = self.minimax(agentIndex + 1, currentDepth, successor)
                
                if score < bestScore:
                    bestScore = score
                    bestAction = action
        
        if(bestAction == None):
            return None, self.evaluationFunction(gameState)
        
        return bestAction, bestScore
                    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def AlphaBetaPrunning(self, agentIndex, currentDepth, alpha, beta, gameState):
        
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            currentDepth += 1
            if currentDepth >= self.depth:
                return None, self.evaluationFunction(gameState)
        
        bestAction = None

        if agentIndex == 0:
            bestScore = float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                _, score = self.AlphaBetaPrunning(agentIndex + 1, currentDepth, alpha, beta, successor)

                                    
                if score > bestScore:
                    bestScore = score
                    bestAction = action

                if score > beta:
                    break
                alpha = max(score, alpha)

        else:
            bestScore = float('inf')
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                _, score = self.AlphaBetaPrunning(agentIndex + 1, currentDepth, alpha, beta, successor)

                if score < bestScore:
                    bestScore = score
                    bestAction = action
                
                if score < alpha:
                    break
                beta = min(score, beta)
        
        if(bestAction == None):
            return None, self.evaluationFunction(gameState)
        
        return bestAction, bestScore

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        return self.AlphaBetaPrunning(0, 0, float('-inf'), float('inf'), gameState)[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectimax(self, agentIndex, currentDepth, gameState):
        
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            currentDepth += 1
            if currentDepth >= self.depth:
                return None, self.evaluationFunction(gameState)
        
        bestAction = None

        if agentIndex == 0:
            bestScore = float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                
                successor = gameState.generateSuccessor(agentIndex, action)
                _, score = self.expectimax(agentIndex + 1, currentDepth, successor)
                
                if score > bestScore:
                    bestScore = score
                    bestAction = action
        else:
            bestScore = 0.0
            for action in gameState.getLegalActions(agentIndex):
                p = 1.0 / float(len(gameState.getLegalActions(agentIndex)))
                
                successor = gameState.generateSuccessor(agentIndex, action)
                _, score = self.expectimax(agentIndex + 1, currentDepth, successor)
            
                bestScore += score * p
                bestAction = action #get some action to not rainse "bestAction == None" condition.
                
        if bestAction == None:
            return None, self.evaluationFunction(gameState)
        
        return bestAction, bestScore

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(0, 0, gameState)[0]

def GetClosestFood(fromP, food, walls):
    
    positions = food.asList()
    frontier = util.Queue()
    frontier.push((fromP, 0))
    
    while not frontier.isEmpty():
        currentPos, counter = frontier.pop()
        for a in [(0,1), (0, -1), (1, 0), (-1,0)]:
            nextPosx, nextPosy = currentPos[0] + a[0], currentPos[1] + a[1]
            nextPos = (nextPosx, nextPosy)
            if walls[nextPosx][nextPosy]:
                continue;
            elif food[nextPosx][nextPosy]:
                return nextPos, counter
            frontier.push((nextPos, counter + 1))
    return None, None            
            
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    e = 0.0
    pacmanPos = currentGameState.getPacmanPosition()
    if currentGameState.isWin():
        e = currentGameState.getScore()
    elif currentGameState.isLose():
        e = float('-inf')
    else:
        newGhostStates = currentGameState.getGhostStates()
        food = currentGameState.getFood().asList()
        foodCount = len(food)
        closestFood, closestDist = None, None
        farhestFood, farthestDist  = None, None
        distancesToFood  = 0.0
        if(foodCount > 0):
            closestFood, closestDist =GetClosestPos(pacmanPos, food)
            farhestFood, farthestDist = GetFarthestPos(pacmanPos, food)
            for f in food:
                distancesToFood = distancesToFood + util.manhattanDistance(pacmanPos, f)
            distancesToFood /= float(foodCount)
            
        e = -distancesToFood + (currentGameState.getScore()) + random.random()
        
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        ghostsPos = [ghostState.getPosition() for ghostState in newGhostStates]
        
        closestGhost, closestGhostDist = GetClosestPos(pacmanPos, ghostsPos)
        
        for scT in newScaredTimes:
            if scT > 0:
                e = 1000.0
                e += -closestGhostDist * 10.0
    return e

# Abbreviation
better = betterEvaluationFunction


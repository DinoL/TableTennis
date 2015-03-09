import random

class Simulator:
    def getFirstVictoryProbability(self, skill1, skill2):
        pass
    def firstPlayerWon(self, player1, player2):
        pass
    def getWinner(self, player1, player2):
        return player1 if self.firstPlayerWon(player1, player2) else player2

class HardSimulator(Simulator):
    def getFirstVictoryProbability(self, skill1, skill2):
        return 1.0 if skill1 > skill2 else 0.0
    def firstPlayerWon(self, player1, player2):
        return player1.skill > player2.skill

class RandomizedSimulator(Simulator):
    def __init__(self, skewness = 10):
        self.skewness = skewness
    def getFirstVictoryProbability(self, skill1, skill2):
        prob = 0.5 * (1-abs(skill1-skill2))**self.skewness
        if skill1 > skill2:
            prob = 1.0 - prob
        return prob
    def firstPlayerWon(self, player1, player2):
        return random.random() < self.getFirstVictoryProbability(player1.skill, player2.skill)

class HardRandomSimulator(Simulator):
    def getFirstVictoryProbability(self, skill1, skill2):
        if skill1 + skill2 == 0.0:
            return 0.5
        return skill1 / (skill1 + skill2)
    def firstPlayerWon(self, player1, player2):
        return random.random() < self.getFirstVictoryProbability(player1.skill, player2.skill)

class NonTransitiveSimulator(Simulator):
    def getFirstVictoryProbability(self, skill1, skill2):
        return 0.0
    def firstPlayerWon(self, player1, player2):
        return False

class RealisticSimulator(Simulator):
    def __init__(self, skewness = 10):
        self.pair = {}
        self.skewness = skewness
    def getFirstVictoryProbability(self, skill1, skill2):
        pass
    def firstPlayerWon(self, player1, player2):
        if (player1, player2) not in self.pair:
            simulator = RandomizedSimulator(self.skewness)
            firstWon = simulator.firstPlayerWon(player1, player2)
            self.pair[(player1, player2)] = firstWon
        return self.pair[(player1, player2)]

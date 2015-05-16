import Queue
import random
import collections

class Player:
    """A class representing table tennis player"""
    def __init__(self, name, skill = None):
        if skill is None:
            skill = random.random()
        self.skill = skill
        self.name = name
        self.gamesCount = 0
        self.streak = 0
        self.victories = 0
        self.games = collections.defaultdict(int)
        self.score = 0
        self.matches = 0
        self.matchVictories = 0

class PlayersQueue:
    """A class representing waiting players"""
    def __init__(self):
        self.queue = Queue.Queue()
    def addPlayer(self, player):
        self.queue.put(player)
    def getNextPlayer(self):
        return self.queue.get()
    def empty(self):
        return self.queue.empty()

class Match:
    """A class representing the game being played"""
    def __init__(self, player1, player2, simulator):
        self.winner = simulator.getWinner(player1, player2)
        self.winner.streak += 1
        self.loser = player1 if self.winner == player2 else player2
        self.loser.streak = 0
        self.winner.victories += 1
        self.winner.gamesCount += 1
        self.loser.gamesCount += 1
        self.winner.games[self.loser.name] += 1
        self.loser.games[self.winner.name] += 1
    def getWinner(self):
        return self.winner
    def getLoser(self):
        return self.loser

class Rules:
    """A set of rules for player change order etc"""
    def __init__(self, maxStreak, gamesCount, plotGamesCount):
        self.maxStreak = maxStreak
        self.gamesCount = gamesCount
        self.plotGamesCount = plotGamesCount

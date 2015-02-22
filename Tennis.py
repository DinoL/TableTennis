import random

def getNextPlayer(curPlayer):
    return curPlayer + 1

def getWinner(player1, player2):
    border = player1.skill / (player1.skill + player2.skill)
    return player1 if random.random() < border else player2

class Player:
    """A class representing table tennis player"""
    def __init__(self, name):
        self.skill = random.random()
        self.name = name
        self.games = 0

class Queue:
    """A class representing waiting players"""
    def __init__(self):
        self.queue = Queue()
    def addPlayer(self, player):
        self.queue.put(player)

class Match:
    """A class representing the game being played"""
    def __init__(self, player1, player2):
        self.winner = getWinner(player1, player2)




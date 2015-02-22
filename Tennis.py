import random
import unittest

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

Leonid = Player("Leonid")
Yaroslav = Player("Yaroslav")
print("Leonid's skill: ", Leonid.skill, "\nYaroslav's skill: ",Yaroslav.skill)
wonByMe = 0
totalGames = 10000
for i in range(totalGames):
    if getWinner(Leonid, Yaroslav) == Leonid:
        wonByMe += 1
print("\nPercentage of won by Leonid: ", wonByMe/totalGames)
print("\nExpected: ", Leonid.skill/(Leonid.skill + Yaroslav.skill))
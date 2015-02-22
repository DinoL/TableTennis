import queue
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

class PlayersQueue:
    """A class representing waiting players"""
    def __init__(self):
        self.queue = queue.Queue()
    def addPlayer(self, player):
        self.queue.put(player)
    def getNextPlayer(self):
        return self.queue.get()

class Match:
    """A class representing the game being played"""
    def __init__(self, player1, player2):
        self.winner = getWinner(player1, player2)
        self.loser = player1 if self.winner == player2 else player2
    def getWinner(self):
        return self.winner
    def getLoser(self):
        return self.loser

def trivialTests():
    Leonid = Player("Leonid")
    Yaroslav = Player("Yaroslav")
    print("Leonid's skill: ", Leonid.skill, "\nYaroslav's skill: ",Yaroslav.skill)
    wonByMe = 0
    totalGames = 10000
    for i in range(totalGames):
        if getWinner(Leonid, Yaroslav) == Leonid:
            wonByMe += 1
    print("Percentage of won by Leonid: ", wonByMe/totalGames)
    print("Expected: ", Leonid.skill/(Leonid.skill + Yaroslav.skill))

    queue = PlayersQueue()
    queue.addPlayer(Leonid)
    queue.addPlayer(Yaroslav)
    print("First: ", queue.getNextPlayer().name)
    print("Second: ", queue.getNextPlayer().name)

    game = Match(Leonid, Yaroslav)
    print("Winner: ", game.getWinner().name, ", Loser: ", game.getLoser().name)

trivialTests()
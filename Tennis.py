import queue
import random
import collections

def getFirstVictoryProbability(skill1, skill2):
    return skill1 / (skill1 + skill2)

def getWinner(player1, player2):
    border = getFirstVictoryProbability(player1.skill,player2.skill)
    return player1 if random.random() < border else player2

class Player:
    """A class representing table tennis player"""
    def __init__(self, name):
        self.skill = random.random()
        self.name = name
        self.gamesCount = 0
        self.streak = 0
        self.games = collections.defaultdict(int)

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
        self.winner.streak += 1
        self.loser = player1 if self.winner == player2 else player2
        self.loser.streak = 0
        self.winner.gamesCount += 1
        self.loser.gamesCount += 1
        self.winner.games[self.loser.name] += 1
        self.loser.games[self.winner.name] += 1
    def getWinner(self):
        return self.winner
    def getLoser(self):
        return self.loser

def printSkills(players):
    for player in players:
        print(player.name + "'s skill: ", player.skill)

def trivialTests():
    Leonid = Player("Leonid")
    Yaroslav = Player("Yaroslav")
    Pavel = Player("Pavel")
    Anna = Player("Anna")

    printSkills([Leonid, Yaroslav, Pavel, Anna])

    wonByMe = 0
    totalGames = 10000
    for i in range(totalGames):
        if getWinner(Leonid, Yaroslav) == Leonid:
            wonByMe += 1
    print("Percentage of won by Leonid: ", wonByMe/totalGames)
    print("Expected: ", getFirstVictoryProbability(Leonid.skill, Yaroslav.skill))

    queue = PlayersQueue()
    queue.addPlayer(Leonid)
    queue.addPlayer(Yaroslav)
    queue.addPlayer(Pavel)

    maxStreak = 2
    previousWinner = Anna
    gamesCount = 20
    for i in range(gamesCount):
        newPlayer = queue.getNextPlayer()
        print("Now playing: ", previousWinner.name, newPlayer.name)
        match = Match(previousWinner, newPlayer)
        previousWinner = match.getWinner()
        loser = match.getLoser()
        loser.streak = 0
        queue.addPlayer(loser)
        if previousWinner.streak >= maxStreak:
            previousWinner.streak = 0
            queue.addPlayer(previousWinner)
            previousWinner = queue.getNextPlayer()

    print("Leonid total games: ", Leonid.gamesCount)
    for name, count in Leonid.games.items():
        print(name, " : ", count)

    print("Yaroslav total games: ", Yaroslav.gamesCount)
    for name, count in Yaroslav.games.items():
        print(name, " : ", count)

trivialTests()
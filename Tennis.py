import queue
import random
import collections
import matplotlib.pyplot as plot
import matplotlib.pylab as lab

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
    def getFirstVictoryProbability(self, skill1, skill2):
        prob = 0.5 * (1-abs(skill1-skill2))**10
        if skill1 > skill2:
            prob = 1.0 - prob
        return prob
    def firstPlayerWon(self, player1, player2):
        return random.random() < self.getFirstVictoryProbability(player1.skill, player2.skill)

class HardRandomSimulator(Simulator):
    def getFirstVictoryProbability(self, skill1, skill2):
        return skill1 / (skill1 + skill2)
    def firstPlayerWon(self, player1, player2):
        return random.random() < self.getFirstVictoryProbability(player1.skill, player2.skill)

class NonTransitiveSimulator(Simulator):
    def getFirstVictoryProbability(self, skill1, skill2):
        return 0.0
    def firstPlayerWon(self, player1, player2):
        return False

class RealisticSimulator(Simulator):
    def __init__(self):
        self.pair = {}
    def getFirstVictoryProbability(self, skill1, skill2):
        pass
    def firstPlayerWon(self, player1, player2):
        if (player1, player2) not in self.pair:
            firstWon = random.random() < 0.5
            self.pair[(player1, player2)] = firstWon
        return self.pair[(player1, player2)]

class Player:
    """A class representing table tennis player"""
    def __init__(self, name):
        self.skill = random.random()
        self.name = name
        self.gamesCount = 0
        self.streak = 0
        self.victories = 0
        self.games = collections.defaultdict(int)

class PlayersQueue:
    """A class representing waiting players"""
    def __init__(self):
        self.queue = queue.Queue()
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


def createPlayers():
    Leonid = Player("Leonid")
    Yaroslav = Player("Yaroslav")
    PavelR = Player("PavelR")
    AnnaO = Player("AnnaO")
    Sergey = Player("Sergey")
    Alexey = Player("Alexei")
    AnnaE = Player("AnnaE")
    PavelS = Player("PavelS")
    Roman = Player("Roman")
    Anatoly = Player("Anatoly")
    return [Leonid, Yaroslav, PavelR, AnnaO, Sergey, Alexey, AnnaE, PavelS, Roman, Anatoly]

def fillQueue(queue, players):
    for player in players:
        queue.addPlayer(player)

def getNames(players):
    return [player.name for player in players]

def createGamesMatrix(players):
    names = getNames(players)
    dim = len(players)
    gamesMatrix = lab.zeros([dim, dim])

    for player in players:
        for competitor in players:
            i = players.index(player)
            j = players.index(competitor)
            count = player.games[competitor.name]
            print(count, end="\t")
            gamesMatrix[i, j] = count
        print()

    lab.matshow(gamesMatrix)
    lab.yticks(range(dim), names)
    lab.xticks(range(dim), names)
    lab.show()

def createGamesPlot(players):
    lists = []
    for player in players:
        lists += [sorted(player.games.values(), reverse = True)]

    hist = [sum(e)/len(players) for e in zip(*lists)]
    print("Average sorted games count:", *hist, sep="\t")

    plot.plot(hist)
    plot.title("Games count plot")
    plot.ylabel("Average games count")
    plot.xlabel("Competitor (in order of games count decreasing)")
    plot.show()

def printGamesStatistics(players):
    print("Name\tSkill\tGames\tWon")
    for player in players:
        print(player.name, player.skill, player.gamesCount, player.victories, sep="\t")

def createPairMatchingPlot(players, matches, count):
    xTicks = range(count)
    matches = [(players.index(player1), players.index(player2)) for (player1, player2) in matches]
    first, second = (zip(*matches))
    plot.scatter(xTicks, first[-count:], color = "red")
    plot.scatter(xTicks, second[-count:], color = "blue")
    plot.vlines(xTicks, first[-count:], second[-count:])
    plot.yticks(range(len(players)), getNames(players))
    plot.show()

def runMatches(players, rules, simulator):
    queue = PlayersQueue()
    fillQueue(queue, players)

    previousWinner = queue.getNextPlayer()
    matches = []
    for i in range(rules.gamesCount):
        newPlayer = queue.getNextPlayer()

        # print("Now playing: ", previousWinner.name, newPlayer.name)

        match = Match(previousWinner, newPlayer, simulator)
        previousWinner = match.getWinner()
        loser = match.getLoser()
        loser.streak = 0
        queue.addPlayer(loser)

        matches.append((previousWinner, loser))

        if previousWinner.streak >= rules.maxStreak:
            previousWinner.streak = 0
            queue.addPlayer(previousWinner)
            previousWinner = queue.getNextPlayer()

    return matches

def trivialTests():
    """ All the tests and statistics for the classes above """

    allPlayers = createPlayers()
    rules = Rules(2, 100, 100)
    simulator = HardSimulator()

    matches = runMatches(allPlayers, rules, simulator)

    # Players sorted by their skill
    orderedPlayers = sorted(allPlayers, key = lambda player : player.skill)

    createGamesMatrix(orderedPlayers)
    createGamesPlot(orderedPlayers)
    printGamesStatistics(orderedPlayers)
    createPairMatchingPlot(orderedPlayers, matches, rules.plotGamesCount)

trivialTests()

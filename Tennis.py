import queue
import random
import collections
import matplotlib.pyplot as plot
import matplotlib.pylab as lab

class Simulator:
    @staticmethod
    def firstPlayerWon(player1, player2):
        # border = player1.skill / (player1.skill + player2.skill)
        # border = 0.5 * (1-abs(player1.skill-player2.skill))**10
        # return random.random() < border
        return player1.skill > player2.skill
    @staticmethod
    def getWinner(player1, player2):
        return player1 if Simulator.firstPlayerWon(player1, player2) else player2

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
    def __init__(self, player1, player2):
        simulator = Simulator()
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


def trivialTests():
    """ All the tests and statistics for the classes above """
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

    allPlayers = [Leonid, Yaroslav, PavelR, AnnaO, Sergey, Alexey, AnnaE, PavelS, Roman, Anatoly]

    queue = PlayersQueue()
    for player in allPlayers:
        queue.addPlayer(player)

    rules = Rules(2, 100, 100)

    previousWinner = queue.getNextPlayer()

    matches = []
    for i in range(rules.gamesCount):
        newPlayer = queue.getNextPlayer()

        # print("Now playing: ", previousWinner.name, newPlayer.name)

        match = Match(previousWinner, newPlayer)
        previousWinner = match.getWinner()
        loser = match.getLoser()
        loser.streak = 0
        queue.addPlayer(loser)

        matches.append((previousWinner, loser))

        if previousWinner.streak >= rules.maxStreak:
            previousWinner.streak = 0
            queue.addPlayer(previousWinner)
            previousWinner = queue.getNextPlayer()

    # Players in the skill order
    orderedPlayers = sorted(allPlayers, key = lambda player : player.skill)

    names = [player.name for player in orderedPlayers]
    dim = len(orderedPlayers)
    gamesMatrix = lab.zeros([dim, dim])

    for player in allPlayers:
        for competitor in allPlayers:
            i = orderedPlayers.index(player)
            j = orderedPlayers.index(competitor)
            count = player.games[competitor.name]
            print(count, end="\t")
            gamesMatrix[i, j] = count
        print()

    lab.matshow(gamesMatrix)
    lab.yticks(range(dim), names)
    lab.xticks(range(dim), names)
    lab.show()

    lists = []
    for player in orderedPlayers:
        lists += [sorted(player.games.values(), reverse = True)]

    hist = [sum(e)/len(orderedPlayers) for e in zip(*lists)]
    print("Average sorted games count:", *hist, sep="\t")

    # plot.plot(hist)
    # plot.title("Games count plot")
    # plot.ylabel("Average games count")
    # plot.xlabel("Competitor (in order of games count decreasing)")
    # plot.show()

    print("Name\tSkill\tGames\tWon")
    for player in orderedPlayers:
        print(player.name, player.skill, player.gamesCount, player.victories, sep="\t")

    xTicks = range(rules.plotGamesCount)
    matches = [(orderedPlayers.index(player1), orderedPlayers.index(player2)) for (player1, player2) in matches]
    first, second = (zip(*matches))
    plot.scatter(xTicks, first[-rules.plotGamesCount:], color = "red")
    plot.scatter(xTicks, second[-rules.plotGamesCount:], color = "blue")
    plot.vlines(xTicks, first[-rules.plotGamesCount:], second[-rules.plotGamesCount:])
    plot.yticks(range(dim), names)
    plot.show()

trivialTests()
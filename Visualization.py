from Tennis import Player, PlayersQueue, Match, Rules
import Simulators
import matplotlib.pyplot as plot
import matplotlib.pylab as lab

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

def splitPlayers(players, matches):
    splittedPlayers = []
    for (player1, player2) in matches:
        if player1 not in splittedPlayers:
            splittedPlayers.append(player1)
        if player2 not in splittedPlayers:
            splittedPlayers.append(player2)
    return splittedPlayers

def createPairMatchingPlot(players, matches, count):
    xTicks = range(count)

    players = splitPlayers(players, matches[-count:])

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

def runAllCalculations():
    """ All the tests and statistics for the classes above """

    allPlayers = createPlayers()
    rules = Rules(2, 1000, 100)
    simulator = Simulators.HardSimulator()

    matches = runMatches(allPlayers, rules, simulator)

    # Players sorted by their skill
    orderedPlayers = sorted(allPlayers, key = lambda player : player.skill)

    createGamesMatrix(orderedPlayers)
    createGamesPlot(orderedPlayers)
    printGamesStatistics(orderedPlayers)
    createPairMatchingPlot(orderedPlayers, matches, rules.plotGamesCount)

runAllCalculations()
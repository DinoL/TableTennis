from Tennis import Player, Match
from Simulators import ManualSimulator
import matplotlib.pyplot as plt
import numpy as np
import pylab

statisticsPath = "Align5thTableTennisTournamentLogs.txt"
playersList = []
edges = []

def findPlayerByName(name):
    for player in playersList:
        if name == player.name:
            return player
    player = Player(name)
    playersList.append(player)
    return player

def parseGames(gamesStr):
    games = gamesStr.split(" ")
    gamesList = []
    for game in games:
        [score1, score2] = game.split("-")
        gamesList.append((int(score1), int(score2)))
    return gamesList

def firstWon(gamesList):
    won1 = 0
    won2 = 0
    for score in gamesList:
        if score[0] > score[1]:
            won1 += 1
        elif score[0] < score[1]:
            won2 += 1
    return won1 > won2

def gamesScore(gamesList):
    score1 = 0
    score2 = 0
    for score in gamesList:
        score1 += score[0]
        score2 += score[1]
    return (score1, score2)

def matchesWon(gamesList):
    matches1 = 0
    matches2 = 0
    for score in gamesList:
        if score[0] > score[1]:
            matches1 += 1
        if score[1] > score[0]:
            matches2 += 1
    return (matches1, matches2)

def parseFile(file):
    for line in file:
        parseLine(line)

def parseLine(line):
    lineList = line.split("\t")
    firstPlayer = findPlayerByName(lineList[1].strip())
    secondPlayer = findPlayerByName(lineList[2].strip())
    gamesList = parseGames(lineList[0])
    simulator = ManualSimulator(firstWon(gamesList))
    match = Match(firstPlayer, secondPlayer, simulator)
    winner = match.getWinner()
    print winner.name
    matchesScore = matchesWon(gamesList)
    edges.append((firstPlayer.name, secondPlayer.name))
    scores = gamesScore(gamesList)
    firstPlayer.score += scores[0]
    secondPlayer.score += scores[1]
    firstPlayer.matchVictories += matchesScore[0]
    secondPlayer.matchVictories += matchesScore[1]
    firstPlayer.matches += len(gamesList)
    secondPlayer.matches += len(gamesList)

def printWinners():
    file = open(statisticsPath, 'r')
    parseFile(file)
    file.close()

printWinners()

pos = pylab.arange(len(playersList))+.5

sortedByScore = sorted(playersList, key=lambda x: x.score)
scores = [player.score for player in sortedByScore]
labelsByScore = [player.name for player in sortedByScore]

pylab.barh(pos, scores, align='center', color="lightblue")
pylab.yticks(pos, labelsByScore)
pylab.xlabel('Total score')
pylab.title('Total score by player')
plt.grid()
plt.axes().set_axisbelow(True)
pylab.savefig('TotalScorePlot.png', bbox_inches='tight', dpi=300)
pylab.clf()

sortedByVictories = sorted(playersList, key=lambda x: x.matchVictories)
victories = [player.matchVictories for player in sortedByVictories]
labelsByVictories = [player.name for player in sortedByVictories]

pylab.barh(pos, victories, align='center', color="lightblue")
pylab.yticks(pos, labelsByVictories)
pylab.xlabel('Victories count')
pylab.title('Victories by players')
plt.grid()
plt.axes().set_axisbelow(True)
pylab.savefig('TotalMatchesPlot.png', bbox_inches='tight',dpi=300)
pylab.clf()

sortedByAvgScores = sorted(playersList, key=lambda x: float(x.score) / x.matches)
avgScores = [float(player.score) / player.matches for player in sortedByAvgScores]
labelsByAvgScores = [player.name for player in sortedByAvgScores]

pylab.barh(pos, avgScores, align='center', color="lightblue")
pylab.yticks(pos, labelsByAvgScores)
pylab.xlabel('Average score')
pylab.title('Average score by player')
plt.grid()
plt.axes().set_axisbelow(True)
pylab.savefig('AverageScoresPlot.png', bbox_inches='tight', dpi=300)
pylab.clf()


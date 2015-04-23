from Tennis import Player, Match
from Simulators import ManualSimulator

statisticsPath = "Align5thTableTennisTournamentLogs.txt"
playersList = []

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

def parseFile(file):
    for line in file:
        parseLine(line)

def parseLine(line):
    lineList = line.split("\t")
    firstPlayer = findPlayerByName(lineList[1].strip())
    secondPlayer = findPlayerByName(lineList[2].strip())
    simulator = ManualSimulator(firstWon(parseGames(lineList[0])))
    match = Match(firstPlayer, secondPlayer, simulator)
    print match.getWinner().name

def printWinners():
    file = open(statisticsPath, 'r')
    parseFile(file)
    file.close()

printWinners()
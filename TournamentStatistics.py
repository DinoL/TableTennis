statisticsPath = "Align5thTableTennisTournamentLogs.txt"

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
    for game in gamesList:
        if game[0] > game[1]:
            won1 += 1
        elif game[0] < game[1]:
            won2 += 1
    return won1 > won2

def parseFile(file):
    for line in file:
        parseLine(line)

def parseLine(line):
    lineList = line.split("\t")
    if firstWon(parseGames(lineList[0])):
        print lineList[1]
    else:
        print lineList[2]

def printWinners():
    file = open(statisticsPath, 'r')
    parseFile(file)
    file.close()

printWinners()
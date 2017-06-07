import os
import sys

def printData(Data):
    for year in Data:
        print("YEAR : ", end = "")
        print(year)
        for league in Data[year]:
            print("\tLEAGUE : ", end = "")
            print(league)            
            for team in Data[year][league]:
                if type(team) == type(0):
                    print("---\n\t\tName", end = "\t")
                    print(Data[year][league][team]["name"])                
                    print("\t\tPoints", end = "\t")
                    print(Data[year][league][team]["points"])
                    print("\t\tWins", end = "\t")
                    print(Data[year][league][team]["wins"])
                    print("\t\tLosses", end = "\t")
                    print(Data[year][league][team]["losses"])
                    print("\t\tDraws", end = "\t")
                    print(Data[year][league][team]["draws"])
                    print("\t\tGD", end = "\t")
                    print(Data[year][league][team]["goals for"] - Data[year][league][team]["goals against"])                
                    print("\t\tPosition", end = "\t")
                    print(team)
            print("Home and Away goals for league {0}".format(league))
            print("Home tally: {0}".format(Data[year][league]["home goals"]))
            print("Away tally: {0}".format(Data[year][league]["away goals"]))

def parseLine(line, Data, year, leagueCounter):
    #needs to check whether this is a valid team line
    #needs to check whether we've reached the end of the league table
    #if the first nonwhitespace in this line is number, we assume the line is a
    #valid team
    deal = line.strip()
    if (len(deal) == 0): 
        return leagueCounter;
    
    if(not deal[0].isdigit()):
        deal = deal[0]
        if(deal == "("):
            leagueCounter += 1
        #elif(deal == "-"):
        #    yearCounter += 1
        return leagueCounter;
        
    teamDict = {};
    if (not leagueCounter in Data[year]):
        Data[year][leagueCounter] = {}
    leagueDict = Data[year][leagueCounter]
    if "home goals" not in leagueDict:
        leagueDict["home goals"] = 0
        leagueDict["away goals"] = 0
    
    
    #get the position
    pos = ""
    for char in line:
        if(char == '.'):
            break
        pos = pos + char
    pos = int(pos);
    
    #Next the name
    teamDict["name"] = line[4:34].strip()
    dataVec = line[34:].split()
    
    teamDict["wins"] = int(dataVec[1]) + int(dataVec[5])
    teamDict["draws"] = int(dataVec[2]) + int(dataVec[6])
    teamDict["losses"] = int(dataVec[3]) + int(dataVec[7])

    goals = dataVec[4].split(":")
    leagueDict["home goals"] += int(goals[0])
    leagueDict["away goals"] += int(goals[1])

    Gfor = Gag = ""
    
    colon = False
    for char in dataVec[9]:
        if (char == ':'):
            colon = True
            continue
        elif (colon):
            Gag += char
        else:
            Gfor += char
    teamDict["goals for"] = int(Gfor)
    teamDict["goals against"] = int(Gag)
    teamDict["points"] = teamDict["wins"]*3 + teamDict["draws"]
    
    
    #at the end
    leagueDict[pos] = teamDict
    return leagueCounter

Data = {}
#yearCounter = 1889
#some other loop
rootDir = "eng-england-master"
for dirName, subdirList, fileList in os.walk(rootDir):
   # path = []
    
    for fname in fileList:
        if(fname[:6] == "README"):
            #print(fname)
            leagueCounter = 1
            Data[dirName[len(dirName)-7:]] = {} #makes the dictionary for the year (once per file)
            file = open(dirName+"/"+fname, 'r')
            for line in file:
                #get the year folder name by only leaving the 
                try:
                    leagueCounter = parseLine(line, Data, dirName[len(dirName)-7:], leagueCounter)
                except ValueError:
                    #catch a string saying this wasn't a valid file (Eg A README THAT WASN'T A SET OF TABLES)
                    '''
                    print("About to exit due to error")
                    print(fname)
                    print(fname[:6])
                    print(dirName[len(dirName)-7:])
                    print(dirName+"/"+fname)
                    print(line)
                    sys.exit("entered wrong file")
                    '''
                    #This error doesn't affect the data so keep going
#printData(Data)

#where league is a dictionary
def findMeanPoints(league):
    total = 0
    teams = 1
    for pos in league:
        if(not pos.isdigit()):
            continue
        total += 3*league[pos]["wins"] + league[pos]["draws"]
        teams = pos
    return (float(total)/teams, teams)
    
#where league is a dictionary
def standardDev(league):
    meanTuple = findMeanPoints(league)
    assert(meanTuple[0] > 0)
    total = 0
    for pos in league:
        if(not pos.isdigit()):
            continue
        total += (3*league[pos]["wins"] + league[pos]["draws"] - meanTuple[0])**2
    total = total/meanTuple[1]
    return total**0.5

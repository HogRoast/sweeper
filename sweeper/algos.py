import collections
import datetime
import inspect

class BaseModel:
    numMatches = 6

    def processMatches(self, results, visitingMethod):
        matchData = {}
        for row in results:
            try:
                matchDate = row['Date']
                homeTeam = row['HomeTeam']
                awayTeam = row['AwayTeam']
            except KeyError:
                break
            if matchDate == '' or None in (homeTeam, awayTeam, matchDate):
                break
            matchDate = matchDate.strip()
            homeTeam = homeTeam.strip()
            awayTeam = awayTeam.strip()
          
            matchData = visitingMethod(
                    matchData, row, matchDate, homeTeam, awayTeam)
        return matchData

    def markMatch(self, matchData, matchDate, homeTeam, awayTeam):
        if isinstance(matchDate, str): matchDate = matchDate.strip()
        if isinstance(homeTeam, str): homeTeam = homeTeam.strip()
        if isinstance(awayTeam, str): awayTeam = awayTeam.strip()

        if matchDate == '' or \
                None in (matchData, matchDate, homeTeam, awayTeam):
            return (matchDate, homeTeam, awayTeam, None, None, None)

        try:
            homeTeamMatchData = matchData[homeTeam]
            awayTeamMatchData = matchData[awayTeam]
        except KeyError:
            return (matchDate, homeTeam, awayTeam, None, None, None)

        # Find match date, assumes the matchData is sorted by date asc!
        homeTeamQ = collections.deque()
        for match in homeTeamMatchData:
            d1 = strToDate(match[0])
            d2 = strToDate(matchDate)
            if d1 > d2:
               break 
            if len(homeTeamQ) >= numMatches:
                homeTeamQ.popleft()
            homeTeamQ.append((match[1], match[2]))

        if len(homeTeamQ) < numMatches:
            return(matchDate, homeTeam, awayTeam, None, None, None)

        awayTeamQ = collections.deque()
        for match in awayTeamMatchData:
            d1 = strToDate(match[0])
            d2 = strToDate(matchDate)
            if d1 > d2:
               break 
            if len(awayTeamQ) >= numMatches:
                awayTeamQ.popleft()
            awayTeamQ.append((match[1], match[2]))

        if len(awayTeamQ) < numMatches:
            return(matchDate, homeTeam, awayTeam, None, None, None)

        # sum the team Qs 
        homeTeamScore = 0
        homeTeamForm = ''
        for i in homeTeamQ:
            homeTeamScore += i[0]
            homeTeamForm += i[1] + ' '
            
        awayTeamScore = 0
        awayTeamForm = ''
        for i in awayTeamQ:
            awayTeamScore += i[0]
            awayTeamForm += i[1] + ' '

        return(matchDate, homeTeam, awayTeam, (homeTeamScore - awayTeamScore), 
                homeTeamForm.strip(), awayTeamForm.strip())

class GoalsScoredSupremacy(BaseModel):
    def processMatches(self, results):
        return BaseModel.processMatches(
                self, results, self.calculateGoalsScored)

    def calculateGoalsScored(
            self, matchData, row, matchDate, homeTeam, awayTeam):
        if row['FTHG'] == '' or row['FTAG'] == '' or row['FTR'] == '':
            return matchData
        fthg = int(row['FTHG'].strip())
        ftag = int(row['FTAG'].strip())
        ftRes = row['FTR']
        resStr = ''
        if homeTeam in matchData:
            if ftRes == 'H':
                resStr = '{}:{}v{}'.format('W', fthg, ftag)
            elif ftRes == 'D':
                resStr = '{}:{}v{}'.format('D', fthg, ftag)
            else: 
                resStr = '{}:{}v{}'.format('L', fthg, ftag)
            matchData[homeTeam].append((matchDate, fthg, resStr))
        else:
            if ftRes == 'H':
                resStr = '{}:{}v{}'.format('W', fthg, ftag)
            elif ftRes == 'D':
                resStr = '{}:{}v{}'.format('D', fthg, ftag)
            else: 
                resStr = '{}:{}v{}'.format('L', fthg, ftag)
            matchData[homeTeam] = [(matchDate, fthg, resStr)]
        if awayTeam in matchData:
            if ftRes == 'A':
                resStr = '{}:{}v{}'.format('W', fthg, ftag)
            elif ftRes == 'D':
                resStr = '{}:{}v{}'.format('D', fthg, ftag)
            else: 
                resStr = '{}:{}v{}'.format('L', fthg, ftag)
            matchData[awayTeam].append((matchDate, ftag, resStr))
        else:
            if ftRes == 'A':
                resStr = '{}:{}v{}'.format('W', fthg, ftag)
            elif ftRes == 'D':
                resStr = '{}:{}v{}'.format('D', fthg, ftag)
            else: 
                resStr = '{}:{}v{}'.format('L', fthg, ftag)
            matchData[awayTeam] = [(matchDate, ftag, resStr)]
        return matchData

class AlgoFactory:
    algos = {
                GoalsScoredSupremacy.__name__ : GoalsScoredSupremacy
            }

    @classmethod
    def create(cls, algoName):
        return cls.algos[algoName]() 

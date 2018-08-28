import collections
import datetime

numMatches = 6

def strToDate(date):
    try:
        d = datetime.datetime.strptime(date, '%d/%m/%y').date()
    except ValueError:
        d = datetime.datetime.strptime(date, '%d/%m/%Y').date()
    return d

class BaseModel:
    def processMatches(self, results, visitingMethod):
        matchData = {}
        for row in results:
            try:
                matchDate = row['Date']
                homeTeam = row['HomeTeam']
                awayTeam = row['AwayTeam']
            except KeyError:
                break
            if matchDate == '' or homeTeam is None or awayTeam is None or matchDate is None:
                break
            matchDate = matchDate.strip()
            homeTeam = homeTeam.strip()
            awayTeam = awayTeam.strip()
          
            matchData = visitingMethod(matchData, row, matchDate, homeTeam, awayTeam)
        return matchData

    def markMatch(self, matchData, matchDate, homeTeam, awayTeam):
        if matchDate == '' or matchData is None or matchDate is None or homeTeam is None or awayTeam is None:
            return (matchDate, homeTeam, awayTeam, None, None, None)

        matchDate = matchDate.strip()
        homeTeam = homeTeam.strip()
        awayTeam = awayTeam.strip()

        homeTeamMatchData = matchData[homeTeam]
        awayTeamMatchData = matchData[awayTeam]
        ''' Find match date, assumes the matchData is sorted by date asc! '''
        homeTeamQ = collections.deque()
        for match in homeTeamMatchData:
            d1 = strToDate(match[0])
            d2 = strToDate(matchDate)
            if d1 >= d2:
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
            if d1 >= d2:
               break 
            if len(awayTeamQ) >= numMatches:
                awayTeamQ.popleft()
            awayTeamQ.append((match[1], match[2]))

        if len(awayTeamQ) < numMatches:
            return(matchDate, homeTeam, awayTeam, None, None, None)

        ''' sum the team Qs '''
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

        return(matchDate, homeTeam, awayTeam, (homeTeamScore - awayTeamScore), homeTeamForm.strip(), awayTeamForm.strip())

class GoalsScoredSupremacy(BaseModel):
    def processMatches(self, results):
        return BaseModel.processMatches(self, results, self.calculateGoalsScored)

    def calculateGoalsScored(self, matchData, row, matchDate, homeTeam, awayTeam):
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

class MatchResultSupremacy(BaseModel):
    def processMatches(self, results):
        return BaseModel.processMatches(self, results, self.calculateMatchResult)

    def calculateMatchResult(self, matchData, row, matchDate, homeTeam, awayTeam):
        if row['FTR'] == '':
            return matchData
        ftRes = row['FTR']
        score = 0
        if homeTeam in matchData:
            if ftRes == 'H' : score = 1
            matchData[homeTeam].append((matchDate, score))
        else:
            if ftRes == 'H' : score = 1
            matchData[homeTeam] = [(matchDate, score)]
        if awayTeam in matchData:
            if ftRes == 'A' : score = 1
            matchData[homeTeam].append((matchDate, score))
        else:
            if ftRes == 'A' : score = 1
            matchData[homeTeam] = [(matchDate, score)]
        return matchData

class GoalDifferenceSupremacy(BaseModel):
    def processMatches(self, results):
        return BaseModel.processMatches(self, results, self.calculateGoalDifference)

    def calculateGoalDifference(self, matchData, row, matchDate, homeTeam, awayTeam):
        if row['FTHG'] == '' or row['FTAG'] == '':
            return matchData
        fthg = int(row['FTHG'].strip())
        ftag = int(row['FTAG'].strip())
        if homeTeam in matchData:
            matchData[homeTeam].append((matchDate, fthg-ftag))
        else:
            matchData[homeTeam] = [(matchDate, fthg-ftag)]
        if awayTeam in matchData:
            matchData[awayTeam].append((matchDate, ftag-fthg))
        else:
            matchData[awayTeam] = [(matchDate, ftag-fthg)]
        return matchData

# The league that we are targetting analysis on (from football-data.co.uk), E0 is the english premier league, E1 the championship and so on
analysisDir = 'Analysis'
league = 'SP1'
#model = GoalDifferenceSupremacy()
model = GoalsScoredSupremacy()
#model = MatchResultSupremacy()

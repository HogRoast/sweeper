import collections
import datetime
import inspect

from abc import ABC, abstractmethod
from sweeper.dbos.match import Match

class BaseModel:
    numMatches = 5

    @abstractmethod
    def markMatch(self, match:Match, homePrev:list, awayPrev:list):
        '''
        Mark the match according to the data from the prior matches,
        assumes prior matches are sorted by date descending.

        :param match: the subject match to be marked
        :param homePrev: the previous matches for the home team
        :param awayPrev: the previous matches for the away team
        :returns: an integer representing the match mark
        '''
        pass

class GoalsScoredSupremacy(BaseModel):
    def sumGoals(self, team:str, matches:list):
        '''
        Add the goals scored by the team in the previous matches

        :param team: the team whose goals we wish to sum
        :matches: a list of historical matches
        :returns: the number of goals scored by team in matches
        '''
        return  sum([m.getHome_Goals() for m in matches \
                    if team == m.getHome_Team()]) \
                + \
                sum([m.getAway_Goals() for m in matches \
                    if team == m.getAway_Team()])

    def markMatch(self, match:Match, homePrev:list, awayPrev:list):
        '''
        Mark the match according to the data from the prior matches,
        assumes prior matches are sorted by date descending.

        :param match: the subject match to be marked
        :param homePrev: the previous matches for the home team
        :param awayPrev: the previous matches for the away team
        :returns: an integer representing the match mark or 99 if there are
        matches to make the calculation
        '''
        if len(homePrev) <= self.numMatches or len(awayPrev) <= self.numMatches:
            return 99
        ''' 
        print(match)
        print(homePrev[:self.numMatches])
        print(awayPrev[:self.numMatches])
        ''' 
        hTeamGoals = self.sumGoals(match.getHome_Team(), \
                homePrev[:self.numMatches]) 
        aTeamGoals = self.sumGoals(match.getAway_Team(), \
                awayPrev[:self.numMatches]) 
        return hTeamGoals - aTeamGoals

class AlgoFactory:
    algos = {
                GoalsScoredSupremacy.__name__ : GoalsScoredSupremacy
            }

    @classmethod
    def create(cls, algoName:str):
        return cls.algos[algoName]() 

# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.result import Result  # noqa: F401,E501
from swagger_server import util


class Fixture(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, home_team: str=None, away_team: str=None, date: str=None, league_id: str=None, result: Result=None):  # noqa: E501
        """Fixture - a model defined in Swagger

        :param home_team: The home_team of this Fixture.  # noqa: E501
        :type home_team: str
        :param away_team: The away_team of this Fixture.  # noqa: E501
        :type away_team: str
        :param date: The date of this Fixture.  # noqa: E501
        :type date: str
        :param league_id: The league_id of this Fixture.  # noqa: E501
        :type league_id: str
        :param result: The result of this Fixture.  # noqa: E501
        :type result: Result
        """
        self.swagger_types = {
            'home_team': str,
            'away_team': str,
            'date': str,
            'league_id': str,
            'result': Result
        }

        self.attribute_map = {
            'home_team': 'homeTeam',
            'away_team': 'awayTeam',
            'date': 'date',
            'league_id': 'leagueId',
            'result': 'result'
        }

        self._home_team = home_team
        self._away_team = away_team
        self._date = date
        self._league_id = league_id
        self._result = result

    @classmethod
    def from_dict(cls, dikt) -> 'Fixture':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Fixture of this Fixture.  # noqa: E501
        :rtype: Fixture
        """
        return util.deserialize_model(dikt, cls)

    @property
    def home_team(self) -> str:
        """Gets the home_team of this Fixture.

        Name of the home team  # noqa: E501

        :return: The home_team of this Fixture.
        :rtype: str
        """
        return self._home_team

    @home_team.setter
    def home_team(self, home_team: str):
        """Sets the home_team of this Fixture.

        Name of the home team  # noqa: E501

        :param home_team: The home_team of this Fixture.
        :type home_team: str
        """
        if home_team is None:
            raise ValueError("Invalid value for `home_team`, must not be `None`")  # noqa: E501

        self._home_team = home_team

    @property
    def away_team(self) -> str:
        """Gets the away_team of this Fixture.

        Name of the away team  # noqa: E501

        :return: The away_team of this Fixture.
        :rtype: str
        """
        return self._away_team

    @away_team.setter
    def away_team(self, away_team: str):
        """Sets the away_team of this Fixture.

        Name of the away team  # noqa: E501

        :param away_team: The away_team of this Fixture.
        :type away_team: str
        """
        if away_team is None:
            raise ValueError("Invalid value for `away_team`, must not be `None`")  # noqa: E501

        self._away_team = away_team

    @property
    def date(self) -> str:
        """Gets the date of this Fixture.

        Date of the fixture YYYYMMDD  # noqa: E501

        :return: The date of this Fixture.
        :rtype: str
        """
        return self._date

    @date.setter
    def date(self, date: str):
        """Sets the date of this Fixture.

        Date of the fixture YYYYMMDD  # noqa: E501

        :param date: The date of this Fixture.
        :type date: str
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def league_id(self) -> str:
        """Gets the league_id of this Fixture.

        The league identifier  # noqa: E501

        :return: The league_id of this Fixture.
        :rtype: str
        """
        return self._league_id

    @league_id.setter
    def league_id(self, league_id: str):
        """Sets the league_id of this Fixture.

        The league identifier  # noqa: E501

        :param league_id: The league_id of this Fixture.
        :type league_id: str
        """
        if league_id is None:
            raise ValueError("Invalid value for `league_id`, must not be `None`")  # noqa: E501

        self._league_id = league_id

    @property
    def result(self) -> Result:
        """Gets the result of this Fixture.


        :return: The result of this Fixture.
        :rtype: Result
        """
        return self._result

    @result.setter
    def result(self, result: Result):
        """Sets the result of this Fixture.


        :param result: The result of this Fixture.
        :type result: Result
        """

        self._result = result

# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.fixture import Fixture  # noqa: F401,E501
from swagger_server import util


class Analysis(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, fixture: Fixture=None, mark: int=None):  # noqa: E501
        """Analysis - a model defined in Swagger

        :param fixture: The fixture of this Analysis.  # noqa: E501
        :type fixture: Fixture
        :param mark: The mark of this Analysis.  # noqa: E501
        :type mark: int
        """
        self.swagger_types = {
            'fixture': Fixture,
            'mark': int
        }

        self.attribute_map = {
            'fixture': 'fixture',
            'mark': 'mark'
        }

        self._fixture = fixture
        self._mark = mark

    @classmethod
    def from_dict(cls, dikt) -> 'Analysis':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Analysis of this Analysis.  # noqa: E501
        :rtype: Analysis
        """
        return util.deserialize_model(dikt, cls)

    @property
    def fixture(self) -> Fixture:
        """Gets the fixture of this Analysis.


        :return: The fixture of this Analysis.
        :rtype: Fixture
        """
        return self._fixture

    @fixture.setter
    def fixture(self, fixture: Fixture):
        """Sets the fixture of this Analysis.


        :param fixture: The fixture of this Analysis.
        :type fixture: Fixture
        """
        if fixture is None:
            raise ValueError("Invalid value for `fixture`, must not be `None`")  # noqa: E501

        self._fixture = fixture

    @property
    def mark(self) -> int:
        """Gets the mark of this Analysis.

        The ranking of this match according to the algo used  for analysis  # noqa: E501

        :return: The mark of this Analysis.
        :rtype: int
        """
        return self._mark

    @mark.setter
    def mark(self, mark: int):
        """Sets the mark of this Analysis.

        The ranking of this match according to the algo used  for analysis  # noqa: E501

        :param mark: The mark of this Analysis.
        :type mark: int
        """
        if mark is None:
            raise ValueError("Invalid value for `mark`, must not be `None`")  # noqa: E501

        self._mark = mark

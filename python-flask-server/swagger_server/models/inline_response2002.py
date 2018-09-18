# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.fixture import Fixture  # noqa: F401,E501
from swagger_server.models.status import Status  # noqa: F401,E501
from swagger_server import util


class InlineResponse2002(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, s: Status=None, errmsg: str=None, d: List[Fixture]=None):  # noqa: E501
        """InlineResponse2002 - a model defined in Swagger

        :param s: The s of this InlineResponse2002.  # noqa: E501
        :type s: Status
        :param errmsg: The errmsg of this InlineResponse2002.  # noqa: E501
        :type errmsg: str
        :param d: The d of this InlineResponse2002.  # noqa: E501
        :type d: List[Fixture]
        """
        self.swagger_types = {
            's': Status,
            'errmsg': str,
            'd': List[Fixture]
        }

        self.attribute_map = {
            's': 's',
            'errmsg': 'errmsg',
            'd': 'd'
        }

        self._s = s
        self._errmsg = errmsg
        self._d = d

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2002':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_2 of this InlineResponse2002.  # noqa: E501
        :rtype: InlineResponse2002
        """
        return util.deserialize_model(dikt, cls)

    @property
    def s(self) -> Status:
        """Gets the s of this InlineResponse2002.


        :return: The s of this InlineResponse2002.
        :rtype: Status
        """
        return self._s

    @s.setter
    def s(self, s: Status):
        """Sets the s of this InlineResponse2002.


        :param s: The s of this InlineResponse2002.
        :type s: Status
        """
        if s is None:
            raise ValueError("Invalid value for `s`, must not be `None`")  # noqa: E501

        self._s = s

    @property
    def errmsg(self) -> str:
        """Gets the errmsg of this InlineResponse2002.


        :return: The errmsg of this InlineResponse2002.
        :rtype: str
        """
        return self._errmsg

    @errmsg.setter
    def errmsg(self, errmsg: str):
        """Sets the errmsg of this InlineResponse2002.


        :param errmsg: The errmsg of this InlineResponse2002.
        :type errmsg: str
        """

        self._errmsg = errmsg

    @property
    def d(self) -> List[Fixture]:
        """Gets the d of this InlineResponse2002.


        :return: The d of this InlineResponse2002.
        :rtype: List[Fixture]
        """
        return self._d

    @d.setter
    def d(self, d: List[Fixture]):
        """Sets the d of this InlineResponse2002.


        :param d: The d of this InlineResponse2002.
        :type d: List[Fixture]
        """

        self._d = d

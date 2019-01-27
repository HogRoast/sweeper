import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.league import League
from swagger_server.models.status import Status
from swagger_server import util

from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from sweeper.utils import getSweeperConfig
from sweeper.dbos.league import League as SWPR_League

def accounts_account_id_algos_get(accountId):  # noqa: E501
    """accounts_account_id_algos_get

    Get available algos for this account # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str

    :rtype: InlineResponse2003
    """
    return 'do some magic!'


def accounts_account_id_analysis_algo_id_get(accountId, algoId):  # noqa: E501
    """accounts_account_id_analysis_algo_id_get

    Run the analysis for the specified algo across all fixtures available to this account # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str
    :param algoId: The algo identifier.
    :type algoId: str

    :rtype: InlineResponse2006
    """
    return 'do some magic!'


def accounts_account_id_fixture_history_get(accountId, maxCount=None):  # noqa: E501
    """accounts_account_id_fixture_history_get

    Get fixture history available to this account. # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str
    :param maxCount: Maximum amount of fixtures to return.
    :type maxCount: 

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def accounts_account_id_fixtures_get(accountId):  # noqa: E501
    """accounts_account_id_fixtures_get

    Get next fixture lists available to this account # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def accounts_account_id_get(accountId):  # noqa: E501
    """accounts_account_id_get

    Get account information. # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def accounts_account_id_leagues_get(accountId):  # noqa: E501
    """accounts_account_id_leagues_get

    Get a list of leagues available to this account. # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str

    :rtype: InlineResponse2007
    """
    return 'do some magic!'


def accounts_account_id_statistics_algo_id_get(accountId, algoId):  # noqa: E501
    """accounts_account_id_statistics_algo_id_get

    Get the statistics for the specified algo across all the leagues available to this account # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str
    :param algoId: The algo identifier.
    :type algoId: str

    :rtype: InlineResponse2005
    """
    return 'do some magic!'


def accounts_account_id_statistics_league_id_algo_id_get(accountId, leagueId, algoId):  # noqa: E501
    """accounts_account_id_statistics_league_id_algo_id_get

    Get the statistics for the specified league and algo # noqa: E501

    :param accountId: The account identifier.
    :type accountId: str
    :param leagueId: The league identifier.
    :type leagueId: str
    :param algoId: The algo identifier.
    :type algoId: str

    :rtype: InlineResponse2004
    """
    return 'do some magic!'


def authorize_post(login, password):  # noqa: E501
    """authorize_post

    Oauth2 Password authorization. # noqa: E501

    :param login: User Login.
    :type login: str
    :param password: User Password.
    :type password: str

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def leagues_get():  # noqa: E501
    """leagues_get

    Get a list of all available leagues. # noqa: E501


    :rtype: InlineResponse2007
    """

    r = InlineResponse2007(s=Status.OK)

    config = getSweeperConfig()
    dbName = config['dbName']
    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        leagues = db.select(SWPR_League())
        listOfLeagues = [League(l.getMnemonic(), l.getDesc()) for l in leagues]
        r.d = listOfLeagues
    return r

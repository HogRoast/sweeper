INSERT INTO source values 
    (1, 'Football-Data', 'www.football-data.co.uk', 'http://www.football-data.co.uk/fixtures.csv');

INSERT INTO source_team_map values 
    (1, 'Waasland-Beveren', 'Waasland Beveren');

INSERT INTO source_league_map values 
    (1, 'E0', 'E0'),
    (1, 'E1', 'E1'),
    (1, 'D1', 'D1'),
    (1, 'B1', 'B1'),
    (1, 'SC0', 'SC0'),
    (1, 'I1', 'I1'),
    (1, 'F1', 'F1'),
    (1, 'SP1', 'SP1');

INSERT INTO source_season_map values 
    (1, '1011', '1011', 'http://www.football-data.co.uk/mmz4281/1011/{}.csv', 1),
    (1, '1112', '1112', 'http://www.football-data.co.uk/mmz4281/1112/{}.csv', 1),
    (1, '1213', '1213', 'http://www.football-data.co.uk/mmz4281/1213/{}.csv', 1),
    (1, '1314', '1314', 'http://www.football-data.co.uk/mmz4281/1314/{}.csv', 1),
    (1, '1415', '1415', 'http://www.football-data.co.uk/mmz4281/1415/{}.csv', 1),
    (1, '1516', '1516', 'http://www.football-data.co.uk/mmz4281/1516/{}.csv', 1),
    (1, '1617', '1617', 'http://www.football-data.co.uk/mmz4281/1617/{}.csv', 1),
    (1, '1718', '1718', 'http://www.football-data.co.uk/mmz4281/1718/{}.csv', 1),
    (1, '1819', '1819', 'http://www.football-data.co.uk/mmz4281/1819/{}.csv', 1);

INSERT INTO season values 
    ('1011', '2010-08-01', '2011-07-31'), 
    ('1112', '2011-08-01', '2012-07-31'), 
    ('1213', '2012-08-01', '2013-07-31'), 
    ('1314', '2013-08-01', '2014-07-31'), 
    ('1415', '2014-08-01', '2015-07-31'), 
    ('1516', '2015-08-01', '2016-07-31'), 
    ('1617', '2016-08-01', '2017-07-31'), 
    ('1718', '2017-08-01', '2018-07-31'), 
    ('1819', '2018-08-01', '2019-07-31'); 




INSERT INTO league values
    ('E0', 'English Prem', 'The English Premier League'),
    ('E1', 'English Champ', 'The English Championship'),
    ('D1', 'German 1', 'The German Bundesliga 1'),
    ('B1', 'Belgian 1.A', 'The Belgian First Division A'),
    ('SC0', 'Scottish Prem', 'The Scottish Premier League'),
    ('I1', 'Italian A', 'The Italian Serie A'),
    ('F1', 'French 1', 'The French Ligue 1'),
    ('SP1', 'Spanish La Liga', 'The Spanish La Liga (Primera Division)');

INSERT INTO algo values (1, 'GoalsScoredSupremacy', 'Home team total goals scored - away team total goals scored over last 6 matches');

INSERT INTO algo_config values 
    ('2018-10-31', 1, 'E0', -1, 6),
    ('2018-10-31', 1, 'E1', 0, 0),
    ('2018-10-31', 1, 'D1', 2, 8),
    ('2018-10-31', 1, 'B1', 0, 0),
    ('2018-10-31', 1, 'SC0', 0, 0),
    ('2018-10-31', 1, 'I1', 0, 0),
    ('2018-10-31', 1, 'F1', 0, 0),
    ('2018-10-31', 1, 'SP1', 0, 0);

DROP TABLE team;
CREATE TABLE team (
    name varchar(64) not null, 
    league varchar(16) not null,
    foreign key(league) references league(name),
    primary key (name)
);

DROP TABLE match;
CREATE TABLE match (
    date text not null, 
    league varchar(16) not null, 
    home_team varchar(64) not null, 
    away_team varchar(64) not null, 
    result char, 
    best_odds real, 
    foreign key (league) references league(name), 
    foreign key (home_team) references team(name), 
    foreign key (away_team) references team(name),
    primary key (date, league, home_team, away_team)
);

DROP TABLE algo;
CREATE TABLE algo (
    id integer not null, 
    name varchar(64), 
    desc varchar(256),
    primary key (id)
);

DROP TABLE plan;
CREATE TABLE plan (
    id integer not null, 
    name varchar(64) not null, 
    desc varchar(256), 
    cost real not null,
    primary key (id)
);

DROP TABLE account;
CREATE TABLE account (
    name varchar(64) not null, 
    expiry_date text, 
    joined_date text not null, 
    plan_id integer not null, 
    foreign key (plan_id) references plan(id),
    primary key (name)
);

DROP TABLE account_perms;
CREATE TABLE account_perms (
    id integer not null, 
    account varchar(64) not null, 
    league varchar(16) not null, 
    algo_id integer not null, 
    foreign key (account) references account(name), 
    foreign key (league) references league(name), 
    foreign key (algo_id) references algo(id),
    primary key (id)
);

DROP TABLE league;
CREATE TABLE league (
    name varchar(16) not null, 
    desc varchar(256),
    primary key (name)
);

DROP TABLE statistics;
CREATE TABLE statistics (
    generation_date text not null, 
    algo_id integer not null, 
    league varchar(16) not null, 
    mark integer not null, 
    mark_freq integer not null, 
    home_freq integer not null, 
    away_freq integer not null, 
    draw_freq integer not null, 
    foreign key (algo_id) references algo(id), 
    foreign key (league) references league(name),
    primary key (generation_date, algo_id, league)
);

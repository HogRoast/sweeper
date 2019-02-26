with results_cte as (
        select r.algo_id, r.league, r.mark, m.result, count(r.mark) as res_freq
        from rating r
        inner join season s on r.match_date < s.u_bnd_date
        inner join algo_config c on -c.algo_id = r.algo_id
                                and c.league = r.league
        inner join match m on m.date = r.match_date
                                and m.home_team = r.home_team
                                and m.away_team = r.away_team
                                and m.league = r.league
        where s.name = '1819'
            and c.algo_id = -1
        group by r.algo_id, r.league, r.mark, m.result
    ),
    mark_cte as (
        select r.algo_id, r.league, r.mark, count(r.mark) as mark_freq 
        from rating r
        inner join season s on r.match_date < s.u_bnd_date
        inner join algo_config c on -c.algo_id = r.algo_id
                                and c.league = r.league
        inner join match m on m.date = r.match_date
                                and m.home_team = r.home_team
                                and m.away_team = r.away_team
                                and m.league = r.league
        where s.name = '1819'
            and c.algo_id = -1
        group by r.algo_id, r.league, r.mark
    )
select m.*, r.mark, (cast(t2.mark_freq as real) / t1.res_freq) as req_odds 
from match m
inner join rating r on r.match_date = m.date
                        and r.home_team = m.home_team
                        and r.away_team = m.away_team 
inner join algo_config c on m.league = c.league
                            and r.mark > c.l_bnd_mark
                            and r.mark < c.u_bnd_mark
                            and r.algo_id = c.algo_id
inner join season s on m.date > s.l_bnd_date
                        and m.date < s.u_bnd_date
inner join results_cte t1 on t1.algo_id = c.algo_id
                            and t1.league = m.league
                            and t1.mark = r.mark
                            and t1.result = 'H'
inner join mark_cte t2 on t2.algo_id = c.algo_id
                        and t2.league = m.league
                        and t2.mark = r.mark
where s.name = '1819' 
    and c.algo_id = 1 
    and m.league in ('E0', 'D1')
    and m.best_odds_h >= (cast(t2.mark_freq as real) / t1.res_freq)
order by m.date, m.home_team;

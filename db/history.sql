select m.*, r.mark, (cast(t.mark_freq as real) / t.home_freq) as req_odds 
from match m
inner join rating r on r.match_date = m.date
                        and r.home_team = m.home_team
                        and r.away_team = m.away_team 
inner join algo_config c on m.league = c.league
                        and r.mark > c.l_bnd_mark
                        and r.mark < c.u_bnd_mark
                        and r.algo_id = c.algo_id
inner join season s on m.date > s.l_bnd_date
inner join statistics t on t.algo_id = c.algo_id
                        and t.league = m.league
                        and t.mark = r.mark
where s.name = '1819' 
    and c.algo_id = 1 
    and m.league in ('E0', 'D1')
    and m.best_odds_h >= (cast(t.mark_freq as real) / t.home_freq);

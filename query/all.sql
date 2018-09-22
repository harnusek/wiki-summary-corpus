-- delete from domain
-- delete from summary
-- delete from sentence

select count(*)
from domain

select count(*)
from summary

select count(*)
from sentence

-- Get number of sentence by summary
select summary_id, count(id) 
from sentence
group by summary_id
order by summary_id

-- Get avarage number of sentence by domain
select domain_id, avg(count)
from(select summary_id, count(id) 
    from sentence
    group by summary_id) as sub
join summary on summary_id = summary.id
group by domain_id
order by domain_id

-- Get aggreated text of summaries
select summary_id, string_agg(text,' ' order by rank)
from sentence
group by summary_id
limit 20
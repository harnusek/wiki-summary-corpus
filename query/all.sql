-- delete from domain
-- delete from summary
-- delete from sentence

-- select count(domain_id)
-- from summary
-- group by domain_id

-- Get size of tables 
select 'domain' as table, count(*)
from domain
union
select 'summary' as table, count(*)
from summary
union
select 'sentence' as table, count(*)
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

-- Get first sentences of summaries by domain.label
select sentence.text
from sentence
join summary on summary_id = summary.id
join domain on domain_id = domain.id
where sentence.rank = 0 and domain.label = 'movies'
order by summary_id
limit 10

-- IAM TRYING FIND 100 BEST SENTENCES
select sentence.text
from sentence
join summary on summary_id = summary.id
join domain on domain_id = 4
-- where sentence.rank = 0
order by RANDOM()
limit 4
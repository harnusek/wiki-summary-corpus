delete from domain
delete from summary
delete from sentence

select *
from domain

select *
from summary

select string_agg(text,' ')
from sentence
group by summary_id
order by rank

select json_object_agg(rank,text)
from sentence
group by summary_id
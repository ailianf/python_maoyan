show tables;

select *
from test;

select *
from maoyan;

# 计算数据总条数。
select count(*)
from maoyan;

# 取重复数据的最大id值。
select max(M.id)
from maoyan M
       inner join (select nickName
                   from maoyan
                   group by movieId, startTime, nickName, cityName, score, content
                   having count(*) > 1) nick on M.nickName = nick.nickName
group by nick.nickName;

# 删除重复的数据，并保留一份重复数据。
delete
from maoyan
where id in(select MY.id
            from (select M.id
                  from maoyan M
                         inner join (select mm.nickName
                                     from maoyan mm
                                     group by mm.movieId, mm.startTime, mm.nickName, mm.cityName, mm.score, mm.content
                                     having count(*) > 1) m3 on M.nickName = m3.nickName
                  where M.id not in(select max(M.id)
                                    from maoyan M
                                           inner join (select mm.nickName
                                                       from maoyan mm
                                                       group by mm.movieId, mm.startTime, mm.nickName, mm.cityName,
                                                                mm.score, mm.content
                                                       having count(*) > 1) nick on M.nickName = nick.nickName
                                    group by nick.nickName)) MY);

# 错误语句。（删除重复的数据，并保留一份重复数据。）
delete
from maoyan
where id in(select M.id
            from maoyan M
                   inner join (select mm.nickName
                               from maoyan mm
                               group by mm.movieId, mm.startTime, mm.nickName, mm.cityName, mm.score, mm.content
                               having count(*) > 1) m3 on M.nickName = m3.nickName
            where M.id not in(select max(M.id)
                              from maoyan M
                                     inner join (select mm.nickName
                                                 from maoyan mm
                                                 group by mm.movieId, mm.startTime, mm.nickName, mm.cityName, mm.score,
                                                          mm.content
                                                 having count(*) > 1) nick on M.nickName = nick.nickName
                              group by nick.nickName));

# 查询重复数据中id最大的数据信息。
select M.*
from maoyan M
       inner join (select nickName
                   from maoyan
                   group by movieId, startTime, nickName, cityName, score, content
                   having count(*) > 1) nick on M.nickName = nick.nickName
where M.id not in(select max(m.id)
                  from maoyan m
                         inner join (select nickName
                                     from maoyan
                                     group by movieId, startTime, nickName, cityName, score, content
                                     having count(*) > 1) nick on m.nickName = nick.nickName
                  group by nick.nickName);

# 统计不同评分的数量
select score, count(score) rate_count
from maoyan
group by score
order by rate_count desc;

# 删除重复数据，包含重复数据本身也删除。
delete
from maoyan
where nickName in(select nickName
                  from (select nickName, score, count(*) rate_count
                        from maoyan
                        group by nickName, score
                        having rate_count > 1) test);

# 取重复数据中的最小id。
select min(id)
from maoyan
group by nickName
having count(nickName) > 1;

# 去重复数中对应的nickName以及重复次数。
select nickName, count(*) rate_count
from maoyan
group by nickName
having rate_count > 1;

# 去重复数中对应的nickName，score以及重复次数。
select nickName, score, count(*) rate_count
from maoyan
group by nickName, score
having rate_count > 1;

# 去重复数中对应的cityName以及重复次数，并根据重复次数倒序排序，去top5。
select cityName, count(*) rate_count
from maoyan
group by cityName
order by rate_count desc
limit 5;

# 查询同一城市出现的次数，并取top5。
select cityName, count(cityName) rate_count
from maoyan
group by cityName
order by rate_count desc
limit 5;

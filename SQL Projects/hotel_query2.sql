with hotels as(
select*
from dbo.['2018$']
union
select*
from dbo.['2019$']
union
select*
from dbo.['2020$'])

SELECT     arrival_date_year, 	hotel,     round(SUM((stays_in_week_nights + stays_in_weekend_nights) * adr), 2) AS revenue  FROM hotels  GROUP BY arrival_date_year, hotel
select *
from [project portfolio in sql]..['covid-death$']
where continent is not null
order by 3,4


--select *
--from [project portfolio in sql]..['covid-vaccination$']
--order by 3,4

-- select the data that we are going to be using 

select location, date, total_cases, new_cases, total_deaths, population 
from [project portfolio in sql]..['covid-death$']
where continent is not null
order by 1,2


-- looking at total cases vs total deaths

select location, date, total_cases, total_deaths, (CONVERT(float, total_deaths) / NULLIF(CONVERT(float, total_cases), 0))*100 as DeathPercentage
from [project portfolio in sql]..['covid-death$']
where continent is not null
order by 1,2

--shows the likelihood of dieing if you contact covid in your country

select location, date, total_cases, total_deaths, (CONVERT(float, total_deaths) / NULLIF(CONVERT(float, total_cases), 0))*100 as DeathPercentage
from [project portfolio in sql]..['covid-death$']
where location like '%states%'
and continent is not null
order by 1,2


--looking at the total cases vs population
-- this shows the percentage of population that got covid

select location, date, population, total_cases, (CONVERT(float, total_cases) / NULLIF(CONVERT(float, population), 0))*100 as Percentpopulationaffected
from [project portfolio in sql]..['covid-death$']
where location like '%states%'
and continent is not null
order by 1,2


-- query showing countries with the highest infection rate compared to population

select location, population, max(total_cases) as HighestinfectionCount, max((CONVERT(float, total_cases) / NULLIF(CONVERT(float, population), 0)))*100 as Percentpopulationaffected
from [project portfolio in sql]..['covid-death$']
--where location like '%states%'
where continent is not null
group by location, population
order by Percentpopulationaffected desc



-- Query showing Countries with the Highest Death rate per population

select location, max((CONVERT(float, total_deaths))) as TotalDeathCount
from [project portfolio in sql]..['covid-death$']
--where location like '%states%'
where continent is not null
group by location
order by TotalDeathCount desc


-- Querying by Continent

select location, max(CAST(total_deaths as int)) as TotalDeathCount
from [project portfolio in sql]..['covid-death$']
--where location like '%states%'
where continent is null
group by location
order by TotalDeathCount desc


-- Beaking things down by continent


--Query showing the continent with the highest death rate

select continent, max(CAST(total_deaths as int)) as TotalDeathCount
from [project portfolio in sql]..['covid-death$']
--where location like '%states%'
where continent is not null
group by continent
order by TotalDeathCount desc


-- Daily Global Death Rate
select date, sum(new_cases) as total_cases, sum(CONVERT(float, new_deaths)) as total_deaths, sum(CONVERT(float, new_deaths) / NULLIF(CONVERT(float, new_cases), 0))*100 as DeathPercentage
from [project portfolio in sql]..['covid-death$']
--where location like '%states%'
where continent is not null
group by date 
order by 1,2


-- Total Global Death Rate
select sum(new_cases) as total_cases, sum(CONVERT(float, new_deaths)) as total_deaths, sum(CONVERT(float, new_deaths) / NULLIF(CONVERT(float, new_cases), 0))*100 as DeathPercentage
from [project portfolio in sql]..['covid-death$']
--where location like '%states%'
where continent is not null
order by 1,2

-- Query showing total population vs vaccination

select death.continent, death.location, death.date, death.population, vaccination.new_vaccinations
from [project portfolio in sql]..['covid-death$'] death
join [project portfolio in sql]..['covid-vaccination$'] vaccination
on death.location = vaccination.location
and death.date = vaccination.date
where death.continent is not null
order by 2,3

-- Using Partition by
select death.continent, death.location, death.date, death.population, vaccination.new_vaccinations,
sum(convert(float, vaccination.new_vaccinations)) over (Partition by death.location order by death.location, death.date) as VaccinatedPeople,
--(VaccinatedPeople/population)*100 --(you cant use the column just created in your table use temp table or CTE instead)
from [project portfolio in sql]..['covid-death$'] death
join [project portfolio in sql]..['covid-vaccination$'] vaccination
on death.location = vaccination.location
and death.date = vaccination.date
where death.continent is not null
order by 2,3

--use CTE

with populationvsvaccination (continent, location, date, population, new_vaccinations, VaccinatedPeople)
as
(
select death.continent, death.location, death.date, death.population, vaccination.new_vaccinations,
sum(convert(float, vaccination.new_vaccinations)) over (Partition by death.location order by death.location, death.date) as VaccinatedPeople
--(VaccinatedPeople/population)*100 --(you cant use the column just created in your table use temp table or CTE instead)
from [project portfolio in sql]..['covid-death$'] death
join [project portfolio in sql]..['covid-vaccination$'] vaccination
on death.location = vaccination.location
and death.date = vaccination.date
where death.continent is not null
--order by 2,3
)
select *, (VaccinatedPeople/population)*100 as percentagevaccinated
from populationvsvaccination


--Temp Table

drop table if exists #Pecentagevaccinated
create table #Pecentagevaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
VaccinatedPeople numeric
)

insert into #Pecentagevaccinated
select death.continent, death.location, death.date, death.population, vaccination.new_vaccinations,
sum(convert(float, vaccination.new_vaccinations)) over (Partition by death.location order by death.location, death.date) as VaccinatedPeople
--(VaccinatedPeople/population)*100 --(you cant use the column just created in your table use temp table or CTE instead)
from [project portfolio in sql]..['covid-death$'] death
join [project portfolio in sql]..['covid-vaccination$'] vaccination
on death.location = vaccination.location
and death.date = vaccination.date
--where death.continent is not null
--order by 2,3

select *, (VaccinatedPeople/population)*100 as percentagevaccinated
from #Pecentagevaccinated

create view Pecentagevaccinated as
select death.continent, death.location, death.date, death.population, vaccination.new_vaccinations,
sum(convert(float, vaccination.new_vaccinations)) over (Partition by death.location order by death.location, death.date) as VaccinatedPeople
--(VaccinatedPeople/population)*100 --(you cant use the column just created in your table use temp table or CTE instead)
from [project portfolio in sql]..['covid-death$'] death
join [project portfolio in sql]..['covid-vaccination$'] vaccination
on death.location = vaccination.location
and death.date = vaccination.date
where death.continent is not null
--order by 2,3


select*
from Pecentagevaccinated

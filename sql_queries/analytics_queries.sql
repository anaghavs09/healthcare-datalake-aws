-- COVID-19 Analytics Queries on Processed Data

-- Table creation
CREATE EXTERNAL TABLE IF NOT EXISTS covid_data_processed (
    country STRING,
    continent STRING,
    population BIGINT,
    cases BIGINT,
    deaths BIGINT,
    recovered BIGINT,
    active BIGINT,
    death_rate_pct DOUBLE,
    recovery_rate_pct DOUBLE,
    active_rate_pct DOUBLE,
    severity_level STRING,
    casesPerOneMillion BIGINT,
    deathsPerOneMillion BIGINT,
    processed_at STRING
)
STORED AS PARQUET
LOCATION 's3://healthcare-datalake-anagha/processed/covid/';

-- Query 1: Top countries by cases with metrics
SELECT 
    country,
    cases,
    deaths,
    death_rate_pct,
    recovery_rate_pct,
    severity_level
FROM covid_data_processed
ORDER BY cases DESC
LIMIT 10;

-- Query 2: Countries by severity level
SELECT 
    severity_level,
    COUNT(*) as country_count,
    ROUND(AVG(death_rate_pct), 2) as avg_death_rate,
    ROUND(AVG(recovery_rate_pct), 2) as avg_recovery_rate
FROM covid_data_processed
GROUP BY severity_level;

-- Query 3: Deadliest countries (by rate)
SELECT 
    country,
    continent,
    cases,
    deaths,
    death_rate_pct
FROM covid_data_processed
WHERE cases > 100000
ORDER BY death_rate_pct DESC
LIMIT 10;

-- Query 4: Continental analysis
SELECT 
    continent,
    COUNT(DISTINCT country) as countries,
    SUM(cases) as total_cases,
    SUM(deaths) as total_deaths,
    ROUND(AVG(death_rate_pct), 2) as avg_death_rate
FROM covid_data_processed
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY total_cases DESC;

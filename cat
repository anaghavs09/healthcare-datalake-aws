-- Create COVID data table in Athena
-- Points to S3 raw zone for schema-on-read querying

CREATE DATABASE IF NOT EXISTS healthcare_catalog;

USE healthcare_catalog;

CREATE EXTERNAL TABLE IF NOT EXISTS covid_data (
    country STRING,
    cases BIGINT,
    todayCases BIGINT,
    deaths BIGINT,
    todayDeaths BIGINT,
    recovered BIGINT,
    todayRecovered BIGINT,
    active BIGINT,
    critical BIGINT,
    casesPerOneMillion BIGINT,
    deathsPerOneMillion BIGINT,
    tests BIGINT,
    testsPerOneMillion BIGINT,
    population BIGINT,
    continent STRING,
    oneCasePerPeople BIGINT,
    oneDeathPerPeople BIGINT,
    oneTestPerPeople BIGINT,
    activePerOneMillion DOUBLE,
    recoveredPerOneMillion DOUBLE,
    criticalPerOneMillion DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://healthcare-datalake-anagha/raw/covid/'
TBLPROPERTIES ('skip.header.line.count'='1');

# 🏥 AWS Healthcare Data Lake - Serverless Analytics Platform

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Serverless](https://img.shields.io/badge/Serverless-Lambda-green)

> Serverless healthcare data lake on AWS processing COVID-19 statistics from 227 countries using Lambda, S3, Glue, and Athena

---

## 📋 Overview

Cloud-native data lake built entirely on AWS serverless services. Automatically collects public health data daily, transforms it with PySpark, and enables SQL analytics without managing any infrastructure.

**Data:** COVID-19 statistics (cases, deaths, recoveries, vaccinations)  
**Scale:** 227 countries, daily updates  

---

## 🏗️ Architecture
```
disease.sh API
    ↓
AWS Lambda (serverless data collection)
    ↓
S3 Data Lake (raw → processed zones)
    ↓
AWS Glue ETL (PySpark transformations)
    ↓
AWS Athena (serverless SQL analytics)
```

**Fully automated, event-driven, serverless pipeline**

---

## 🛠️ Tech Stack

**AWS Services:**
- S3 - Multi-zone data lake storage
- Lambda - Serverless data collection
- EventBridge - Daily scheduling
- Glue - ETL transformations (PySpark)
- Athena - Serverless SQL queries
- IAM - Security and permissions
- CloudWatch - Monitoring and logs

**Languages:**
- Python 3.12 (Lambda functions)
- PySpark (Glue ETL)
- SQL (Athena analytics)

**Libraries:**
- boto3 (AWS SDK)
- urllib3 (HTTP requests)

---

## 📊 Data Pipeline

### Data Collection (Lambda)
- Fetches COVID data from disease.sh API
- Runs daily via EventBridge trigger
- Saves to S3 raw zone as CSV
- 227 countries, ~150KB per file

### Transformation (Glue ETL)
- Reads CSV from raw zone
- Calculates death rate, recovery rate percentages
- Categorizes severity (High/Medium/Low/Minimal)
- Writes to processed zone as Parquet
- PySpark transformations in under 2 minutes

### Analytics (Athena)
- Query both raw and processed data with SQL
- No database infrastructure needed
- Sub-second query performance
- Pay only per query

---

## 🚀 Key Features

✅ **Serverless** - No servers to manage or maintain  
✅ **Automated** - Daily data collection with EventBridge  
✅ **Scalable** - Handles unlimited data growth  
✅ **Cost-effective** - Free Tier covers entire pipeline  
✅ **Multi-zone** - Raw, processed, curated architecture  
✅ **Schema-on-read** - Query files directly with SQL  
✅ **Monitored** - CloudWatch logs for all components  

---

## 💡 Business Metrics

**Calculated in ETL:**
- Death rate percentage by country
- Recovery rate percentage
- Active case rates
- Severity categorization
- Population-adjusted metrics (per million)

**Analytics Queries:**
- Top countries by cases/deaths
- Continental aggregations
- Severity level distributions
- Trend analysis over time

---

## 📂 S3 Data Lake Structure
```
s3://healthcare-datalake-anagha/
├── raw/
│   └── covid/
│       └── disease-sh-countries_*.csv
├── processed/
│   └── covid/
│       └── *.parquet (with calculated metrics)
├── curated/
│   └── (future aggregations)
└── glue-scripts/
    └── covid_transformation.py
```

---

## 🎯 Skills Demonstrated

**Cloud Engineering:**
- AWS service integration (6 services)
- Serverless architecture design
- Data lake patterns (multi-zone)
- Infrastructure as code (AWS CLI)
- Cost optimization (Free Tier)

**Data Engineering:**
- ETL pipeline development
- PySpark transformations
- Schema-on-read implementation
- Data cataloging
- Automated workflows

**Python:**
- boto3 (AWS SDK)
- Lambda function development
- Error handling
- API integration

**SQL:**
- Athena DDL (CREATE EXTERNAL TABLE)
- Analytics queries
- Aggregations and calculations

---

## 📖 Setup (AWS Free Tier)

### Prerequisites
- AWS Account (Free Tier)
- AWS CLI configured
- Python 3.12+

### AWS Resources

**1. S3 Bucket**
```bash
aws s3 mb s3://healthcare-datalake-anagha
```

**2. Lambda Function**
- Runtime: Python 3.12
- Code: `lambda_functions/fetch_covid_data.py`
- IAM Role: AWSLambdaBasicExecutionRole + S3FullAccess

**3. EventBridge Rule**
- Schedule: rate(1 day)
- Target: fetch-covid-data Lambda

**4. Glue ETL Job**
```bash
aws glue create-job \
    --name covid-data-transformation \
    --role AWSGlueServiceRole-CovidETL \
    --command Name=glueetl,ScriptLocation=s3://healthcare-datalake-anagha/glue-scripts/covid_transformation.py,PythonVersion=3 \
    --glue-version "4.0" \
    --worker-type G.1X \
    --number-of-workers 2
```

**5. Athena Tables**
- Run DDL in `sql_queries/create_tables.sql`
- Query data immediately

---

## 📈 Results

**Data Processing:**
- 227 countries processed daily
- Raw → Processed in <2 minutes
- CSV → Parquet (10x compression)
- Zero infrastructure management

**Query Performance:**
- Athena queries: <1 second
- No database startup time
- Pay only for data scanned

---

## 🔮 Future Enhancements

- Add more data sources (hospital data, vaccination rates)
- Schedule Glue ETL job automatically
- Add data quality tests
- Create QuickSight dashboard
- Implement data retention policies
- Add Step Functions for orchestration
